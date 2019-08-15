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
"""Controller for parsing and persisting a file in the GCS filesystem."""
import abc
import datetime
import logging
import os
from typing import Optional, List

from recidiviz import IngestInfo
from recidiviz.common.ingest_metadata import SystemLevel
from recidiviz.ingest.direct.controllers.base_direct_ingest_controller import \
    BaseDirectIngestController
from recidiviz.ingest.direct.controllers.gcsfs_direct_ingest_job_prioritizer \
    import GcsfsDirectIngestJobPrioritizer
from recidiviz.ingest.direct.controllers.gcsfs_direct_ingest_utils import \
    GcsfsIngestArgs, filename_parts_from_path, \
    gcsfs_direct_ingest_storage_directory_path_for_region, \
    gcsfs_direct_ingest_directory_path_for_region
from recidiviz.ingest.direct.controllers.gcsfs_factory import GcsfsFactory
from recidiviz.ingest.direct.errors import DirectIngestError, \
    DirectIngestErrorType


class GcsfsDirectIngestController(BaseDirectIngestController[GcsfsIngestArgs,
                                                             str]):
    """Controller for parsing and persisting a file in the GCS filesystem."""

    _MAX_STORAGE_FILE_RENAME_TRIES = 10

    def __init__(self,
                 region_name: str,
                 system_level: SystemLevel,
                 ingest_directory_path: Optional[str] = None,
                 storage_directory_path: Optional[str] = None):
        super().__init__(region_name, system_level)
        self.fs = GcsfsFactory.build()

        if ingest_directory_path:
            self.ingest_directory_path = ingest_directory_path
        else:
            self.ingest_directory_path = \
                gcsfs_direct_ingest_directory_path_for_region(region_name,
                                                              system_level)
        if storage_directory_path:
            self.storage_directory_path = storage_directory_path
        else:
            self.storage_directory_path = \
                gcsfs_direct_ingest_storage_directory_path_for_region(
                    region_name, system_level)

        self.file_prioritizer = \
            GcsfsDirectIngestJobPrioritizer(
                self.fs,
                self.ingest_directory_path,
                self._get_file_tag_rank_list())

    # ============== #
    # JOB SCHEDULING #
    # ============== #

    @abc.abstractmethod
    def _get_file_tag_rank_list(self) -> List[str]:
        pass

    def _get_next_job_args(self) -> Optional[GcsfsIngestArgs]:
        return self.file_prioritizer.get_next_job_args()

    def _wait_time_sec_for_next_args(self, args: GcsfsIngestArgs) -> int:
        if self.file_prioritizer.are_next_args_expected(args):
            # Run job immediately
            return 0

        now = datetime.datetime.utcnow()

        file_upload_time: datetime.datetime = \
            filename_parts_from_path(args.file_path).utc_upload_datetime

        # TODO(1628): This calculation is buggy and seems to sometimes be
        #  producing times up to 24 hours in the future. Needs debugging and
        #  also should be updated to wait longer than 5 seconds in production.
        five_sec_from_file_upload_time = \
            file_upload_time + datetime.timedelta(seconds=5)

        wait_time = max((five_sec_from_file_upload_time - now).seconds, 0)
        logging.info("Waiting [%s] sec for [%s]",
                     wait_time, self._job_tag(args))
        return wait_time

    def _on_job_scheduled(self, ingest_args: GcsfsIngestArgs):
        pass

    # =================== #
    # SINGLE JOB RUN CODE #
    # =================== #

    def _job_tag(self, args: GcsfsIngestArgs) -> str:
        return f'{self.region.region_code}/{self.file_name(args.file_path)}:' \
            f'{args.ingest_time}'

    def _read_contents(self, args: GcsfsIngestArgs) -> str:
        if not args.file_path:
            raise DirectIngestError(
                msg=f"File path not set for job [{self._job_tag(args)}]",
                error_type=DirectIngestErrorType.INPUT_ERROR)

        with self.fs.open(args.file_path) as fp:
            return fp.read().decode('utf-8')

    @abc.abstractmethod
    def _parse(self,
               args: GcsfsIngestArgs,
               contents: str) -> IngestInfo:
        pass

    def _do_cleanup(self, args: GcsfsIngestArgs):
        self.fs.mv_path_to_processed_path(args.file_path)

        parts = filename_parts_from_path(args.file_path)
        directory_path, _ = os.path.split(args.file_path)

        next_args_for_day = \
            self.file_prioritizer.get_next_job_args(date_str=parts.date_str)

        # TODO(1628): Consider moving all files to storage after a whole day has
        #  passed, even if there are still expected files?
        day_complete = not next_args_for_day and not \
            self.file_prioritizer.are_more_jobs_expected_for_day(parts.date_str)

        if day_complete:
            logging.info(
                "All expected files found for day [%s]. Moving to storage.",
                parts.date_str)
            self.fs.mv_paths_from_date_to_storage(directory_path,
                                                  parts.date_str,
                                                  self.storage_directory_path)

    @staticmethod
    def file_name(file_path: Optional[str]) -> Optional[str]:
        if not file_path:
            return None

        _, file_name = os.path.split(file_path)
        return file_name

    @staticmethod
    def file_tag(file_path: str) -> str:
        return filename_parts_from_path(file_path).file_tag
