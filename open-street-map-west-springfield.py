
# coding: utf-8

# # Project Overview
# You will choose any area of the world in https://www.openstreetmap.org and use data munging techniques, such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity, to clean the OpenStreetMap data for a part of the world that you care about. Finally, you will choose either MongoDB or SQL as the data schema to complete your project.
# 
# ## Approach
# This project involves cleaning data.  It will look at ways and nodes and make the data more uniform.  Here's the big picture:
# 
# 1. Create a smaller file to test
# 2. Clean the data (need to expand here)
#  1. Check for problem characters in each tag
#  2. Clean up street names
# 3. Convert from xml to csv
# 4. Import the cleaned .csv into a SQL database
# 5. Explore the database through queries
# 6. Document
# 
# ### Cleaning
# What do you do when you find you need to clean the data?  Should you modify the osm?  Handle it right there?  Handle it further down?  Figure out what they want you to do to clean the data.
# 
# Once you know what they want you to do with any 'dirty' data, do it.  I think every step after that is already completed.
# 
# ## What will I learn?
# After completing the project, you will be able to:
# 
# Assess the quality of the data for validity, accuracy, completeness, consistency and uniformity.
# Parsing and gather data from popular file formats such as .json, .xml, .csv, .html
# Process data from many files and very large files that can be cleaned with spreadsheet programs
# Learn how to store, query, and aggregate data using MongoDB or SQL
# ## Why this Project?
# What’s so hard about retrieving data from databases or various files formats? You grab some data from this file and that database, clean it up, merge it, and then feed it into your state of the art, deep learning algorithm … Right?
# 
# But the reality is this -- anyone who has worked with data extensively knows it is an absolute nightmare to get data from different data sources to play well with each other.
# 
# And this project will teach you all of the skills you need to deal with even the most nightmarish data wrangling scenarios.
# 
# ## Why is this Important to my Career?
# As this New York Times article points out, the less heralded part of doing data science is manually collecting and cleaning data so it can be easily explored and analyzed later. Or otherwise known as “data wrangling” or “data munging” in the data science community.
# 
# Though not as glamorous as building cool machine learning models, data wrangling is a task that data scientists can spend up to 50-80% of their time doing according to many practicing data analyst and data scientists.
# 
# ## To Prepare for the Project
# Step 1: Complete the Data Wrangling Course.
# 
# Step 2: Choose between MongoDB and SQL and complete the associated course
# 
# For MongoDB, prepare for this project with: MongoDB For Data Analysis.
# 
# For SQL, prepare for this project with: SQL for Data Analysis.
# 
# ### Note
# If you have successfully completed the project for the Data Wrangling with MongoDB course in the past (which entails having graduated from the course and having access to your course certificate), simply email us at dataanalyst-project@udacity.com with your passing evaluation and we'll give you credit for this project.

# # Project Details
# This project is connected to the Data Wrangling course. You have the choice between two databases for this project: SQL and MongoDB. For an explanation of the differences between these two databases, see this node. There are separate instructions where relevant below for each database choice.
# 
# Here's what you should do:
# 
# ## Step One - Complete Programming Exercises
# Make sure all programming exercises are solved correctly in the "Case Study: OpenStreetMap Data" Lesson in the course you have chosen (MongoDB or SQL). This is the last lesson in that section.
# 
# ## Step Two - Review the Rubric and Sample Project
# The Project Rubric. will be used to evaluate your project. It will need to Meet Specifications for all the criteria listed. Here are examples of what your final report could look like:
# 
# SQL Sample Project
# 
# MongoDB Sample Project
# 
# ## Step Three - Choose Your Map Area
# Choose any area of the world from https://www.openstreetmap.org, and download a XML OSM dataset. The dataset should be at least 50MB in size (uncompressed). We recommend using one of following methods of downloading a dataset:
# 
# - Download a preselected metro area from Map Zen.
# - Use the Overpass API to download a custom square area. Explanation of the syntax can found in the wiki. In general you will want to use the following query:(node(minimum_latitude, minimum_longitude, maximum_latitude, maximum_longitude);<;);out meta; e.g. (node(51.249,7.148,51.251,7.152);<;);out meta; the meta option is included so the elements contain timestamp and user information. You can use the Open Street Map Export Tool to find the coordinates of your bounding box. Note: You will not be able to use the Export Tool to actually download the data, the area required for this project is too large.
# 
# ## Step Four - Process your Dataset
# It is recommended that you start with the problem sets in your chosen course and modify them to suit your chosen data set. As you unravel the data, take note of problems encountered along the way as well as issues with the dataset. You are going to need these when you write your project report.
# 
# Hint: You may want to start out by looking at a smaller sample of your region first when auditing it to make it easier to iterate on your investigation. See code in the notes below for how to do this.
# 
# ### SQL
# Thoroughly audit and clean your dataset, converting it from XML to CSV format. Then import the cleaned .csv files into a SQL database using this schema or a custom schema of your choice.
# 
# ## Step Five - Explore your Database
# After building your local database you’ll explore your data by running queries. Make sure to document these queries and their results in the submission document described below. See the Project Rubric for more information about query expectations.
# 
# ## Step Six - Document your Work
# Create a document (pdf, html) that directly addresses the following sections from the Project Rubric.
# 
# - Problems encountered in your map
# - Overview of the Data
# - Other ideas about the datasets
# 
# Try to include snippets of code and problematic tags (see MongoDB Sample Project or SQL Sample Project) and visualizations in your report if they are applicable.
# Use the following code to take a systematic sample of elements from your original OSM region. Try changing the value of k so that your resulting SAMPLE_FILE ends up at different sizes. When starting out, try using a larger k, then move on to an intermediate k before processing your whole dataset.

# In[1]:

# This block creates a smaller file size to work with
# This block was taken directly from the udacity assignment description page
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "ex_w76EfPgoM8PsPLbMqJ93rbViRM5yT.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample.osm"

k = 7 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')


# In[ ]:

# This block will get all users that have worked on the project
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")

To get all the uid's you will need to go through all of tags.  Way tags
have a uid as do relations and nodes.


"""

def get_user(element):
    if element.tag == 'node' or element.tag == 'way' or element.tag == 'relation':
        id = element.attrib['uid']
        return id


def process_map(filename):
    users = set()
    
    # This parses through all elements and that's why there are nulls.  It checks whether it has a uid only after getting to the function, so it's possible to have a nonetype there
    for _, element in ET.iterparse(filename):
        if get_user(element):
            users.add(get_user(element))

    return users


def test():

    users = process_map('sample.osm')
    pprint.pprint(users)
    #assert len(users) == 6



if __name__ == "__main__":
    test()


# In[ ]:

# This block will grab all of the tags from the file
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    
    # Tag name is key, number of times encountered is value
    # 
    tag_dictionary = {}
    #tree = ET.parse(filename)
    #root = tree.getroot()
    for _, element in ET.iterparse(filename):
        #print element.tag
        if element.tag in tag_dictionary:
            tag_dictionary[element.tag] += 1
        else:
            tag_dictionary[element.tag] = 1
    return tag_dictionary
        # YOUR CODE HERE


def test():

    tags = count_tags('sample.osm')
    pprint.pprint(tags)
    '''assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    '''

if __name__ == "__main__":
    test()


# In[ ]:

## This block will check for problem characters in tags
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into your database, you should check the
"k" value for each "<tag>" and see if there are any potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data
model and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with
problematic characters.

Please complete the function 'key_type', such that we have a count of each of
four tag categories in a dictionary:
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
See the 'process_map' and 'test' functions for examples of the expected format.
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):

    # Checks whether the element passed is a 'tag' tag
    if element.tag == "tag":
        
        # Finds and assigns the 'k' value of the tag
        attribute = element.attrib['k']
        #print attribute
                
        # Checks whether the attribute is lowercase, has a colon is a problem character or other category
        if is_lower(attribute):
            keys['lower'] += 1
        elif is_lower_colon(attribute):
            keys['lower_colon'] += 1
        elif is_problem_char(attribute):
            keys['problemchars'] += 1
        else:
            print attribute
            keys['other'] += 1
                
    return keys

# Checks whether an attribute is lowercase
def is_lower(attribute):
    m = lower.search(attribute)
    return m

# Checks whether an attribute has a colon in the name
def is_lower_colon(attribute):
    m = lower_colon.search(attribute)
    return m

# Checks whether there are problem characters present
def is_problem_char(attribute):
    m = problemchars.search(attribute)
    return m

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    
    # This iterates through the file, so you shouldn't have to go line by line in the key_type function
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
        
    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('sample.osm')
    pprint.pprint(keys)
    #assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()


# In[ ]:

# This block will print a list of street codes (avenue, street, road, etc)

from collections import defaultdict
OSMFILE = "ex_w76EfPgoM8PsPLbMqJ93rbViRM5yT.osm"

# checks whether a given element is a street name
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_name(elem):
    return (elem.attrib['k'] == 'name')

def is_highway(elem):
    if (elem.attrib['k'] == 'highway') and (elem.attrib['v'] != 'bus_stop'):
        return True
    else:
        return False

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
    
# This saves the street types to a set
def audit(osmfile):
    street_names = set()
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "way":
            is_hw = False
            for tag in elem.iter("tag"):
                #m = re.search('Beverly', tag.attrib['v'])
                #if m:
                    #print tag.attrib['v']
                    #print tag.attrib['k']
                if is_highway(tag):
                    is_hw = True
            if is_hw:
                for tag in elem.iter("tag"):
                    if is_name(tag):
                        audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    pprint.pprint(dict(street_types))
    return street_types

audit(OSMFILE)


# In[23]:

# This block will audit tags to look for patterns
# This will also help develop a mapping to clean up any bad data
# before inserting them into the database
"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "ex_w76EfPgoM8PsPLbMqJ93rbViRM5yT.osm"

# This finds the last word in the address ($ matches at the end of the string instead of the beginning)
street_type_re = re.compile(r'\b(\w+)\s*$', re.IGNORECASE)
address_type_re = re.compile(r'\b(\w+)\s*$')
area_code_re = re.compile(r'...')
post_code_re = re.compile(r'.....')

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Slope", "Circle", "Terrace", "Center"]

highway_types = set()

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St ": "Street",
            "St  ": "Street",
            "St.": "Street",
            "ST": "STREET",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Dr  ": "Drive",
            "Dr ": "Drive",
            "Dr": "Drive"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
def audit_address_type(address_types, address_name):
    addy = address_name.split(',')[0]
    m = address_type_re.search(addy)
    if m:
        address_type = m.group()
        address_types[address_type].add(address_name)
        #if address_type not in expected_addresses:
            #address_types[address_type].add(address_name)

def audit_phone_number(area_codes, phone_number):
    m = area_code_re.search(phone_number)
    if m:
        area_code = m.group()
        area_codes[area_code].add(phone_number)

def audit_post_code(post_codes, post_code):
    m = post_code_re.search(post_code)
    if m:
        postcode = m.group()
        post_codes[postcode].add(post_code)
        
def is_phone(elem):
    return (elem.attrib['k'] == 'phone')
        
def is_address(elem):
    return (elem.attrib['k'] == 'address')
            
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_name(elem):
    return (elem.attrib['k'] == 'name')

def is_highway(elem):
    if (elem.attrib['k'] == 'highway') and (elem.attrib['v'] != 'bus_stop'):
        return True
    else:
        return False

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    address_types = defaultdict(set)
    area_codes = defaultdict(set)
    post_codes = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "way":
            
            is_hw = False
            for tag in elem.iter("tag"):
                
                # Clean up 'address' tags
                if is_address(tag):
                    if has_double_zero(tag):
                        audit_address_type(address_types, tag.attrib['v'])
                
                # Clean up 'phone' tags
                elif is_phone(tag):
                    audit_phone_number(area_codes, tag.attrib['v'])
                
                # Clean up 'name' tags.  If a highway tag is present, we know it's a street
                elif is_highway(tag):
                    is_hw = True
                    highway_types.add(tag.attrib['v'])
                    
                # Checks if it's an 'addr:postcode' tag
                elif is_post_code(tag):
                    audit_post_code(post_codes, tag.attrib['v'])
                
                # If we know it's a street, we want to get to the highway tag
                '''if is_hw:
                    for tag in elem.iter("tag"):
                        
                        # Ways street names are on the name line
                        if is_name(tag):
                            audit_street_type(street_types, tag.attrib['v'])
                            break
                '''
                            
        elif elem.tag == "node":
            for tag in elem.iter("tag"):
                
                # Clean up 'name' tags
                # If there's a highway tag present, we want to go back and get the name
                if is_highway(tag):
                    is_hw = True
                    
                    # Loops back through tag lines looking for 'name' tag
                    for tag in elem.iter("tag"):
                        if is_name(tag):
                            audit_street_type(street_types, tag.attrib['v'])
                
                # Node street names are on the addr:street line
                elif is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                    
                # Clean up 'phone' tags
                elif is_phone(tag):
                    audit_phone_number(area_codes, tag.attrib['v'])
                    
                # Clean up 'address' tags
                # Checks to see if it's an 'address' tag
                elif is_address(tag):
                    
                    # If it is an address tag, check if it has 00 for a zip
                    if has_double_zero(tag):
                        audit_address_type(address_types, tag.attrib['v'])
                        
                # Checks if it's an 'addr:postcode' tag
                elif is_post_code(tag):
                    audit_post_code(post_codes, tag.attrib['v'])
                
    osm_file.close()
    #print street_types
    #print highway_types
    
    print "Post Codes:"
    pprint.pprint(dict(post_codes))
    
    print "Street Types:"
    pprint.pprint(dict(street_types))
    
    print "Area Codes:"
    pprint.pprint(dict(area_codes))
    
    print "Bad Zip Codes"
    pprint.pprint(dict(address_types))
    return street_types

# Checks whether a given element is a postal code
def is_post_code(elem):
    #return ('post' in elem.attrib['k'])
    return (elem.attrib['k'] == "addr:postcode")

def has_double_zero(elem):
    address = elem.attrib['v']
    m = re.search('\d\d\d\d\d$', address)
    return not m

# This should look at the name and replace any street abbreviations with the appropriate mapping
def update_name(name, mapping):
    
    updated_name = name
    
    split_name = re.split(' ', name)
    for nm in split_name:
        if nm in mapping:
            updated_name = re.sub(nm, mapping[nm], updated_name)
            
    #street_type = re.search(r'\b(\w+)\s*$', name)
    #print "Street type is: " + street_type.group()
    #st_type = street_type.group()
    
    #if st_type in mapping:
        #updated_name = re.sub(r'\b(\w+)\s*$', mapping[st_type], name)
    
    return updated_name

# This will look at the complete address, pull the street address and replace any street abbreviations with the appropriate mapping
def update_address(address, mapping):
    
    updated_address = address
    
    # Gets the street address
    addy = address.split(',')[0]
    
    # Splits the street address up by spaces
    split_addy = re.split(' ', addy)
    
    # Loops through the parts of the street address
    for ad in split_addy:
        
        # If it finds an abbreviation, it replaces it
        if ad in mapping:
            updated_address = re.sub(ad, mapping[ad], updated_address)
    
    
    
    

def test():
    st_types = audit(OSMFILE)
    #assert len(st_types) == 3
    #pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            #print name, "=>", better_name
            if name == "West Lexington St.":
                assert better_name == "West Lexington Street"
            if name == "Baldwin Rd.":
                assert better_name == "Baldwin Road"


if __name__ == '__main__':
    test()


# In[ ]:

address = '31 Springfield Street, Chicopee MA 00'
m = re.search('00$', address)
print m.group()



# In[ ]:

address = '91 East Mountain Rd, Westfield, MA'

# Gets the street address part
addy = address.split(',')[0]

# This gets the street type
address_type_re = re.compile(r'\b(\w+)\s*$')

# Creates a list of address types
address_types = defaultdict(set)

def audit_address_type(address_types, address_name):
    
    # Gets the street type
    m = address_type_re.search(addy)
    if m:
        address_type = m.group()
        # Prints the street type
        print address_type
    address_types[address_type].add(address_name)

#add_types = audit()
audit_address_type(address_types, address)


# In[113]:

## This code will create dictionaries from all nodes and ways tags
## I completed most of the processing but I did borrow one small portion from a github user.
## The code I borrowed was:
'''
        node_attribs['id'] = temp_node_attribs['id']
        node_attribs['lat'] = temp_node_attribs['lat']
        node_attribs['lon'] = temp_node_attribs['lon']
        node_attribs['user'] = temp_node_attribs['user']
        node_attribs['uid'] = temp_node_attribs['uid']
        node_attribs['version'] = temp_node_attribs['version']
        node_attribs['changeset'] = temp_node_attribs['changeset']
        node_attribs['timestamp'] = temp_node_attribs['timestamp']
'''
## !/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

OSM_PATH = "ex_w76EfPgoM8PsPLbMqJ93rbViRM5yT.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Slope", "Circle", "Terrace", "Center"]

# UPDATE THIS VARIABLE
mapping = { # These street types are abbreviations
            "St": "Street",
            "St ": "Street",
            "St  ": "Street",
            "St.": "Street",
            "ST": "STREET",
            "Rd": "Road",
            "Rd.": "Road",
            "Ave": "Avenue",
            "Dr  ": "Drive",
            "Dr ": "Drive",
            "Dr": "Drive",
            "Dr.": "Drive",
           
           # These addresses are missing street types
            "36 Margaret, Springfield MA 01105": "36 Margaret Street, Springfield MA 01105",
            "118 Riverdale, West Springfield MA 01089": "118 Riverdale Street, West Springfield MA 01089",
            "587 Grattan, Chicopee MA 01020": "587 Grattan Street, Chicopee MA 01020",
            "63 South, Chicopee MA 01013": "63 South Street, Chicopee MA 01013",
           
           # These addresses hav incorrect zip code info
            '165 Front Street, Chicopee MA 01014-0368': "165 Front Street, Chicopee, MA 01013",
            '200 Park Street, West Springfield MA 00': "200 Park Street, West Springfield, MA 01089",
            '220 State Street, Springfield MA 00': "220 State Street, Springfield, MA 01103",
            '271 Carew Street, Springfield MA 00': "271 Carew Street, Springfield, MA 01104",
            '271 Carew Street, Springfield, MA': "271 Carew Street, Springfield, MA 01104",
            '291 Springfield Street, Chicopee MA 00': "291 Springfield Street, Chicopee, MA 01013",
            '31 Springfield Street, Chicopee MA 00': "13 Center Street, Chicopee, MA 01013", #Matched by GPS data
            '50 State Street, Springfield MA 00': "50 State Street, Springfield, MA 01103",
            '516 Carew Street, Springfield, MA': "516 Carew Street, Springfield, MA 01104",
            '65 Elliot Street, Springfield MA 00': "65 Elliot Street, Springfield, MA 01105",
            '759 Chestnut Street, Springfield, MA': "759 Chestnut Street, Springfield, MA 01199",
            '1233 Main St, Holyoke, MA': "1233 Main Street, Holyoke, MA 01040",
            '1 Armory Square, Springfield MA 00': "1 Armory Street, Springfield, MA 01105", # Armory Square is improper, need Armory Street
            '91 East Mountain Rd, Westfield, MA': "91 East Mountain Road, Westfield, MA 01085",
            '32 Ridgewood Place, Springfield MA 01105-1315': "32 Ridgewood Place, Springfield, MA 01105",
            '1150 West Columbus Avenue, Springfield MA 00': "1150 West Columbus Avenue, Springfield, MA 01105"
            
            }

street_types = defaultdict(set)

def shape_element(element):
    """Clean and shape node or way XML element to Python dict"""
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # YOUR CODE HERE
    if element.tag == 'node':
        
        # Create a temporary dictionary from the xml element and make 
        # the node_attribs dictionary:
        
        temp_node_attribs = element.attrib

        node_attribs['id'] = temp_node_attribs['id']
        node_attribs['lat'] = temp_node_attribs['lat']
        node_attribs['lon'] = temp_node_attribs['lon']
        node_attribs['user'] = temp_node_attribs['user']
        node_attribs['uid'] = temp_node_attribs['uid']
        node_attribs['version'] = temp_node_attribs['version']
        node_attribs['changeset'] = temp_node_attribs['changeset']
        node_attribs['timestamp'] = temp_node_attribs['timestamp']
                
        ''' 
        Sometimes, there are tags nested inside node tags.  Need a way 
        to try to access these.  If it's a node tag, 
        immediately check if there are tags nested within
        
        Check the solution from getting author email addys
        '''
        
        
        # Need to capture any node tags
        for tag in element.iter("tag"):
            node_tag = {}
            node_tag['id'] = node_attribs['id']
            node_tag['value'] = tag.attrib['v']
            key_plus_type = tag.attrib['k']
            
            # If there are problem characters, don't add to node tags
            if is_problem_char(key_plus_type):
                print key_plus_type
                continue              
            
            # If there are colons, need to split up to get key
            elif is_lower_colon(key_plus_type):
                k_t_split = key_plus_type.split(':')
                
                # If ther are 2 colons, key is last two words joined by a colon
                if len(k_t_split) == 3:
                    node_tag['key'] = k_t_split[1] + ':' + k_t_split[2]
                    node_tag['type'] = k_t_split[0]
                    
                    # Append the node tags to the list of node tags
                    tags.append(node_tag)
                
                # If there is 1 colon
                if len(k_t_split) == 2:
                    node_tag['key'] = k_t_split[1]
                    node_tag['type'] = k_t_split[0]
                    
                    # Checks if it's an 'addr:street' tag
                    if is_street_name(tag):
                        node_tag['value'] = update_name(node_tag['value'], mapping)
                    
                    # Checks if it's an 'addr:postcode' tag
                    #elif is_post_code(tag):
                        #print 'found a postcode: ' + tag.attrib['v']
                        
                    # Append the node tags to the list of node tags
                    tags.append(node_tag)
                
            # If there are no colons, processing is easier
            else:
                node_tag['key'] = key_plus_type
                
                # Clean 'address' tags
                if key_plus_type == 'address':
                    node_tag['value'] = update_address(node_tag['value'], mapping)
                    
                # Clean 'name' tags
                elif key_plus_type == 'name':                                
                    if check_highway(element):
                        node_tag['value'] = update_address(node_tag['value'], mapping)                   
                
                # Clean up 'phone' tags
                elif key_plus_type == 'phone':
                    node_tag['value'] = update_phone(node_tag['value'])
                    
                node_tag['type'] = 'regular'
                # Append the node tags to the list of node tags
                tags.append(node_tag)
        
        return {'node': node_attribs, 'node_tags': tags}
    
    elif element.tag == 'way':
        
        # Create a temporary dictionary from the xml element and make the 
        # node_attribs dictionary:
        temp_way_attribs = element.attrib
        
        way_attribs['id'] = temp_way_attribs['id']
        way_attribs['user'] = temp_way_attribs['user']
        way_attribs['uid'] = temp_way_attribs['uid']
        way_attribs['version'] = temp_way_attribs['version']
        way_attribs['changeset'] = temp_way_attribs['changeset']
        way_attribs['timestamp'] = temp_way_attribs['timestamp']
        
        ''' 
        Sometimes, there are tags nested inside way tags.  Need a way 
        to try to access these.  For instance, if it's a way tag, 
        immediately check if there are nodes and tags nested within
        '''
        
        way_node_position = 0
        for node in element.iter("nd"):
            way_node = {}
            way_node['id'] = way_attribs['id']
            way_node['node_id'] = node.attrib['ref']
            way_node['position'] = way_node_position
            way_node_position += 1
            way_nodes.append(way_node)
          
        # Need to capture any way tags
        for tag in element.iter('tag'):
            way_tag = {}
            way_tag['id'] = way_attribs['id']
            way_tag['value'] = tag.attrib['v']
            key_plus_type = tag.attrib['k']
            
            # If there are problem characters, don't add to way tags
            if is_problem_char(key_plus_type):
                print key_plus_type
                continue
              
            # If there are colons, need to split up to get key
            elif is_lower_colon(key_plus_type):
                
                k_t_split = key_plus_type.split(':')
                
                # If ther are 2 colons, key is last two words joined by a colon
                if len(k_t_split) == 3:
                    way_tag['key'] = k_t_split[1] + ':' + k_t_split[2]
                    way_tag['type'] = k_t_split[0]
                    # Append the node tags to the list of node tags
                    tags.append(way_tag)
                # If there is 1 colon
                if len(k_t_split) == 2:
                    way_tag['key'] = k_t_split[1]
                    way_tag['type'] = k_t_split[0]
                    
                    # Checks if it's an 'addr:street' tag
                    if is_street_name(tag):
                        #print "Old value: " + way_tag['value']
                        way_tag['value'] = update_name(way_tag['value'], mapping)
                        #print "New value: " + way_tag['value']
                        
                    # Append the node tags to the list of node tags
                    tags.append(way_tag)
                
            # If there are no colons, processing is easier
            else:
                way_tag['key'] = key_plus_type
                
                # This cleans up name tags
                if (key_plus_type == 'name'):# or (key_plus_type == 'address'):
                    # Only name tags that are highways are actual street names
                    if check_highway(element):
                        way_tag['value'] = update_name(way_tag['value'], mapping)
                
                # This cleans up address tags
                elif key_plus_type == 'address':
                    way_tag['value'] = update_address(way_tag['value'], mapping)
                    
                # This cleans up phone tags
                elif key_plus_type =='phone':
                    way_tag['value'] = update_phone(way_tag['value'])
                
                way_tag['type'] = 'regular'
                # Append the node tags to the list of way tags
                tags.append(way_tag)
            

        
        # way_attribs are the id, etc. way nodes include each id + relative position + way id, way tags are 
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #

# This should look at the name and replace any street abbreviations with the appropriate mapping
def check_highway(elem):
    for tag in elem.iter('tag'):
        if (tag.attrib['k'] == 'highway') and (tag.attrib['v'] != 'bus_stop'):
            return True
    return False

def update_name(name, mapping):
    
    updated_name = name
    
    split_name = re.split(' ', name)
    for nm in split_name:
        if nm in mapping:
            updated_name = re.sub(nm, mapping[nm], updated_name)
    
    return updated_name

# This will look at the complete address, pull the street address and replace any street abbreviations with the appropriate mapping
def update_address(address, mapping):
    
    updated_address = address
    
    # Check if the address has missing zip code info
    if address in mapping:
        # This updates all addresses with 00 for zip
        updated_address = re.sub(address, mapping[address], updated_address)
        return updated_address
    
    # Gets the street address
    addy = address.split(',')[0]
    
    # Splits the street address up by spaces
    split_addy = re.split(' ', addy)
    
    # Loops through the parts of the street address
    for ad in split_addy:
        
        # If it finds an abbreviation, it replaces it
        if ad in mapping:
            updated_address = re.sub(ad, mapping[ad], updated_address)
            
    return updated_address

def update_phone(phone):
    
    updated_phone = phone
    
    # Splits up phone to look at leading characters
    split_phone = phone.split(' ')
    
    # If phone isn't formated properly, clean it
    if split_phone[0] == '+1':
        
        # This places all phone numbers in xxx.xxx.xxxx format
        updated_phone = updated_phone = re.sub(r'..\s+(\d\d\d)\s+(\d\d\d)(\d\d\d\d)', r'\1-\2-\3', phone)
    
    return updated_phone

# Checks whether a given element is a postal code
def is_post_code(elem):
    #return ('post' in elem.attrib['k'])
    return (elem.attrib['k'] == "addr:postcode")

# checks whether a given element is a street name
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_name(elem):
    return (elem.attrib['k'] == 'name')

def is_highway(elem):
    if (elem.attrib['k'] == 'highway') and (elem.attrib['v'] != 'bus_stop'):
        return True
    else:
        return False

# Checks whether an attribute has a colon in the name
def is_lower_colon(attribute):
    m = LOWER_COLON.search(attribute)
    return m

# Checks whether there are problem characters present
def is_problem_char(attribute):
    m = PROBLEMCHARS.search(attribute)
    return m

def is_int(v):
    if isinstance(v, int):
        return True
    else:
        return False

def is_float(v):
    
    try:
        float(v)
        return True
    except ValueError:
        return False

def is_list(v):
    if v[0] == '{':
        return True
    else:
        return False
    
def is_null(v):
    if v == 'NULL':
        return True
    else:
        return False

def is_str(v):
    if type(v) is str:
        return True
    else:
        return False
    
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()
        

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=True)


# In[ ]:

phone = "+1 413 2624079"

updated_phone = updated_phone = re.sub(r'..\s+(\d\d\d)\s+(\d\d\d)(\d\d\d\d)', r'\1-\2-\3', phone)

print updated_phone


# In[116]:

# Create Nodes Database
import sqlite3
import csv
from pprint import pprint

sqlite_file = "west-springfield.db"

# Connect to the database
conn = sqlite3.connect(sqlite_file)

'''
NODES_PATH = "nodes.csv"
'''
# Get a cursor object
cur = conn.cursor()

# Before creating the table, drop the table if it already exists
cur.execute('DROP TABLE IF EXISTS nodes')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes(id INTEGER primary key, 
    lat REAL, 
    lon REAL, 
    user TEXT references ways, 
    uid INTEGER references ways, 
    version TEXT references ways, 
    changeset INTEGER references ways, 
    timestamp TEXT references ways)
    ''')

# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the data as a list of tuples:
with open('nodes.csv', 'rb') as fin:
    dr = csv.DictReader(fin) # comma is default limiter
    to_db = [(i['id'], i['lat'], i['lon'], i['user'].decode("utf-8"), i['uid'], i['version'].decode("utf-8"), i['changeset'], i['timestamp'].decode("utf-8")) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()

cur.execute('SELECT * FROM nodes')
all_rows = cur.fetchall()
print('1):')
for i, row in enumerate(all_rows):
    if i < 100:
        print row
    else:
        break
#pprint(all_rows)

conn.close()


# In[117]:

# Create Node Tags Database
import sqlite3
import csv
from pprint import pprint

sqlite_file = "west-springfield.db"

# Connect to the database
conn = sqlite3.connect(sqlite_file)

'''
NODE_TAGS_PATH = "nodes_tags.csv"
'''
# Get a cursor object
cur = conn.cursor()

# Before creating the table, drop the table if it already exists
cur.execute('DROP TABLE IF EXISTS nodes_tags')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER references nodes, 
    key TEXT, 
    value TEXT, 
    type TEXT)
    ''')

# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the data as a list of tuples:
with open('nodes_tags.csv', 'rb') as fin:
    dr = csv.DictReader(fin) # comma is default limiter
    to_db = [(i['id'], i['key'], i['value'].decode("utf-8"), i['type']) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()


cur.execute('SELECT * FROM nodes_tags')
all_rows = cur.fetchall()
print('1):')
for i, row in enumerate(all_rows):
    if i < 100:
        print row
    else:
        break
#pprint(all_rows)

conn.close()


# In[118]:

# Create Ways Database

import sqlite3
import csv
from pprint import pprint

sqlite_file = "west-springfield.db"

# Connect to the database
conn = sqlite3.connect(sqlite_file)

'''
WAYS_PATH = "ways.csv"
'''
# Get a cursor object
cur = conn.cursor()

# Before creating the table, drop the table if it already exists
cur.execute('DROP TABLE IF EXISTS ways')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways(id INTEGER primary key, 
    user TEXT references nodes, 
    uid INTEGER references nodes, 
    version TEXT references nodes, 
    changeset INTEGER references nodes, 
    timestamp TEXT references nodes)
    ''')

# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the data as a list of tuples:
with open('ways.csv', 'rb') as fin:
    dr = csv.DictReader(fin) # comma is default limiter
    to_db = [(i['id'],  i['user'].decode("utf-8"), i['uid'], i['version'].decode("utf-8"), i['changeset'], i['timestamp'].decode("utf-8")) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO ways(id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()


cur.execute('SELECT * FROM ways')
all_rows = cur.fetchall()
print('1):')
for i, row in enumerate(all_rows):
    if i < 100:
        print row
    else:
        break
#pprint(all_rows)

conn.close()


# In[119]:

# Create Ways Nodes Database

import sqlite3
import csv
from pprint import pprint

sqlite_file = "west-springfield.db"

# Connect to the database
conn = sqlite3.connect(sqlite_file)

'''
WAY_NODES_PATH = "ways_nodes.csv"
'''
# Get a cursor object
cur = conn.cursor()

# Before creating the table, drop the table if it already exists
cur.execute('DROP TABLE IF EXISTS ways_nodes')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways_nodes(id INTEGER references ways, 
    node_id INTEGER references nodes (id), 
    position INTEGER)
    ''')

# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the data as a list of tuples:
with open('ways_nodes.csv', 'rb') as fin:
    dr = csv.DictReader(fin) # comma is default limiter
    to_db = [(i['id'],  i['node_id'], i['position']) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db)
# commit the changes
conn.commit()


cur.execute('SELECT * FROM ways_nodes')
all_rows = cur.fetchall()
print('1):')
for i, row in enumerate(all_rows):
    if i < 100:
        print row
    else:
        break
#pprint(all_rows)

conn.close()


# In[120]:

# Create Way Tags Database

import sqlite3
import csv
from pprint import pprint

sqlite_file = "west-springfield.db"

# Connect to the database
conn = sqlite3.connect(sqlite_file)

'''
WAY_TAGS_PATH = "ways_tags.csv"
'''
# Get a cursor object
cur = conn.cursor()

# Before creating the table, drop the table if it already exists
cur.execute('DROP TABLE IF EXISTS ways_tags')
conn.commit()

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE ways_tags(id INTEGER references ways, 
    key TEXT, 
    value TEXT, 
    type TEXT)
    ''')

# commit the changes
conn.commit()

# Read in the csv file as a dictionary, format the data as a list of tuples:
with open('ways_tags.csv', 'rb') as fin:
    dr = csv.DictReader(fin) # comma is default limiter
    to_db = [(i['id'],  i['key'].decode("utf-8"), i['value'].decode("utf-8"), i['type'].decode("utf-8")) for i in dr]

# insert the formatted data
cur.executemany("INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
# commit the changes
conn.commit()


cur.execute('SELECT * FROM ways_tags')
all_rows = cur.fetchall()
print('1):')
for i, row in enumerate(all_rows):
    if i < 100:
        print row
    else:
        break
#pprint(all_rows)

conn.close()


# In[121]:

# Distribution of Postal Codes
# To see how the various functions in the DB-API work, take a look at this code,
# then the results that it prints when you press "Test Run".
#


import sqlite3
import pandas as pd

# This will show the distribution of postal codes
db = sqlite3.connect("west-springfield.db")
c = db.cursor()
query = '''
select value, count(*) as total from nodes_tags 
where key='postcode' group by value order by total desc;
'''
c.execute(query)
rows = c.fetchall()

# rows.sort()

# And let's loop over it too:
#print
print "Ids and User names:"
for row in rows:
    print row[0], "  ", row[1]
    
df = pd.DataFrame(rows)
print df    

db.close()


# In[122]:

# Kinds of Amenities
#

import sqlite3
import pandas as pd

# This will show the distribution of amenities
db = sqlite3.connect("west-springfield.db")
c = db.cursor()
query = '''
select value, count(*) as total from nodes_tags
where key='amenity'
group by value order by total desc;
'''
c.execute(query)
rows = c.fetchall()
    
df = pd.DataFrame(rows)
print df    

db.close()


# In[123]:

# Distribution of Users
#

# This will show the distribution of amenities
db = sqlite3.connect("west-springfield.db")
c = db.cursor()
query = '''
select user, count(*) as total
from (select user from nodes union all select user from ways)
group by user
order by total desc
limit 10;
'''
c.execute(query)
rows = c.fetchall()
    
df = pd.DataFrame(rows)
print df    

db.close()


# In[106]:

# How did the User Alan Bragg contribute to the project?
#

# This will show the distribution of amenities
db = sqlite3.connect("west-springfield.db")
c = db.cursor()
query = '''
select key, count(*) as total
from nodes, nodes_tags
where nodes.id = nodes_tags.id and user='Tomash Pilshchik'
group by key
order by total desc;
'''
c.execute(query)
rows = c.fetchall()
    
df = pd.DataFrame(rows)
print df    

db.close()


# In[107]:

# How did the User Alan Bragg contribute to the project?
#

# This will show the distribution of amenities
db = sqlite3.connect("west-springfield.db")
c = db.cursor()
query = '''
select key, count(*) as total
from ways, ways_tags
where ways.id = ways_tags.id and user='Tomash Pilshchik'
group by key
order by total desc;
'''
c.execute(query)
rows = c.fetchall()
    
df = pd.DataFrame(rows)
print df    

db.close()


# In[96]:

# Types of Nodes Tags
# This will show the distribution of nodes tags
#

import sqlite3
import pandas as pd

# This will show the distribution of postal codes
db = sqlite3.connect("west-springfield.db")
c = db.cursor()
query = '''
select key, count(*) as total from nodes_tags
group by key order by total desc;
'''
c.execute(query)
rows = c.fetchall()
    
df = pd.DataFrame(rows)
print df    

db.close()


# In[110]:

# Types of Ways Tags
# This will show the distribution of nodes tags
#

import sqlite3
import pandas as pd

# This will show the distribution of postal codes
db = sqlite3.connect("west-springfield.db")
c = db.cursor()
query = '''
select key, count(*) as total from ways_tags
group by key order by total desc;
'''
c.execute(query)
rows = c.fetchall()
    
df = pd.DataFrame(rows)
print df    

db.close()


# In[ ]:




# In[124]:

# Types of Ways Highway Tags
# This will show the distribution of nodes tags
#

import sqlite3
import pandas as pd

# This will show the distribution of postal codes
db = sqlite3.connect("west-springfield.db")
c = db.cursor()
query = '''
select value, count(*) as total from ways_tags
where key='name'
group by value order by total desc;
'''
c.execute(query)
rows = c.fetchall()
    
print "Highway Names and Totals:"
for row in rows:
    print row[0]#, "  ", row[1]

db.close()


# In[ ]:



