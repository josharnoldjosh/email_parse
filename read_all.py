import str_parse, argparse, os
from multiprocessing import Pool

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="The number of emails in a thread necessary to display information", type=int, default=2)
args = parser.parse_args()

from glob import glob
result = [(y, args) for x in os.walk(os.getcwd()) for y in glob(os.path.join(x[0], '*.mbox'))]
pool = Pool()
pool.starmap(str_parse.create_csv, result)
print("Script finished running! All CSVs created :)")