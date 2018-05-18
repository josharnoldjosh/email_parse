# modify script to save to csv format that at least includes the name, email and HackDavis contact email, HackDavis contact name
import re

def get_names(text):
	names = []
	i = 0
	if ('<' in text):
		new_text = re.sub('<[^>]+>', '', text)
		new_text = new_text.strip()		
		if (i > 0):
			new_text += ','
		i += 1	
		if ('@' not in new_text):
			names.append(new_text)
	return names

def get_email_string(text):
	emails = []
	if ('<' in text):
		while '<' in text:
			for i in range(0, len(text)):
				if text[i] == '<':
					text = text[i+1:]

					for j in range(0, len(text)):
						
						if text[j] == '>':
							text = text[:j]
							emails.append(text)
							break
					break
	elif(' ' not in text.strip()):
		emails.append(text) 
	elif(',' in text):
		pattern = re.compile("^\s+|\s*,\s*|\s+$")
		temp_arr = [x for x in pattern.split(text) if x]		
		for i in range(0, len(temp_arr)-1):
			temp_arr[i] = temp_arr[i] + ','
		emails += temp_arr
	return emails

import mailbox, sys, csv

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file_path', help="The path to your .mbox file", type=str)
parser.add_argument('num_in_thread', help="The number of emails in a thread necessary to display information", type=int)
args = parser.parse_args()

print("Loading... (Please be patient)")

mbox = mailbox.mbox(args.file_path)

if (mbox):
	print("Mailbox loaded.")
else:
	print("Can't read mailbox! Please make sure file path is correct.")
	exit()

to_list = ["To (Person)"]
subject_list = ["Email subject"]
emails = ["To person\'s email"]
names = ['To person\'s name']

for message in mbox:
    if (message.is_multipart()):
        pay_load = message.get_payload()
        if (len(pay_load) >= args.num_in_thread):
            to_str = str(message['to'])

            emails.append(get_email_string(to_str))
            names.append(get_names(to_str))         

            subj_str = str(message['subject'])
            print(to_str, "\n", subj_str, '\n\n')
            to_list.append(to_str)
            subject_list.append(subj_str)

should_save = input("Do you want to save to a CSV? y/n: ")
if should_save == '':
	should_save = 'y'
if ('y' in should_save.lower()):
	# SAVE to CSV
	file_name = input("Enter file name to save: ")
	if file_name == '':
		file_name = "output.csv"
	if ".csv" not in file_name.lower():
		file_name += ".csv"
	with open(file_name, 'w') as myfile:
	    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	    i = 0
	    while i < len(to_list):
	    	to_write = [to_list[i], subject_list[i]]
	    	if (i < len(names)):
	    		if (i == 0):
	    			to_write.append(names[i])
	    		to_write.append(" ".join(names[i]))
	    	if (i < len(emails)):
	    		if (i == 0):
	    			to_write.append(emails[i])
	    		to_write.append(" ".join(emails[i]))	    	
	    	wr.writerow(to_write)
	    	i += 1
	    print("Done!")


