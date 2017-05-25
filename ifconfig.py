from subprocess import call
from subprocess import check_output
from subprocess import Popen
import subprocess
import smtplib
import datetime as dt
process = Popen(["ifconfig"],stdout=subprocess.PIPE)
output = process.stdout.read()
print(output)

server_ssl = smtplib.SMTP_SSL("smtp.gmail.com",465)
server_ssl.ehlo()
server_ssl.login('eqbookservice','ggininder')
#server_ssl.sendmail('eqbookservice@gmail.com','raylo@wustl.edu',output)
server_ssl.close()

f = open('email_log.txt',"a")
f.write(str(dt.datetime.now()) + '\n')
f.close()
