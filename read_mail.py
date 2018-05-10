import mailbox, sys

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('file_path', help="The path to your .mbox file", type=str)
parser.add_argument('num_in_thread', help="The number of emails in a thread necessary to display information", type=int)
args = parser.parse_args()

mbox = mailbox.mbox(args.file_path)

if (mbox):
	print("Mailbox loaded.")
else:
	print("Can't read mailbox!")
	
for message in mbox:
    if (message.is_multipart()):
    	pay_load = message.get_payload()
    	if (len(pay_load) >= args.num_in_thread):
    		print(message['to'])
    		print(message['subject'])    		    	
    		print('\n\n')