import yaml
import psutil
import datetime
import time
import json
import os
import psycopg2
from collections import OrderedDict

class main:
    joutput = "output"
    toutput = "outputtext"
    dboutput = "prog1"
    data = OrderedDict()
    def __init__(self):
        with open("settings", "r") as yamlset:
            self.settings=yaml.load(yamlset)

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

class run(output):
    def run(self):
        number = 1
        while True:
            time.sleep(self.settings["interval"])
            output.monitor(number)
            output.output(self.settings["output"])
            number+=1

obj=run()
obj.display_init()
obj.run()