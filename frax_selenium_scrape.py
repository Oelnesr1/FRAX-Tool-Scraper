from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
import pandas as pd
import numpy as np
import platform
import os
import time
import argparse 

# Initialize arguments

parser = argparse.ArgumentParser(prog = "FRAX Selenium Scraper",
                                 description = "This program is a Selenium-based web scraper to use the FRAX Fracture Risk Assessment Tool Webpage"
                                 )
parser.add_argument('-infile', required=False, help = "An input file. If not defined, the input file will be 'frax_data.csv'", nargs = "?", default = "frax_data.csv")
parser.add_argument('-ofile', required=False, help = "An output file. If not defined, the output file will be 'frax_results.csv'", nargs = "?", default = "frax_results.csv")

args = parser.parse_args()

# Check the platform system and use the right name for the Chrome driver for cross-platform compatibility

if (platform.system() == 'Darwin' or platform.system() == 'Linux'):
    chromedriver_name = 'chromedriver'
elif (platform.system() == 'Windows'):
    chromedriver_name = 'chromedriver.exe'
else:
    raise Exception('This may not be supported in your operating system.')

# Initialize selenium

service = Service(os.path.join(os.getcwd(), chromedriver_name))
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Initialize pandas

df = pd.read_csv(args.infile)
results_df = pd.DataFrame(columns = np.append(df.columns.values, ['major osteoporotic risk', 'hip fracture risk']))

country_df = pd.read_csv('frax_country_ids.csv')
country_dict = country_df.set_index('country')['id'].to_dict()

optional_parameters = {
    'previous fracture': "ctl00_ContentPlaceHolder1_previousfracture2",
    'parent fractured hip': "ctl00_ContentPlaceHolder1_pfracturehip2",
    'current smoking': "ctl00_ContentPlaceHolder1_currentsmoker2",
    'glucocorticoids': "ctl00_ContentPlaceHolder1_glucocorticoids2",
    'rheumatoid arthritis': "ctl00_ContentPlaceHolder1_arthritis2",
    'secondary osteoporosis': "ctl00_ContentPlaceHolder1_osteoporosis2",
    'alcohol >3': "ctl00_ContentPlaceHolder1_alcohol2",
}

for index, row in df.iterrows():

    # Reloading the webpage is more consistent than clearing form data
    
    if 'country' in df.columns and row['country'] != "":
        country_id = country_dict[row['country']]
        driver.get("https://frax.shef.ac.uk/FRAX/tool.aspx?country="+str(country_id))
    else:
        driver.get('https://frax.shef.ac.uk/FRAX/tool.aspx')

    # Must pause for 3 seconds or we will receive an error from the webpage's API of accessing the calculator too fast
    time.sleep(3)

    # Add age, weight, and height into the webform
    age_input = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_toolage")
    weight_input = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_toolweight")
    height_input = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ht")

    age_input.send_keys(row['age'])
    weight_input.send_keys(row['weight'])
    height_input.send_keys(row['height'])

    # Click the corresponding button for sex
    if (row['sex'] == "male"):
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_sex1").click()
    else:
        driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_sex2").click()

    for (key, value) in optional_parameters.items():
        if (key in df.columns and row[key]):
            driver.find_element(By.ID, value).click()

    # NM = No Measurement, or in other words, to leave this part blank

    if ('femoral neck bmd unit' in df.columns and row['femoral neck bmd unit'] != "NM"):
        select = Select(driver.find_element(By.ID, "dxa"))
        select.select_by_visible_text(row['femoral neck bmd unit'])

        # Alert appears when clicking "T-Score" specifically, so have to wait and close the alert before proceeding
        if (row['femoral neck bmd unit'] == "T-Score"):
                wait = WebDriverWait(driver, timeout=0.5)
                alert = wait.until(lambda d : d.switch_to.alert)
                text = alert.text
                alert.accept()

        driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_bmd_input").send_keys(row['femoral neck bmd value'])

    # Click the calculate button
    driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnCalculate").click()

    # Wait until the results loaded
    wait = WebDriverWait(driver, 5)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_lbrs1"))).click()

    # Grab the results for both risk calculators
    major_osteoporotic_risk = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lbrs1")
    hip_fracture_risk = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_lbrs2")

    # Add results to a new dataframe

    results_df = pd.concat([results_df, 
        pd.DataFrame([np.append(row, [major_osteoporotic_risk.text, hip_fracture_risk.text])], 
                     columns=results_df.columns)], 
                     ignore_index=True)

    # Print results to console to make sure the program is running properly
    print(np.append(row, [major_osteoporotic_risk.text, hip_fracture_risk.text]))

# Print the results to the output file

results_df.to_csv(args.ofile, index=False)