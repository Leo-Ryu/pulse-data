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
"""Reference views used by other views."""
from typing import List

from recidiviz.big_query.big_query_view import BigQueryView
from recidiviz.calculator.query.state.views.reference.augmented_agent_info import AUGMENTED_AGENT_INFO_VIEW
from recidiviz.calculator.query.state.views.reference.us_mo_sentence_statuses import US_MO_SENTENCE_STATUSES_VIEW
from recidiviz.calculator.query.state.views.reference.most_recent_job_id_by_metric_and_state_code import \
    MOST_RECENT_JOB_ID_BY_METRIC_AND_STATE_CODE_VIEW
from recidiviz.calculator.query.state.views.reference.persons_to_recent_county_of_residence import \
    PERSONS_TO_RECENT_COUNTY_OF_RESIDENCE_VIEW
from recidiviz.calculator.query.state.views.reference.persons_with_last_known_address import \
    PERSONS_WITH_LAST_KNOWN_ADDRESS_VIEW
from recidiviz.calculator.query.state.views.reference.ssvr_to_agent_association import \
    SSVR_TO_AGENT_ASSOCIATION_VIEW
from recidiviz.calculator.query.state.views.reference.supervision_period_to_agent_association import \
    SUPERVISION_PERIOD_TO_AGENT_ASSOCIATION_VIEW
from recidiviz.calculator.query.state.views.reference.event_based_admissions import \
    EVENT_BASED_ADMISSIONS_VIEW
from recidiviz.calculator.query.state.views.reference.event_based_program_referrals import \
    EVENT_BASED_PROGRAM_REFERRALS_VIEW
from recidiviz.calculator.query.state.views.reference.event_based_revocations import \
    EVENT_BASED_REVOCATIONS_VIEW
from recidiviz.calculator.query.state.views.reference.event_based_supervision import \
    EVENT_BASED_SUPERVISION_VIEW
from recidiviz.calculator.query.state.views.reference.revocations_matrix_by_person import \
    REVOCATIONS_MATRIX_BY_PERSON_VIEW
from recidiviz.calculator.query.state.views.reference.supervision_matrix_by_person import \
    SUPERVISION_MATRIX_BY_PERSON_VIEW

REF_VIEWS: List[BigQueryView] = [
    MOST_RECENT_JOB_ID_BY_METRIC_AND_STATE_CODE_VIEW,
    AUGMENTED_AGENT_INFO_VIEW,
    SSVR_TO_AGENT_ASSOCIATION_VIEW,
    SUPERVISION_PERIOD_TO_AGENT_ASSOCIATION_VIEW,
    PERSONS_WITH_LAST_KNOWN_ADDRESS_VIEW,
    PERSONS_TO_RECENT_COUNTY_OF_RESIDENCE_VIEW,
    EVENT_BASED_ADMISSIONS_VIEW,
    EVENT_BASED_PROGRAM_REFERRALS_VIEW,
    EVENT_BASED_REVOCATIONS_VIEW,
    EVENT_BASED_SUPERVISION_VIEW,
    REVOCATIONS_MATRIX_BY_PERSON_VIEW,
    SUPERVISION_MATRIX_BY_PERSON_VIEW,
    US_MO_SENTENCE_STATUSES_VIEW,
]
