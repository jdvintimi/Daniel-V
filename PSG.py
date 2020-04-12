# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 22:04:20 2020

@author: Daniel
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 21:54:46 2020

@author: Daniel
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import time
import re
import numpy as np
import datetime
import unidecode as unidecode

def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

alist=[]
team1_list=[]
team2_list=[]
team1_score_list=[]
team2_score_list=[]
team1_regionlist=[]
team2_regionlist=[]
team1_betlist=[]
team2_betlist=[]
draw_betlist=[]
match_datelist=[]
count=0

for i in range(0,46):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) chrome/41.0.2228.0 Safari/537.3'}
    reg_url = "https://www.gosugamers.net/dota2/teams/2933-psg-lgd/matches?maxResults=21&page=" + str(i + 1)
    req = Request(url=reg_url, headers=headers) 
    html = urlopen(req).read() 
    soup=BeautifulSoup(html,"lxml")
    
    time.sleep(1)
    matchlist = soup.find_all('a', attrs={'href': re.compile('/dota2/tournaments/')})
    for matchlistitem in matchlist:
        try:
            #matchtag = matchlistitem.find('a', attrs={'href': re.compile("/dota2/tournaments/" )})
            matchurl = matchlistitem.get('href')
            
        except Exception as e:
            matchurl = 'a'
        
        #if (matchurl.find('dota2') != -1):
        #    alist.append(matchurl)
            
        
        alist.append(matchurl)
        
urllist = getUniqueItems(alist)

for i in urllist:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) chrome/41.0.2228.0 Safari/537.3'}
    reg_url = "https://www.gosugamers.net" + i
    req = Request(url=reg_url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html,"lxml")
    
    try:
        team1 = soup.find('div', attrs={'class':'team cell small-7 large-6'})
        team2 = soup.find('div', attrs={'class':'team cell small-7 large-6 large-order-3'})
        board = soup.find('div', attrs={'class':'details cell large-3 large-order-2'})
    
    #Names here
        team1_name = team1.find('a').text.lower()
        if ('lgd' in team1_name):
            team1_name = 'psg.lgd'
        
        team2_name = team2.find('a').text.lower()
        if ('lgd' in team2_name):
            team2_name = 'psg.lgd'
    
    #Region here
        team1_region = team1.find('div', attrs={'class': 'region'}).text.strip()
        team2_region = team2.find('div', attrs={'class': 'region'}).text.strip()
    
    #Remove commas from names to avoid issues when saving with numpy
        team1_name = team1_name.replace(',', '')
        team2_name = team2_name.replace(',', '')
        team1_region = team1_region.replace(',', '')
        team2_region = team2_region.replace(',', '')
    
    #Result
        variable1 = soup.find('div', attrs={'id':'gosubetSpoiler'}).text.strip()
        winner = variable1.replace('Winner: ', '')
    
    #Series
    
    #Score
        if (winner == 'Draw'):
            team1_score= 1
            team2_score= 1
        elif (team1_name == 'psg.lgd' and winner == 'PSG.LGD'): 
            team1_score= 1
            team2_score= 0
        elif (team1_name != 'psg.lgd' and winner == 'PSG.LGD'):
            team1_score= 0
            team2_score= 1
        elif (team1_name == 'psg.lgd' and winner != 'PSG.LGD'):
            team1_score= 0
            team2_score= 1
        elif (team1_name != 'psg.lgd' and winner != 'PSG.LGD'):
            team1_score= 1
            team2_score= 0
        
    #Bets
        gosubet = soup.find('section', attrs={'class':"module gosubet row"})
        team1_mod = gosubet.find('li', attrs={'class':'team team-1'})
        team2_mod = gosubet.find('li', attrs={'class':'team team-2'})
        team1_bet = team1_mod.find('small').text
        team2_bet = team2_mod.find('small').text
    
#    Draw scenario
        teamdraw_mod = gosubet.find('li', attrs={'class':'team draw'})
        try:
            teamdraw_bet = teamdraw_mod.find('small').text
        except Exception as e:
            teamdraw_bet = '0'
        
#    Date
        datetext = board.find('small').text.strip()
        datefor = datetext[:-8]
        datedef = datetime.datetime.strptime(datefor, "%b %d, %Y, %H:%M")
        datestring = datedef.strftime('%d/%m/%Y')
    
        count = count +1
    
        print('Winner: '+ winner)
        print(team1_name + ' ' + str(team1_bet) + ':' + str(team2_bet) + ' ' + team2_name + str(teamdraw_bet))
        print(count)
        
        team1_list.append(team1_name)
        team2_list.append(team2_name)
        team1_score_list.append(team1_score)
        team2_score_list.append(team2_score)
        team1_regionlist.append(team1_region)
        team2_regionlist.append(team2_region)
        team1_betlist.append(team1_bet)
        team2_betlist.append(team2_bet)
        draw_betlist.append(teamdraw_bet)
        match_datelist.append(datestring)
        
        
    except Exception as e:
        team1_name='error'
        team2_name='error'
        team1_score='error'
        team2_score='error'
        team1_region='error'
        team2_region='error'
        team1_bet=0
        team2_bet=0
        teamdraw_bet=0
        datestring='error'
    
        team1_list.append(team1_name)
        team2_list.append(team2_name)
        team1_score_list.append(team1_score)
        team2_score_list.append(team2_score)
        team1_regionlist.append(team1_region)
        team2_regionlist.append(team2_region)
        team1_betlist.append(team1_bet)
        team2_betlist.append(team2_bet)
        draw_betlist.append(teamdraw_bet)
        match_datelist.append(datestring)
    time.sleep(3)
        
    
    
np.savetxt('PSG.csv', [team1_list, team2_list, team1_score_list, team2_score_list, team1_regionlist, team2_regionlist, team1_betlist, team2_betlist, draw_betlist, match_datelist], delimiter=',', fmt='%s')


        