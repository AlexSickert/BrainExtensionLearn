import smtplib
import log
import config as cfg
import threading
import queue
import time





def send_mail(to_email, email_subject, email_message):

    log.log_info("in send_mail")

    FROM = cfg.parameters["email-user"]
    TO = [to_email]

    #print(email_message)

    password = cfg.parameters["email-password"]

    SUBJECT = "" + email_subject

    TEXT = email_message

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # SMTP_SSL Example
    #server_ssl = smtplib.SMTP_SSL(host="smtp.alexandersickert.com", port=465)
    server_ssl = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)


    server_ssl.ehlo() # optional, called by login()
    server_ssl.login(FROM, password)
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(FROM, TO, message)
    #server_ssl.quit()
    server_ssl.close()
    #print( 'successfully sent the mail')
    log.log_info("end send_mail")


q = queue.Queue(0)


class Worker(threading.Thread):

    def __init__(self, queue):
        self.__queue = queue
        threading.Thread.__init__(self)

    def run(self):
        while True:
            item = self.__queue.get()
            if item is not None:
                try:
                    send_mail(item[0], item[1], item[2])
                except Exception as ex:
                    log.log_error("Error sending mail threaded... " + str(ex))
                    time.sleep(100)
                time.sleep(1)
            else:
                time.sleep(10)


# starting the endless loop in thread
Worker(q).start()


def send_mail_queued(to_email, email_subject, email_message):

    global q

    try:
        element = [to_email, email_subject, email_message]
        q.put(element)
    except Exception as ex:
        log.log_error("send_mail_queued() could not add element to queue" + str(ex))


def send_mail_queued_monitoring(subject, body):

    arr = cfg.parameters["emails-monitoring"]

    for ele in arr:
        send_mail_queued(ele, "Monitoring: " + str(subject), body)


