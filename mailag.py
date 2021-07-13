import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import config



smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()


def send_message(email, code):
    try:
        smtpObj.login(config.email, config.password)
    except Exception as e:
        print('Произошла ошибка входа, либо проблемы с аккаунтом, либо превышен лимит спама - необходимо что-то сделать')
        time.sleep(20)
        return send_message(email,code)
    try:
        msg = MIMEText(code, 'plain', 'utf-8')
        msg['Subject'] = Header('avtorisation bot', 'utf-8')
        msg['From'] = config.email
        msg['To'] = email
        smtpObj.sendmail(config.email, email, msg.as_string())
        smtpObj.quit()
    except Exception as e:
        return 'Другая ошибка'


if __name__ == "__main__":
    print(send_message('chastytim@mail.ru', 'спасибо1'))
