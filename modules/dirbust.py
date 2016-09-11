import requests
from celery import Celery
import time

directories = open('util/raft-small-directories.txt').read().split('\n')

app = Celery('modules.dirbust', broker='amqp://guest@localhost//')

@app.task()
def run(domain):
    print 'Running DIRBUST'
    with open(domain['domain'] + '.dirbust.txt', 'w+') as file:
        url = 'http://www.' + domain['domain']
        # try:
        r = requests.get(url, timeout=2.0)
        if r.status_code != 200:
            url = 'https://www.' + domain['domain'] + '/'
        for directory in directories:
            time.sleep(3)
            uri = url + '/' + directory
            r = requests.get(uri,timeout=2.0)
            print r.status_code
            if r.status_code != 404 and r.status_code != 301 and r.status_code != 302:
                status = ''
                if r.status_code == 401:
                    status = "Authorization Required"
                elif r.status_code == 403:
                    status = "Forbidden"
                elif r.status_code == 503:
                    status = "Server error"
                elif r.status_code == 200:
                    status = '200 OK'
                else:
                    status = '' + r.status_code
                print((directory, status))
                file.write(directory + ':' + status + '\n')
