from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os
from crawler import *
from predictions import *
import numpy as np

app = Flask('Website Timer')
CORS(app)
d = {}
websites = {}
times = {}
predict = [0]

#get -> return data to extension
#post -> get data from extension
@app.route('/test', methods = ['GET','POST'])
def testfunc():
    print("\ntestfunc")
    message = {'flask': 'Hello World'}
    print('sending hello world to extension')
    data = request.get_json()
    if data == {}:
        return jsonify({'flask': 'nothing received'})
    return jsonify(message)

@app.route('/saveTime', methods=['POST'])
#@cross_origin()
def saveTime():
    print('\nsaving time')
    data = request.get_json()
    print(data)
    if data == {}:
        return jsonify({'flask': 'nothing received'})
    name = data['username']
    time = data['time']
    website = data['website']
    print(name, time, website)
    print(d)
    print(times)
    #save_file()
    #store stats of website into server
    if website not in websites.keys():
        websites[website] = webscrape(website)
    try:
      times[name].append([time, websites[website][1],websites[website][3],websites[website][4]])
    except:
      times[name] = [[time,websites[website][1],websites[website][3],websites[website][4]]]
    #store user data into server
    if name in d.keys():
        if website in d[name].keys():
            d[name][website].append(time)
        else:
            d[name][website] = [time]
    else:
        d[name] = {}
        d[name][website] = [time]
    with open("data.json", "w") as f:
        json.dump(d, f)
    print(d)
    print(times)
    with open("time.json", "w") as f:
        json.dump(times,f)
    try:
        temp = sorted(d[name][website])[:10]
    except KeyError:
        return jsonify({'flask': 'nothing received'})
    return jsonify({"time": temp})

@app.route('/showPrediction', methods=['GET', 'POST'])
def showPrediction():
    data = request.get_json()
    if data == {}:
        return jsonify({'flask': 'nothing received'})
    name = data['username']
    website = data['website']
    #store stats of website into server
    if website not in websites.keys():
        websites[website] = webscrape(website)
    try:
        test = [websites[website][1],websites[website][3],websites[website][4]]
        temp2 = websites[website]
        temp2[0] = temp2[0][:10]
        predict[0] = (predictTimes(times[name], test))
        temp2[2] = round(int(predict[0]),2)
    except:
      temp2[2] = 0
      return jsonify({"webstats": temp2})
    return jsonify({"webstats": temp2})

@app.route('/delTime', methods=['POST'])
#@cross_origin()
def deleteTime():
    print('\ndeleting time')
    data = request.get_json()
    print(data)
    if data == {}:
        return jsonify({'flask': 'nothing received'})
    name = data['username']
    website = data['website']
    print(name, website)
    print(d)
    #store stats of website into server
    if website not in websites.keys():
        websites[website] = webscrape(website)
    if name in d.keys():
        if website in d[name].keys():
            del d[name][website]
    #save_file()
    with open("data.json", "w") as f:
        json.dump(d, f)
    message = {'flask': 'Time Deleted!'}
    print(d)
    return jsonify(message)

@app.route('/showTime', methods=['GET', 'POST'])
#@cross_origin()
def showTime():
    print("\nsending Times")
    data = request.get_json()
    print(data)
    if data == {}:
        return jsonify({'flask': 'nothing received'})
    name = data['username']
    website = data['website']
    print(name, website)
    print(d)
    #store stats of website into server
    if website not in websites.keys():
        websites[website] = webscrape(website)
    try:
      test = [websites[website][1],websites[website][3],websites[website][4]]
      print("predicts", predictTimes(times[name],test))
      predict[0] = (predictTimes(times[name], test))
    except:
      print("no prediction")
      predict[0] = 0
    try:
        temp = sorted(d[name][website])[:10]
    except KeyError:
        return jsonify({'flask': 'nothing received'})
    return jsonify({"time": temp})

@app.route('/showWords', methods=['GET', 'POST'])
#@cross_origin()
def showWords():
    print("\nshowWords")
    dat = request.get_json()
    print(dat)
    if dat == {}:
        return jsonify({'flask': 'nothing received'})
    website = dat['website']
    print("website", website)
    print(d)
    #store stats of website into server
    if website not in websites.keys():
        websites[website] = webscrape(website)
    temp2 = websites[website]
    temp2[0] = temp2[0][:10]
    try:
      temp2[2] = round(int(predict[0]),2)
    except:
      print("Prediction not found")
      return jsonify({"webstats": temp2})
    return jsonify({"webstats": temp2})

if __name__ == '__main__':
    #open file
    if os.stat('data.json').st_size != 0:#check if file exists and is not empty
        try:
            with open('data.json') as f:
                d = json.load(f)
        except FileNotFoundError:
            pass
    print(d)
    if os.stat('time.json').st_size != 0:#check if file exists and is not empty
        try:
            with open('time.json') as f:
                times = json.load(f)
        except FileNotFoundError:
            pass
    print(times)
    #app.run(debug = True)
    app.run(host='0.0.0.0', port=8080, debug = False, threaded = True)