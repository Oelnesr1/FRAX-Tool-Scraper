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

BMD_bounds = {
    "GE-Lunar": [0.2, 1.87],
    "Hologic": [0.14, 1.58],
    "Norland": [0.17, 1.76],
    "T-Score": [-5, 2],
    "DMS/Medilink": [0, 1.3],
    "Mindways QCT": [0, 1],
    "NM": [0, 0]
}

BMD_units = [random.choice(["GE-Lunar", "Hologic", "Norland", "T-Score", "DMS/Medilink", "Mindways QCT", "NM"]) for _ in range(args.nrows)]

data = {
    'age': [random.randint(40, 90) for _ in range(args.nrows)],
    'weight': [str(round(random.uniform(25, 125), 2)) for _ in range(args.nrows)],
    'height': [str(round(random.uniform(100, 220), 2)) for _ in range(args.nrows)],
    'sex': [random.choice(['male', 'female']) for _ in range(args.nrows)],
    'previous fracture': [random.choice([0, 1]) for _ in range(args.nrows)],
    'parent fractured hip':[random.choice([0, 1]) for _ in range(args.nrows)],
    'current smoking': [random.choice([0, 1]) for _ in range(args.nrows)],
    'glucocorticoids': [random.choice([0, 1]) for _ in range(args.nrows)],
    'rheumatoid arthritis': [random.choice([0, 1]) for _ in range(args.nrows)],
    'secondary osteoporosis': [random.choice([0, 1]) for _ in range(args.nrows)],
    'alcohol >3': [random.choice([0, 1]) for _ in range(args.nrows)],
    'femoral neck bmd unit': BMD_units,
    'femoral neck bmd value': [str(round((random.uniform(0, 1) * (BMD_bounds[BMD_units[row]][1] - BMD_bounds[BMD_units[row]][0])) + BMD_bounds[BMD_units[row]][0], 3)) 
                               for row in range(args.nrows)]
}


df = pd.DataFrame(data)
df.to_csv(args.ofile, index=False)

print("Successfully created random data")