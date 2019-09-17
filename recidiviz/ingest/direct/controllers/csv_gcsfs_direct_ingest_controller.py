# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2019 Recidiviz, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================
"""Direct ingest controller for regions that read CSV files from the
GCSFileSystem.
"""

import abc
import inspect
import io
import logging
import os
from typing import List, Iterable, Optional, Callable, Type

import pandas as pd
from more_itertools import spy

from recidiviz import IngestInfo
from recidiviz.common.ingest_metadata import SystemLevel
from recidiviz.ingest.direct.controllers.direct_ingest_gcs_file_system import \
    to_normalized_unprocessed_file_path, SPLIT_FILE_SUFFIX

from recidiviz.ingest.direct.controllers.gcsfs_direct_ingest_controller import \
    GcsfsDirectIngestController
from recidiviz.ingest.direct.controllers.gcsfs_direct_ingest_utils import \
    GcsfsIngestArgs, filename_parts_from_path
from recidiviz.ingest.direct.controllers.gcsfs_path import GcsfsFilePath, \
    GcsfsDirectoryPath
from recidiviz.ingest.direct.errors import DirectIngestError, \
    DirectIngestErrorType
from recidiviz.ingest.extractor.csv_data_extractor import CsvDataExtractor


class CsvGcsfsDirectIngestController(GcsfsDirectIngestController):
    """Direct ingest controller for regions that read CSV files from the
    GCSFileSystem.
    """
    # TODO(1628): Once we have migrated to new Cloud Tasks infrastructure,
    #  we should be able to handle much larger files - change this threshold.
    CSV_LINE_LIMIT = 300

    def __init__(self,
                 region_name: str,
                 system_level: SystemLevel,
                 ingest_directory_path: Optional[str],
                 storage_directory_path: Optional[str],
                 # TODO(2104): Remove this once UsTxBrazosDataExtractor is no
                 #  longer used.
                 csv_data_extractor_cls:
                 Type[CsvDataExtractor] = CsvDataExtractor):
        super().__init__(region_name,
                         system_level,
                         ingest_directory_path,
                         storage_directory_path)
        self.csv_data_extractor_cls = csv_data_extractor_cls
        self.line_limit = self.CSV_LINE_LIMIT

    @abc.abstractmethod
    def _get_file_tag_rank_list(self) -> List[str]:
        pass

    def _contents_to_str(self, contents: Iterable[str]):
        return '\n'.join(contents)

    def _file_meets_file_line_limit(self, contents: Iterable[str]):
        df = pd.read_csv(io.StringIO(self._contents_to_str(contents)),
                         dtype=str)
        return len(df) <= self.line_limit

    def _split_file_if_necessary(self, path: GcsfsFilePath):
        file_tag = filename_parts_from_path(path).file_tag

        if file_tag not in self._get_file_tag_rank_list():
            logging.info("File tag [%s] for path [%s] not in rank list - "
                         "not splitting.",
                         file_tag,
                         path.abs_path())
            return False

        file_contents = self._read_file_contents(path)

        if not file_contents:
            logging.info("File [%s] has no rows - not splitting.",
                         path.abs_path())
            return False

        if self._can_proceed_with_ingest_for_contents(file_contents):
            logging.info("No need to split file path [%s].", path.abs_path())
            return False

        logging.info("Proceeding to file splitting for path [%s].",
                     path.abs_path())

        output_dir = GcsfsDirectoryPath.from_file_path(path)

        str_contents = self._contents_to_str(file_contents)

        upload_paths_and_df = []
        for i, df in enumerate(pd.read_csv(io.StringIO(str_contents),
                                           dtype=str,
                                           chunksize=self.line_limit)):
            upload_path = self._create_split_file_path(
                path, output_dir, split_num=i)
            upload_paths_and_df.append((upload_path, df))

        for output_path, df in upload_paths_and_df:
            logging.info("Writing file split [%s] to Cloud Storage.",
                         output_path.abs_path())

            self.fs.upload_from_string(
                output_path, df.to_csv(index=False), 'text/csv')

        logging.info("Done splitting file [%s] into [%s] paths, returning.",
                     path.abs_path(), len(upload_paths_and_df))

        self.fs.mv_path_to_storage(path, self.storage_directory_path)

        return True

    def _create_split_file_path(self,
                                original_file_path: GcsfsFilePath,
                                output_dir: GcsfsDirectoryPath,
                                split_num: int) -> GcsfsFilePath:
        parts = filename_parts_from_path(original_file_path)

        rank_str = str(split_num + 1).zfill(3)
        existing_suffix = \
            f'_{parts.filename_suffix}' if parts.filename_suffix else ''
        updated_file_name = \
            f'{parts.file_tag}{existing_suffix}_{rank_str}' \
            f'_{SPLIT_FILE_SUFFIX}.{parts.extension}'
        return GcsfsFilePath.from_directory_and_file_name(
            output_dir,
            to_normalized_unprocessed_file_path(updated_file_name,
                                                dt=parts.utc_upload_datetime))

    def _yaml_filepath(self, file_tag):
        return os.path.join(os.path.dirname(inspect.getfile(self.__class__)),
                            f'{self.region.region_code}_{file_tag}.yaml')

    def _parse(self,
               args: GcsfsIngestArgs,
               contents: Iterable[str]) -> IngestInfo:
        file_tag = self.file_tag(args.file_path)

        if file_tag not in self._get_file_tag_rank_list():
            raise DirectIngestError(
                msg=f"No mapping found for tag [{file_tag}]",
                error_type=DirectIngestErrorType.INPUT_ERROR)

        file_mapping = self._yaml_filepath(file_tag)

        row_pre_processors = self._get_row_pre_processors_for_file(file_tag)
        row_post_processors = self._get_row_post_processors_for_file(file_tag)
        file_post_processors = self._get_file_post_processors_for_file(file_tag)
        # pylint: disable=assignment-from-none
        primary_key_override = self._get_primary_key_override_for_file(file_tag)
        # pylint: disable=assignment-from-none
        ancestor_key_override = \
            self._get_ancestor_key_override_for_file(file_tag)
        should_set_with_empty_values = \
            file_tag in self._get_files_to_set_with_empty_values()
        should_cache = self._get_should_cache()

        data_extractor = self.csv_data_extractor_cls(
            file_mapping,
            row_pre_processors,
            row_post_processors,
            file_post_processors,
            ancestor_key_override,
            primary_key_override,
            self.system_level,
            should_set_with_empty_values,
            should_cache=should_cache)

        return data_extractor.extract_and_populate_data(contents)

    def _are_contents_empty(self,
                            contents: Iterable[str]) -> bool:
        """Returns true if the CSV file is emtpy, i.e. it contains no non-header
         rows.
         """
        vals, _ = spy(contents, 2)
        return len(vals) < 2

    def _can_proceed_with_ingest_for_contents(self, contents: Iterable[str]):
        return self._are_contents_empty(contents) or \
               self._file_meets_file_line_limit(contents)

    def _get_row_pre_processors_for_file(self, _file_tag) -> List[Callable]:
        """Subclasses should override to return row_pre_processors for a given
        file tag.
        """
        return []

    def _get_row_post_processors_for_file(self, _file_tag) -> List[Callable]:
        """Subclasses should override to return row_post_processors for a given
        file tag.
        """
        return []

    def _get_file_post_processors_for_file(self, _file_tag) -> List[Callable]:
        """Subclasses should override to return file_post_processors for a given
        file tag.
        """
        return []

    def _get_ancestor_key_override_for_file(
            self, _file_tag: str) -> Optional[Callable]:
        """Subclasses should override to return an ancestor_key_override for a
        given file tag.
        """
        return None

    def _get_primary_key_override_for_file(
            self, _file_tag: str) -> Optional[Callable]:
        """Subclasses should override to return a primary_key_override for a
        given file tag.
        """
        return None

    def _get_files_to_set_with_empty_values(self) -> List[str]:
        """Subclasses should override to return which files to set with empty
        values (see CsvDataExtractor).
        """
        return []

    def _get_should_cache(self) -> bool:
        """Subclasses should override to return whether should_cache should be
        True for CsvDataExtractor construction.
        """
        return True
