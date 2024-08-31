Redbus Data Scraping with Selenium DOCUMENTATION
--------------------------------------------------------------------------------

1. Sample image dict
          goto ---> "StreamLit\img"
   
   ![States page](https://github.com/user-attachments/assets/f7f9832e-1225-4fde-b7a1-7adecd90cd90)
   ![Bus Selection page](https://github.com/user-attachments/assets/28b27d5f-223e-453d-8b22-05f86ea2714e)
   ![Filter_1](https://github.com/user-attachments/assets/d0ed51fb-4dff-4dc5-b118-5e727413b29f)
   ![Filter_2](https://github.com/user-attachments/assets/112f3041-d0de-4f0f-a49f-579c8a9403fb)





3. Selenium code for web scraping and MySQL database interaction are in the folder
          
          goto ---> “Web Scrapping & upload to DB\Final_full_scraping_to_DB.ipynb"

          Install packages
            ! pip install selenium
            ! pip install pandas
          
          - Created the empty list to store the collected data during the scraping
          - Select the states to scrap the data
          - Use page navigation for next page
          - Loop the states to scrap the data and store it as key values pair in list in bus_routes = []
          - Next loop through the bus_routes and get link ,routes name, state name
          - Loop the link to collect each routes data
          - Collect the data in each bus_routes through the link and store the data in bus_details = []
          - Use pandas to convert the collected data to dataframe to connect to DB


4. MySQL connection

          - Install package
              ! pip instal mysql-connector

          - Create the DB connection and
          - CREATE TABLE to add data in DB
          - INSERT THE DATA by looping through the dataframe
          - Close all DB connections


5. StreamLit app located in 
          goto ---> "StreamLit\redbus.py"
    
          - Import the packages
              import pandas as pd
              import streamlit as st
              from streamlit_option_menu import option_menu
              import mysql.connector as db
          
          - Connect to MySQL DB and convert the data to DataFrame using the pandas
          - Used if conditions to filter the data and display using st.write function

