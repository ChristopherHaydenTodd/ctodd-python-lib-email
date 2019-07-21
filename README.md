# Christopher H. Todd's Python Lib for Emails

The ctodd-python-lib-email project is responsible for interacting with emails. Specifically, it is used for reading and sending emails from a user's account.

The library relies on Python's gmail-api package, and is wrapped with custom/specific exception handling, simpler interactions, and a more functional style to reduce code in projects dealing with Gmail API directly.

This library also has assumptions about token files and credential files, which may take pre-work depending on the usecase.

## Table of Contents

* [Dependencies](#dependencies)
* [Libraries](#libraries)
* [Example Scripts](#example-scripts)
* [Notes](#notes)
* [TODO](#todo)

## Dependencies

### Python Packages

* google-api-python-client==1.7.9
* google-auth-httplib2==0.0.3
* google-auth-oauthlib==0.4.0
* google-auth==1.6.3
* oauthlib==3.0.2

## Libraries

### [gmail_helpers.py](https://github.com/ChristopherHaydenTodd/ctodd-python-lib-email/blob/master/email_helpers/gmail_helpers.py)

Gmail Helpers.

This library is used to interact with Google's gmail application. Will
include sending emails, pulling emails, etc.

Functions:

```
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
```

```
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
```

```
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
```

```
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
```

```
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
```

```
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
```

## Example Scripts

Example executable Python scripts/modules for testing and interacting with the library. These show example use-cases for the libraries and can be used as templates for developing with the libraries or to use as one-off development efforts.

### [send_test_email_with_gmail.py](https://github.com/ChristopherHaydenTodd/ctodd-python-lib-email/blob/master/example_usage/send_test_email_with_gmail.py)

```
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
```

## Notes

 - Relies on f-string notation, which is limited to Python3.6.  A refactor to remove these could allow for development with Python3.0.x through 3.5.x
 - Only implemented Gmail, other email providers not supported

## TODO

 - Unittest framework in place, but lacking tests
 - Yahoo support
 - Outlook/Hotmail support
