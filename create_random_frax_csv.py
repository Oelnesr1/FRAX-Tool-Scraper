import pandas as pd
import random
import argparse

# Initialize argparse

parser = argparse.ArgumentParser(prog = "FRAX data generator",
                                 description = "Creates random data that can be used in the FRAX Web Page"
                                 )
parser.add_argument('-nrows', required=False, help = "The number of rows to create. If not defined, the number of rows will be 100.", nargs = "?", default = 100, type=int)
parser.add_argument('-ofile', required=False, help = "An output file. If not defined, the output file will be 'frax_data.csv'", nargs = "?", default = "frax_data.csv")

args = parser.parse_args()

# Generate random data
data = {
    'age': [random.randint(40, 90) for _ in range(args.nrows)],
    'weight': [str(round(random.uniform(25, 125), 2)) for _ in range(args.nrows)],
    'height': [str(round(random.uniform(100, 220), 2)) for _ in range(args.nrows)],
    'sex': [random.choice(['male', 'female']) for _ in range(args.nrows)]
}

df = pd.DataFrame(data)
df.to_csv(args.ofile, index=False)

print("Successfully created random data")