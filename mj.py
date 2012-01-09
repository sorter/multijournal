#!/usr/bin/env python
#
# multijournal script for journal management
# create journals and stub entries
import sys, datetime, os, subprocess, mjlib

# args that take no parms have a value of NONE so they are skipped
# by the arg parser
args = { 'type': '', 'title': '', 'jtitle': '', 'list': False, 'open': False, 
         'eid': 0 }
acceptable_args = args.keys()
next_arg = ''
journals_dir = '/home/askhader/scratch/mj/js/'

new_object_path = ''

for arg in sys.argv:
    if next_arg == '' and len(arg) > 2 and arg[2:] in acceptable_args:
        if args[arg[2:]] is False: # skip arg params
            args[arg[2:]] = True
            next_arg = ''
        else:
            next_arg = arg[2:]
    else:
        args[next_arg] = arg
        next_arg = ''

if args['list']:
    if args['eid'] > 0:
        e = mjlib.get_entry(args['jtitle'], args['eid'])
        print e['title'] + "\n" + e['date'] + "\n" + e['body']
    elif args['jtitle'] != '':
        for j in mjlib.list_entries(args['jtitle']):
            print ' | '.join([j['eid'], j['title'], j['date']])
    else:
        for j in mjlib.list_journals():
            print ' | '.join([str(j['count']), j['title'], j['last_entry']])

elif args['type'] == '':
    print "No object type specified. Journal or entry?"
    sys.exit(1)
else:

    if args['type'].lower() == 'journal':
        new_object_path = mjlib.mkjournal(args['title']) 

    elif args['type'].lower() == 'entry':
        if args['jtitle'] == '':
            print "Journal title required."
            sys.exit(1)
        elif args['jtitle'].lower() not in\
            [jn.lower() for jn in os.listdir(journals_dir)]:
            print "No journals entitled: " + args['jtitle']
            sys.exit(2)
        else:
            new_object_path = mjlib.mkentry(args['jtitle'], args['title'])


if  args['open']:
    subprocess.call(['vim', new_object_path])
