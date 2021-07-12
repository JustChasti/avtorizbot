import smtplib
import config


smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()


def send_message(email, code):
    try:
        smtpObj.login(config.email, config.password)
    except Exception as e:
        return 'Произошла ошибка входа, либо проблемы с аккаунтом, либо превышен лимит спама - необходимо что-то сделать'
    try:
        print(email, code)
        smtpObj.sendmail(config.email, email, (str(code)).encode('cp1251'))
        smtpObj.quit()
    except Exception as e:
        return 'Другая ошибка'


if __name__ == "__main__":
    print(send_message('chastytim@mail.ru', '123456'))
