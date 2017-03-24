#!/usr/bin/env python
import smtplib
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart

fromaddr = "testcwavms@gmail.com"
toaddr = "jstntang3@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test Email2"

body = "Test Message body"
msg.attach(MIMEText(body,'plain'))

try:
	s = smtplib.SMTP('smtp.gmail.com',587)
	s.set_debuglevel(1)
	s.ehlo()
	s.starttls()
	s.login(fromaddr,"iron#315")
	text = msg.as_string()
	s.sendmail(fromaddr,toaddr,text)
	s.quit()
	print "Status: 200 ok\n"
except smtplib.SMTPException as e:
	print "Status: 200 ok\n"
	print e
except smtplib.socket.error as e:
	print "Status: 200 ok\n"
	print e
