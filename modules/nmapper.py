import nmap

def run(scan):
    nm = nmap.PortScanner()
    nm.scan(scan, arguments='-F')
    print nm[nm.all_hosts()[0]]

    if len(nm.all_hosts()) > 0:
        return nm[nm.all_hosts()[0]]
    else:
        return '{}'
