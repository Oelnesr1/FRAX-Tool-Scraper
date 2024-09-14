import pandas as pd
import argparse

parser = argparse.ArgumentParser(prog = "CSV printer",
                                 description = "Prints a CSV to console using Pandas"
                                 )
parser.add_argument('-ofile', required=False, help = "An output file. If not defined, the output file will be 'frax_results.csv'", nargs = "?", default = "frax_results.csv")

args = parser.parse_args()

df = pd.read_csv(args.ofile)

with pd.option_context('display.max_rows', None, 'display.max_columns', None): 
    print(df)
