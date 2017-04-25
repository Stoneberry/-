import requests
import json
import matplotlib.pyplot as plt
import sys
import re
import time
from datetime import datetime, date, time

# возраст и город
# возраст - средняя длина поста
# город - средняя длина поста 

def opening():
    f = open('new.json', 'r', encoding = 'utf-8')
    data = f.read()
    users = json.loads(data)
    return users # - {id автора : [[texts], [age, city]]}

def no_emoji(a):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    text = a.translate(non_bmp_map)
    return text

def howlong(users, user_id):
    num = 0
    texts = users[user_id][0]
    for text in texts:
        text1 = no_emoji(text)
        words = text1.split(' ')
        num += len(words)
    return num

def today_year():
    date = str(datetime.now(tz=None))
    reg = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
    pip = re.findall(reg, date)
    date1 = pip[0].split('-')
    return date1[0]

def today_month():
    date = str(datetime.now(tz=None))
    reg = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
    pip = re.findall(reg, date)
    date1 = pip[0].split('-')
    return date1[1]

def today_day():
    date = str(datetime.now(tz=None))
    reg = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
    pip = re.findall(reg, date)
    date1 = pip[0].split('-')
    return date1[2]

 #12.5.1996
def howold(uage):
    reg = '[1-3][0-9]?\.1?[0-9]\.[0-9]{4}'
    z = re.findall(reg, uage) # - массив ['12.5.1996']
    if z!=[]:
        date = uage.split('.')
        int_years = int(today_year()) - int(date[2]) # - cколько полных лет должно быть
        month = int(today_month()) - int(date[1])
        if month < 0:
            age = int_years - 1
        elif month ==0:
            bdate = int(today_day()) - int(date[0])
            if bdate <0:
                age = int_years - 1
            else:
                age = int_years
        else:
            age = int_years
    else:
         age = 0          
    return age

def ages(users):
    user_age = {}
    for user_id in users:
        uage1 = users[user_id][1][0]
        if uage1 != '0':
            uage = howold(uage1)
            if uage != 0:
                if uage in user_age:
                    user_age[uage].append(howlong(users, user_id))
                else:
                    user_age[uage] = []
                    user_age[uage].append(howlong(users, user_id))
            else:
                continue
        else:
            continue
    return user_age  # {age: [длины]}

def average(numbers):
    num = 0
    for i in numbers:
        num = num + i
    y = num//len(numbers)
    return y

def graph_age(user_age):
    age = []
    length = []
    for i in sorted(user_age):
        age.append(i)
        if len(user_age[i]) == 1:
            length.append(user_age[i][0])
        else:
            length.append(average(user_age[i]))
    plt.plot(age, length)
    plt.show()
    return 

def task_3(users):
    user_city = {}  # - city: length
    for user_id in users:
        ucity = users[user_id][1][1]
        if ucity != 0:
            if ucity != '':
                if ucity in user_city:
                   user_city[ucity].append(howlong(users, user_id))
                else:
                    user_city[ucity] = []
                    user_city[ucity].append(howlong(users, user_id))
            else:
               continue
    return user_city

def graph_city(user_city):
    city = []  # название столбиков
    length = [] # длина столбиков
    z = []
    for i in sorted(user_city):
        city.append(i)
        if len(user_city[i]) == 1:
            length.append(user_city[i][0])
        else:
            length.append(average(user_city[i]))
    for l in range(len(city)):
        z.append(l)
    plt.bar(z, length)
    plt.xticks(z, city)
    plt.show()
    return 

def final():
    a0 = opening()
    a1 = ages(a0)
    a3 = graph_age(a1)
    a4 = task_3(a0)
    a5 = graph_city(a4)
    return

if __name__=='__main__':
    final()
