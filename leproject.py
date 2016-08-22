import yaml
import psutil
import datetime
import time
import json
import os
import psycopg2
import asis

from collections import OrderedDict

with open("settings", "r") as yamlset:
    settings=yaml.load(yamlset)

def monitor(number, output, interval):
    print(output)
    data=OrderedDict()
    ts=time.time()
    data["snapshot"]="Snapshot"+str(number)
    data["timestamp"]=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    data["cpu"]=psutil.cpu_times()
    data["virtual_memory"]=psutil.virtual_memory()
    data["disk_usage"]=psutil.disk_usage('/')
    data["IO"]=psutil.disk_io_counters()
    data["network"]=psutil.net_io_counters()
    try:
        if output=="db":
            con = psycopg2.connect("dbname='pytest' user='root'")
            cur = con.cursor()
            cols = data.keys()
            vals = [data[x] for x in cols]
            vals_str_list = ["%s"] * len(vals)
            vals_str = ", ".join(vals_str_list)
            cur.execute("INSERT INTO prog1 VALUES ({vals_str})".format(vals_str=vals_str), vals)
            con.commit()
        if output=="json":
            with open("output", "a") as jf:
                json.dump(data, jf, indent=3)
                jf.write(os.linesep)
        elif output=="text":
            with open("outputtext", "a") as tf:
                for key, value in data.items():
                    tf.write('%s:%s\n' % (key, value))
    except:
        print("wrong output format!")

def run():
    number = 1
    while True:
        time.sleep(settings["interval"])
        monitor(number, **settings)
        number+=1

run()