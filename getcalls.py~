#!/usr/bin/env python
# Get call log from a Thomson TG784 router

# This page contains call info
# http://192.168.1.254/cgi/b/_stats_/stats/?be=0&l0=3&l1=5

# BeautifulSoup is used to parse Html
#apt-get install python-bs4

# About BeautifulSoup: https://automatetheboringstuff.com/chapter11/
#

import urllib2, sys
from bs4 import BeautifulSoup

# Check if there are missed calls
req = "http://192.168.1.254/cgi/b/_stats_/stats/?be=0&l0=3&l1=5"
try:
    response = urllib2.urlopen(req)
except HTTPError as e:
    print 'The server couldn\'t fulfill the request.'
    print 'Error code: ', e.code
except URLError as e:
    print 'We failed to reach a server.'
    print 'Reason: ', e.reason
else:
    #print "Ok, got data from router"
    html = response.read()
    #print html
    soup = BeautifulSoup(html)
    table = soup.find("table", "edittable")  
    secondtable = soup.findAll('table', "edittable")[1]
    btns = soup.findAll('input', {'type': 'button'})
    numbers = len(btns)
    #print "There are " + str(numbers) + " numbers."
    
    # Every number is listed twice, just show one of them by looping with two steps
    numberList=[]
    for i in xrange(0,numbers,2):
      elems = soup.select('input[type="button"]')[i]
      #print elems.get('value')
      numberList.append(elems.get('value'))
    #print "There are " + str(i) + " numbers."
        
    # Find times
    timeList=[]
    timestamps = soup.findAll('td', {'width': '14%'})
    #print timestamps
    ts = len(timestamps)
    #print "There are " + str(ts) + " timestamps"
    
    elems = soup.select('td[width="14%"]')
    # Here we find 8 lines if there are 2 numbers. We want line #1, #5, #9 etc
    for i in xrange(1,ts,4):
      #print i
      #print elems[i].getText()
      timeList.append(elems[i].getText())
    #print elems.get('text')
    
    #print len(numberList)
    #print len(timeList)

    # Print oput the results
    x=0
    for i in numberList:
      datetime = timeList[x].split('T')
      date = datetime[0]
      time = datetime[1]
      print i + " called @ " + time +", " + date
      
      
      
      x=+1
    
sys.exit()

