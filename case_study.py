
# Declaring variables and importing packages
import pattern
import parser
import re
import pandas as pd
from pattern.en import parse
from pattern.en import pprint
from pattern.en import parsetree
from pattern.en import tag
str_food=''
str_place=''
flag_q1=0a
flag_n1=0
flag_n2=0
merge_lst=[]
list2=['was','am','is','does','are']
sentenc="Amazing XYZ at City Square Mall!!!" # here, XYZ is the food type and place is City Sqlare mall.
#The dummy dataset XYZ.csv contains the list of food and places in CSV format.
adjectvs=[]
DT=[]
i=0
nouns=[]

#eliminating all special characters(added after our discussion and it can handle sentences ending with exclamation

word_lst=sentenc[-1].lower()


# Splitting the sentence to get the first and the last word
word_list=sentenc.split()
sentenc = re.sub(r'[?|$|.|!]',r'',sentenc)
word_fst=word_list[0].lower()

#loading the CSV file into a dataframe and segregating the columns for street names and food
df = pd.read_csv('XYZ.csv', names=['places','food'],skiprows=1)
df['places']=df['places'].str.lower()
df['food']=df['food'].str.lower()

#parsing the sentence
p_tree = parsetree(sentenc.lower(), relations=True, lemmata=True)

#conditions to get the part of speech(pos) of the sentence and determining the intention of the sentence
if word_fst in list2:
    flag_q1=1
for words,pos in tag(sentenc.lower()):
    if pos=="JJ":
        adjectvs.append(words)
    if pos=="DT":
        DT.append(words)
    if (word_fst == words and (pos=="PRP" or pos == "DT" or word_fst=="i")):
        flag_n1 = 1
    if word_lst==words and pos=="JJ":
        flag_n2=1

# merging the adjectives and the determinators

merge_lst=DT+adjectvs

# parsing the values of the nouns and eliminationg the adjectives
for sentence in p_tree:
    for chunk in sentence.chunks:
        if chunk.type=="NP":
            noun_str=[(w.string) for w in chunk.words]
            nouns.append([' '.join(str(w) for w in noun_str if w.lower() not in merge_lst)])

# comparing the list of nouns to the places and food dataframe
for ki in nouns:
    ki= ', '.join(ki)
    if df['places'].str.contains(ki).any():
        str_place=ki
    if df['food'].str.contains(ki).any():
        str_food=ki

# Determining the intention of the sentence through the flags set
if (flag_q1==0 and (flag_n1==1 or flag_n2==1)):
    str_sent="The intention of the sentence is a statement"
elif (flag_q1==1 ):
    str_sent="The intention of the sentence is a question"
else:
    str_sent = "The intention of the sentence is a question"

print ("intent:"+str_sent , "place:" +str_place, "food:"+ str_food)

