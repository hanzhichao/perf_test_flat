# coding:utf-8
from flask import Flask, render_template, request, redirect, url_for
import subprocess
from time import sleep


app = Flask(__name__)


@ app.route("/")
def index():
    return render_template('index.html')


@ app.route("/wrk", methods=["GET", "POST"])
def perf():
    global result
    result = ''
    if request.method == "POST":
        method = request.form["methods"]
        connection = request.form["connection"]
        url = request.form["url"]
        c = request.form["c"]
        t = request.form["t"]
        d = request.form["d"]
        subprocess.Popen("nmon -s 1 -c %s -F report.nmon" % str(int(d)+2),shell=True, stdout=subprocess.PIPE)
        subprocess.Popen("wrk -c %s -t %s -d %s -H '%s'--latency %s://%s > wrk.log" % (c, t, d, connection, method, url),
                         shell=True, stdout=subprocess.PIPE)
        sleep(int(d)+2)
    with open("wrk.log",'r') as f:
        result = f.read().replace('\n','<br/>')
    subprocess.Popen("pyNmonAnalyzer -b -t static -x -o static/report -i report.nmon", shell=True,stdout=subprocess.PIPE)
    
    return render_template("wrk.html", result=result)


@ app.route("/nmon", methods=["GET", "POST"])
def nmon():
    if request.method == "POST":
        s = request.form["s"]
        c = request.form["c"]
        subprocess.Popen("nmon -s %s -c %s -F report.nmon" % (s,c),shell=True, stdout=subprocess.PIPE) 
        sleep(int(s)*int(c))
    subprocess.Popen("pyNmonAnalyzer -b -t static -x -o static/report -i report.nmon", shell=True,stdout=subprocess.PIPE)
    return render_template("nmon.html")

@ app.route("/report")
def report():
    return render_template("report.html")

if __name__ == '__main__':
    app.run("0.0.0.0")


