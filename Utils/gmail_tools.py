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
    toaddr = ["adim.talpiot@gmail.com", "alonb.39.talpiot@gmail.com"]
    # toaddr = ["alonb.39.talpiot@gmail.com"]

    subject = "סוציומטרי מחזור מא"  # Sociometry machzor 41"
    body = (
            u'\u202B'
            + "היי עדי! מה שלומך?"
            + "\n\n"
            + " איך בבית? מצרפים את קבצי הסוציומטרי של מחזור מא, בתיקייה מכווצת. הסיסמא לתיקייה היא:"
            + "\n\n"
            + "sociometry2020"
            + "\n\n"
            + "בגדול כל הקבצים שאת צריכה לערוך זה רק התיקייה קבצים_חניכים, אשר מכילה את כל הטפסים של המחזור כבר בוורד, תערכי על גבי הוורדים עצמם"
            + "\n\n"
            + "בברכה,"
            + "\n"
            + "צוות Talporteam!"
    )
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
