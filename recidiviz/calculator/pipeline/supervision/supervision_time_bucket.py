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
"""Buckets of time on supervision that may have included a revocation."""
from typing import Optional

import attr

from recidiviz.common.attr_mixins import BuildableAttr
from recidiviz.common.constants.state.state_supervision import \
    StateSupervisionType
from recidiviz.common.constants.state.state_supervision_violation import \
    StateSupervisionViolationType
from recidiviz.common.constants.state.state_supervision_violation_response \
    import StateSupervisionViolationResponseRevocationType


@attr.s(frozen=True)
class SupervisionTimeBucket(BuildableAttr):
    """Models details related to a bucket of time on supervision.

    Describes either a year or a month in which a person spent any amount of
    time on supervision. This includes the information pertaining to time on
    supervision that we will want to track when calculating supervision and
    revocation metrics."""

    # The state where the supervision took place
    state_code: str = attr.ib()

    # Year for when the person was on supervision
    year: int = attr.ib()

    # Month for when the person was on supervision
    month: Optional[int] = attr.ib()

    # The type of supervision the person was on
    supervision_type: Optional[StateSupervisionType] = attr.ib(default=None)


@attr.s(frozen=True)
class RevocationReturnSupervisionTimeBucket(SupervisionTimeBucket):
    """Models a SupervisionTimeBucket where the person was incarcerated for a
    revocation."""

    # The type of revocation of supervision
    revocation_type: Optional[StateSupervisionViolationResponseRevocationType] \
        = attr.ib(default=None)

    # StateSupervisionViolationType enum for the type of violation that
    # eventually caused the revocation of supervision
    source_violation_type: Optional[StateSupervisionViolationType] = \
        attr.ib(default=None)

    @staticmethod
    def for_year(state_code: str, year: int,
                 supervision_type: Optional[StateSupervisionType],
                 revocation_type:
                 Optional[StateSupervisionViolationResponseRevocationType],
                 source_violation_type:
                 Optional[StateSupervisionViolationType]) -> \
            'RevocationReturnSupervisionTimeBucket':
        return RevocationReturnSupervisionTimeBucket(
            state_code=state_code,
            year=year,
            month=None,
            supervision_type=supervision_type,
            revocation_type=revocation_type,
            source_violation_type=source_violation_type
        )

    @staticmethod
    def for_year_from_month(month_bucket:
                            'RevocationReturnSupervisionTimeBucket') -> \
            'RevocationReturnSupervisionTimeBucket':
        return RevocationReturnSupervisionTimeBucket(
            state_code=month_bucket.state_code,
            year=month_bucket.year,
            month=None,
            supervision_type=month_bucket.supervision_type,
            revocation_type=month_bucket.revocation_type,
            source_violation_type=month_bucket.source_violation_type
        )

    @staticmethod
    def for_month(state_code: str, year: int, month: int,
                  supervision_type: Optional[StateSupervisionType],
                  revocation_type:
                  Optional[StateSupervisionViolationResponseRevocationType],
                  source_violation_type:
                  Optional[StateSupervisionViolationType]) -> \
            'RevocationReturnSupervisionTimeBucket':
        return RevocationReturnSupervisionTimeBucket(
            state_code=state_code,
            year=year,
            month=month,
            supervision_type=supervision_type,
            revocation_type=revocation_type,
            source_violation_type=source_violation_type
        )


@attr.s(frozen=True)
class NonRevocationReturnSupervisionTimeBucket(SupervisionTimeBucket):
    """Models a SupervisionTimeBucket where the person was not incarcerated for
    a revocation."""

    @staticmethod
    def for_year(state_code: str, year: int,
                 supervision_type: Optional[StateSupervisionType]) -> \
            'NonRevocationReturnSupervisionTimeBucket':
        return NonRevocationReturnSupervisionTimeBucket(
            state_code=state_code,
            year=year,
            month=None,
            supervision_type=supervision_type
        )

    @staticmethod
    def for_year_from_month(month_bucket:
                            'NonRevocationReturnSupervisionTimeBucket') -> \
            'NonRevocationReturnSupervisionTimeBucket':
        return NonRevocationReturnSupervisionTimeBucket(
            state_code=month_bucket.state_code,
            year=month_bucket.year,
            month=None,
            supervision_type=month_bucket.supervision_type,
        )

    @staticmethod
    def for_month(state_code: str, year: int, month: int,
                  supervision_type: Optional[StateSupervisionType]) -> \
            'NonRevocationReturnSupervisionTimeBucket':
        return NonRevocationReturnSupervisionTimeBucket(
            state_code=state_code,
            year=year,
            month=month,
            supervision_type=supervision_type
        )
