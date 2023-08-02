import json
from data import Reservations
from os import listdir
from os.path import isfile, join
from ui import Airbnb

# Get input files
mypath = 'data/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
files = [f"data/{file}" for file in files if '.csv' in file]



reservations = Reservations(files)
window = Airbnb(reservations)




with open('output_data/data.json', 'w') as f:
    json.dump(reservations.reservation_data, f, indent=6)

try:
    reservations.reservation_df.to_csv("output_data/data.csv")
except PermissionError:
    print("Please make sure the file isn't already open!\n\n")

    print(f"Remaining Allowance: £{reservations.remaining_allowance}")
