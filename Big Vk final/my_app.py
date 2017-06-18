from flask import Flask
from flask import url_for, render_template, request, redirect
from urllib.parse import unquote
import requests
import json
from collections import Counter
import sys
import re
import time
from conf import access_token

app = Flask(__name__)

def daate(items, date1):
    for i in items:
        if type(i) == dict:
            date1.append(time.localtime(i["date"]))
    return date1

def owner_id(items, idd):
    for i in items:
        if type(i) == dict:
            idd.append(i["owner_id"])
    return idd
 
def seconds(date):
    tiime = []
    for l in range(len(date[4])):
        time = str(date[2][l]) + ':' + str(date[3][l]) + ':' + str(date[4][l])
        tiime.append(time)
    name = Counter(tiime)
    return name

def minutes(date):
    tiime = []
    for l in range(len(date[3])):
        time = str(date[2][l]) + ':' + str(date[3][l])
        tiime.append(time)
    name = Counter(tiime)
    return name

def hours(date):
    tiime = []
    for l in date[2]:
        time = str(l) + ' h'
        tiime.append(time)
    name = Counter(tiime)
    return name

def days(date):
    tiime = []
    for l in range(len(date[1])):
        time = str(date[1][l]) + '.' + str(date[0][l])
        tiime.append(time)
    name = Counter(tiime)
    return name

def months(date):
    tiime = []
    d = {1:'Январь', 2:'Февраль', 3:'Март', 4:'Апрель', 5:'Май', 6:'Июнь', 7:'Июль', 8:'Август', 9:'Сентябрь', 10:'Октябрь', 11:'Ноябрь', 12:'Декабрь'}
    for l in date[0]: 
        tiime.append(d[l])
    name = Counter(tiime)
    return name

def graph(date):
    if len(date) == 0:
        return "No"
    else:
        for i in range(len(date)):
            pop = Counter(date[i])
            if len(pop) != 1:
                if i == 4:
                    name = seconds(date)
                elif i == 3:
                    name = minutes(date)
                elif i == 2:
                    name = hours(date)
                elif i == 1:
                    name = days(date)
                elif i == 0:
                    name = months(date)         
                return name
            else:
                continue
    return name

def dates(date1):
    date = []
    date.append([i[1] for i in date1]) # month
    date.append([i[2] for i in date1]) # day
    date.append([i[3] for i in date1]) # hour
    date.append([i[4] for i in date1]) # min
    date.append([i[5] for i in date1]) # sec
    a2 = graph(date)
    return a2

def bday(idd):
    user_info = []
    for user_id in idd:
        if str(user_id)[0]=='-':
            continue
        else:
            link = 'http://api.vk.com/method/'
            link+='users.get?user_ids={}&v=5.65&fields={}'.format(user_id, 'bdate')
            response = requests.get(link)
            data = json.loads(response.text)
            z = data['response'][0]
            if "bdate" in z:
                user_info.append(z["bdate"])
    return user_info

def city(idd):
    city1 = []
    for user_id in idd:
        if str(user_id)[0]=='-':
            continue
        else:
            link = 'http://api.vk.com/method/'
            link+='users.get?user_ids={}&v=5.65&fields={}'.format(user_id, 'city')
            response = requests.get(link)
            data = json.loads(response.text)
            z = data['response'][0]
            if "city" in z:
                city1.append(z["city"]['title'])
    return city1

def howold(uage):
    date = uage.split('.')
    if len(date) == 3:
        int_years = time.localtime()[0] - int(date[2]) # - cколько полных лет должно быть
        month = time.localtime()[1] - int(date[1])
        if month < 0:
            age = int_years - 1
        elif month ==0:
            bdate = time.localtime()[2] - int(date[0])
            if bdate <0:
                age = int_years - 1
            else:
                age = int_years
        else:
            age = int_years
    else:
        return 'Non'
    return age

def gr_age(idd):
    ages = []
    bdays = bday(idd)
    for uage in bdays:
        a1 = howold(uage)
        if a1 == 'Non':
            continue
        else:
            ages.append(a1)
    if len(ages) == 0:
        return "No"
    else:
        pop = Counter(ages)
        return pop

def gr_city(city1):
    if len(city1) == 0:
        return "No"
    else:
        pop = Counter(city1)
        return pop

def download1(word, next_from, idd):
    link = 'https://api.vk.com/method/' 
    link+='newsfeed.search?q={}&start_time={}&start_from={}&v=5.65&access_token={}'.format(word, int(time.time() - 1209600), next_from, access_token)
    response = requests.get(link)
    data = json.loads(response.text)
    if data["response"]["total_count"] != 0:
        items = data["response"]["items"]
        date = owner_id(items, idd)
        if len(idd) == 210:
           return idd
        else:
            a2 = nextt3(data, word, idd)
    return idd

def download2(word, next_from, date1):
    link = 'https://api.vk.com/method/' 
    link+='newsfeed.search?q={}&start_time={}&start_from={}&v=5.65&access_token={}'.format(word, int(time.time() - 1209600), next_from, access_token)
    response = requests.get(link)
    data = json.loads(response.text)
    if data["response"]["total_count"] != 0:
        items = data["response"]["items"]
        date = daate(items, date1)
        if len(date1) == 210:
           return date1
        else:
            a2 = nextt(data, word, date1)
    else:
        return date1

def nextt3(data, word, date1):
    if "next_from" in data["response"]:
        next_from = data["response"]["next_from"]
        if next_from != "":
            s1 = download1(word, next_from, date1)
    return date1 

def nextt(data, word, date1):
    if "next_from" in data["response"]:
        next_from = data["response"]["next_from"]
        if next_from != "":
            s1 = download2(word, next_from, date1)
    return date1 

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/result')
def result():
    urls = {'Вернуться к поиску': url_for('index')}
    link = 'https://api.vk.com/method/'
    if request.args:
        date1 = []
        idd = []
        stat = unquote(request.args['answer'])
        word = unquote(request.args['word'])
        link+='newsfeed.search?q={}&start_time={}&v=5.65&access_token={}'.format(word, int(time.time() - 1209600), access_token) # за 2 нед.
        response = requests.get(link)
        data = json.loads(response.text)
        if data["response"]["total_count"] != 0:
            items = data["response"]["items"]
            if stat == 'time':
               p1 = daate(items, date1)
               plus = nextt(data, word, date1)
               date = dates(plus)
               if date == 'No':
                   return render_template('nothing.html', urls=urls)
               else:
                   return render_template('result_time.html', urls=urls, date = date)
            elif stat == 'age':
                p2 = owner_id(items, idd)
                plus = nextt3(data, word, idd)
                date = gr_age(plus)
                if date == 'No':
                   return render_template('nothing.html', urls=urls)
                else:
                    return render_template('result_age.html', urls=urls,  date = date)
            elif stat == 'city':
                p2 = owner_id(items, idd)
                plus = nextt3(data, word, idd)
                a2 = city(plus)
                date = gr_city(a2) 
                if date == 'No':
                    return render_template('nothing.html', urls=urls)
                else:
                    return render_template('result_city.html', urls=urls, date = date)
        else:
            return render_template('result_oops.html', urls=urls)       
   
if __name__ == '__main__':
    app.run(debug=True)

