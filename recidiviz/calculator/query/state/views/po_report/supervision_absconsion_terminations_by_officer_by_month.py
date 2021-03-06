# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2020 Recidiviz, Inc.
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
"""Supervision terminations for absconsion per officer by month."""
# pylint: disable=trailing-whitespace

from recidiviz.big_query.big_query_view import SimpleBigQueryViewBuilder
from recidiviz.calculator.query import bq_utils
from recidiviz.calculator.query.state import dataset_config
from recidiviz.utils.environment import GCP_PROJECT_STAGING
from recidiviz.utils.metadata import local_project_id_override

SUPERVISION_ABSCONSION_TERMINATIONS_BY_OFFICER_BY_MONTH_VIEW_NAME = \
    'supervision_absconsion_terminations_by_officer_by_month'

SUPERVISION_ABSCONSION_TERMINATIONS_BY_OFFICER_BY_MONTH_DESCRIPTION = """
 Total supervision periods terminated for absconsion by officer and by month.
 """

# TODO(#4155): Use the supervision_termination_metrics instead of the raw state_supervision_period table
SUPERVISION_ABSCONSION_TERMINATIONS_BY_OFFICER_BY_MONTH_QUERY_TEMPLATE = \
    """
    /*{description}*/

    WITH absconsions AS (
      SELECT violation.state_code, violation.person_id, response_type, response_date, violation_type, 
        agent.agent_external_id AS officer_external_id,
        EXTRACT(YEAR FROM response_date) AS year, EXTRACT(MONTH FROM response_date) AS month
      -- TODO(#4491): Consider using `external_id` instead of `agent_external_id`
      FROM `{project_id}.{state_dataset}.state_supervision_violation_response` violation
      LEFT JOIN `{project_id}.{state_dataset}.state_supervision_violation_type_entry` type
        USING (supervision_violation_id, person_id, state_code)
      LEFT JOIN `{project_id}.{state_dataset}.state_supervision_period` period
      ON period.person_id = violation.person_id 
        AND period.state_code = violation.state_code
        AND response_date >= period.start_date
        AND response_date <= COALESCE(period.termination_date, '9999-12-31')
      LEFT JOIN `{project_id}.{reference_views_dataset}.supervision_period_to_agent_association` agent
        ON period.supervision_period_id = agent.supervision_period_id
          AND period.state_code = agent.state_code
      WHERE violation_type = 'ABSCONDED'
        AND supervision_period_supervision_type IN ('DUAL', 'PROBATION', 'PAROLE', 'INTERNAL_UNKNOWN')
    ), absconsions_per_officer AS (
      SELECT
        state_code, year, month, officer_external_id,
        COUNT(DISTINCT person_id) AS absconsion_count
      FROM absconsions
      GROUP BY state_code, year, month, officer_external_id
    ),
    avg_absconsions_by_district_state AS (
        -- Get the average monthly absconsions by district and state
        SELECT
          state_code, year, month,
          district,
          AVG(IFNULL(absconsion_count, 0)) AS avg_absconsions
        FROM `{project_id}.{po_report_dataset}.officer_supervision_district_association_materialized`
        LEFT JOIN absconsions_per_officer
            USING (state_code, year, month, officer_external_id),
        {district_dimension}
        GROUP BY state_code, year, month, district   
    )
    SELECT
      state_code, year, month,
      officer_external_id, district,
      IFNULL(absconsions_per_officer.absconsion_count, 0) AS absconsions,
      district_avg.avg_absconsions AS absconsions_district_average,
      state_avg.avg_absconsions AS absconsions_state_average
    FROM `{project_id}.{po_report_dataset}.officer_supervision_district_association_materialized`
    LEFT JOIN absconsions_per_officer
      USING (state_code, year, month, officer_external_id)
    LEFT JOIN(
        SELECT * FROM avg_absconsions_by_district_state
        WHERE district != 'ALL'
    ) district_avg
        USING (state_code, year, month, district)
    LEFT JOIN (
      SELECT * EXCEPT (district) FROM avg_absconsions_by_district_state
      WHERE district = 'ALL'
    ) state_avg
      USING (state_code, year, month)
    ORDER BY state_code, year, month, district, officer_external_id
    """

SUPERVISION_ABSCONSION_TERMINATIONS_BY_OFFICER_BY_MONTH_VIEW_BUILDER = SimpleBigQueryViewBuilder(
    dataset_id=dataset_config.PO_REPORT_DATASET,
    view_id=SUPERVISION_ABSCONSION_TERMINATIONS_BY_OFFICER_BY_MONTH_VIEW_NAME,
    should_materialize=True,
    view_query_template=SUPERVISION_ABSCONSION_TERMINATIONS_BY_OFFICER_BY_MONTH_QUERY_TEMPLATE,
    description=SUPERVISION_ABSCONSION_TERMINATIONS_BY_OFFICER_BY_MONTH_DESCRIPTION,
    reference_views_dataset=dataset_config.REFERENCE_VIEWS_DATASET,
    state_dataset=dataset_config.STATE_BASE_DATASET,
    district_dimension=bq_utils.unnest_district(district_column='district'),
    po_report_dataset=dataset_config.PO_REPORT_DATASET
)

if __name__ == '__main__':
    with local_project_id_override(GCP_PROJECT_STAGING):
        SUPERVISION_ABSCONSION_TERMINATIONS_BY_OFFICER_BY_MONTH_VIEW_BUILDER.build_and_print()
