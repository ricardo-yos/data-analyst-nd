#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

OSMFILE = "santo-andre_brazil.osm"
street_type_re = re.compile(r'\b\w+\S+\.?', re.IGNORECASE)
abbrev_street_re = re.compile(r'(\b\w+|_)[.]', re.IGNORECASE)
num_street_re = re.compile(r'\d[°ª]', re.IGNORECASE)
lowercase_re = re.compile(r'\b[a-z]+', re.LOCALE)
postalcode_re = re.compile(r'\d{5}[-]\d{3}')


expected = ["Rua", "Avenida", u"Praça", "Travessa", "Alameda", "Largo", "Rodovia", "Complexo", "Estrada", "Rodoanel", "Passagem"]

mapping = { "Av.": "Avenida",
            "Sen.": "Senador",
            "Prof.": "Professor",
            "Dr.": "Doutor",
            "Pres.": "Presidente",
            "B.": "Barreto",
            u"1ª": "Primeira"
          }

allowed_lowercase = ["da", "de", "do", "das", "dos", "e"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
def audit_street_name(street_types, street_name):
    m = abbrev_street_re.search(street_name)
    if m:
        abbreviation = m.group()
        street_types[abbreviation].add(street_name)
        
def audit_num_street(street_types, street_name):
    m = num_street_re.search(street_name)
    if m:
        number = m.group()
        street_types[number].add(street_name)

def is_lower(street_types, street_name):
    m = lowercase_re.search(street_name)
    if m:
        word = m.group()
        if word not in allowed_lowercase:
            street_types[word].add(street_name)

def audit_postcode(postcode_types, postal_code):
    m = postalcode_re.search(postal_code)
    if m:
        pass
    else:
        postcode_types[postal_code].add(postal_code)
    if postal_code[:2] == "09":
        pass
    elif postal_code[:5] >= "01000" and postal_code[:5] <= "05999":
        pass
    elif postal_code[:5] >= "08000" and postal_code[:5] <= "08499":
        pass
    else:
        postcode_types[postal_code].add(postal_code)
        
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_post_code(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(osmfile):
    """Audit the OSM file by searching unexpected street names and incorrect postalcodes"""
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    postcode_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
                    audit_street_name(street_types, tag.attrib['v'])
                    audit_num_street(street_types, tag.attrib['v'])
                    is_lower(street_types, tag.attrib['v'])
                if is_post_code(tag):
                    audit_postcode(postcode_types, tag.attrib['v'])
                    
    osm_file.close()
    return street_types, postcode_types


def update_name(name, mapping):
    """"Fix the street names and street types"""
    words_name = name.split(" ")
    if words_name not in expected:
        for word in words_name:
            if word in mapping:
                name = name.replace(word, mapping[word])
                
            if word == word.lower():
                if word not in allowed_lowercase:
                    name = name.replace(word, word.capitalize())
        
        if words_name[0] not in expected:
            if words_name[0] not in mapping:
                if words_name[0] == "Fernando":
                    name = "Avenida " + name
                elif words_name[0] == "rua":
                    pass
                else:
                    name = "Rua " + name

    return name


def update_postalcode(code):
    """Fix the postalcodes"""
    # Adjust the postal code format
    digits = []
    for num in code:
        if num not in ["-", " "]:
            digits.append(num)
    
    code = "".join(digits[0:5])+"-"+"".join(digits[5:])
    # Change the wrong postal code to the correct one
    correct_cep = {"11060-301":"09891-420", "13087-901": "09080-001"}
    if code in correct_cep:
        code = correct_cep[code]
    
    return code


def audit_process():
    """Create dictionaries containing the correct street name and postal code"""
    st_types, pc_types = audit(OSMFILE)
    #pprint.pprint(dict(st_types))
    #pprint.pprint(dict(pc_types))

    correct_name = {}
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            correct_name[name] = better_name
            #print name, "=>", better_name
    
    correct_code = {}
    for _, pc_type in pc_types.iteritems():
        for code in pc_type:
            better_code = update_postalcode(code)
            correct_code[code] = better_code
            #print code, "=>", better_code
    
    return correct_name, correct_code


if __name__ == '__main__':
    test()
