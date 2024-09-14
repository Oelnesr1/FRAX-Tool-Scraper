# FRAX — Fracture Risk Assessment Tool Web Scraper

This directory is a Selenium-based web scraper for the FRAX Fracture Risk Assessment Web Tool. 

To run, ensure that the correct Chrome driver for your operating system is installed into this directory. Then, to run the web scraper, simply execute:

```
	python3 ./frax_selenium_scrape.py -infile [INFILE] -ofile [OFILE]
```

`-infile` and -`ofile` are optional arguments for an input file and output file, respectively. 

`create_random_frax_csv.py` uses the bounds acceptable in the FRAX calculator to create a CSV of random data to feed into the webpage.

`print_pandas.py` can be used to print the output file to console using pandas, and is formatted slightly nicer than the CSV.

For help on how to run any of the python programs, or for more information on optional arguments, run:

```
	python3 ./[program_name].py -h
```

and more information will be provided.
