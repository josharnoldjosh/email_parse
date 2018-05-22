import argparse
parser = argparse.ArgumentParser()
parser.add_argument('num_in_thread', help="The number of emails in a thread necessary to display information", type=int)
args = parser.parse_args()

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

import os.path
def get_file_name():
	i = 1
	file_name = "output_" + str(i) + ".csv"
	while os.path.isfile(file_name):
		i += 1
		file_name = "output_" + str(i) + ".csv"
	return file_name

def create_csv(path):
	print("Loading... (Please be patient)")
	mbox = mailbox.mbox(path)
	if (mbox):
		print("Mailbox loaded.")
	else:
		print("Can't read mailbox! Please make sure file path is correct.")
		return
	to_list = ["To (Person)"]
	subject_list = ["Email subject"]
	names = ['Receiver name']
	emails = ["Receiver email"]
	from_email = ["Sender email (HackDavis contact)"]
	from_name = ["Sender name (HackDavis contact name)"]
	for message in mbox:
	    if (message.is_multipart()):
	        pay_load = message.get_payload()
	        if (len(pay_load) >= args.num_in_thread):
	            to_str = str(message['to'])
	            from_str = str(message['from'])
	            emails.append(get_email_string(to_str))
	            from_email.append(get_email_string(from_str))
	            names.append(get_names(to_str))
	            from_name.append(get_names(from_str))        
	            subj_str = str(message['subject'])
	            print(to_str, "\n", subj_str, '\n\n')
	            to_list.append(to_str)
	            subject_list.append(subj_str)
	file_name = get_file_name()
	print("Opening file ", file_name)      
	with open(file_name, 'w') as myfile:
	    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	    i = 0

	    while i < len(to_list):	    		    	
	    	to_write = [subject_list[i], " ".join(from_email[i]), " ".join(from_name[i]), " ".join(names[i]), " ".join(emails[i])]	  
	    	if (i == 0):
	    		to_write = [subject_list[i], from_email[i], from_name[i], names[i], emails[i]]
	    	wr.writerow(to_write)
	    	i += 1
	    print("Saved", file_name, "!")

import os, re, mailbox, sys, csv
from glob import glob
result = [y for x in os.walk(os.getcwd()) for y in glob(os.path.join(x[0], '*.mbox'))]
for i in result:
	create_csv(i)
print("Script finished running! All CSVs created :)")