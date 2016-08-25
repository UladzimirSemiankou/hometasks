import yaml
import psutil
import datetime
import time
import json
import os
import psycopg2
from collections import OrderedDict

with open("settings", "r") as yamlset:
    settings = yaml.load(yamlset)

class main:
    number = 1
    joutput = "output"
    toutput = "outputtext"
    dboutput = "prog1"
    data = OrderedDict()
    def __init__(self):
        self.number = 1
        self.joutput = "output"
        self.toutput = "outputtext"
        self.dboutput = "prog1"
        self.data = OrderedDict()

    def display_init(self):
        print("initial setting: %s" % self.settings)

class monitor(main):
    def monitor(number):
        data=main.data
        ts = time.time()
        data["snapshot"]="Snapshot"+str(number)
        data["timestamp"]=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        data["cpu"]=psutil.cpu_times()
        data["virtual_memory"]=psutil.virtual_memory()
        data["disk_usage"]=psutil.disk_usage('/')
        data["IO"]=psutil.disk_io_counters()
        data["network"]=psutil.net_io_counters()

class output(monitor):
    def output(output):
        print(output)
        try:
            if output=="db":
                con = psycopg2.connect("dbname='pytest' user='root'")
                cur = con.cursor()
                cols = monitor.data.keys()
                vals = [monitor.data[x] for x in cols]
                vals_str_list = ["%s"] * len(vals)
                vals_str = ", ".join(vals_str_list)
                cur.execute("INSERT INTO "+main.dboutput+" VALUES ({vals_str})".format(vals_str=vals_str), vals)
                con.commit()
            if output=="json":
                with open(main.joutput, "a") as jf:
                    json.dump(monitor.data, jf, indent=3)
                    jf.write(os.linesep)
            elif output=="text":
                with open(main.toutput, "a") as tf:
                    for key, value in monitor.data.items():
                        tf.write('%s:%s\n' % (key, value))
        except:
            print("wrong output format!")

def decor(function):
    def logging(snapshot, output_type, interval):
        log = [snapshot, output_type, interval]
        with open('decor_log', 'a') as dl:
            dl.write("Function name: {0}; function arguments: {1}\n".format(function.__name__, log))
        function(snapshot, output_type, interval)
    def no_log(snapshot, output_type, interval):
        function(snapshot, output_type, interval)

    if settings["decorate"]:
        return logging
    else:
        return no_log

@decor
def run(snapshot, output_type, interval):
    while True:
        time.sleep(interval)
        output.monitor(snapshot)
        output.output(output_type)
        snapshot += 1

run(main.number, settings["output"], settings["interval"])