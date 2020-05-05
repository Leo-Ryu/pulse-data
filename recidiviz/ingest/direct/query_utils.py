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
"""Util functions useful for any region specific SQL queries."""
import os
from typing import List, Tuple, Optional


def output_sql_queries(query_name_to_query_list: List[Tuple[str, str]], dir_path: Optional[str] = None):
    """If |dir_path| is unspecified, prints the provided |query_name_to_query_list| to the console. Otherwise
    writes the provided |query_name_to_query_list| to the specified |dir_path|.
    """
    if not dir_path:
        _print_all_queries_to_console(query_name_to_query_list)
    else:
        _write_all_queries_to_files(dir_path, query_name_to_query_list)


def _write_all_queries_to_files(dir_path: str, query_name_to_query_list: List[Tuple[str, str]]):
    """Writes the provided queries to files in the provided path."""
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    for query_name, query_str in query_name_to_query_list:
        with open(os.path.join(dir_path, f'{query_name}.sql'), 'w') as output_path:
            output_path.write(query_str)


def _print_all_queries_to_console(query_name_to_query_list: List[Tuple[str, str]]):
    """Prints all the provided queries onto the console."""
    for query_name, query_str in query_name_to_query_list:
        print(f'\n\n/* {query_name.upper()} */\n')
        print(query_str)


UPDATE_DATETIME_PARAM_NAME = "update_timestamp"

LATEST_VIEW_QUERY = """
SELECT 
  *, 
FROM 
  `{project_id}.{state_code}_raw_data_up_to_date_views.{raw_table_name}_latest`
"""

_LATEST_UPLOAD_DATE_QUERY = "(SELECT MAX(update_datetime) FROM `{project_id}.{dataset}.{table_name}`)"

_RAW_DATA_VIEW_QUERY_TEMPLATE = """
WITH rows_with_recency_rank AS (
   SELECT 
      *, 
      ROW_NUMBER() OVER (PARTITION BY {primary_keys} ORDER BY update_datetime DESC) AS recency_rank
   FROM 
      `{project_id}.{dataset}.{table_name}`
   WHERE 
       update_datetime <= {update_datetime}
)

SELECT * 
EXCEPT (file_id, recency_rank, update_datetime)
FROM rows_with_recency_rank
WHERE recency_rank = 1
"""


def create_date_bound_query_for_raw_table(project_id, state_code, raw_table_name):
    """Returns a parameterized query for the given |raw_table_name|. The caller is responsible for filling out the
    parameter. When used, this query will load all rows in the provided table up to the date of the provided date
    parameter.
    """
    primary_key_str = get_primary_key_str_for_table_name(state_code, raw_table_name)
    raw_dataset = _get_raw_data_dataset_name_for_state_code(state_code)
    parameterized_variable = '@' + UPDATE_DATETIME_PARAM_NAME
    by_update_date_query = _RAW_DATA_VIEW_QUERY_TEMPLATE.format(
        primary_keys=primary_key_str,
        project_id=project_id,
        dataset=raw_dataset,
        table_name=raw_table_name,
        update_datetime=parameterized_variable,
    )
    return by_update_date_query


def create_latest_query_for_raw_table(state_code, project_id, raw_table_name):
    """Returns a query for the given |raw_table_name|, which when used will load the most up-to-date values of all rows
    in that table.
    """
    primary_key_str = get_primary_key_str_for_table_name(state_code, raw_table_name)
    raw_dataset = _get_raw_data_dataset_name_for_state_code(state_code)
    latest_query = _RAW_DATA_VIEW_QUERY_TEMPLATE.format(
        primary_keys=primary_key_str,
        project_id=project_id,
        dataset=raw_dataset,
        table_name=raw_table_name,
        update_datetime=_LATEST_UPLOAD_DATE_QUERY.format(
            project_id=project_id,
            dataset=raw_dataset,
            table_name=raw_table_name)
    )
    return latest_query


def _get_raw_data_dataset_name_for_state_code(state_code):
    return f'{state_code}_raw_data'


# TODO(3020): Move all PK logic into Raw Yaml class
US_ID_RAW_TABLES_TO_PKS = [
    ('applc_usr', ['usr_id']),
    ('assess_qstn', ['assess_qstn_num', 'tst_sctn_num', 'assess_tst_id']),
    ('assess_qstn_choice', ['qstn_choice_num', 'assess_qstn_num', 'tst_sctn_num', 'assess_tst_id']),
    ('assess_tst', ['assess_tst_id']),
    ('behavior_evaluation_source_cd', ['behavior_evaluation_source_cd']),
    ('body_loc_cd', ['body_loc_cd']),
    ('casemgr', ['move_srl', 'case_dtd']),
    ('cis_codepersonnamesuffix', ['id']),
    ('cis_codepersonnametype', ['id']),
    ('cis_offender', ['id']),
    ('cis_personname', ['id']),
    ('clssfctn_cust_lvl', ['clssfctn_cust_lvl_cd']),
    ('cntc_rslt_cd', ['cntc_rslt_cd']),
    ('cntc_typ_cd', ['cntc_typ_cd']),
    ('cntc_typ_subtyp_cd', ['cntc_typ_cd', 'cnt_subtyp_cd']),
    ('county', ['cnty_cd']),
    ('early_discharge', ['early_discharge_id']),
    ('early_discharge_form_typ', ['early_discharge_form_typ_id']),
    ('early_discharge_sent', ['early_discharge_sent_id']),
    ('ethnic', ['ethnic_cd']),
    ('facility', ['fac_cd']),
    ('hrchy', ['staff_usr_id']),
    ('judge', ['judge_cd']),
    ('jurisdiction_decision_code', ['jurisdiction_decision_code_id']),
    ('lgl_stat_cd', ['lgl_stat_cd']),
    ('loc_typ_cd', ['loc_typ_cd']),
    ('location', ['loc_cd']),
    ('lvgunit', ['fac_cd', 'lu_cd']),
    ('mittimus', ['mitt_srl']),
    ('movement', ['move_srl']),
    ('offender', ['docno']),
    ('offense', ['off_cat', 'off_cd', 'off_deg']),
    ('offstat', ['docno', 'incrno', 'statno']),
    ('ofndr_agnt', ['ofndr_num']),
    ('ofndr_behavior_evaluation', ['ofndr_behavior_evaluation_id']),
    ('ofndr_classifications', ['classification_id']),
    ('ofndr_dob', ['ofndr_num']),
    ('ofndr_sctn_eval', ['ofndr_tst_id', 'tst_sctn_num', 'assess_tst_id']),
    ('ofndr_tst', ['ofndr_tst_id']),
    ('ofndr_tst_cert', ['ofndr_tst_id']),
    ('ofndr_wrkld', ['ofndr_wrkld_id']),
    ('sentdisp', ['sent_disp']),
    ('sentence', ['mitt_srl', 'sent_no']),
    ('sentprob', ['mitt_srl', 'sent_no']),
    ('sentretn', ['mitt_srl', 'sent_no', 'retn_no']),
    ('sexcod', ['sex_cd']),
    ('sprvsn_cntc', ['sprvsn_cntc_id']),
    ('statrls', ['stat_rls_typ', 'stat_cd']),
    ('statstrt', ['stat_strt_typ']),
    ('tst_qstn_rspns', ['tst_qstn_rspns_id']),
    ('wrkld_cat', ['wrkld_cat_id']),
]

RAW_TABLES_TO_PKS_BY_STATE = {
    'us_id': US_ID_RAW_TABLES_TO_PKS,
}


def get_raw_tables_for_state(state_code: str) -> List[str]:
    """Returns the names of all raw data tables for the given |state_code|."""
    table_names = []
    for table_name, _ in get_raw_tables_and_pk_tuples_for_state(state_code=state_code):
        table_names.append(table_name)
    return table_names


def get_raw_tables_and_pk_tuples_for_state(state_code: str) -> List[Tuple[str, List[str]]]:
    """For the provided |state_code|, returns a list of tuples which contain the raw data table name and a corresponding
    list of primary keys for that table.
    """
    raw_tables_to_pks = RAW_TABLES_TO_PKS_BY_STATE.get(state_code)
    if raw_tables_to_pks is None:
        raise ValueError(f'No found tables to primary key associations for state {state_code}')
    return raw_tables_to_pks


def get_primary_keys_for_table_name(state_code, table_name) -> List[str]:
    """Returns a list of the primary keys for the provided |state_code| and |table_name|"""
    raw_tables_to_pks = get_raw_tables_and_pk_tuples_for_state(state_code)
    for raw_table_name, pks in raw_tables_to_pks:
        if raw_table_name == table_name:
            return pks
    return []


def get_primary_key_str_for_table_name(state_code, table_name) -> str:
    """Returns the primary keys for the provided |state_code| and |table_name| in a concatenated string meant for
    SQL queries.
    """
    primary_keys = get_primary_keys_for_table_name(state_code, table_name)
    return ", ".join(primary_keys)
