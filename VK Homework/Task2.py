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
    f = open('pizza.json', 'r', encoding = 'utf-8')
    data = f.read()
    info = json.loads(data)
    return info # ключ -  id, значение - [длина текста, длина ком, id автора]

def download_comments(post_id):
    link = 'http://api.vk.com/method/'
    owner_id = '-31513532'
    count = '100' # - больше ста комментариев не было 
    link+='wall.getComments?owner_id={}&post_id={}&count={}'.format(owner_id, post_id, count)
    response = requests.get(link)
    data = json.loads(response.text)
    z = data['response']
    users = {} # - key - id author, value - [text]
    if z != [0]:
        for i in z:
            if type(i)==dict:
                user_id = i["uid"]
                text = re.sub('<br>', '', i["text"])
                if user_id in users:
                    users[user_id].append(text)
                else:
                    users[user_id] = []
                    users[user_id].append(text)                  
    return users

def age_city(user_id):
    user_info = []
    link = 'http://api.vk.com/method/'
    link+='users.get?user_ids={}&fields={}'.format(user_id, 'bdate,city')
    response = requests.get(link)
    data = json.loads(response.text)
    z = data['response'][0]
    if "bdate" in z:
        user_info.append(z["bdate"])
    else:
        user_info.append('0')
    if "city" in z:
        user_info.append(z["city"])
    else:
        user_info.append('')
    return user_info

# автором всех постов является сообщество, поэтому их не учитываем  

def all_in_all(info):
    pip = {}
    for post_id in info:
        if info[post_id][1] != 0:
            users = download_comments(post_id)
            for i in users:
                if i in pip:
                    for text in users[i]:
                        pip[i][0].append(text) # на случай, если люди комментируют несколько постов
                else:
                    agecity = age_city(i)
                    pip[i] = []
                    pip[i].append(users[i])
                    pip[i].append(agecity)
        else:
            continue
    f = open('new.json', 'a', encoding = 'utf-8')
    f.write(json.dumps(pip))
    f.close()
    return users  # - {id автора : [[texts], [age, city]]}

            
def final():
    a0 = opening()
    a1 = all_in_all(a0)
    return

if __name__=='__main__':
    final()
