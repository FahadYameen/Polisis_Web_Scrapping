import csv
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

output_file = open('polisis_output.csv', 'w')
fieldnames = ["Data_Type_Handled", "Data_Collection_Purpose"]
newFileWriter = csv.DictWriter(output_file, fieldnames=fieldnames)

data_type_handled_list = ['computer information', 'contact', 'cookies and tracking elements', 'demographic', 'financial', 'health', 'ip address and device ids',
                          'location', 'personal identifier', 'social media data', 'survey data', 'user online activities', 'user profile', 'generic personal information', 'other data']
data_collection_purpose_list = ['additional service feature', 'advertising', 'analytics research', 'basic service feature', 'legal requirement',
                                'marketing', 'merger acquisition', 'personalization customization', 'service operation and security', 'service operation and security', 'other purposes']
url_file = open('polisis_urls.txt')
urls = url_file.readlines()
output_file = open('polisis_output.csv', 'w')

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
chrome_driver_binary = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(chrome_options=options)
for url in urls:
    row = {}
    if(url != 'none'):
        vendor_data_type_handle = []
        vendor_data_collection_purpose = []
        try:
            driver.get(url)
            inputElement1 = WebDriverWait(driver, 200).until(
                EC.presence_of_element_located((By.ID, "googleSankey")))
            extracted_list = inputElement1.text.split('\n')
            extracted_list = [x.lower() for x in extracted_list]

            for extracted_value in extracted_list:
                if extracted_value in data_type_handled_list:
                    vendor_data_type_handle.append(extracted_value)
                elif(extracted_value in data_collection_purpose_list):
                    vendor_data_collection_purpose.append(extracted_value)

            print("**** Data type handled ******")
            print(vendor_data_type_handle)

            print("***** Data collection ******")
            print(vendor_data_collection_purpose)

            row['Data_Type_Handled'] = vendor_data_type_handle
            row['Data_Collection_Purpose'] = vendor_data_collection_purpose
            newFileWriter.writerow(row)

        except:
            traceback.print_exc()
            row['Data_Type_Handled'] = 'timeout'
            row['Data_Collection_Purpose'] = 'timeout'
            newFileWriter.writerow(row)

    else:
        row['Data_Type_Handled'] = 'none'
        row['Data_Collection_Purpose'] = 'none'
        newFileWriter.writerow(row)


driver.close()
output_file.close()
