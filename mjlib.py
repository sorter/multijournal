#!/usr/bin/env python
#
# helper functions for multijournal
#

import os

USERNAME = 'askhader'
LOCALDIR = '/scratch/mj/'
JSPATH = '/home/' + USERNAME + LOCALDIR + 'js/'

def list_entries(jtitle):
    """Return a list of { 'title': str, 'eid': int, 'date': str }"""
    j_path = JSPATH + jtitle
    es = []
    if os.path.exists(j_path):
        for jf in [f for f in os.listdir(j_path) if f.isdigit()]:
            jf_handle = open(j_path + "/" + jf, 'r')
            entry_title = jf_handle.readline().rstrip()
            entry_date = jf_handle.readline().rstrip()
            es.append({'title': entry_title, 'date': entry_date, 'eid': jf})
            jf_handle.close()
        return sorted(es, key=lambda a: a['eid'])
    else:
        raise Exception()


def get_entry_count(jtitle):
    """Return an integer representing the number of entries in a journal"""
    try:
        return max([int(j) for j in os.listdir(JSPATH+jtitle) if j.isdigit()])
    except ValueError:
        return 0

def get_entry(jtitle, eid):
    """Return {'title': str, 'date': str}"""
    efile = open(JSPATH + jtitle + "/" + eid, 'r')
    etitle = efile.readline().rstrip()
    edate = efile.readline().rstrip()
    body = efile.read()
    return {'title': etitle, 'date': edate, 'body': body}

def list_journals():
    """Return a list of { 'title': str, 'count': int, last_entry: str }"""
    js = []
    for j in [d for d in os.listdir(JSPATH) if os.path.isdir(JSPATH+d)]:
        c = get_entry_count(j)
        if c > 0:
            last_entry_path = JSPATH + j + "/" + str(c)
            entry_handle = open(last_entry_path, 'r')
            entry_handle.readline().rstrip()
            date = entry_handle.readline().rstrip()
        else:
            date = ''
        js.append({'title': j, 'count': c, 'last_entry': date})
    return js            


def mkjournal(jtitle):
    """Create a journal with the given title. Return a path to the manifest"""
    tstr = jtitle + "\n" + str(datetime.datetime.now()) + "\n####\n"
    os.mkdir(JSPATH+jtitle.replace(' ', '_').lower())
    new_object_path = JSPATH + jtitle + '/manifest'
    jmf = open(new_object_path, 'w')
    jmf.write(tstr)
    jmf.close()
    return new_object_path


def mkentry(jtitle, title):
    """Create a new journal entry with given title. Return path to the entry"""
    tstr = title + "\n" + str(datetime.datetime.now()) + "\n####\n"
    files = os.listdir(journals_dir+args['jtitle'])
    count = get_entry_count(jtitle)
    new_object_path = journals_dir+args['jtitle']+"/"+str(count+1)
    ef = open(new_object_path, 'w')
    ef.write(tstr)
    ef.close()
    return new_object_path

def journal_exists(jtitle):
    
