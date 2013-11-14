#!/usr/bin/env python

import json
import string
import sys
from collections import Counter

for line in sys.stdin:
  boilerplate = line.split('\t')[2].strip('""').replace('""','"')
  try:
    body = json.loads(boilerplate)['body'].lower()
    exclude = set(string.punctuation)
    body = ''.join(ch for ch in body if ch not in exclude)
    c = Counter(body.split())
    for k, num in c.iteritems():
      print "%s\t%d" % (k, num)
  except:
    pass
