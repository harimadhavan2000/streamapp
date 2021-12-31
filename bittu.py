import pandas as pd
import re
import math
from datetime import datetime
import matplotlib.pyplot as plt
import  numpy as np
import streamlit as st
df1 = pd.read_csv('zhavli.csv')

def conflict(tablex):  
    flag = 1
    arr = []
    for i in tablex:
        for j in list(filter(lambda x : x != i, tablex)):
            start1= i[1]*60 + i[2]
            end1= i[4]*60 + i[5]
            start2= j[1]*60 + j[2]
            end2= j[4]*60 + j[5]
            day1 = i[0]
            day2 = j[0]
            if ((start1 < end2) and (start2 < end1)) and (day1 == day2):
                flag = 0
                b_list = sorted([i[6], j[6]])
                arr.append(b_list)
    return flag, arr

def gethu(choices, dare = 0):
    df1 = pd.read_csv('zhavli.csv')
    tables = []
    
    for choice in choices:

        x = df1[df1['Course']==choice]
        d = x['Discussion Schedule']
        t = x['Tutorial Schedule']
        p = x['Practical Schedule']
        na = x['Course Name']        

        if(not pd.isna(na.values[0]) and not dare):
            st.write(choice + ' - ' + na.values[0])


        if(not pd.isna(d.values[0])):
            for item in d.values[0].split(' ,'):
                types = 'discussion'
                days = item.split('  ')[0]
                delx = item.split('  ')[1]
                start = delx.split('-')[0]
                end = delx.split('-')[1]
                for z in re.findall('[A-Z][^A-Z]*', days):
                    #print(z, start, end, types, choice)
                    tables.append([z, start, end, types, choice])
                
        if(not pd.isna(t.values[0])):
            for item in t.values[0].split(' ,'):
                types = 'tutorial'
                days = item.split(' ')[0]
                delx = item.split(' ')[1]
                start = delx.split('-')[0]
                end = delx.split('-')[1]
                for z in re.findall('[A-Z][^A-Z]*', days):
                    #print(z, start, end, types, choice)
                    tables.append([z, start, end, types, choice])
    
        if(not pd.isna(p.values[0])):
            for item in p.values[0].split(','):
                types = 'practical'
                days = item.split(' ')[0]
                delx = item.split(' ')[1]
                start = delx.split('-')[0]
                end = delx.split('-')[1]
                for z in re.findall('[A-Z][^A-Z]*', days):
                    #print(z, start, end, types, choice)
                    tables.append([z, start, end, types, choice])
    
    weeks = {
      "M": 1,
      "T": 2,
      "W": 3,
      "Th": 4,
      "F": 5
    }
    tablex = []
    for x in tables:
        h = x[1].split(':')
        h1 = float(h[0])
        h2 = float(h[1])
        m = x[2].split(':')
        m1 = float(m[0])
        m2 = float(m[1])
        delta = datetime.strptime(x[2], '%H:%M') - datetime.strptime(x[1], '%H:%M')
        delta = float(delta.seconds/60)
        #print(weeks[x[0]], h1, h2, delta,m1,m2, x[4], x[3])
        tablex.append([weeks[x[0]], h1, h2, delta,m1, m2,  x[4], x[3]])

    flag, arr = conflict(tablex)

    if(flag == 0):
        return arr
    
    
    rooms = ['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday']
    types = ['discussion', 'tutorial', 'practical']
    colors=['pink', 'lightgreen', 'lightblue', 'wheat', 'salmon']
     
    input_files=['data1.txt']
    day_labels=['Day 1']
    fig=plt.figure(figsize=(20,11.8))
     
       
    for data in tablex:
        event=data[-2]
        typez = data[-1]
        data=list(map(float, data[:-2]))
        room=data[0]-0.48
        start=data[1]+data[2]/60
        end=start+data[3]/60
        # plot event
        plt.fill_between([room, room+0.96], [start, start], [end,end], color=colors[types.index(typez)], edgecolor='k', linewidth=1)
        # plot beginning time
        plt.text(room+0.02, start+0.05 ,'{0}:{1:0>2}-{2}:{3:0>2}'.format(int(data[1]),int(data[2]),int(data[4]),int(data[5])), va='top', fontsize=10)
        # plot event name
        plt.text(room+0.48, (start+end)*0.5, event, ha='center', va='center', fontsize=14)
     
         # Set Axis
    ax=fig.gca()
    ax.yaxis.grid()
    ax.set_xlim(0.5,len(rooms)+0.5)
    ax.set_ylim(20.1, 7.9)
    ax.set_xticks(range(1,len(rooms)+1))
    ax.set_xticklabels(rooms)
    ax.set_ylabel('Time')
     
         # Set Second Axis
    ax2=ax.twiny().twinx()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_ylim(ax.get_ylim())
    ax2.set_xticks(ax.get_xticks())
    ax2.set_xticklabels(rooms)
    ax2.set_ylabel('Time')
     
     
    plt.title('Time Table',y=1.07)
    return fig

def getho(choices):
    arr = np.random.normal(1, 1, size=100)
    fig, ax = plt.subplots()
    ax.hist(arr, bins=20)
    return fig    

    
