#!/usr/bin/env python
#-----------------------------------------
# deal.ii translator for doxygen documents
# Jiaqi-Knight 2021
# based on Dmitry R. Gulevich 2020 getxfix
#-----------------------------------------

import re
import sys
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()

if(re.search('.txt$',args.filename)==None):
    sys.exit('The input should be .txt file. Exit.')

print('Input file:',args.filename)


filebase = re.sub('_0_T.txt$','',args.filename)
doxygen_latex=filebase+'_doxygen_latex'
doxygen_commands=filebase+'_doxygen_commands'


### Load LaTeX data from binary files
with open(args.filename, 'r') as fin:
    source = fin.read()
with open (doxygen_commands, 'rb') as fp:
    commands = pickle.load(fp)   
with open (doxygen_latex, 'rb') as fp:
    latex = pickle.load(fp)

### Replace weird characters introduced by translation
trtext=re.sub('\u200B',' ',source)

### Fix spacing
trtext = re.sub(r'\\ ',r'\\',trtext)
trtext = re.sub(' ~ ','~',trtext)
trtext = re.sub(' {','{',trtext)

### Restore LaTeX and formulas
here=0
newtext=''
nl=0
nc=0
corrupted=[]
for m in re.finditer('\[{0,1}[012][\.\, ][xX][\.\,][0-9]+\]{0,1}',trtext):
    print(m)
    t=int( re.search('(?<=\[{0})[012](?=[\.\,][xX][\.\,])',m.group()).group() )
    n=int( re.search('(?<=[\.\,][xX][\.\,])[0-9]+(?=\]{0})',m.group()).group() )
    if(t==1):
        #if(n<nl):
        #    print('Token ',m.group(),'found in place of [%d.%d]. Edit manually and run again.'%(t,nl))
        #    break
        #while(nl!=n):
        #    corrupted.append('[%d.%d]'%(t,nl))
        #    nl+=1
        newtext += trtext[here:m.start()] + latex[n]
        #nl+=1
    elif(t==2):
        #if(n<nc):
        #    print('Token ',m.group(),'found in place of [%d.%d]. Edit manually and run again.'%(t,nc))
        #    break
        #while(nc!=n):
        #    corrupted.append('[%d.%d]'%(t,nc))
        #    nc+=1
        newtext += trtext[here:m.start()] + " " + commands[n] + " "
        #nc+=1
    here=m.end()
newtext += trtext[here:]
trtext=newtext



##最后再进行一些修剪的工作
regex = r"(?<=\<\/h[0-9]\>)[。]|(?<=\<\/h[0-9]\>).[。]|(?<=@f})[。]|(?<=@f}).[。]"
subst = ""
trtext = re.sub(regex, subst, trtext , 0)


### Save the processed output to .tex file
output_filename = re.sub('.txt$','.h',args.filename)
with open(output_filename, 'w') as translation_file:
	translation_file.write(trtext)
print('Output file:',output_filename)

### Report the corrupted tokens
if(corrupted==[]):
    print('No corrupted tokens. The translation is ready.')	
else:
    print('Corrupted tokens detected:',end=' ')
    for c in corrupted:
        print(c,end=' ')
    print()
    print('To improve the output manually change the corrupted tokens in file',args.filename,'and run from.py again.')

