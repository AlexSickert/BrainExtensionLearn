import smtplib
import log
import config as cfg


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


# def send_new_registered_user(user, password):
#
#
#     log.log_info("in send_new_registered_user()")
#
#     subject_line = "Your registration at GliaLab WebApp."
#
#     body_text = "Dear User,\n"
#     body_text += "\n"
#     body_text += "Thank you for your registration at GliaLab WebApp.\n"
#     body_text += "\n"
#     body_text += "Please login using these login credentials:\n"
#     body_text += "\n"
#     body_text += "User: " + user + "\n"
#     body_text += "Password: " + password + "\n"
#     body_text += "\n"
#     body_text += "The WebApp can be reachd via the URL http://34.214.34.79:8888/:\n"
#     body_text += "\n"
#     body_text += "\n"
#     body_text += "With kind regards,\n"
#     body_text += "\n"
#     body_text += "GliaLab Team\n"
#
#     send_mail(user, subject_line,body_text)
#     # for controlling purposes is end it to here as well
#     send_mail("alex.solensky@gmail.com", subject_line, body_text)
#
#     log.log_info("done send_new_registered_user()")

# def send_password_reset(user, password):
#
#     subject_line = "GliaLab WebApp password reset."
#
#     body_text = "Dear User,\n"
#     body_text += "\n"
#     body_text += "We have reset your password\n"
#     body_text += "\n"
#     body_text += "Please login using these login credentials:\n"
#
#     body_text += "User: " + user + "\n"
#     body_text += "Password: " + password + "\n"
#     body_text += "\n"
#     body_text += "The WebApp can be reachd via the URL http://34.214.34.79:8888/:\n"
#     body_text += "\n"
#     body_text += "\n"
#     body_text += "With kind regards,\n"
#     body_text += "\n"
#     body_text += "GliaLab Team\n"
#
#     send_mail(user, subject_line,body_text)
#     # for controlling purposes is end it to here as well
#     send_mail("alex.solensky@gmail.com", subject_line, body_text)

