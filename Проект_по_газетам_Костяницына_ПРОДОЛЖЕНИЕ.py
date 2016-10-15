import re
import os
import urllib.request
import os.path
import csv

def year(html): # - ищем год
    regex = '<a class="headerDate" href="/component/blog_calendar/\?year=(.*?)&amp;month=.{2}&amp;modid=.*?">.*?</a></td>'
    a=re.findall( regex, html, flags=re.U | re.DOTALL)
    year1=''.join(a)
    return year1

def month(html): # - ищем месяц
    regex = '<a class="headerDate" href="/component/blog_calendar/\?year=.{4}&amp;month=(.*?)&amp;modid=.*?">.*?</a></td>'
    a=re.findall( regex, html, flags=re.U | re.DOTALL)
    d = ''.join(a)
    if d[0]=='0':
        month1 = d[1]
    else:
        month1 = d
    return month1

def date(html):
    regex = '<a class="headerDate" href="/component/blog_calendar/\?year=.{4}&amp;month=.*?&amp;modid=.*?">(.*?)</a></td>'
    a=re.findall( regex, html, flags=re.U | re.DOTALL)
    data=''.join(a)
    return data

def author(html): # - имя автора
    regex = '  <meta name="author" content="(.*?)" />'
    a1 = re.findall( regex, html, flags=re.U | re.DOTALL)
    authors = ''.join(a1)
    return authors


def name(html): # - название статьи
    regex = '  <meta name="og:title" content="(.*?)" />'
    a1=re.findall( regex, html, flags=re.U | re.DOTALL)
    name2=''.join(a1)
    clean_4 = re.sub('&laquo;','«', name2)
    name1 = re.sub('&raquo;', '»', clean_4)
    return name1

def engname(html): # - mystem не работает с кириллицой, поэтому названия латиницей 
    regex = '<input type="hidden" class="link-to-share" id="link-to-share-[0-9]*?" value="http://noviput.info/stati/.*?/[0-9]*?-(.*?)"/>'
    a1=re.findall( regex, html, flags=re.U | re.DOTALL)
    name2=''.join(a1)
    return name2

def categoria(html): # -категория
    regex = ' &gt;  <a href="/stati/.*?" class="pathway">(.*?)</a>  &gt;'
    a1 = re.findall( regex, html, flags=re.U | re.DOTALL)
    cate=''.join(a1)
    return cate

def link(html): # - ссылка
    regex = '<input type="hidden" class="link-to-share" id="link-to-share-.*?" value="(http://noviput.info/stati/.*?/.*?)"/>'
    a1 = re.findall( regex, html, flags=re.U | re.DOTALL)
    url=''.join(a1)
    return url

def searchingtext(html): # - найти сам текст статьи
    reg = '</div><p>(.*?)<div id=\'jlvkcomments\'></div>'
    a1=re.findall( reg, html, flags=re.U | re.DOTALL)
    text=''.join(a1)
    return text

def cleaning(text): # - очищаем от ненужных символов 
    clean_1 = re.sub('<.*?>', '', text)
    clean_2 = re.sub('/>', '', clean_1)
    clean_3 = re.sub('&nbsp;', ' ', clean_2)
    clean_4 = re.sub('&laquo;','«', clean_3)
    clean_5 = re.sub('&raquo;', '»', clean_4)
    clean_12 = re.sub(' <!.*&//-->', '', clean_5)
    clean_6 = re.sub('&quot;', '"', clean_12)
    return clean_6

def new( year1, month1, name2, authors, name1, data, cate, url, clean_6):
    for root, dirs, files in os.walk('C:\\Users\\Та\\Desktop\\прога\\mystem-3.0-win7-64bit\\Paper\\plain\\' + year1 + '\\'+ month1):
        for i in files:
            fw = open('C:\\Users\\Та\\Desktop\\прога\\mystem-3.0-win7-64bit\\Paper\\plain\\' + year1 + '\\'+ month1 + '\\' + name2 + '.txt', 'w', encoding='utf-8')
            fw.write('@au ' + authors + '\n' + '@ti ' + name1 + '\n' + '@da ' + data + '\n' + '@topic ' + cate + '\n' + '@url ' + url + '\n' + clean_6)
            fw.close()
    return fw

def download_page(pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl)
        html = page.read().decode('utf-8')
    except:
        print('Error at', pageUrl)
        return
    d = year(html)
    d1 = month(html)
    d2 = date(html)
    a = author(html)
    n = name(html)
    n1 = engname(html)
    c = categoria(html)
    l= link(html)
    s = searchingtext(html)
    cl = cleaning(s)
    nw = new( d, d1, n1, a, n, d2, c, l, cl)

def fk():
    commonUrl = 'http://www.noviput.info/stati/'
    for i in range(4500, 5088): # - иначе получалось очень много статей, компьютер работал 2 дня и сильно перегрелся, поэтому я урезала число статей.
        pageUrl = commonUrl + str(i)
        a = download_page(pageUrl)
    return a

if __name__=='__main__':
    fk()


