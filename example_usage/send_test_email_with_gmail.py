#!/usr/bin/env python3.6
"""
    Purpose:
        Send a test email utilizing Gmail

    Steps:
        - Generate a token
        - Connect to Google Service
        - Build Message Object
        - Send Email

    function call:
        send_test_email_with_gmail.py [-h]
            [--gmail-token-file GMAIL_TOKEN_FILE]
            [--gmail-credentials-file GMAIL_CREDENTIALS_FILE]
            [--email-cc EMAIL_CC]
            [--email-bcc EMAIL_BCC]
            [--email-attachements EMAIL_ATTACHEMENTS]
            --gmail-account GMAIL_ACCOUNT --email-to
            EMAIL_TO --email-subject EMAIL_SUBJECT
            --email-body EMAIL_BODY

    example call:
        python3.6 send_test_email_with_gmail.py \
            --gmail-account="gmail_account@gmail.com" \
            --email-to="gmail_account_to@gmail.com" \
            --email-subject="Test Email" \
            --email-body="This is a test email" \
            --email-cc="gmail_account_cc1@gmail.com" \
            --email-cc="gmail_account_cc2@gmail.com" \
            --email-bcc="gmail_account_bcc@gmail.com" \
            --email-attachements="/pah/to/file.png" \
            --email-attachements="/pah/to/file2.png"
"""

# Python Library Imports
import logging
import os
import sys
from argparse import ArgumentParser

# Local Library Imports
from email_helpers import gmail_helpers


def main():
    """
    Purpose:
        Read an .avro File
    """
    logging.info("Starting Send Email Process")

    opts = get_options()

    gmail_credentials = gmail_helpers.get_gmail_credentials(
        gmail_credentials_file=opts.gmail_credentials_file,
        gmail_token_file=opts.gmail_token_file,
    )
    gmail_service = gmail_helpers.get_gmail_service(gmail_credentials)

    email_msg = gmail_helpers.build_msg_obj(
        opts.gmail_account,
        opts.email_subject,
        opts.email_body,
        opts.email_to,
        email_cc=opts.email_cc,
        email_bcc=opts.email_bcc,
        email_attachments=opts.email_attachements,
    )

    gmail_helpers.send_email(gmail_service, email_msg)

    logging.info("Send Email Process Complete")


###
# General/Helper Methods
###


def get_options():
    """
    Purpose:
        Parse CLI arguments for script
    Args:
        N/A
    Return:
        N/A
    """

    parser = ArgumentParser(description="Send Test Email With Gmail")
    required = parser.add_argument_group('Required Arguments')
    optional = parser.add_argument_group('Optional Arguments')

    # Optional Arguments
    optional.add_argument(
        "--gmail-token-file",
        dest="gmail_token_file",
        help="Gmail Token Filename",
        required=False,
        default=os.path.expanduser("~/.gmail/gmail_token.pickle"),
    )
    optional.add_argument(
        "--gmail-credentials-file",
        dest="gmail_credentials_file",
        help="Gmail Credential Filename",
        required=False,
        default=os.path.expanduser("~/.gmail/gmail_credentials.json"),
    )
    optional.add_argument(
        "--email-cc",
        dest="email_cc",
        help="Emails to CC",
        required=False,
        default=None,
        action="append",
    )
    optional.add_argument(
        "--email-bcc",
        dest="email_bcc",
        help="Emails to BCC",
        required=False,
        default=None,
        action="append",
    )
    optional.add_argument(
        "--email-attachements",
        dest="email_attachements",
        help="Objects to attach to the email",
        required=False,
        default=None,
        action="append",
    )


    # Required Arguments
    required.add_argument(
        "--gmail-account",
        dest="gmail_account",
        help="Gmail account to use to send email",
        required=True,
    )
    required.add_argument(
        "--email-to",
        dest="email_to",
        help="Emails to TO",
        required=True,
        action="append",
    )
    required.add_argument(
        "--email-subject",
        dest="email_subject",
        help="Subject of the email",
        required=True,
    )
    required.add_argument(
        "--email-body",
        dest="email_body",
        help="Body of the email",
        required=True,
    )

    return parser.parse_args()


if __name__ == "__main__":

    log_level = logging.INFO
    logging.getLogger().setLevel(log_level)
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format="[send_test_email_with_gmail] %(asctime)s %(levelname)s %(message)s",
        datefmt="%a, %d %b %Y %H:%M:%S"
    )

    try:
        main()
    except Exception as err:
        print(
            "{0} failed due to error: {1}".format(os.path.basename(__file__), err)
        )
        raise err
