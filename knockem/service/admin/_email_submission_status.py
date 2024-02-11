import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from ._get_admin_email import get_admin_email
from ._get_daemon_email import get_daemon_email
from ._get_sendgrid_api_key import get_sendgrid_api_key


def email_submission_status(
    submissionId: str, userEmail: str, status: str, statusDetails: str
) -> None:
    sendgrid_api_key = get_sendgrid_api_key()
    if sendgrid_api_key is None:
        logging.warning("No SendGrid API key found, skipping email.")
        return

    nl = "\n"  # no slashes in fstring
    message = Mail(
        from_email=get_daemon_email(),
        to_emails=userEmail,
        subject=f"knockem submission {submissionId}",
        html_content=f"""<strong>status:</strong> {status}<br>
        <strong>details:</strong><br>
        <blockquote>{statusDetails.replace(nl, "<br>")}</blockquote><br><br>
        <i>not expecting this email? contact {get_admin_email()}</i>
        """,
    )
    try:
        logging.info(
            f"Sending {status} email to {userEmail} "
            f"for submission {submissionId}",
        )
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)
        logging.info(
            f"{response.status_code=} {response.body=} {response.headers=}",
        )
    except Exception as e:
        logging.error(e.message)
