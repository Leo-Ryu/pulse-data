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
"""Util functions and types used by GCSFileSystem Direct Ingest code."""

import datetime
import os
import re
from typing import Optional

import attr

from recidiviz.common.ingest_metadata import SystemLevel
from recidiviz.ingest.direct.controllers.direct_ingest_types import IngestArgs
from recidiviz.ingest.direct.errors import DirectIngestError, \
    DirectIngestErrorType
from recidiviz.utils import metadata

_FILEPATH_REGEX = \
    re.compile(
        r'.*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}:\d{6})_'
        r'([A-Za-z]+[A-Za-z_]*)(_.+)?\.(.*)')


@attr.s(frozen=True)
class GcsfsFilenameParts:
    """A convenience struct that contains information about a file parsed from
    a filename that has been generated by
    cloud_function_utils.py::to_normalized_unprocessed_file_path().

    E.g. Consider the following file path
    "/processed_2019-08-14T23:09:27:047747_elite_offenders_019_historical.csv"

    This will be parsed by filename_parts_from_path() to:
    utc_upload_datetime=datetime.fromisoformat(2019-08-14T23:09:27:047747)
    date_str="2019-08-14"
    file_tag="elite_offenders"
    filename_suffix="019_historical"
    extension="csv"
    """

    utc_upload_datetime: datetime.datetime = attr.ib()
    date_str: str = attr.ib()
    # Must only contain letters or the '_' char
    file_tag: str = attr.ib()
    # Must start a number and be separated from the file_tag by a '_' char.
    filename_suffix: Optional[str] = attr.ib()
    extension: str = attr.ib()


@attr.s(frozen=True)
class GcsfsIngestArgs(IngestArgs):
    file_path: str = attr.ib()


def gcsfs_direct_ingest_storage_directory_path_for_region(
        region_code: str, system_level: SystemLevel) -> str:
    project_id = metadata.project_id()
    if not project_id:
        raise ValueError("Project id not set")

    storage_bucket = \
        f'{project_id}-direct-ingest-{system_level.value.lower()}-storage'
    return os.path.join(storage_bucket, region_code)


def gcsfs_direct_ingest_directory_path_for_region(
        region_code: str, system_level: SystemLevel) -> str:
    project_id = metadata.project_id()
    if not project_id:
        raise ValueError("Project id not set")

    if system_level == SystemLevel.COUNTY:
        bucket = f'{project_id}-direct-ingest-county'
        return os.path.join(bucket, region_code)
    if system_level == SystemLevel.STATE:
        normalized_region_code = region_code.replace('_', '-')
        return f'{project_id}-direct-ingest-state-{normalized_region_code}'

    raise DirectIngestError(
        msg=f"Cannot determine ingest directory path for region: "
            f"[{region_code}]",
        error_type=DirectIngestErrorType.INPUT_ERROR
    )


def filename_parts_from_path(file_path: str) -> GcsfsFilenameParts:
    _, filename = os.path.split(file_path)
    match = re.match(_FILEPATH_REGEX, filename)
    if not match:
        raise DirectIngestError(
            msg=f"Could not parse upload_ts, file_tag, extension "
            f"from path [{file_path}]",
            error_type=DirectIngestErrorType.INPUT_ERROR)

    full_upload_timestamp_str = match.group(1)
    utc_upload_datetime = \
        datetime.datetime.fromisoformat(full_upload_timestamp_str)

    return GcsfsFilenameParts(
        utc_upload_datetime=utc_upload_datetime,
        date_str=utc_upload_datetime.date().isoformat(),
        file_tag=match.group(2),
        filename_suffix=match.group(3),
        extension=match.group(4),
    )
