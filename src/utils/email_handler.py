from fastapi.responses import JSONResponse
from fastapi import HTTPException
import smtplib
from email.message import EmailMessage
import ssl
from dotenv import load_dotenv
from os import getenv
from pydantic import EmailStr
from .create_verification_code import create_verification_code

load_dotenv()

class EmailHandler:
    def __init__(self, email: EmailStr) -> None:
        self.email = email
        self.email_address = getenv("EMAIL")
        self.email_password = getenv("EMAIL_PASSWORD")
        self.change_password_endpiont = getenv("CHANGE_PASSWORD_ENDPIONT")
        self.verification_code = create_verification_code()
    
    def get_verification_code(self):
        return self.verification_code
  
    def send_verification_email(self):
        msg = EmailMessage()
        msg['Subject'] = "Register Verification Code"
        msg['From'] = self.email_address
        msg['To'] = self.email
        html_message = f"""\
        <html>
            <body>
              <div style="text-align: center;">
                <p style= "font-weight: bold;
                          font-family: sans-serif;"
                          >Type or copy-paste this code to verify your registration:</p>
                <p style="display: inline-block;
                          background-color: rgb(61, 61, 254);
                          padding: 7px 11px;
                          color: white;
                          border-radius: 11px;
                          font-size: 24px;
                          font-family: sans-serif;
                          letter-spacing: 3px;
                          ">{self.verification_code}
                </p>
              </div>
            </body>
          </html>
        """
        msg.set_content(html_message, subtype='html')
        context1 = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context1) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error sendin email in src/utils/email_handler.py: {e}")
      
    def send_change_password_email(self):
        msg = EmailMessage()
        msg['Subject'] = "Recover Password"
        msg['From'] = self.email_address
        msg['To'] = self.email
        html_message = f"""\
        <html>
            <body>
            <div style="text-align: center;">
              <h1 style= "font-weight: bold;
                        font-family: sans-serif;"
                        >Let's Reset your Password:</h1>
              <p>If you want to reset your Recipe Master password, use the button below. This action will take you to a secure page where you can reset it.</p>
              <a style="display:inline-block;
                        font-family:'RoobertPRO',Helvetica,Arial,sans-serif;
                        font-size:16px;line-height:24px;
                        color:#ffffff;background-color:#4262ff;
                        text-decoration:none;
                        padding:11px 16px 13px 16px;
                        border-radius:8px;
                        text-align:center"
                        href='{self.change_password_endpiont}'>Reset Password</a>
              <p>If you don't want to reset your password, ignore this message.</br>Your password will not be reset.
                Happy collaborating,
                Recipe Master Team
              </p>
            </div>
            </body>
          </html>
        """
        msg.set_content(html_message, subtype='html')
        context1 = ssl.create_default_context()
        try:
          with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context1) as smtp:
              smtp.login(self.email_address, self.email_password)
              smtp.send_message(msg)
          return JSONResponse(status_code=200, content={"message": f'Email to {self.email} sended successfully'})
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error sending change password email: {e}")
  
# Test
if __name__ == "__main__":
    WEB_MASTER_EMAIL = getenv('WEB_MASTER_EMAIL')
    mail = EmailHandler("WEB_MASTER_EMAIL")
    mail.send_verification_email()