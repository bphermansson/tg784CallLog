#!/usr/bin/env python

# http://jeanphix.me/Ghost.py/

url = "http://192.168.1.254/info.lp?be=0&l0=3&l1=5&no"

import ghost

g = ghost.Ghost()
with g.start() as session:
    session.wait_timeout = 999

    page, extra_resources = session.open(url)
    if page.http_status == 200:
      print page