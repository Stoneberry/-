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

def title(date, index, tiime):
    if len(Counter(date[index])) == 1:
        tiime.append(date[index][0])
    else:
        line = ''
        for i in date[index]:
            line = line + str(i) + '-'
        tiime.append(line)
    return tiime

def title_for_seconds(date, tiime):
    line = str(date[2]) + ':' + str(date[3]) # hour:minute
    tiime.append(line)
    return tiime

def seconds(date):
    tiime = {} # - [seconds, hours + minutes, {seconds}] 0 - ось Х, 1 - title, 2 - значения
    a1 = title_for_seconds(date, tiime)
    d1 = []
    for i in date[4]:
        d1.append(i)
    d = Counter(d1)
    pop = []
    for l in sorted(d):
        a0 = []
        a0.append(l)
        a0.append(d[l])
        pop.append(a0)
    tiime.append(pop)
    return tiime

def title_for_minutes(date, tiime):
    line = str(date[2][0]) + 'h'
    tiime.append(line)
    return tiime

def minutes(date):
    tiime = []  # - [minutes, hours, {minutes}] 0 - ось Х, 1 - title, 2 - значения
    tiime.append('minutes')
    a1 = title_for_minutes(date, tiime)
    d1 = []
    for i in date[3]:
        d1.append(i)
    d = Counter(d1)
    pop = []
    for l in sorted(d):
        a0 = []
        a0.append(l)
        a0.append(d[l])
        pop.append(a0)
    tiime.append(pop)
    return tiime

def title_for_hours(date, tiime):
    months = {1:'Январь', 2:'Февраль', 3:'Март', 4:'Апрель', 5:'Мая', 6:'Июнь', 7:'Июль', 8:'Август', 9:'Сентябрь', 10:'Октябрь', 11:'Ноябрь', 12:'Декабрь'}
    line = str(date[1][0]) + ', ' + months[date[0][0]] # day, month
    tiime.append(line)
    return tiime

def hours(date):
    tiime = []  # - [hours, days, {hours}] 0 - ось Х, 1 - title, 2 - значения
    tiime.append('hours')
    a1 = title_for_hours(date, tiime)
    d1 = []
    for i in date[2]:
        d1.append(i)
    d = Counter(d1)
    pop = []
    for l in sorted(d):
        a0 = []
        a0.append(l)
        a0.append(d[l])
        pop.append(a0)
    tiime.append(pop)
    return tiime


def title_for_days(date, index, tiime):
    months = {1:'Январь', 2:'Февраль', 3:'Март', 4:'Апрель', 5:'Мая', 6:'Июнь', 7:'Июль', 8:'Август', 9:'Сентябрь', 10:'Октябрь', 11:'Ноябрь', 12:'Декабрь'}
    if len(Counter(date[index])) == 1:
        tiime.append(months[date[index][0]])
    else:
        line = ''
        for i in date[index]:
            line = line + months[i] + '-'
        tiime.append(line)
    return tiime


def days(date):
    tiime = [] # - [days, month, {days}] 0 - ось Х, 1 - title, 2 - значения
    tiime.append('days')
    a1 = title_for_days(date, 0, tiime)
    d1 = []
    for i in date[1]:
        d1.append(i)
    d = Counter(d1)
    pop = []
    for l in sorted(d):
        a0 = []
        a0.append(l)
        a0.append(d[l])
        pop.append(a0)
    tiime.append(pop)
    return tiime


def months(date):
    tiime = [] # - [month, year, {months}]  0 - ось Х, 1 - title, 2 - значения
    tiime.append('month')
    a1 = title(date, 5, tiime)
    d1 = []
    for i in date[0]:
        d1.append(i)
    d = Counter(d1)
    pop = []
    for l in sorted(d):
        a0 = []
        a0.append(l)
        a0.append(d[l])
        pop.append(a0)
    tiime.append(pop)
    return tiime


def year(date):
    tiime = [] # - [year, years, {years}] 0 - ось Х, 1 - title, 2 - значения
    tiime.append('year')
    a1 = title(date, 5, tiime)
    tiime.append(sorted(Counter(date[5])))
    return tiime


def graph(date):
    if len(date) == 0:
        return "No"
    else:
        for i in range(len(date)):
            pop = Counter(date[i])
            if len(pop) != 1:
                if i == 5:
                    name == year(date)
                elif i == 4:
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
    date.append([i[0] for i in date1]) # year
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
        d = Counter(ages)
        pop = []
        for l in sorted(d):
            a0 = []
            a0.append(l)
            a0.append(d[l])
            pop.append(a0)
        return pop

def gr_city(city1):
    if len(city1) == 0:
        return "No"
    else:
        pop = Counter(city1)
        return sorted(pop)

def new_file(pip):
    f = open('new.json', 'a', encoding = 'utf-8')
    f.write(json.dumps(pip))
    f.close()
    return

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
 #           a67 = new_file(data)
            items = data["response"]["items"]
            if stat == 'time':
               p1 = daate(items, date1)
               plus = nextt(data, word, date1)
               date = dates(plus) #- [year, years, {years}] 0 - ось Х, 1 - title, 2 - значения
               title = date[1]
               os = date[0]
               date1 = date[2]
               if date == 'No':
                   return render_template('nothing.html')
               else:
                   return render_template('time1.html', date1 = date1, os = os, title = title)
            elif stat == 'age':
                p2 = owner_id(items, idd)
                plus = nextt3(data, word, idd)
                date = gr_age(plus)
                if date == 'No':
                   return render_template('nothing.html')
                else:
                    return render_template('result_age.html',  date = date)
            elif stat == 'city':
                p2 = owner_id(items, idd)
                plus = nextt3(data, word, idd)
                a2 = city(plus)
                date = gr_city(a2)
                if date == 'No':
                    return render_template('nothing.html')
                else:
                    return render_template('result_city.html', date = date)
        else:
            return render_template('result_oops.html')
    else:
        return render_template('result_oops.html')

if __name__ == '__main__':
    app.run(debug=True)

