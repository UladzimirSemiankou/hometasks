import re
import operator

file_default="log.txt"

try:
    print("Leave empty for default")
    file=input()
    if not file:
        raise ValueError()
except ValueError:
    file=file_default

def ips(file):
    pattern=re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    ip_dict={}
    for line in open(file, "r"):
        ipis=pattern.findall(line)
        for ip in ipis:
            if ip not in ip_dict:
                ip_dict[ip]=1
            else:
                ip_dict[ip]+=1
    sorted_ip = sorted(ip_dict.items(), key=operator.itemgetter(1))
    print(sorted_ip[:-11:-1])

ips(file)