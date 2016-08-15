import csv
import requests

from bs4 import BeautifulSoup
import pandas as pd

url = 'http://aucoe.annauniv.edu/cgi-bin/result/cograde.pl' #URL for coimbatore region, check aucode for URLs for other cities

spamwriter = []
df=pd.read_csv('clg.csv') #Aggregated college codes for coimbatore region (Not sure if correct)
li=0
for iop,r1 in df.iterrows():
    print 'At row ' + str(li)
    li=li+1
    for i in range(int(r1['start']),int(r1['end'])):
        studata = dict()
        regno= {'regno': i}
        r = requests.post(url, data=regno)
        soup = BeautifulSoup(r.text)
        table = soup.find_all('table')
        rows = table[2].findAll('tr')[0:]
        '''
        header = table[2].findAll('tr')[0:][0].find_all('font')
        header = map(lambda x : x.contents[0],header)
        header.append('Name')
        header.append('University')
        header.append('Branch')
        studata['header'] = header
        '''
        headname = table[1].find_all('strong')
        try:
            headname = map(lambda x : x.contents[0],headname)
        except:
            continue
        subs=[]
        res=[]
        subs = dict()
        for row in rows[1:]:
            data = row.findAll('td')
            subs[data[0].find('strong').contents[0]] = data[1].find('strong').contents[0]
        studata['studentdetail'] = headname
        studata['res'] = subs
        spamwriter.append(studata)

import json
with open('out.json', 'w') as outfile:
    json.dump(spamwriter, outfile)