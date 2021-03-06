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
# pylint:disable=bare-except

"""A single module containing all Python code related to Email Reporting.

"""

from http import HTTPStatus
import logging
from typing import Tuple

from flask import Blueprint, request

import recidiviz.reporting.data_retrieval as data_retrieval
import recidiviz.reporting.email_delivery as email_delivery
from recidiviz.utils.auth import authenticate_request
from recidiviz.utils.params import get_str_param_value

reporting_endpoint_blueprint = Blueprint('reporting_endpoint_blueprint', __name__)


@reporting_endpoint_blueprint.route('/start_new_batch', methods=['GET', 'POST'])
@authenticate_request
def start_new_batch() -> Tuple[str, HTTPStatus]:
    """Start a new batch of email generation for the indicated state.

    Query parameters:
        state_code: (required) A valid state code for which reporting is enabled (ex: "US_ID")
        report_type: (required) A valid report type identifier (ex: "po_monthly_report)
        test_address: (optional) Should only be used for testing. When provided, the test_address is used to generate
        the email filenames, ensuring that all emails in the batch can only be delivered to the test_address and not
        to the usual recipients of the report. The email filenames will include the original recipient's email username,
        for example: tester+recipient_username@tester-domain.org.

    Returns:
        Text indicating the results of the run and an HTTP status

    Raises:
        Nothing.  Catch everything so that we can always return a response to the request
    """
    state_code = get_str_param_value('state_code', request.args)
    report_type = get_str_param_value('report_type', request.args)
    test_address = get_str_param_value('test_address', request.args)

    if not state_code or not report_type:
        msg = "Request does not include 'state_code' and 'report_type' parameters"
        logging.error(msg)
        return msg, HTTPStatus.BAD_REQUEST

    state_code = state_code.upper()

    batch_id = data_retrieval.start(state_code, report_type, test_address)

    test_address_text = f"Emails generated for test address: {test_address}" if test_address else ""
    return (f"New batch started for {state_code} and {report_type}.  Batch "
            f"id = {batch_id}. {test_address_text}"), HTTPStatus.OK


@reporting_endpoint_blueprint.route('/deliver_emails_for_batch', methods=['GET', 'POST'])
@authenticate_request
def deliver_emails_for_batch() -> Tuple[str, HTTPStatus]:
    """Deliver a batch of generated emails.

    Query parameters:
        batch_id: (required) Identifier for this batch
        redirect_address: (optional) An email address to which all emails will be sent. This can be used for redirecting
        all of the reports to a supervisor.

    Returns:
        Text indicating the results of the run and an HTTP status

    Raises:
        Nothing.  Catch everything so that we can always return a response to the request
    """
    batch_id = get_str_param_value('batch_id', request.args)
    redirect_address = get_str_param_value('redirect_address', request.args)

    if not batch_id:
        msg = "Query parameter 'batch_id' not received"
        logging.error(msg)
        return msg, HTTPStatus.BAD_REQUEST

    if redirect_address:
        success_count, failure_count = email_delivery.deliver(batch_id, redirect_address=redirect_address)
        return (f"Sent {success_count} emails to the test address {redirect_address}. "
                f"{failure_count} emails failed to send"), HTTPStatus.OK

    success_count, failure_count = email_delivery.deliver(batch_id)
    return f"Sent {success_count} emails. {failure_count} emails failed to send", HTTPStatus.OK
