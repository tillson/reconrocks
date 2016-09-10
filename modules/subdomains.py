import subbrute

from celery import Celery

app = Celery('subbrute', broker='amqp://guest@localhost//')

@app.task
def run(domain_object):
    domain_object['subdomains'] = []
    for d in subbrute.run(domain_object['domain'], subdomains='./util/names_small.txt'):
        domain_object['subdomains'].append(d)
        print d
