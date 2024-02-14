from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.edge import service
from scrapper.common import connect, Inject_login_cookies
from firebase_admin import storage
import os
import datetime
from pyspark.sql.types import StructType, StructField, StringType   


def upload_firebase(fileName: str, folder_name: str = "ticket_ids"):
    # Get a reference to the storage bucket
    bucket = storage.bucket()
    # Specify the folder name
    file = fileName.split("/")[-1]
    # Upload the file to the folder
    blob = bucket.blob(f"{folder_name}/{file}")
    blob.upload_from_filename(fileName)

    # Optional: Delete the local CSV file after upload
    # os.remove(fileName)
    print("File saved")

    # Print the public URL of the uploaded file
    print("Your file URL:", blob.public_url)


def ticket_scanner(df, spark):
    filtered_list = df.select("Ticket").rdd.flatMap(lambda x: x).collect()
    driver = connect()
    driver.get("http://support.timsoft-solutions.com/ticket")
    Inject_login_cookies(driver)
    wait = WebDriverWait(driver, 70)
    iteration_count = 0 
    filtered_count = 0
    error_count = 0
    
    # Move repetitive code outside the loop
    driver.get("http://support.timsoft-solutions.com/ticket")
    Inject_login_cookies(driver)
    list_data = []
    start_time = datetime.datetime.now()
    half_hour = datetime.timedelta(minutes=20)
    iteration_count += 1 
    filtered_count = 0
    error_count = 0
    
    for url in filtered_list:
        elapsed_time = datetime.datetime.now() - start_time
        if elapsed_time >= half_hour:
            print("Half an hour has passed. Exiting the loop.")
            break
                
        if iteration_count == 20 or filtered_count == 8: 
            driver.close()
            time.sleep(10)
            driver = connect()
            driver.get("http://support.timsoft-solutions.com/ticket")
            Inject_login_cookies(driver)
            iteration_count = 0 
        if iteration_count == 300:
            error_count += 1
            print("number of ids passed is : ", error_count)
            break
        try:
            # Perform actions on the page (e.g., scraping, interaction)
            url_detail = f"http://support.timsoft-solutions.com/ticket/detail/{url}"
            driver.get(url_detail)  # Open the URL
            time.sleep(3)
            # Use implicit waits instead of time.sleep()
            wait = WebDriverWait(driver, 30)  # Set the timeout to 30 seconds
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ball-scale-multiple")))
            sujet_xpath = '//input[@placeholder="Entrer Sujet" or @placeholder="Enter Subject"]'
            sujet_element = driver.find_element(By.XPATH, sujet_xpath)
            sujet_text = driver.execute_script("return arguments[0].value;", sujet_element)
            wait = WebDriverWait(driver, 10)
            ifram_element_1 = wait.until(EC.presence_of_element_located((By.XPATH, '(//td[@class="k-editable-area"]//iframe)[1]')))

            # Execute JavaScript to get the text content of the first iframe
            description = driver.execute_script("return arguments[0].contentDocument.body.innerText;", ifram_element_1)

            # Switch to the second iframe
            ifram_element_2 = driver.find_element(By.XPATH, '(//td[@class="k-editable-area"]//iframe)[2]')

            # Execute JavaScript to get the text content of the second iframe
            solution = driver.execute_script("return arguments[0].contentDocument.body.innerText;", ifram_element_2)

            list_data.append([url, sujet_text, description, solution])
            driver.switch_to.default_content()
            print(list_data[-1])
        except Exception as e:
            print("error", {e})
            error_count += 1
            print("number of ids passed is : ", error_count)
            continue

    driver.close()
    
    df = spark.createDataFrame(list_data, ["url", "sujet_text", "description", "solution"])
    current_datetime = datetime.datetime.now()
    filename = f"tickets_ids_{current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    df_tickets = df.select("url").withColumnRenamed("url", "Ticket")
    # to be changed with your locale directory's project path !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    filepath = f"C:/Users/ahafsi/timsoftScrapper/{filename}"
    df_tickets.write.mode('overwrite').csv(filepath, header=True)
        # upload ticket ids to firebase
    try:
        for file in os.listdir(filepath):
            if file.endswith(".csv"):
                upload_firebase(os.path.join(filepath, file))
    except PermissionError as e:
        print(f"PermissionError: {e}")
    return df, driver

