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

"""Functionality for delivery of email reports.

This module implements delivery of emails. The expectation is that the emails are in the appropriate Storage bucket
and conform to the following:

1) The bucket contains a folder whose name is the batch id
2) Inside the folder is a single html file for each recipient
3) Each file name is [email address].html
4) The contents of the file are ready to be sent with no further modification
"""

import logging
from typing import Dict, Tuple, Optional
from google.cloud import storage

import recidiviz.reporting.email_reporting_utils as utils
from recidiviz.reporting.sendgrid_client_wrapper import SendGridClientWrapper

EMAIL_SUBJECT = "Your monthly Recidiviz report"


def deliver(batch_id: str, redirect_address: Optional[str] = None) -> Tuple[int, int]:
    """Delivers emails for the given batch.

    Delivers emails to the email address specified in the generated email filename.

    If a redirect_address is provided, emails are sent to the redirect_address and the original recipient's email
    address's name (without the domain) is appended to the name (i.e. dev+recipient_name@recidiviz.org).

    Args:
        batch_id: The identifier for the batch
        redirect_address: (optional) An email address to which all emails will be sent

    Returns:
        A tuple with counts of successful deliveries and failures (successes, failures)

    Raises:
        Raises errors related to external services like Google Storage but continues attempting to send subsequent
        emails if it receives an exception while attempting to send.  In that case the error is logged.
    """
    if redirect_address:
        logging.info("Redirecting all emails for batch %s to be sent to %s", batch_id, redirect_address)
    else:
        logging.info("Delivering emails for batch %s", batch_id)

    try:
        from_email_address = utils.get_env_var('FROM_EMAIL_ADDRESS')
        from_email_name = utils.get_env_var('FROM_EMAIL_NAME')
    except KeyError:
        logging.error("Unable to get a required environment variables `FROM_EMAIL_ADDRESS` or `FROM_EMAIL_NAME`. "
                      "Exiting.")
        raise

    files = retrieve_html_files(batch_id)
    success_count = 0
    fail_count = 0
    sendgrid = SendGridClientWrapper()

    for recipient_email_address in files:
        sent_successfully = sendgrid.send_message(to_email=recipient_email_address,
                                                  from_email=from_email_address,
                                                  from_email_name=from_email_name,
                                                  subject=EMAIL_SUBJECT,
                                                  html_content=files[recipient_email_address],
                                                  redirect_address=redirect_address)

        if sent_successfully:
            success_count = success_count + 1
        else:
            fail_count = fail_count + 1

    logging.info("Sent %s emails. %s emails failed to send", success_count, fail_count)
    return success_count, fail_count


def email_from_blob_name(blob_name: str) -> str:
    """Extract the email address from a blob name.

    Args:
        blob_name: Assumes that the blob name is of the form [folder names]/[email address].html
    """
    a = blob_name.rsplit("/", 1)
    email_address = a[1].replace(".html", "")
    return email_address


def retrieve_html_files(batch_id: str) -> Dict[str, str]:
    """Loads the HTML files for this batch from Storage.

    This function is guaranteed to either return a dictionary with 1 or more results or throw an exception if there is
    a problem loading any of the files.

    Args:
        batch_id: The identifier for this batch

    Returns:
        A dict whose keys are the email addresses of recipients and values are strings of the email body to send.

    Raises:
        Passes through exceptions from Storage and raises its own if there are no results in this batch.
    """
    storage_client = storage.Client()

    html_bucket = utils.get_html_bucket_name()
    try:
        blobs = storage_client.list_blobs(html_bucket, prefix=batch_id)
    except Exception:
        logging.error("Unable to list files in html folder. Bucket = %s, folder = %s", html_bucket, batch_id)
        raise

    files = {}
    for blob in blobs:
        try:
            body = utils.load_string_from_storage(html_bucket, blob.name)
        except Exception:
            logging.error("Unable to load html file %s from bucket %s", blob.name, html_bucket)
            raise
        else:
            email_address = email_from_blob_name(blob.name)
            files[email_address] = body

    if len(files) == 0:
        msg = f"No html files found for batch {batch_id} in the bucket {html_bucket}"
        logging.error(msg)
        raise IndexError(msg)

    return files
