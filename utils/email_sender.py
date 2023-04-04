
from redmail import EmailSender
from smtplib import SMTP_SSL


class ManyEmailsSender(EmailSender):
    
    def __init__(self, email, 
                 password, host='smtp.yandex.ru', 
                 port=465,
                 *args, **kwargs):
        super().__init__(
            username=email,
            password=password,
            host=host,
            port=port,
            use_starttls=False,
            cls_smtp=SMTP_SSL,
            *args, **kwargs
        )
    
    
    def send_emails(
        self, subject: str, text_template: str, 
        html_template: str, receivers: list[dict], 
        common_fields: dict, attachments: dict[str, bytes]
    ):
        with self:
            for receiver in receivers:
                body_params = receiver | common_fields
                email = body_params.pop('email')
                data = self.send(
                    subject=subject,
                    text=text_template,
                    html=html_template,
                    receivers=email,
                    body_params=body_params,
                    attachments=attachments,
                    headers={
                        'list-unsubscribe': common_fields['unsubscribe_link'],
                        'Precedence': 'bulk'
                    }
                )
                print(data)
        return self
        



