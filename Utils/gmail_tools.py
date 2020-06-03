import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def get_name(path):
    lst = path.split("/")
    name = lst[-1]
    return name


def sendGmail(fromaddr, toaddr, subject, body, path, psw):
    # open the file to be sent
    filename = get_name(path)
    attachment = open(path, "rb")
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = ", ".join(toaddr)

    # storing the subject
    msg['Subject'] = subject

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, psw)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


def stage1(path):
    fromaddr = "talportal.talpiot@gmail.com"
    psw = "CyberCyber1*"
    toaddr = ["talportal.talpiot@gmail.com"]
    # toaddr = ["amit.dovner.40@gmail.com"]
    # toaddr = ["alonb.39.talpiot@gmail.com"]

    subject = "סוציומטרי מחזור מא"  # Sociometry machzor 41"
    body = "היי עדי! מה שלומך? איך בבית? מצרפים את קבצי הסוציומטרי של מחזור מא, בהצלחה!!!"
    sendGmail(fromaddr, toaddr, subject, body, path, psw)


def stage2(path):
    fromaddr = "talportal.talpiot@gmail.com"
    psw = "CyberCyber1*"
    toaddr = ['zohar.radovsky.41@gmail.com', 'z.radovsky@gmail.com', 'talportal.talpiot@gmail.com']

    subject = "סוציומטרי אחרי עריכה של מחזור מא 4"  # Sociometry machzor 41"
    body = "היי מפקדים מצורפים טפסי סוציומטרי"
    sendGmail(fromaddr, toaddr, subject, body, path, psw)


# path = "./try.zip"
# stage2(path)
