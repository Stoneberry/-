from flask import Flask
from flask import url_for, render_template, request, redirect
from urllib.parse import unquote
import json

app = Flask(__name__)

def file(a1):
    f = open('/Users/Stoneberry/Desktop/my_app/data/new.txt', 'a', encoding='utf-8')
    f.write(a1[0]+'\t'+a1[1]+'\t'+a1[2]+'\t'+a1[3]+'\t'+a1[4]+'\t'+a1[5]+'\t'+a1[6]+'\t'+a1[7]+'\t')
    f.close()
    return f

def corpus():
    f = open('/Users/Stoneberry/Desktop/my_app/data/new.txt', 'r', encoding='utf-8')
    a=f.read()
    a1 = a.split('\t')
    return a1
    
def znaki(a1):
    foot = a1[3::8]
    turkish = a1[4::8]
    finger = a1[5::8]
    hand = a1[6::8]
    face = a1[7::8]
    slovar = {}
    slovar['Положить ногу на ногу'] = foot
    slovar['Сесть по-турецки'] = turkish
    slovar['Встать на цыпочки'] = finger
    slovar['Поднять руку'] = hand
    slovar['Опереть лицо рукой'] = face
    return slovar
    
def apa(d, username, age, lang, nogananogu, poturezki, natsipochki, podniatruku, operetlitso):
    d.append(username)
    d.append(age)
    d.append(lang)
    d.append(nogananogu)
    d.append(poturezki)
    d.append(natsipochki)
    d.append(podniatruku)
    d.append(operetlitso)
    return d

def search(word, slovar):
    if word in slovar:
        return slovar[word]
    

@app.route('/')
def index():
    d=[]
    if request.args:
        username = unquote(request.args['username'])
        if username=='':
            return redirect(url_for('index'))
        age = unquote(request.args['age'])
        lang = unquote(request.args['language'])
        nogananogu = unquote(request.args['nogananogu'])
        poturezki = unquote(request.args['poturezki'])
        natsipochki = unquote(request.args['natsipochki'])
        podniatruku = unquote(request.args['podniatruku'])
        operetlitso = unquote(request.args['operetlitso'])
        a1 = apa(d, username, age, lang, nogananogu, poturezki, natsipochki, podniatruku, operetlitso)
        z = file(a1)
        return redirect(url_for('searching'))
    return render_template('index2.html')

@app.route('/search')
def searching():
    urls = {'Анкета': url_for('index'),
            'Поиск по результатам': url_for('searching'),
            'Статистика': url_for('table'),
            'Json': url_for('son'),}
    variant = ['Положить ногу на ногу', 'Сесть по-турецки','Встать на цыпочки', 'Поднять руку', 'Опереть лицо рукой']
    return render_template('searching.html', variant = variant, urls=urls)
    
@app.route('/result')
def results():
    urls = {'Анкета': url_for('index'),
            'Поиск по результатам': url_for('searching'),
            'Статистика': url_for('table'),
            'Json': url_for('son'),}
    if request.args:
        word = unquote(request.args['word']) # - слово и на всякий его в норм кодировку
        a1 = corpus()
        slovar = znaki(a1)
        if word in slovar:
            answer = search(word, slovar) 
            return render_template('result.html', answer = answer, urls=urls)
        else:
            return redirect(url_for('searching'))

@app.route('/stats')
def table():
    urls = {'Анкета': url_for('index'),
            'Поиск по результатам': url_for('searching'),
            'Статистика': url_for('table'),
            'Json': url_for('son'),}
    x = corpus()
    number = x[0::8]
    age = x[1::8]
    kid = []
    young = []
    adult = []
    grand = []
    for i in age:
        if i.startswith('k'):
            kid.append(i)
        elif i.startswith('y'):
            young.append(i)
        elif i.startswith('a'):
            adult.append(i)
        else:
            grand.append(i)
    return render_template('table.html', number = len(number), kid = len(kid), young = len(young), adult =len(adult) , grand = len(grand), urls=urls)

@app.route('/json')
def son():
    x = corpus()
    y =json.dumps(x)
    return y
    
if __name__ == '__main__':
    app.run(debug=True)
