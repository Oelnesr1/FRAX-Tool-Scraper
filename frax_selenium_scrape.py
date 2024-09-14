from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
import argparse 

# Initialize arguments

parser = argparse.ArgumentParser(prog = "FRAX Selenium Scraper",
                                 description = "This program is a Selenium-based web scraper to use the FRAX Fracture Risk Assessment Tool Webpage"
                                 )
parser.add_argument('-infile', required=False, help = "An input file. If not defined, the input file will be 'data.csv'", nargs = "?", default = "frax_data.csv")
parser.add_argument('-ofile', required=False, help = "An output file. If not defined, the output file will be 'frax_results.csv'", nargs = "?", default = "frax_results.csv")

args = parser.parse_args()


# Initialize selenium

service = Service(os.path.join(os.getcwd(), 'chromedriver'))
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
# driver.get('https://frax.shef.ac.uk/FRAX/tool.aspx')

# Initialize pandas

df = pd.read_csv(args.infile)
results_df = pd.DataFrame(columns = ['age', 'weight', 'height', 'sex', 'major osteoporotic risk', 'hip fracture risk'])


for index, row in df.iterrows():

    driver.get('https://frax.shef.ac.uk/FRAX/tool.aspx')

    time.sleep(3)

    # Add age, weight, and height into the webform
    age_input = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$toolage")
    age_input.clear()
    age_input.send_keys(row['age'])

    weight_input = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$toolweight")
    weight_input.clear()
    weight_input.send_keys(row['weight'])
    
    height_input = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$ht")
    height_input.clear()
    height_input.send_keys(row['height'])

    # Click the corresponding button for sex
    if (row['sex'] == "male"):
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_sex1").click()
    else:
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_sex2").click()

    # Click the calculate button
    driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$btnCalculate").click()

    # Wait until the results loaded
    wait = WebDriverWait(driver, 5)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_lbrs1"))).click()

    # Grab the results for both risk calculators
    major_osteoporotic_risk = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lbrs1")
    hip_fracture_risk = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lbrs2")

    # Add results to a new dataframe

    results_df = results_df.append({
        'age': row['age'],
        'weight': row['weight'],
        'height': row['height'],
        'sex': row['sex'],
        'major osteoporotic risk': major_osteoporotic_risk.text,
        'hip fracture risk': hip_fracture_risk.text
    }, ignore_index=True)


    print(major_osteoporotic_risk.text, hip_fracture_risk.text)

# Print the results to the output file

results_df.to_csv(args.ofile, index=False)





