#!/usr/bin/env python
from random import random
import requests
import time
import json
import sys
import re
import cgi, cgitb
import webbrowser
import cgi, cgitb
import os

urlidform = cgi.FieldStorage()
urlidlink = urlidform.getvalue('link')
print("Content-type:text/html")
print
print("")
print("")
FORM = 1
FIELDS = 1
TITLE = 8
ID = 0
NAME = 1
DESCRIPTION = 2
TYPE = 3
VALUE = 4
OPTIONS = 1
URL = -2


types = {
    0: 'Short Answer',
    1: 'Paragraph',
    2: 'Radio',
    3: 'Dropdown',
    4: 'Checkboxes',
    5: 'List',
    6: 'Toggle',
    7: 'Date',
    8: 'Section'
}

choice_types = ['Radio', 'Checkboxes', 'Dropdown','Toggle']
choice_no=[2,3,4,6,5]
unknowntypes=[6,7,9,10,11,12,13]
answer={}
def get_url(data):
    #print(data[URL])
    return 'https://docs.google.com/forms/d/e/' + data + '/formResponse'

def get_name(data):
    return data[FIELDS][TITLE]

def get_options(elem):
    options_raw = elem[VALUE][0][OPTIONS]
    return list(map(lambda l: l[0], options_raw))

def get_fields(data):
    fields = {}
    try:
        for elem in data[FORM][FIELDS]:
            field = {
                    'description': elem[DESCRIPTION],
                    'type': types.get(elem[TYPE]),
                    'id': elem[VALUE][0][ID],
                    'submit_id': 'entry.' + str(elem[VALUE][0][ID]),
                    }
            
            if field['type'] in choice_types:
                field['options'] = get_options(elem)

            fields[elem[NAME]] = field
    except:
        print('')
    return fields
def myfunc(mydata,urlid):
    file = open("sample.html","w")
    text='''<html><body><form method="post" action="formsubmit.py">'''
    file.write(text)
    text='''<input type="hidden" name="linkval" value="'''+urlid+'''">'''
    file.write(text)
    j=0
    for el in mydata[FORM][FIELDS]:
        if el[TYPE]==8:
            j=j+1
            text='''<h3>Section:'''+str(j)+''' '''
            file.write(text)  
            text='''<label>'''+str((el[NAME]))+'''</label></h3>'''
            file.write(text) 
        else:
            text='''<b><label>'''+str((el[NAME]))+'''</label></b><br><br>'''
            file.write(text) 
        if el[TYPE] in choice_no:
            opt=(get_options(el))
            i=0
            if el[TYPE]==5:
                text=el[VALUE][0][3][0]+'''<br>'''
                file.write(text)            
            if el[TYPE]==2 or el[TYPE]==5:     
                try:
                    for optel in opt: 
                        text='''<input type="radio" name="'''+el[NAME]+'''" value="'''+optel+'''"'>'''+optel+'''<br>'''
                        file.write(text)
                        #print(str(i)+" "+optel)
                        i=i+1
                    text='''<br>'''
                    file.write(text)
                except:
                    pass
            if el[TYPE]==5:
                text=el[VALUE][0][3][1]+'''<br>'''
                file.write(text)    
            elif el[TYPE]==3:
                text='''<select name="'''+el[NAME]+'''">'''
                file.write(text) 
                for optel in opt: 
                    text='''<option value="'''+optel+'''">'''+optel+'''</option'''
                    print(str(i)+" "+optel)
                    i=i+1
                text='''</select>'''
                file.write(text)
            elif el[TYPE]==4:
                for optel in opt: 
                    text='''<input type="checkbox" name="'''+el[NAME]+'''" value="'''+optel+'''"'>'''+optel+'''<br>'''
                    file.write(text)
                    #print(str(i)+" "+optel)
                    i=i+1
                text='''<br>'''
                file.write(text)
            #answer[el[NAME]]=input('Enter option:')
        elif el[TYPE]==1:
            text='''<textarea rows="4" cols="50" name="'''+el[NAME]+'''"></textarea><br><br>'''
            file.write(text)
            #answer[el[NAME]]=input('Enter answer:')
        elif el[TYPE]==0:
            text='''<input type="text" name="'''+el[NAME]+'''"><br><br>'''
            file.write(text)
        elif el[TYPE]==8:
            pass
        if el[TYPE] in unknowntypes:
            print(el[TYPE])
            #answer[el[NAME]]=input('Enter answer:')
        #print("answer is: "+answer[el[NAME]])
    text='''<input type="submit" value="Submit"></form></body></html>'''
    file.write(text)
    file.close()
        
def parse_data(data_str,urlid):
    data = json.loads(data_str) 
    global impdata
    impdata=data
    myfunc(data,urlid)
    return {
        'url': get_url(urlid),
        'name': get_name(data),
        'fields': get_fields(data),
    }

def get_form(url,urlid):
    body = requests.get(url).text
    match = re.search(r'FB_PUBLIC_LOAD_DATA_ = ([^;]*);', body)
    if not match: return None
    data = parse_data(match.group(1),urlid)
    return data

def output(form):
    for name in form['fields']:
        field = form['fields'][name]
        print(name + ' (' + str(field['id']) + ')')
        if field['description']: print('> ' + field['description'])
        if 'options' in field:
            for option in field['options']:
                print('  - ' + option)
        print()

def submit(form):
    payload = {}
    for name in form['fields']:
        field = form['fields'][name]
        if field['type'] in choice_types and field['value'] not in field['options']:
            payload[field['submit_id']] = '__other_option__'
            payload[field['submit_id'] + '.other_option_response'] = field['value']
        else:
            payload[field['submit_id']] = field['value']

    return requests.post(form['url'], data=payload)


def main(url,urlid):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36'
    })

    form = get_form(url,urlid)
    # output(form) # uncomment this to print out the contents of the form
    fields = form['fields']

    
    # fill out the fields here
    # fields['Field Name']['value'] = 'What you want to submit'
    
    #for name in answer:
     #   fields[name]['value']=answer[name]
      #  print(answer[name])
      
    #fields['Greek Sing Show']['value'] = 'Booth > Greek Sing'
    #fields['Best Ceremony']['value'] = 'Flag & Badge'
    #fields['Mac & Cheese']['value'] = 'Lobster Mac'
    #fields['What are your favorite colors?']['value'] = 'Purple, White, and Gold'
    #fields['If a man is unsatisfied with himself, with who he is, and he wants to make of himself a better man, what must he do?']['value'] = \
        #'Um... idk man, I thought it was Zach\'s job to tell me that?'
    
    #submit(form)
    
    #num_submitions = 0 # change this to spam more/less
   # for i in range(num_submitions):
  #      time.sleep(1 + random())
#        submit(form)


if __name__ == '__main__':
    # put your url here
    urlid=urlidlink
    url = 'https://docs.google.com/forms/d/e/'+urlid+'/viewform?usp=sf_link'
    main(url,urlid)
    new = 1 # open in a new tab, if possible
    url = "sample.html"
    print('Redirecting..')
    webbrowser.open(url,new=new)
