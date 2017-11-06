#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
from collections import Counter
from collections import defaultdict

## Create a function to find out what and how many tags in the data 
# Iterative parsing
def count_tags(filename):
    tag_li=[]
    for _, ele in ET.iterparse(filename, events=('start',)):
        tag_li.append(ele.tag)
    
    return dict(Counter(tag_li))

## Explore the data to see if there are tags that fit the following four categories: lower, lower_colon, problemchars and others
lower = re.compile(r'^([a-z]|_)*$') # For tags that contain only lowercase letters and are valid
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$') # For otherwise valid tags with a colon in their names
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')  # For tags with problematic characters

def key_type(element, keys):
    if element.tag == "tag":
        if re.search(lower, element.attrib.get('k')):
            keys["lower"] += 1
        elif re.search(lower_colon, element.attrib.get('k')):
            keys["lower_colon"] += 1
        elif re.search(problemchars, element.attrib.get('k')):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1  #  "other", for other tags that do not fall into the other three categories
        
    return keys      

def process_map_key(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys
    
## Audit street names
street_type_ascii = re.compile(r'\w+') # For street names that are standard strings
street_type_unicode=re.compile(ur'\w+', re.UNICODE)  # For street names coded with Unicode
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE) # For street names containing abbreviation signs

def audit_street_type(street_types, street_name):
    m = street_type_ascii.search(street_name)
    n = street_type_unicode.search(street_name)
    u = street_type_re.search(street_name)
    # Match street names coded with ASCII
    if m:
        street_type = m.group()
        street_types[street_type].add(street_name)
    # Match street names coded with Unicode
    elif n:
        street_type = n.group()
        street_types[street_type].add(street_name)
    # Match street names containing abbreviation signs
    elif u:
        street_type = u.group()
        street_types['abbreviation'].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

## Audit postal codes
postCode_type_re = re.compile(r'^(\d{3})\s+(\d{2})$') # For postal codes written in the standard format: xxx xx

def audit_postCode_type(post_types, postCode):
    m = postCode_type_re.search(postCode)
    # Match postal codes written in the standard format
    if m:
        post_type = m.group()
        post_types[post_type].add(postCode)
    else:
        post_types['exclude'].add(postCode)  # For the rest of postal codes

def is_postCode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_postCode(osmfile):
    osm_file = open(osmfile, "r")
    post_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postCode(tag):
                    audit_postCode_type(post_types, tag.attrib['v'])
    osm_file.close()
    return post_types


osm_file='sample.osm'

## Get what and how many tags in the file
tags=count_tags(osm_file)
print 'Information for all the tags in the file:'
#pprint.pprint(tags)
print(tags)


## Check if there are any problematic tags in the file
keys = process_map_key(osm_file)
print 'Number of different tags in the file:'
pprint.pprint(keys)


## Audit street names in the file
street_types=audit_street(osm_file)
# Check if street names in the file had abbreviations 
if 'abbreviation' in dict(street_types):
    print True
else:
    print False
    print ': Abbreviations not found in the street names.'
#print 'Types of street names in the file:'
#pprint.pprint(dict(street_types))
  
    
## Check the types of postal code format in the file
post_types=audit_postCode(osm_file)
if 'exclude' in dict(post_types):
    print 'Incorrected/Unstandardized postal codes in the file:'
    #pprint.pprint(dict(post_types)['exclude'])
    print dict(post_types)['exclude']
