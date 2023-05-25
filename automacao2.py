# from twilio.rest import Client

# account_sid = 'ACef1da88cb8569c6a6d159901520bfd0f'
# auth_token = 'a9be6ab6ef382e41b7554a5860237dfe'
# client = Client(account_sid, auth_token)

# message = client.messages.create(
#   from_='whatsapp:+14155238886',
#   body='Your appointment is coming up on July 21 at 3PM',
#   to='whatsapp:+5512992356793'
# )

# print(message.sid)


# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
#EMAIL_API = "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"
#sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
EMAIL_API = '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'

message = Mail(
    from_email='thiago@tahigomachado.dev',
    to_emails='thiagocmachado@yahoo.com.br',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(EMAIL_API)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)



# import time 
# import pywhatkit
# import pyautogui
# from pynput.keyboard import Key, Controller

# keyboard = Controller()

# def send_whatsapp_message(msg: str):
#     try:
#         pywhatkit.sendwhatmsg_instantly(
#             phone_no="<número-do-telefone>", 
#             message=msg,
#             tab_close=True
#         )
#         time.sleep(10)
#         pyautogui.click()
#         time.sleep(2)
#         keyboard.press(Key.enter)
#         keyboard.release(Key.enter)
#         print("Mensagem enviada!")
#     except Exception as e:
#         print(str(e))

# if __name__ == "__main__":
#     send_whatsapp_message(msg="Mensagem de teste de um script Python!")
