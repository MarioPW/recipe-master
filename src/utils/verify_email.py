import smtplib
from email.message import EmailMessage
import ssl
from dotenv import load_dotenv
from os import getenv
from random import randint
from pydantic import EmailStr


load_dotenv()

class SendEmailVerify:
  
  def __init__(self, email: EmailStr) -> None:
      self.email = email
  
  def create_verify_code(self) -> int: 
    code_list = [randint(0, 9) for _ in range(4)]
    if code_list[0] == 0: # If the number begins with 0, the 'int' type will be incorrect; 
       code_list[0] = 7   # so in that case, I changed it to a seven just because :)
    code_str = ''.join(map(str, code_list))
    code_int = int(code_str)
    return code_int
  
  def sendVerify(self, code):
    email_address = getenv("EMAIL")
    email_password = getenv("EMAIL_PASSWORD")
    # create email
    msg = EmailMessage()
    msg['Subject'] = "Register Verification Code"
    msg['From'] = email_address
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
                    ">{code}</p>
        </div>
        </body>
      </html>
    """
    msg.set_content(html_message, subtype='html')
    context1 = ssl.create_default_context()
    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context1) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
# Test
if __name__ == "__main__":

    mail = SendEmailVerify("mariotriana1978@gmail.com")
    mail.sendVerify(1234)