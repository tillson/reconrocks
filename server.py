from flask import Flask, request, send_from_directory, render_template, redirect
import time
import random
import string
import imp
import threading
import atexit

import modules.subdomains as subdomains
# subdomains = imp.load_source('subdomains', './modules/subdomains.py')

app = Flask(__name__)

things = []

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/generate", methods = ['GET'])
def generate():
    # request.form['domain'] = 'https://google.com'
    domain = 'https://google.com'
    if '//' in domain:
        domain = domain.split('//')[1].replace('www.', '')

    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    domainObj = {'id': id, 'domain': domain, 'start': int(time.time())}
    print domainObj

    things.append(domainObj)

    subdomains.run(domainObj)

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
    subdomains = open(object['domain']).read().split('\n')

    return render_template('status.html', domain=object, subdomains=subdomains)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":


    app.run()
