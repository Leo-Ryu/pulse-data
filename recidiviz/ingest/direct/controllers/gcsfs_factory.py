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
"""Factory for GCSFileSystem objects"""
from gcsfs import GCSFileSystem

from recidiviz.cloud_functions.cloud_function_utils import GCSFS_NO_CACHING
from recidiviz.ingest.direct.controllers.direct_ingest_gcs_file_system import \
    DirectIngestGCSFileSystem, DirectIngestGCSFileSystemImpl
from recidiviz.utils import metadata


class GcsfsFactory:
    @classmethod
    def build(cls) -> DirectIngestGCSFileSystem:
        return DirectIngestGCSFileSystemImpl(
            GCSFileSystem(project=metadata.project_id(),
                          cache_timeout=GCSFS_NO_CACHING))
