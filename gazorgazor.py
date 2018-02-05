# https://stackoverflow.com/questions/22233848/how-to-verify-an-email-address-in-python-using-smtplib
# https://pypi.python.org/pypi/validate_email
import re
import socket
import smtplib
import dns.resolver

email_address = 'khelilamira@hotmail.fr'

#Step 1: Check email
#Check using Regex that an email meets minimum requirements, throw an error if not
addressToVerify = email_address
match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)

if match == None:
    print('Bad Syntax in ' + addressToVerify)
    raise ValueError('Bad Syntax')

#Step 2: Getting MX record
#Pull domain name from email address
domain_name = email_address.split('@')[1]

#get the MX record for the domain
records = dns.resolver.query(domain_name, 'MX')
mxRecord = records[0].exchange
mxRecord = str(mxRecord)

#Step 3: ping email server
#check if the email address exists

# Get local server hostname
host = socket.gethostname()

# SMTP lib setup (use debug level for full output)
server = smtplib.SMTP()
server.set_debuglevel(0)

# SMTP Conversation
server.connect(mxRecord)
server.helo(host)
server.mail('me@domain.com')
code, message = server.rcpt(str(addressToVerify))

server.quit()

# Assume 250 as Success
if code == 250:
	print('Success')
else:
	print('Bad')

#print(code)
#print(message)