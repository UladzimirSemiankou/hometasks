import requests
import time
import argparse
import sys
from datetime import datetime
from collections import OrderedDict

class Github_statistics:

    def __init__(self):
        keys = argparse.ArgumentParser(description = 'GitHub pull request statistics', usage = "gitpull.py [-h] [-v] [OPTIONS] [-d YYYY-MM-DD]")
        keys.add_argument("--version", action = 'version', version = 'gitpull v6.6.6', help = "Print version")
        keys.add_argument("--mc-stat", action = "store_true", help = "basic merged/closed rate")
        keys.add_argument("--num_days_o", action = "store_true", help = "number of days opened")
        keys.add_argument("--comments", action = "store_true", help = "number of comments created")
        keys.add_argument("--day-opened", action = "store_true", help = "day of the week opened")
        keys.add_argument("--day-closed", action = "store_true", help = "day of the week closed")
        keys.add_argument("--hour-opened", action = "store_true", help = "hour of day opened")
        keys.add_argument("--hour-closed", action = "store_true", help = "hour of day closed")
        keys.add_argument("--week-opened", action = "store_true", help = "week opened")
        keys.add_argument("--week-closed", action = "store_true", help = "week closed")
        keys.add_argument("--user-opened", action = "store_true", help = "user who opened")
        keys.add_argument("--user-closed", action = "store_true", help = "user who closed")
        keys.add_argument("--labels", action = "store_true", help = "attached labels")
        keys.add_argument("--lines-add", action = "store_true", help = "number of lines added")
        keys.add_argument("--lines-deleted", action = "store_true", help = "number of lines deleted")
        keys.add_argument("--after", type = str, help = "only pull requests opened after this date")
        keys.add_argument("user", metavar = "user", type = str, nargs = 1, help = 'github user')
        keys.add_argument("repo", metavar = "repo", type = str, nargs = 1, help = 'github repo')
        self._args = keys.parse_args()
        self.AUTH_TOKEN = "1375def973ae56919411cb5cc92cbe4546b855ae"
        self.pull_requests = self.get_pull_requests()
        self.issues_pulls = self._get_issues()
        self.comments_list = self._get_Comments()
        self.files_dict = self._get_Files()

    def get_pull_requests(self):
        if self._args.after != None:
            temp_req = requests.get('https://api.github.com/repos/{0}/{1}/pulls?state=all&access_token={2}'.format(self._args.user[0], self._args.repo[0], self.AUTH_TOKEN)).json()
            final_req = OrderedDict()
            try:
                for i in range(len(temp_req)):
                    if datetime.strptime(temp_req[i]["created_at"].split("T")[0], '%Y-%m-%d') >= datetime.strptime(self._args.after, '%Y-%m-%d'):
                        final_req[i] = temp_req[i]
                return final_req
            except:
                print("BAD ARGUMENTS!!!")
                sys.exit(1)
        else:
            return requests.get('https://api.github.com/repos/{0}/{1}/pulls?state=all&access_token={2}'.format(self._args.user[0], self._args.repo[0], self.AUTH_TOKEN)).json()

    def _get_issues(self):
        issues = OrderedDict()
        for i in range(len(self.pull_requests)):
            try:
                temp_issue = requests.get('{0}?access_token={1}'.format(self.pull_requests[i]["_links"]["issue"]["href"], self.AUTH_TOKEN)).json()
                issues[i] = temp_issue
            except:
                print("BAD ARGUMENTS!!!")
                sys.exit(1)
        return issues

    def _get_Comments(self):
        comments = OrderedDict()
        for i in range(len(self.pull_requests)):
            comment_list = requests.get('{0}?access_token={1}'.format(self.pull_requests[i]["_links"]["comments"]["href"], self.AUTH_TOKEN)).json()
            comments[i] = comment_list
        return comments

    def _get_Files(self):
        files = OrderedDict()
        for i in range(len(self.pull_requests)):
            files_list = requests.get('https://api.github.com/repos/{0}/{1}/pulls/{2}/files?access_token={3}'.format(self._args.user[0], self._args.repo[0], self.pull_requests[i]["number"], self.AUTH_TOKEN)).json()
            files[i] = files_list
        return files

    def Lines_added(self, p_req):
        line_add_count = 0
        for i in range(len(self.files_dict[p_req])):
            line_add_count += self.files_dict[p_req][i]["additions"]
        print("Lines of code added: {0}".format(line_add_count))

    def Lines_del(self, p_req):
        line_del_count = 0
        for i in range(len(self.files_dict[p_req])):
            line_del_count += self.files_dict[p_req][i]["deletions"]
        print("Lines of code deleted: {0}".format(line_del_count))

    def Week_op(self, p_req):
        week_n_open=datetime.strptime(self.pull_requests[p_req]["created_at"].split("T")[0], '%Y-%m-%d').isocalendar()[1]
        print("Pull request opened on week #{0}".format(week_n_open))

    def Week_cl(self, p_req):
        if self.pull_requests[p_req]["closed_at"]:
            week_n_close=datetime.strptime(self.pull_requests[p_req]["closed_at"].split("T")[0], '%Y-%m-%d').isocalendar()[1]
            print("Pull request closed on week #{0}".format(week_n_close))
        else:
            print("Not closed")

    def Hour_op(self, p_req):
        hour_open=datetime.strptime(self.pull_requests[p_req]["created_at"].split("T")[1].split("Z")[0], '%H:%M:%S').hour
        print("Pull request opened on {0} hour".format(hour_open))

    def Hour_cl(self, p_req):
        if self.pull_requests[p_req]["closed_at"]:
            hour_closed = datetime.strptime(self.pull_requests[p_req]["closed_at"].split("T")[1].split("Z")[0], '%H:%M:%S').hour
            print("Pull request closed on {0} hour".format(hour_closed))
        else:
            print("Not closed")

    def Day_of_Week_op(self, p_req):
        week_open=datetime.strptime(self.pull_requests[p_req]["created_at"].split("T")[0], '%Y-%m-%d').strftime('%A')
        print("Pull request opened on {0}".format(week_open))

    def Day_of_Week_cl(self, p_req):
        if self.pull_requests[p_req]["closed_at"]:
            week_close=datetime.strptime(self.pull_requests[p_req]["closed_at"].split("T")[0], '%Y-%m-%d').strftime('%A')
            print("Pull request closed on {0}".format(week_close))
        else:
            print("Not closed")

    def Num_of_Comments(self, p_req):
        print("Number of comments: {0}".format(len(self.comments_list[p_req])))

    def Days_Opened(self, p_req):
        t_format='%Y-%m-%d'
        if self.pull_requests[p_req]["closed_at"]:
            if datetime.strptime(self.pull_requests[p_req]["closed_at"].split("T")[0], t_format) == datetime.strptime(self.pull_requests[p_req]["created_at"].split("T")[0], t_format):
                t_difference="0 day"
            else:
                t_difference = datetime.strptime(self.pull_requests[p_req]["closed_at"].split("T")[0], t_format) - datetime.strptime(self.pull_requests[p_req]["created_at"].split("T")[0], t_format)
        else:
            if datetime.strptime(time.strftime(t_format), t_format) == datetime.strptime(self.pull_requests[p_req]["created_at"].split("T")[0], t_format):
                t_difference="0 day"
            else:
                t_difference = datetime.strptime(time.strftime(t_format), t_format) - datetime.strptime(self.pull_requests[p_req]["created_at"].split("T")[0], t_format)
        print("Pull request opened for {0}(s)".format((str(t_difference)).split(",")[0]))

    def Merge_Close_stats(self):
        merged_counter=0
        closed_counter=0
        print("***********************************")
        for p_req in range(len(self.pull_requests)):
            if self.pull_requests[p_req]["state"]=="closed": closed_counter+=1
            if self.pull_requests[p_req]["merged_at"]: merged_counter+=1
        print("{0} of {1} pull requests are merged".format(merged_counter, len(self.pull_requests)))
        print("{0} of {1} pull requests are closed".format(closed_counter, len(self.pull_requests)))
        print("***********************************")

    def Labels(self, p_req):
        print("Request labels:")
        print("_________________________")
        if self.issues_pulls[p_req]["labels"]:
            for i in self.issues_pulls[p_req]["labels"]:
                print(i["name"])
        else:
            print("No labels")
        print("_________________________")

    def Created_User(self, p_req):
        print("User who opened: {0}".format(self.pull_requests[p_req]["user"]["login"]))

    def Closed_User(self, p_req):
        if self.issues_pulls[p_req]["closed_by"]:
            print("User who closed: {0}".format(self.issues_pulls[p_req]["closed_by"]["login"]))
        else:
            print("Not closed")

    def Default(self, p_req):
        print("--------------------------")
        print("Pull request ID: {0}".format(self.pull_requests[p_req]["id"]))
        print("Pull Request Name: {0}".format(self.pull_requests[p_req]["title"]))

    def start(self):
        if self._args.mc_stat:
            self.Merge_Close_stats()
        for id in range(len(self.pull_requests)):
            self.Default(id)
            if self._args.num_days_o:
                self.Days_Opened(id)
            if self._args.comments:
                self.Num_of_Comments(id)
            if self._args.day_opened:
                self.Day_of_Week_op(id)
            if self._args.day_closed:
                self.Day_of_Week_cl(id)
            if self._args.hour_opened:
                self.Hour_op(id)
            if self._args.hour_closed:
                self.Hour_cl(id)
            if self._args.week_opened:
                self.Week_op(id)
            if self._args.week_closed:
                self.Week_cl(id)
            if self._args.user_opened:
                self.Created_User(id)
            if self._args.user_closed:
                self.Closed_User(id)
            if self._args.labels:
                self.Labels(id)
            if self._args.lines_add:
                self.Lines_added(id)
            if self._args.lines_deleted:
                self.Lines_del(id)

github = Github_statistics()
github.start()