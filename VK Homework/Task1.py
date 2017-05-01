# выкачиваем все посты и коментарии к ним сообщества

import requests
import json
import matplotlib.pyplot as plt
import sys
import re

def download_first():
    link = 'http://api.vk.com/method/'
    owner_id = '-31513532'
    count = '100'
    link+='wall.get?owner_id={}&count={}'.format(owner_id, count)
    response = requests.get(link)
    data = json.loads(response.text)
    y = data['response']
    return y

def download_second():
    link = 'http://api.vk.com/method/'
    owner_id = '-31513532'
    count = '100'
    offset = '101'
    link+='wall.get?owner_id={}&count={}&offset={}'.format(owner_id, count, offset)
    response = requests.get(link)
    data = json.loads(response.text)
    x = data['response']
    return x

def download_comments(post_id):
    link = 'http://api.vk.com/method/'
    owner_id = '-31513532'
    count = '100' # - больше ста комментариев не было 
    link+='wall.getComments?owner_id={}&post_id={}&count={}'.format(owner_id, post_id, count)
    response = requests.get(link)
    data = json.loads(response.text)
    z = data['response']
    comments = []
    if z != [0]:
        for i in z:
            if type(i)==dict:
                text = re.sub('<br>', '', i["text"]) # - строка
                comments.append(text)
    return comments 

##def download_comments2(post_id):  # просто показать, что я понимаю, как скачивать большее кол-во коментариев, но в этом нет необходимости
##    link = 'http://api.vk.com/method/'
##    owner_id = '-31513532'
##    count = '100' 
##    offset = '101'
##    link+='wall.getComments?owner_id={}&post_id={}&count={}&offset={}'.format(owner_id, post_id, count, offset)
##    response = requests.get(link)
##    data = json.loads(response.text)
##    z = data['response']
##    comments = []
##    if z != [0]:
##        for i in z:
##            if type(i)==dict:
##                text = re.sub('<br>', '', i["text"]) # - строка
##                comments.append(text)
##    return comments 
    
def post_ids(y):
    info = {} # - ключ - id, значение - [текст, [коментарии], id автора]
    for i in y:
        if type(i)==dict:
            post_id = i["id"]
            info[post_id] = []
            text = re.sub('<br>', '', i["text"])
            com = download_comments(post_id) # - массив комментариев
            from_id = i["from_id"]
            info[post_id].append(text)
            info[post_id].append(com)
            info[post_id].append(from_id)
    f = open('info.json', 'a', encoding = 'utf-8')
    f.write(json.dumps(info))
    f.close()
    return info

def no_emoji(a):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    text = a.translate(non_bmp_map)
    return text

def howlong_text(info, note):
    a = info[note][0]
    text1 = no_emoji(a)
    words = text1.split(' ')
    return len(words)

def howlong_comments(info, note):
    num = 0
    a = info[note][1]
    if a==[]:
        num = 0
    elif a==['']:
        num = 0
    else:
        for i in a:
            post = no_emoji(i)
            words = post.split(' ')
            num += len(words)
    return num

def numbers(info):
    d = {} # - ключ - длина текста, значение -  [длина комментариев]
    for note in info:
        y = howlong_text(info, note)
        z = howlong_comments(info, note)
        if y in d:
            d[y].append(z)
        else:
            d[y] = []
            d[y].append(z)
    return d

def special_for_task_2(info):
    d = {} # ключ -  id, значение - [длина текста, длина ком, id автора]
    for note in info:
        d[note] = []
        d[note].append(howlong_text(info, note))
        d[note].append(howlong_comments(info, note))
        d[note].append(info[note][2])
    f = open('pizza.json', 'a', encoding = 'utf-8')
    f.write(json.dumps(d))
    f.close()
    return

def all_in_all():
    a0 = download_first()
    a1 = download_second()
    a2_a = post_ids(a0)
    a2_b = post_ids(a1)
    for i in a2_b:
       a2_a[i] = a2_b[i]
    a3 = numbers(a2_a)
    s0 = special_for_task_2(a2_a)
    return a3

def average(numbers):
    num = 0
    for i in numbers:
        num = num + i
    y = num//len(numbers)
    return y          
        
def length(a3):
    length_text = []
    length_com = []
    for i in sorted(a3):
        if len(a3[i])==1:
            length_text.append(i)
            length_com.append(a3[i][0])
        else:
            length_text.append(i)
            length_com.append(average(a3[i]))
    plt.plot(length_text, length_com)
    plt.show()
    return
        
def final():
    a0 = all_in_all()
    a1 = length(a0)
    return

if __name__=='__main__':
    final()

