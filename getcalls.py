#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Get call log from a Thomson TG784 router

# This page contains call info
# http://192.168.1.254/cgi/b/_stats_/stats/?be=0&l0=3&l1=5

# BeautifulSoup is used to parse Html
#apt-get install python-bs4

# About BeautifulSoup: https://automatetheboringstuff.com/chapter11/
#

import urllib2, sys
from bs4 import BeautifulSoup

def lookup(number):
  #print number
  if (number!="null"):
    req = "http://www.hitta.se/s%C3%B6k?vad="+number
    req="http://personer.eniro.se/resultat/"+number
    #print req
    try:
      response = urllib2.urlopen(req)
    except HTTPError as e:
      print 'The server couldn\'t fulfill the request.'
      print 'Error code: ', e.code
    except URLError as e:
      print 'We failed to reach a server.'
      print 'Reason: ', e.reason
    else:
      #print "Checking number"
      html = response.read()
      #print html
      soup = BeautifulSoup(html)
      span = soup.findAll('span', {'class':'hit-name-ellipsis'})
      name = span[0].text
      fullname = name.strip()
      fullname = fullname.encode(sys.stdout.encoding, 'replace')
      #print "Full name: " + fullname
      return fullname
       
  else:
    print "No number to look up"
  
def main():
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
      
      # Incoming call indicated by image "/images/inco__md.gif, miss__md.gif" 
      btns = soup.findAll('img', {'src': ['/images/inco__md.gif', '/images/miss__md.gif', '/images/outg__md.gif']})
      #print btns
      #print btns['src']
      numberList=[]
      timeList=[]
      numbers = len(btns)
      #print "There are " + str(numbers) + " numbers."

      # Find values in column Port
      phonetds = soup.select('td[colspan="3"]')
      
      # Find timestamps
      timestamps = soup.findAll('td', {'width': '14%'})
      #print timestamps
      
      for i in xrange(0,numbers,1):
	elems = soup.select('input[type="button"]')[i]
	#print elems
	#print i
	val=elems.get('value')	# Get value from buttons
	btnsrc = btns[i]['src'] # Get src from image row
	if (btnsrc == "/images/inco__md.gif" or btnsrc == "/images/miss__md.gif"):
	  # Port tds start at td number 4
	  phone1 = phonetds[i+4].getText()
	  if (phone1 == "Telefon 1"):
	    #print phone1
	    #print "Elems:" + str(i) + "-" + val + "-" + btnsrc
	    timestamp = timestamps[i+1].getText()
	    timeList.append(timestamp)
	    numberList.append(val)

      #print "There are " + str(len(numberList)) + " valid numbers"
      
      # Print out the results
      numbersCount=len(timeList)
      #print "Numbers=" + str(numbersCount)
      if (numbersCount!=0):
	x=0
	for i in numberList:
	  datetime = timeList[x].split('T')
	  date = datetime[0]
	  time = datetime[1]
	  # Check who owns the number
	  fullname = lookup(i)
	  alldata = fullname + "/" + i + "/" + date.encode() + "/" + time.encode()
	  print alldata
#	  print i + "(" + fullname + ")" + " called @ " + time +", " + date
	  #print date + ":" + time + "-" + i + "-" + lookup(i)
	  x+=1
      else:
	print ("No numbers in call log")
	lookup("null")


  sys.exit()

if __name__ == "__main__":
    main()

