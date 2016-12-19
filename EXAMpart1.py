import re

def opening1():
    f = open('in/text_for_exam.txt', 'r', encoding = 'utf-8')
    lines1 = f.readlines()
    f.close()
    lines = []
    for i in lines1:
        i = i.strip('\n')
        lines.append(i)
    return lines

def opening2():
    f = open('examsite.htm', 'r', encoding = 'utf-8')
    html1 = f.readlines()
    f.close()
    html = []
    for i in html1:
        i = i.lower()
        html.append(i)
    return html

def reg(lines, html):
    a1 = set()
    for line in lines:
        req = '(?: |,|\.|!|\?|:|;)' + line + '(?: |,|\.|!|\?|:|;)'
        for i in html:
            a2 = re.findall(req, i)
            if a2!= []:
                a1.add(line)
    return a1

def new_file(a1):
    f = open('wordlist.txt', 'a', encoding = 'utf-8')
    for i in a1:
        f.write(i+'\n')
    f.close()
    return

def final():
    a1 = opening1()
    a2 = opening2()
    a3 = reg(a1, a2)
    a4 = new_file(a3)
    return

if __name__=='__main__':
    final()
