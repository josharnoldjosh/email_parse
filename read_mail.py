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
	print("Can't read mailbox!")

to_list = ["To (Person)"]
subject_list = ["Email subject"]

for message in mbox:
    if (message.is_multipart()):
    	pay_load = message.get_payload()
    	if (len(pay_load) >= args.num_in_thread):
    		to_str = str(message['to'])
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
	    	wr.writerow([to_list[i], subject_list[i]])
	    	i += 1
	    print("Done!")


