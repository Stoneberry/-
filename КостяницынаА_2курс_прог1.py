import urllib.request
import re

def function0():
    req = urllib.request.Request('http://pr-vesti.ru/')
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8') #- получили строчки
    return html

def searching(html):  
    a=[]
    regex='rel="bookmark">(.*?)</a></h2>'
    titles=re.findall( regex, html, flags=re.U | re.DOTALL)
    for i in titles:
        if i in a:
            continue
        else:
            a.append(i)
    return a

def cleaning(a): 
    new_titles = []
    reg=re.compile('&#.{3};', flags=re.U | re.DOTALL)
    for l in a:
        clean_t = reg.sub("", l)
        new_titles.append(clean_t)
    return new_titles

def new(new_titles):
    fw = open('C:\\Users\\Та\\Desktop\\name1.txt','w', encoding='utf-8')
    for i in new_titles:
        fw.write(i+'\n')
    fw.close()
    return fw


def main():
    vab1 = function0()
    vab2 = searching(vab1)
    vab3 = cleaning(vab2)
    vab4 = new(vab3)


if __name__=='__main__':
    main()
