# import smtplib
# from email.message import EmailMessage
# import ssl
# from dotenv import load_dotenv
# from os import getenv
# from random import randint

# load_dotenv()

# class SendEmailVerify:
 
#   def sendVerify(self, email):
#     email_address = getenv("EMAIL")
#     email_password = getenv("EMAIL_PASSWORD")
#     # create email
#     msg = EmailMessage()
#     msg['Subject'] = "Register Verification Code"
#     msg['From'] = email_address
#     msg['To'] = email
#     verify_code = [randint(0,9) for i in range(4)]
#     code_str = ''.join(map(str, verify_code))

#     # Crea un mensaje HTML con estilo
#     html_message = f"""\
#     <html>
#       <body>
#       <div style="text-align: center;">
#         <p style= font-weight: bold;
#                   >Type or copy-paste this code to verify your registration to our Page:</p>
#         <p style="bockground-color: blue;
#                   rounded: 
#                   font-size: 24px;
#                   font-weight: bold;
#                   ">{code_str}</p>
#       </div>
#       </body>
#     </html>
#     """

#     # Establece el contenido del mensaje como HTML
#     msg.set_content(html_message, subtype='html')

#     context1 = ssl.create_default_context()

#     # send email
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context1) as smtp:
#         smtp.login(email_address, email_password)
#         smtp.send_message(msg)

# if __name__ == "__main__":

#     mail = SendEmailVerify()
#     mail.sendVerify("mariotriana1978@gmail.com")