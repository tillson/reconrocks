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
import modules.nmapper as nmapper
import modules.dirbust as dirbust
# subdomains = imp.load_source('subdomains', './modules/subdomains.py')

app = Flask(__name__)

things = []

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/generate", methods = ['POST'])
def generate():



    # request.form['domain'] = 'https://google.com'
    domain = request.form['urlToTest']
    if '//' in domain:
        domain = domain.split('//')[1].replace('www.', '').strip(';').strip('|')

    open(domain + ".json","a+")
    open(domain + "","a+")

    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    domainObj = {'id': id, 'domain': domain, 'start': int(time.time())}
    print domainObj

    things.append(domainObj)

    subdomains.run(domainObj)
    recon.run(domainObj)
    # dirbust.run.apply_async(args=[domainObj])
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
    print subdomains
    data = None
    # recon = json.loads()
    with open(object['domain'] + '.json') as data_file:
        print data_file
        try:
            data = json.load(data_file)
        except:
            print "except"
        return render_template('status.html', domain=object, subdomains=subdomains, recon=data)

@app.route('/nmap/<host>')
def nmap_vis(host):
    return render_template('nmap.html', host=host)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route("/api/nmap/<host>", methods = ['GET'])
def get_nmap(host):
    output = nmapper.run(host)
    return json.dumps(output)

if __name__ == "__main__":


    app.run(threaded=True,port=80)
