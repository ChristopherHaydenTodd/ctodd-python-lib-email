"""
    Purpose:
        Gmail Helpers.

        This library is used to interact with Google's gmail application. Will
        include sending emails, pulling emails, etc.
"""

# Python Library Imports
import base64
import logging
import mimetypes
import os.path
import pickle
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


###
# Gmail Connection Functions
###


def get_gmail_service(gmail_credentials):
    """
    Purpose:
        Connect to Gmail with credentials file that is locally stored (or
        log in) so that you can read/utilize gmail services.
    Args:
        gmail_credentials (Gmail Credentials Obj): Authenticated Gmail credentials object
            that can be used to connect to Gmail
    Return:
        gmail_service (Gmail Services Obj): A connecteed Gmail service object
    """

    return build('gmail', 'v1', credentials=gmail_credentials)


###
# Credentials Functions
###


def get_gmail_credentials(
    gmail_credentials_file="~/.gmail/gmail_credentials.json",
    gmail_token_file="~/.gmail/gmail_token.pickle",
):
    """
    Purpose:
        Create or reauthenticate a token for Gmail services using a credentials file
        located on the host or reauthenticate an already existing token
    Args:
        gmail_credentials_file (String): Filename of the Gmail credentials file
        gmail_token_file (String): Filename of the Gmail token file
    Return:
        gmail_credentials (Gmail Credentials Obj): Authenticated Gmail credentials object
            that can be used to connect to Gmail
    """
    logging.info(f"Getting Gmail Credentials")

    gmail_credentials_file = os.path.expanduser(gmail_credentials_file)
    gmail_token_file = os.path.expanduser(gmail_token_file)

    # Load Pickled Gmail Token from file on disk
    gmail_credentials = None
    if os.path.exists(gmail_token_file):
        with open(gmail_token_file, 'rb') as token:
            gmail_credentials = pickle.load(token)

    # Generate/Refresh Token in Gmail
    if not gmail_credentials:
        gmail_credentials = generate_gmail_token(gmail_credentials_file)
        with open(gmail_token_file, "wb") as token:
            pickle.dump(gmail_credentials, token)
    elif gmail_credentials.expired and gmail_credentials.refresh_token:
        gmail_credentials.refresh(Request())
        with open(gmail_token_file, "wb") as token:
            pickle.dump(gmail_credentials, token)
    elif gmail_credentials.expired and not gmail_credentials.refresh_token:
        gmail_credentials = generate_gmail_token(gmail_credentials_file)
        with open(gmail_token_file, "wb") as token:
            pickle.dump(gmail_credentials, token)

    return gmail_credentials


def generate_gmail_token(gmail_credentials_file):
    """
    Purpose:
        Create a new gmail token for authentication of services
    Args:
        gmail_credentials_file (String): Filename of the Gmail credentials file
    Return:
        gmail_credentials (Gmail Credentials Obj): Authenticated Gmail credentials object
            that can be used to connect to Gmail
    """

    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.expanduser(gmail_credentials_file),
        ["https://mail.google.com/"],
    )
    gmail_credentials = flow.run_local_server(port=0)

    return gmail_credentials


###
# Sending Functions
###


def send_email(gmail_service, email_msg):
    """
    Purpose:
        Send email through a gmail server object
    Args:
        gmail_service (Gmail Service Object): Connected Gmail Service
        email_msg (Message Object): Email message to send through Gmail
    Return:
        N/A
    """
    logging.info("Sending Email through Gmail")

    try:
        gmail_service.users().messages().send(userId="me", body=email_msg).execute()
    except Exception as err:
        logging.exception(f"Error: unable to send email through gmail: {err}")
        raise err


###
# Build Message Functions
###


def build_msg_obj(
    email_from,
    email_subject,
    email_body,
    email_to,
    email_cc=[],
    email_bcc=[],
    email_attachments=[],
):
    """
    Purpose:
        Build and encode an email message object to send through a gmail
        server
    Args:
        email_from (String): From address for the email
        email_subject (String): Subject of the email
        email_body (String): String body of the email
        email_to (List of Strings): List of email addresses to add as a TO on email
        email_cc (List of Strings): List of email addresses to add as a CC on email.
            Defaults to [] (no addresses)
        email_bcc (List of Strings): List of email addresses to add as a BCC on email.
            Defaults to [] (no addresses)
        email_attachments (List of Strings): List of filenames that will be attached
            to the email. Defaults to [] (no attachmensts)
    Return:
        email_msg (Message Object): Encoded email message object ready to be sent
    """
    logging.info("Building Email")

    # Create Email Metadata
    email_msg = MIMEMultipart()
    email_msg["subject"] = email_subject
    email_msg["from"] = email_from
    email_msg["to"] = ", ".join(email_to)
    email_msg["cc"] = "" if not email_cc else ", ".join(email_cc)
    email_msg["bcc"] = "" if not email_bcc else ", ".join(email_bcc)

    # Create Message Body
    email_msg.attach(MIMEText(email_body, "plain"))

    # Handle Atachment
    for attachment_filename in email_attachments:
        attachment = encode_attachment_for_email(attachment_filename)
        attachment.add_header(
            "Content-Disposition", "attachment", filename=attachment_filename
        )
        email_msg.attach(attachment)

    return {'raw': base64.urlsafe_b64encode(email_msg.as_string().encode()).decode()}


def encode_attachment_for_email(attachment_filename):
    """
    Purpose:
        Guess the encoding and prepare the attachment for being added to the email
    Args:
        attachment_filename (String): String filename of the attachment
    Returns:
        attachment (Encoded Attachment Obj): Encoded Attachment Obj ready to be
            added to the email message
    """

    # Guess Encoding
    content_type, encoding = mimetypes.guess_type(attachment_filename)
    if content_type is None or encoding is not None:
        content_type = "application/octet-stream"
    if attachment_filename.endswith(".xlsx"):
        content_type = "application/vnd-xls"
    main_type, sub_type = content_type.split("/")

    # Prepage Attachment
    with open(attachment_filename, "rb") as attachment_file_obj:
        if main_type == "text":
            attachment = MIMEText(attachment_file_obj.read(), _subtype=sub_type)
        elif main_type == "image":
            attachment = MIMEImage(attachment_file_obj.read(), _subtype=sub_type)
        elif main_type == "audio":
            attachment = MIMEAudio(attachment_file_obj.read(), _subtype=sub_type)
        elif sub_type == "vnd-xls":
            attachment = MIMEApplication(attachment_file_obj.read(), _subtype=sub_type)
        else:
            attachment = MIMEBase(main_type, sub_type)
            attachment.set_payload(attachment_file_obj.read())

    return attachment
