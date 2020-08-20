from typing import List

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content
from sendgrid.helpers.mail import From
from sendgrid.helpers.mail import HtmlContent
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import PlainTextContent
from sendgrid.helpers.mail import SendGridException
from sendgrid.helpers.mail import Subject
from sendgrid.helpers.mail import To

from . import Engine
from .. import DeliveryNotMade


class SendGridDeliveryEngine(Engine):
    def __init__(self, api_key):
        self.api_key = api_key

    def send_simple_message(
        self,
        from_address: str,
        to_addresses: List[str],
        subject: str,
        text_body: str = None,
        html_body: str = None,
    ):
        message = Mail(
            from_email=From(from_address),
            to_emails=[To(to_address) for to_address in to_addresses],
            subject=Subject(subject),
        )
        if html_body:
            message.content = HtmlContent(html_body.strip())
        if text_body:
            message.content = PlainTextContent(text_body.strip())

        try:

            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)

            if response.status_code < 200 or response.status_code > 299:
                raise DeliveryNotMade(
                    details=f"Got unexpected status from mailgun: {response.status_code}",
                    response=response,
                )
            return True
        except SendGridException as e:
            print(str(e))
            raise e
        except DeliveryNotMade as e:
            print(str(e))
            raise e
        except Exception as e:
            print(str(e))
            raise e
