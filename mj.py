#!/usr/bin/env python
#
# multijournal script for journal management
# create journals and stub entries
import sys, datetime, os, subprocess, mjlib

# args that take no parms have a value of NONE so they are skipped
# by the arg parser
args = { 'title': '', 'jtitle': '', 'list': False, 'open': False, 
         'eid': 0, 'help': False }
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
        if next_arg == 'type':
            args[next_arg] = arg.lower()
        else:
            args[next_arg] = arg
        next_arg = ''

if args['help']:
    print "To create a journal: ../mj.py --title \"Fitness Tracking\"\n"+\
          "To create an entry: ../mj.py --jtitle \"Fitness Tracking\" --title "+\
          "\"Ran For Ten Extra Minutes Today\"\n"+\
          "Append the --open option to open the new entry or journal in a vim"+\
          "buffer for editting"
elif args['list']:
    if args['eid'] > 0:
        e = mjlib.get_entry(args['jtitle'].replace(" ", "_").lower(), args['eid'])
        print e['title'] + "\n" + e['date'] + "\n" + e['body']
    elif args['jtitle'] != '':
        entries = mjlib.list_entries(args['jtitle'])
        longest_title = max(map(lambda x: len(x['title']), entries))
        for e in entries:
            print ' | '.join([e['eid'], e['title']+\
                " "*(longest_title-len(e['title'])), e['date']])
    else:
        journals = mjlib.list_journals()
        # bit of string formatting
        longest_title = max(map(lambda x: len(x['title']), journals))
        for j in journals:
            print ' | '.join([str(j['count']), j['title']+\
                    " "*(longest_title-len(j['title'])), j['last_entry']])

elif args['title'] == '' and args['jtitle'] == '':
    # print usage if no title or journal title given
    print "./mj.py --help"

elif args['jtitle'] == '':
    if args['title'] == '':
        print "Journal title required"
        sys.exit(1)
    else:
        new_object_path = mjlib.mkjournal(args['title']) 

else:
    if args['jtitle'].lower() not in\
        [jn.lower() for jn in os.listdir(journals_dir)]:
        print "No journals entitled: " + args['jtitle']
        sys.exit(2)
    else:
        new_object_path = mjlib.mkentry(args['jtitle'], args['title'])

print new_object_path

if args['open']:
    subprocess.call(['vim', new_object_path])
