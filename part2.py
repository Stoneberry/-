import os
import re


def change():
    f = open('/Users/Stoneberry/Desktop/Университет/Прога/in/text_for_exam.txt', 'r', encoding = 'utf-8')
    words1 = f.read()
    f.close()
    clean = re.sub('ӏ', 'l', words1)
    f1 = open('/Users/Stoneberry/Desktop/Университет/Прога/in/text_for_exam.txt', 'w', encoding = 'utf-8')
    f1.write(clean)
    f1.close()
    return

def mystem():
    inp = "/Users/Stoneberry/Desktop/Университет/Прога/in"
    lst = os.listdir(inp)
    for fl in lst:
        os.system("/Users/Stoneberry/Desktop/Университет/Прога/mystem " + inp + os.sep + fl + " /Users/Stoneberry/Desktop/Университет/Прога/out" + os.sep + fl + " -cnid --format text")
    return

def work():
    f = open('/Users/Stoneberry/Desktop/Университет/Прога/out/text_for_exam.txt', 'r', encoding = 'utf-8') 
    lines1 = f.readlines()
    lines = []
    for i in lines1:
    	i = i.strip('\n')
    	lines.append(i)
    return lines

def opening1():
    f = open('/Users/Stoneberry/Desktop/Университет/Прога/in/text_for_exam.txt', 'r', encoding = 'utf-8')
    words1 = f.readlines()
    f.close()
    words = []
    for i in words1:
        i = i.strip('\n')
        words.append(i)
    return words

def reg(lines):
    a1 = []
    req = '=им,ед'
    for i in lines:
        if req in i:
            a1.append(i)
    return a1

def finding(words, a1):
    a2 = set()
    for i in words:
        for l in a1: 
            if i in l:
                a2.add(i)
    return a2
    
def new_file(a2):
    f = open ('/Users/Stoneberry/Desktop/Университет/Прога/in/rus_nouns.txt', 'a', encoding = 'utf-8')
    for i in a2:
        f.write(i + '\n')
    f.close()
    return

def final():
    a = change()
    a1 = mystem()
    a2 = work()
    a0 = opening1()
    a3 = reg(a2)
    a3b = finding(a0, a3)
    a4 = new_file(a3b)

if __name__=='__main__':
    final()
