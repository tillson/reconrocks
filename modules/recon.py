from subprocess import Popen, PIPE
from threading import Thread, Timer
from Queue import Queue, Empty
import sys

ON_POSIX = 'posix' in sys.builtin_module_names

def run(domain_object):
    execute('recon/domains-contacts/whois_pocs', domain_object['domain'], './')
    execute('discovery/info_disclosure/interesting_files', domain_object['domain'], './')
    # execute('recon/domains-contacts/metacrawler', domain_object['domain'], './')
    execute('recon/domains-vulnerabilities/ghdb', domain_object['domain'], './')
    execute('recon/domains-vulnerabilities/punkspider', domain_object['domain'], './')
    execute('recon/domains-vulnerabilities/xssed', domain_object['domain'], './')
    execute('recon/domains-vulnerabilities/xssposed', domain_object['domain'], './')
    report(domain_object['domain'])

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
        print line
    out.close()

def execute(module,cmd,path):
    # Ironically, this is vulnerable to command injection.
    p = Popen(['~/recon-ng/recon-cli -w ' + cmd + ' -m ' + module + ' -x -o SOURCE=' + cmd + ' -o DOMAIN=' + cmd], stdout=PIPE, bufsize=1, shell=True, close_fds=ON_POSIX, cwd=path)
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True # thread dies with the program
    t.start()

def report(cmd):
    p = Popen(['~/recon-ng/recon-cli -w ' + cmd + ' -m reporting/json -x -o filename=' + cmd + '.json'], stdout=PIPE, bufsize=1, shell=True, close_fds=ON_POSIX, cwd='./')
    q = Queue()
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True # thread dies with the program
    t.start()
