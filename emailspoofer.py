#!/usr/bin/env python3

import argparse
import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    args = get_args()
    print(args)

def gmail_send_message(to_addr, from_addr, msg, subj):
    """
    Sends an email using Google's Gmail API
    This function is from https://developers.google.com/gmail/api/guides/sending
    """

    creds, _ = google.auth.default()

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(msg)

        message['To'] = to_addr
        message['From'] = from_addr
        message['Subject'] = subj

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'[+] Sending email with ID: {send_message["id"]}')
    except HttpError as error:
        print(F'[-] An error occurred: {error}')
        send_message = None
    return send_message

def get_args():
    """
    Parses the command line arguemtns needed to run the spoofer.

    options:
    -t TO_ADDRESS, --to-address TO_ADDRESS
                            The address to send the email to.
    -f FROM_ADDRESS, --from-address FROM_ADDRESS
                            The from address.
    -s SUBJECT, --subject SUBJECT
                            The subject of the email.
    -a AUTH_FILE, --auth-file AUTH_FILE
                            The file path of the credentials.json used for authentication.
    -m MESSAGE, --message MESSAGE
                            The message/body of the email.
    -o FILE, --file FILE  The message specified from a file.
    """
    parser = argparse.ArgumentParser(
                    description = 'Uses the gmail cloud API to send an email.',
                    epilog = 'Use at your own discretion.')

    parser.add_argument('-t', '--to-address', help='The address to send the email to.', required=True)
    parser.add_argument('-f', '--from-address', help='The from address.', required=True)
    parser.add_argument('-s', '--subject', help='The subject of the email.', required=True)
    parser.add_argument('-a', '--auth-file', help='The file path of the credentials.json used for authentication.', required=True)
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--message', help='The message/body of the email.')
    group.add_argument('-o', '--file', help='The message specified from a file.')

    return parser.parse_args()

if __name__ == '__main__':
    main()