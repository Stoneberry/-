import urllib.request
import re

def load(i):
    req = urllib.request.Request(i)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html

def textfinder(html):
    reg = '<p>(.*?)</p>'
    a1 = re.findall(reg, html)
    zz = []
    for i in a1:
        clean = re.sub('&quot;', '', i)
        clean_0 = re.sub('&nbsp;', '', clean)
        clean_1 = re.sub('&laquo;','', clean_0)
        clean_2 = re.sub('&raquo;','', clean_1)
        clean_3 = re.sub('<.*?>', '', clean_2)
        zz.append(clean_3)
    return zz

def chastota1(zz):
    d = {}
    for i in zz:
        a2 = i.split('.')
        for l in a2:
            l = l.lower()
            for word in l.split(' '):
                word = word.strip('"«»,.:;?!()—')
                if word in d:
                    d[word]+=1
                else:
                    d[word]=1
    return d

def chastota2(d):
    a1 =set()
    for i in d:
        if d[i]>1:
            a1.add(i)
        else:
            continue
    return a1

def chastota3(block2):
    x = block2[0]
    y = block2[1]
    z = block2[2]
    t = block2[3]
    m1 = x^y^z^t
    m=[]
    for i in m1:
        m.append(i)
    return m

def mnog(zz):
    a1 = set()
    for i in zz:
        a2 = i.split('.')
        for l in a2:
            for word in l.split(' '):
                word = word.strip('«»",.:;?!()—')
                a1.add(word)
    return a1

def peresek(block):
    x = block[0]
    y = block[1]
    z = block[2]
    t = block[3]
    m1 = x&y&z&t
    m = []
    for i in m1:
        m.append(i)
    return m

def raznost(block):
    x = block[0]
    y = block[1]
    z = block[2]
    t = block[3]
    m1 = x^y^z^t
    m=[]
    for i in m1:
        m.append(i)
    return m

def newfile(a4, a5, a6):
    f = open('new11.txt', 'a', encoding = 'utf-8')
    for i in sorted(a4): # - 4 задание
        f.write(i+'\n')
    f.close()
    f1 = open('new12.txt', 'a', encoding = 'utf-8')
    for l in sorted(a5): # - 5 задание
        f1.write(l+'\n')
    f1.close()
    f2 = open('new13.txt', 'a', encoding = 'utf-8')
    for k in sorted(a6): # - 6 задание
        f2.write(k+'\n')
    f2.close()
    return

def fil():
    block = []
    block2 =[]
    files = ['http://vladnews.ru/2016/12/03/117438/zveropolis-nazvan-luchshim-multfilmom-goda.html','http://runews24.ru/kino/02/12/2016/217e1b2997f5b59372b07164c7a59ebc', 'https://nation-news.ru/228766-zveropolis-priznali-luchshim-multfilmom-2016-goda', 'http://tsargrad.tv/news/2016/12/02/v-ssha-nazvali-luchshij-multfilm-goda']
    for i in files:
        a1 = load(i)
        a2 = textfinder(a1)
        a6 = chastota1(a2)
        a7 = chastota2(a6)
        block2.append(a7)
        a3 = mnog(a2)
        block.append(a3)
    a4 = peresek(block)
    a5 = raznost(block)
    a6 = chastota3(block2)
    a8 = newfile(a4, a5, a6)
    return

if __name__=='__main__':
    fil()
    
