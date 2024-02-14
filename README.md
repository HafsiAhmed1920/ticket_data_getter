# Timesoft Scrapper - Comprehensive Project Readme

## Project Overview

Welcome to the Timesoft Scrapper, your essential guide for efficient data scraping! The project is situated in the "Downloads" folder under the name "timesoft-scrapper."

### Setup

1. **Accessing the Project:**
   - Navigate to the "Downloads" folder.
   - Locate the project folder named "timesoft-scrapper."
   - Open it using VSCode: Right-click and select "Open with VSCode."
   - Alternatively, open VSCode and click on the project; it will open the last code you worked on.

   **Note:** Avoid moving the project folder unless you understand the implications, as it contains paths that need updating if relocated.

### Code Execution

To run the code efficiently, follow these steps:

1. **Run the Ticket IDs Getter:**
   - Execute the `ticket_ids_getter.py` file.
   - It fetches ticket IDs, filters out previously scraped ones, and passes new tickets to the main scraper.

### Configuration Options

Adjust the code according to your preferences:

1. **Time and Page Limit:**
   - Modify time limit: Locate the line with "half_hour = datetime.timedelta(minutes=20)" in `tickets_getter.py`.
   - Adjust the number of minutes as needed (recommended: 30).

   - Remove page limit: In `tickets_ids_getter.py`, find the while loop around line 80.
   - Delete the second condition (`i < 3`) for unlimited scraping.
   - If removing the limit, change the line to "select.select_by_value("100")" instead of "select.select_by_value("20")".

 

2. **Connect Function in `scrapper.common.py`:**
   - Around line 16, in the `connect` function in `scrapper.common.py`, you can remove the headless option by uncommenting it.
   - Uncomment the line `# options.add_argument('--headless')` to run the scraper in a non-headless mode.

!!!!!!!!!!!!!!!!! Urgent Note :  **After Changes:** Save the file, then write  `pip install e .` in the terminal within the setup.py directory before rerunning the code. 
   this will make the code aware of the changes in your modules !!!! 

### Data Handling

The scraped data is saved locally and in the Firebase account. Clear existing data before performing a fresh scrape.

1. **Firebase Access:**
   - Credentials: fireon552@gmail.com / 4Share#@.
   - Access the storage and open your bucket using [Firebase Console](https://console.firebase.google.com/project/timesoft-fad2f/storage/timesoft-fad2f.appspot.com/files).

### Resource Considerations

Beware that the code demands significant resources. Adjust timing and data limits cautiously to prevent overloading your computer.

### Data Output

- **Local Machine:** Find the output in the "ticket_data" folder, saved as a PySpark DataFrame.
- **Firebase:** Learn how to use the reader in `Common.reader.reader.py` for Firebase data.

### Environment

- **Environment Setup:**
  - Hadoop 3.3.6
  - Java 1.8.0 (JDK)
  - Python 3.11.4
  - PySpark 3.4.2
  - Selenium
  - Firebase
  - Regex
  - Retry

### Integration Advice ( if ever you wanna integrate it in another computer or server ) 

If integrating elsewhere:

- Install a 64-bit version of the environment mentioned below.
- Create a virtual environment and install required packages:

  ```
  pip install pyspark==3.4.2
  pip install selenium
  pip install regex
  pip install retry
  pip install pandas
  pip install firebase-admin
  ```

### Additional Details

- **Output Data Format:**
  - Local data: Stored in the "ticket_data" folder, formatted as a PySpark DataFrame.
  - Firebase data: Utilize the reader in `Common.reader.reader.py` for optimal retrieval.

- **Data Manipulation:**
  - Explore online platforms like Databricks or Deepnote for effective manipulation and visualization of the scraped data.

### Important Reminder

Be cautious when modifying the code and always save a backup. If significant changes are made, save a copy named "timesoftscrapper," place it in the "Downloads" folder, and run it with Python 3.11.4.

Feel free to explore advanced features and tools for an enhanced experience. If issues arise, consult online resources and maintain a backup copy. Happy scraping!
Good Luck!
Best of luck with your Timesoft Scrapper project! Remember, if you make significant code changes, save a copy named "timesoftscrapper," place it in the "Downloads" folder, and run it with Python 3.11.4.

Feel free to explore data visualization tools like Databricks or Deepnote for an enhanced experience. If issues arise, consult online resources and maintain a backup copy. Happy scraping!
