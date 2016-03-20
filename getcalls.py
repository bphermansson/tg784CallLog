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
      html = response.read() 
      soup = BeautifulSoup(html)
      span = soup.findAll('span', {'class':'hit-name-ellipsis'})
      name = span[0].text
      fullname = name.strip()
      #fullnameenc = fullname.encode(sys.stdout.encoding, 'replace')
      fullnameenc = fullname.encode('utf8', 'replace')
      #print "Full name: " + fullnameenc
      return fullnameenc
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
      html = response.read()
      soup = BeautifulSoup(html)
      table = soup.find('form', {'name': 'voip_call_log'})
      for row in table.findAll("tr"):
	for img in row.select('img'):
	  imgsrc = img.get('src')
	  # Type of called are identified by different images
	  # Here we look for incoming answered and missed calls
	  if (imgsrc=="/images/inco__md.gif" or imgsrc=="/images/miss__md.gif"):
	    # Find numbers
	    for btn in row.select('input[type="button"]'):
	      number=btn.get('value')	# Get value from buttons == phone number
	    # Find timestamp. Finds  all td:s in current row. 
	    # Then td[0] (first td in row) is the timestamp
	    td = row.findAll("td")
	    """
	    Calls are listed twice, both for phone line 1 and phone line 2
	    Just list the calls on line 1. It is identified by "Telefon 1" in the
	    7:th td.
	    """
	    phoneline = td[6].get_text()
	    if (phoneline == "Telefon 1"):
	      # Get timestamp and decode it
	      ts = td[0].get_text().encode('utf8', 'replace')
	      # Split date and time
	      datetime = ts.split("T")
	      date = datetime[0]
	      #print date
	      time = datetime[1]
	      #print time
	      #print val
	      if (imgsrc=="/images/inco__md.gif"):
		status = "Besvarat"
	      else:
		status = "Missat"
	      # Check owner of number
	      name = lookup(number)

	      print date + " @ " + time + " _ " + name + "(" + number + ")" + " (" + status + ")"
	      
	
  sys.exit()

if __name__ == "__main__":
    main()

