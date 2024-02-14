from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from firebase_admin import storage
from scrapper.common import (
    connect,
    Inject_login_cookies,
    get_current_page,
    click_next_button
)
import time
from pyspark.sql.types import StructType, StructField, StringType
from firebase_config.fireConf import initialise_firebase
import os
import datetime
from Common.reader.reader import reader
from scrapper.tickets_Getter import ticket_scanner
from data_Cleaning.spark_config import SparkConfig
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data_Cleaning.Spark_cleaner import clean_text


spark_config = SparkConfig()
spark = spark_config.spark


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


driver = connect()
driver.get("http://support.timsoft-solutions.com/ticket")
Inject_login_cookies(driver)
driver.get("http://support.timsoft-solutions.com/ticket")
time.sleep(20)
# Wait for the dropdown button to be present
dropdown_button = WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='dropdown']/button[@type='button']"))
)

# Check if the dropdown button is inside the viewport
if not dropdown_button.is_displayed():
    # Scroll to the dropdown button
    driver.execute_script("arguments[0].scrollIntoView();", dropdown_button)

# Wait for the element to be clickable before clicking
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown']/button[@type='button']"))).click()

# Wait for the 'Tickets Terminés' or 'Completed Tickets' option to be clickable
ticket_termines = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-item ng-star-inserted' and (contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'tickets terminés') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'completed tickets'))]"))
)

# Check if the 'Tickets Terminés' or 'Completed Tickets' option is inside the viewport
if not ticket_termines.is_displayed():
    # Scroll to the 'Tickets Terminés' or 'Completed Tickets' option
    driver.execute_script("arguments[0].scrollIntoView();", ticket_termines)

# Click on the 'Tickets Terminés' or 'Completed Tickets' option
ticket_termines.click()

# make it show 100 ticket by page instead of 10
select_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/div/ng-component/div/div[2]/div/div/div/div/div[2]/ticket-commongrid/div[3]/span/select")))
select = Select(select_element)
select.select_by_value("100")

tickets_data = []
i = 0
while True:
    try:
        elements = WebDriverWait(driver, 25).until(
            EC.presence_of_all_elements_located((By.XPATH, '//td/span[starts-with(text(), "Ticket-")]'))
        )
        tickets_data.extend(element.text for element in elements)
        # Wait for the next page button to appear
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination")))
        # Print the current page number
        print(f"Current page: {get_current_page(driver)}")

        if not click_next_button(driver):
            break
    except Exception as e:
        print("error", {e})
driver.close()
filtered_tuple = [(item,) for item in tickets_data if 'Ticket-' in item]

schema = StructType([StructField("Ticket", StringType(), True)])
# Create DataFrame
df = spark.createDataFrame(filtered_tuple, schema)
filename = f"tickets_ids_{datetime.date.today()}.csv"

# to be changed with your locale directory's project path !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
filepath = f"C:/Users/ahafsi/timsoftScrapper/{filename}"
# check the history of the tickets
initialise_firebase()
try:
    history_df = reader("ticket_ids/")
    # Create a DataFrame new_df that contains the new ids that are not processed yet.
    new_df = df.join(history_df, df.Ticket == history_df.Ticket, "left_anti")
    new_df = new_df.dropDuplicates()

    # Save the DataFrame as a CSV file
    new_df.write.mode('overwrite').csv(filepath, header=True)
except Exception as e:
    new_df = df


# scrape the data of the new ticketspip i 
finale_data, mydriver = ticket_scanner(new_df, spark)
print(finale_data.count())
finale_data = clean_text(finale_data)
finale_data = finale_data.repartition(10)  # Adjust the number of partitions
print(finale_data.count())

# upload finale_data to firebase
try:

    finale_folder_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    finale_folder_path = f"ticket_data/{finale_folder_name}"
    finale_data.write.mode('overwrite').csv(finale_folder_path, header=True)
    for file in os.listdir(finale_folder_path):
        if file.endswith(".csv"):
            upload_firebase(os.path.join(finale_folder_path, file), finale_folder_path)
except PermissionError as e:
    print(f"PermissionError: {e}")
    # to be changed with your locale directory's project path !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    filepath = f"C:/Users/ahafsi/timsoftScrapper/{filename}"
mydriver.quit()

