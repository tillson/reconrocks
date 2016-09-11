from flask import Flask, request, send_from_directory, render_template, redirect
import time
import random
import string
import imp
import threading
import atexit
import json

import modules.subdomains as subdomains
import modules.recon as recon
# subdomains = imp.load_source('subdomains', './modules/subdomains.py')

app = Flask(__name__)

things = []

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/generate", methods = ['GET'])
def generate():
    # request.form['domain'] = 'https://google.com'
    domain = 'https://portergaud.edu'
    if '//' in domain:
        domain = domain.split('//')[1].replace('www.', '')

    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    domainObj = {'id': id, 'domain': domain, 'start': int(time.time())}
    print domainObj

    things.append(domainObj)

    subdomains.run(domainObj)
    recon.run(domainObj)

    return redirect("/status/" + id, code=302)

@app.route("/status/<domain_id>")
def status(domain_id):
    object = None
    for thing in things:
        if thing['id'] == domain_id:
            object = thing
    if object is None:
        return '404 not found'
    print object
    recon.report(object['domain'])

    subdomains = open(object['domain']).read().split('\n')
    data = None
    with open(object['domain'] + '.json') as data_file:
        data = json.load(data_file)

    return render_template('status.html', domain=object, subdomains=subdomains, recon=data)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":


    app.run()
