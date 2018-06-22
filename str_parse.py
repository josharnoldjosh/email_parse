import re, os.path, os, re, mailbox, sys, csv
import threading
from multiprocessing import Queue

blacklist = open("blacklist.txt", "r")
data = blacklist.readlines()
blackListRegexes = []
for i in data:
	blackListRegexes.append(re.compile(i))
blacklist.close()

def blacklisted_email(email):
	for regex in blackListRegexes:
		if regex.match(email):
			return True
	return False

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
	filtered_emails = []
	for i in emails:
		if (blacklisted_email(i) == False):
			filtered_emails.append(i)
	return filtered_emails

def get_file_name():
	i = 1
	file_name = "output_" + str(i) + ".csv"
	while os.path.isfile(file_name):
		i += 1
		file_name = "output_" + str(i) + ".csv"
	return file_name

def check_to_write(to_write):
	if '?' in to_write[2] or "Gmail Team" in to_write[2] or "Taco from Trello" in to_write[2]: 
		return False
	if "hackdavis" in to_write[1]:
		return False
	if to_write[1].strip() == "":
		return False
	if to_write[4].strip() == "":
		return False
	return True

def create_csv(path, args):
	print("Loading... (Please be patient)")
	mbox = mailbox.mbox(path)
	if (mbox):
		print("Mailbox loaded.")
	else:
		print("Can't read mailbox! Please make sure file path is correct.")
		return
	messages = Queue()
	done = threading.Event()
	writer = threading.Thread(target=write_thread, args=(done, messages))
	writer.start()
	thread_ids = set()
	for message in mbox:
		if (message.is_multipart()):
			pay_load = message.get_payload()

			thread_id = message["X-GM-THRID"]
		
			if (thread_id not in thread_ids):
				thread_ids.add(thread_id)
				if (len(pay_load) >= args.n):
					item = {}
					to_str = str(message['to'])
					from_str = str(message['from'])
					item["to"] = get_email_string(to_str)
					item["from"] = get_email_string(from_str)
					item["name"] = get_names(to_str)
					item["from_name"] = get_names(from_str)
					subj_str = str(message['subject'])
					# print(to_str, "\n", subj_str, '\n\n')
					item["subject"] = subj_str
					messages.put_nowait(item)
	done.set()

def write_thread(done, messages):
	file_name = get_file_name()
	print("Opening file ", file_name)
	with open(file_name, 'w') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		header = ["Email subject", "Receiver email", "Receiver name", "Sender email", "Sender name"]
		header_written = False
		while not done.is_set():
			try:
				element = messages.get(timeout=3)
			except:
				if done.is_set():
					print("Timed out, Saving", file_name)
					myfile.close()
					return
				else:
					continue
			to_write = [element["subject"], " ".join(element["from"]), " ".join(element["from_name"]), " ".join(element["to"]), " ".join(element["name"])]
			if (check_to_write(to_write) == False):
				continue 
			if not header_written:
				to_write = header
				header_written = True		
			wr.writerow(to_write)
			

	print("Saved", file_name, "!")
	myfile.close()































