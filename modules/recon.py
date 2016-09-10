from subprocess import Popen, PIPE
from threading import Thread, Timer
from Queue import Queue, Empty
import sys

ON_POSIX = 'posix' in sys.builtin_module_names

def run(domain_object):
    execute(domain_object['domain'], './')

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def execute(cmd,path):
    # Ironically, this is vulnerable to command injection.
    p = Popen(['~/recon-ng/recon-cli -w ' + cmd + ' -m recon/domains-contacts/whois_pocs'], stdout=PIPE, bufsize=1, shell=True, close_fds=ON_POSIX, cwd=path)
    q = Queue()
    print(p)
    t = Thread(target=enqueue_output, args=(p.stdout, q))
    t.daemon = True # thread dies with the program
    t.start()
