from email.mime.text import MIMEText
import smtplib
from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser
from app.models import Message

router = APIRouter(prefix="/utils", tags=["utils"])

def send_email(subject, body, to_email):
    from_email = "mux.campuscar@gmail.com"
    password = "igep netf tgzv kien"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, password)
        server.send_message(msg)

@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    send_email("Test Alert", "This is a test message from your app", email_to)
    return Message(message="Test email sent")



@router.get("/health-check/")
async def health_check() -> bool:
    return True
