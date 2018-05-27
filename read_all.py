import str_parse, argparse, os

parser = argparse.ArgumentParser()
parser.add_argument('num_in_thread', help="The number of emails in a thread necessary to display information", type=int)
args = parser.parse_args()

from glob import glob
result = [y for x in os.walk(os.getcwd()) for y in glob(os.path.join(x[0], '*.mbox'))]
for i in result:
	str_parse.create_csv(i, args)
print("Script finished running! All CSVs created :)")