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
    
    # Find number of missed calls
    table = soup.find("table", "edittable")  
    #print table
    # The rightmost column contains the total of calls and is the only one using 'colspan="3"'
    elems = soup.select('td[colspan="3"]')
    # The number of missed calls are on line 1 (note, we start at line 0)
    #print "Missed calls: " + elems[1].string
    
    # Find incoming calls/numbers
    # This is done by finding the buttons where the numbers are presented. 
    # Aint no good as this also fetches outgoing calls. 
    secondtable = soup.findAll('table', "edittable")[1]
    #btns = soup.findAll('input', {'type': 'button'})
    #btns=soup.findAll('img')
    # Incoming call indicated by image "/images/inco__md.gif" 
    
    btns = soup.findAll('img', {'src': ['/images/inco__md.gif']})

    #c=0
    numberList=[]
    #for x in btns:
    #  imgName = soup.findAll('img')[c].get('src')
    #  if imgName == "/images/outg__md.gif":
    #	numberlist[c]=  
    #	c+=1
    numbers = len(btns)
    #print "There are " + str(numbers) + " numbers."
    
    # Every number is listed twice, just show one of them by looping with two steps
    for i in xrange(0,numbers,1):
      elems = soup.select('input[type="button"]')[i]
      #print elems.get('value')
      numberList.append(elems.get('value'))
    #print "'i' is " + str(i)
        
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

    # Print out the results
    numbersCount=len(timeList)
    #print "Numbers=" + str(numbersCount)
    if (numbersCount!=0):
      x=0
      for i in numberList:
	datetime = timeList[x].split('T')
	date = datetime[0]
	time = datetime[1]
	#print i + " called @ " + time +", " + date
	#Clean output
	print i + ":" + date + ":" + time
	x+=1
    else:
      print ("No numbers in call log")


sys.exit()

