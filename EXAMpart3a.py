# wordform lemma
# пае{пай=S,муж,неод=пр,ед}
import os
import re

def mystem(): #- полный путь, потому что относительный не работал
    os.system("/Users/Stoneberry/Desktop/Университет/Прога/mystem " + '/Users/Stoneberry/Desktop/Университет/Прога/in/rus_nouns.txt'  + ' /Users/Stoneberry/Desktop/Университет/Прога/out/rus_nouns.txt' + " -cnd --format text")
    return

def opening2():
    f = open('/Users/Stoneberry/Desktop/Университет/Прога/out/rus_nouns.txt', 'r', encoding = 'utf-8')
    words1 = f.readlines()
    f.close()
    words = []
    for i in words1:
        i = i.strip('\n\\n')
        if i!='':
            words.append(i)
        else:
            continue
    return words

def wordss(line):
    reg = '(.*?){.*?}'
    word = re.findall(reg, line)
    return word[0]

def lemmass(line):
    reg = '.*?{(.*?)}'
    lemma = re.findall(reg, line)
    return lemma[0]

def new_file(wordform, lemma):
    f = open('/Users/Stoneberry/Desktop/Университет/Прога/sql.txt', 'a', encoding = 'utf-8')
    f.write('insert into Rus_words values ("' + str(wordform) + '", "' + str(lemma) + '")' + '\n')
    f.close()
    return

def finding(words):
    for word in words:
        wordform = wordss(word)
        lemma = lemmass(word)
        a1 = new_file(wordform, lemma)
    return

def final():
    a1 = mystem()
    a2 = opening2()
    a3 = finding(a2)

if __name__=='__main__':
    final()
