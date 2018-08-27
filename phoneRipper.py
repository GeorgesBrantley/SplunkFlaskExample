#!/usr/bin/python2.7
from flask import Flask, flash, redirect, render_template, request, session, abort
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from random import randint 
import subprocess
import sys 
import shlex
import json
import os
import time

sys.path.insert(0,"//splunk-sdk-python-1.6.5/")
DEBUG = True
app = Flask(__name__)
app.secret_key = 'ThisisSuperSecret2346242235293hd' 
app.config.from_object(__name__)
PYTHONPATH = "/splunk-sdk-python-1.6.5" 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route("/")
def mainMenu():
    return render_template('mainMenu.html')
 
@app.route("/upload")
def upload():
    return render_template(
        'upload.html')

@app.route("/uploadResult", methods=['GET','POST'])
def uploadResult():
    global PYTHONPATH
    # get file contents or name?
    if request.method == 'POST':
        result = request.form
        index = result['indexName']
        # Save file locally
        file = request.files['file'] 
        filename = file.filename
        file.save(os.path.join('/downloadData',filename))
        # Send data to Splunk, under INDEX name
        # create index
        time.sleep(2)
        #try:
        if True:
            subprocess.check_output('python splunkFunct/index.py create ' + str(index), shell=True,\
                    env={"PYTHONPATH":PYTHONPATH})
            # Upload file!
            #TODO does not work
            subprocess.check_output('python splunkFunct/upload.py ' +\
                    'wnloadData/'+\
                    str(filename) + ' --index=' + str(index) +\
                    ' --sourcetype=gencalls',shell=True,\
                    env={"PYTHONPATH":PYTHONPATH})
            success = 'SUCCESS'
        #except:
        #    success = 'FAIL'
    return render_template(
            'uploadResult.html', fileV=filename,indexV=index,suc=success)

@app.route("/chooseIndex")
def chooseIndex():

    indexL = 0
    indexL = subprocess.check_output('python splunkFunct/index.py list',shell=True, env={"PYTHONPATH":"ts/splunkSDK/splunk-sdk-python-1.6.5"})
    indexL = indexL.replace("\n"," ")
    indexL = indexL.split(" ")
    trueIndex = []
    for x in range(0,len(indexL)):
        if x % 2 == 0:
            if indexL[x] != '':
                trueIndex.append(indexL[x])
        

    #indexL = str(indexL)
    #indexL = json.loads(indexL)
    return render_template('chooseIndex.html', indexes=trueIndex)

@app.route("/indexMenu", methods=['GET','POST'])
def indexMenu():
    # get index name from previous selection
    if request.method== 'POST':
        indexChosen = request.form['indexChosen'][:-1]
    # list searches as buttons
    return render_template('indexMenu.html', indexChosen=indexChosen)

@app.route("/indexMenu/result", methods=['GET','POST'])
def indexResult():
    # Preform search and do results
    graph = ''
    if request.method == 'POST':
        index = request.form['index']
        if request.form['choice'] == "TopCallsAll":
            newoutput = subprocess.check_output('python splunkFunct/search.py "search index='+index+\
                    ' | top target" --output_mode=json', shell=True,\
                    env={"PYTHONPATH":"k-sdk-python-1.6.5"})
            newoutput = json.loads(newoutput)
            newoutput = newoutput['results']
            output =[]
            graph = 'Top Calls (All)'
            for x in newoutput:
                output.append([x['count'],x['target'],x['percent']])
        elif request.form['choice'] == "TopCallsOut":
            newoutput = subprocess.check_output('python splunkFunct/search.py "search index='+index+\
                    ' direction=outgoing | top target" --output_mode=json', shell=True,\
                    env={"PYTHONPATH":"/splunkSDK/splunk-sdk-python-1.6.5"})
            newoutput = json.loads(newoutput)
            newoutput = newoutput['results']
            output =[]
            graph = 'Top Calls (Outgoing)'
            for x in newoutput:
                output.append([x['count'],x['target'],x['percent']])
        elif request.form['choice'] == "TopCallsIn":
            newoutput = subprocess.check_output('python splunkFunct/search.py "search index='+index+\
                    ' direction=incoming | top target" --output_mode=json', shell=True,\
                    env={"PYTHONPATH":"/splunk-sdk-python-1.6.5"})
            newoutput = json.loads(newoutput)
            newoutput = newoutput['results']
            output =[]
            graph = 'Top Calls (Incoming)'
            for x in newoutput:
                output.append([x['count'],x['target'],x['percent']])
    # maybe this is a form return

    return render_template('indexResults.html',output=output,indexChosen=index,graph=graph)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
