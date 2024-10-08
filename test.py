"""
Cpts 415 gorup project

Amazon product reccomendation system

This file is used to parse the data from the original data file.
"""

import re
import gzip
from tqdm import tqdm
from utils import get_line_number

def parse(filename, total):
  IGNORE_FIELDS = ['Total items', 'reviews']
  f = gzip.open(filename, 'r')
  entry = {}
  categories = []
  reviews = []
  similar_items = []
  
  for line in tqdm(f, total=total):
    line = line.strip()
    colonPos = line.find(':')

    if line.startswith("Id"):
      if reviews:
        entry["reviews"] = reviews
      if categories:
        entry["categories"] = categories
      yield entry
      entry = {}
      categories = []
      reviews = []
      rest = line[colonPos+2:]
      entry["id"] = unicode(rest.strip(), errors='ignore')
      
    elif line.startswith("similar"):
      similar_items = line.split()[2:]
      entry['similar_items'] = similar_items

    # "cutomer" is typo of "customer" in original data
    elif line.find("cutomer:") != -1:
      review_info = line.split()
      reviews.append({'customer_id': review_info[2], 
                      'rating': int(review_info[4]), 
                      'votes': int(review_info[6]), 
                      'helpful': int(review_info[8])})

    elif line.startswith("|"):
      categories.append(line)

    elif colonPos != -1:
      eName = line[:colonPos]
      rest = line[colonPos+2:]

      if not eName in IGNORE_FIELDS:
        entry[eName] = unicode(rest.strip(), errors='ignore')

  if reviews:
    entry["reviews"] = reviews
  if categories:
    entry["categories"] = categories
    
  yield entry


if __name__ == '__main__':
  file_path = "sample.txt"

  import simplejson

  line_num = get_line_number(file_path)

  for e in parse(file_path, total=line_num):
    if e:
      print(simplejson.dumps(e))
