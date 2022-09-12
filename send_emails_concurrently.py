import os
import ssl
import csv
import smtplib
import pathlib
import argparse
import concurrent.futures
from email.message import EmailMessage
from typing import Iterator, Generator, NamedTuple


parser = argparse.ArgumentParser()
parser.add_argument(
    '--input-file',
    dest='input_file',
    type=argparse.FileType('r'),
    default=pathlib.Path(__file__).parent / pathlib.Path('data.csv'),
    help=(
        'Path to a .csv file that contains mailing information.'
        ' The following headers are used: recipient, subject, content.'
        ' data.csv file is used by default.'
    )
)
args = parser.parse_args()


SMTP_SERVER_HOST = os.environ['SMTP_SERVER_HOST']
SMTP_SERVER_PORT = int(os.environ['SMTP_SERVER_PORT'])
EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']


class _Email(NamedTuple):
    recipient: str
    subject: str
    content: str
    sender: str = EMAIL_ADDRESS


def _get_email_data() -> Generator[_Email, None, None]:
    with open(args.input_file, 'rt', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Recipient, subject, content.

        for row in csv_reader:
            yield _Email(*row)


def _compose_message(datum: _Email) -> EmailMessage:
    message = EmailMessage()
    message['From'] = datum.sender
    message['To'] = datum.recipient
    message['Subject'] = datum.subject
    message.set_content(datum.content)
    return message


def send_emails_concurrently() -> Iterator:
    with smtplib.SMTP_SSL(
        host=SMTP_SERVER_HOST,
        port=SMTP_SERVER_PORT,
        context=ssl.create_default_context()
    ) as smtp_server:
        smtp_server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return executor.map(
                smtp_server.send_message,
                (_compose_message(datum) for datum in _get_email_data())
            )


if __name__ == '__main__':
    send_emails_concurrently()
