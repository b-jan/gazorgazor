from flask import Flask, render_template, jsonify
from flask_cors import CORS
from random import *

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

import pip

def install(package):
    pip.main(['install', package])

install('dnspython')

@app.route('/api/email-validator')
def random_number():
    import re
    import socket
    import smtplib
    import dns.resolver

    email_address = 'akhelilokokok.pro@gmail.com'

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
    	answer = 'Success'
    else:
    	answer = 'Bad'
    response = {
        'validEmail': answer
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
