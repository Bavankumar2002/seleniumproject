from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import sqlite3


#Execute webdriver path 
chrome_driver_path = "C:/Users/bavan/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

urls = [
    "https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/astc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile",
    "https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile"
]

# Initialize a list to store the data
bus_data = []



def extract_bus_details(url):
    print("Test ->1")
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    #Looping the Routes
    for i in range(3,12):
        try:#try-2
            print("Test-> 2")
            route_name = driver.find_element(By.XPATH, '//*[@class="D117_main D117_container"]/div['+str(i)+']/div[1]/a').text
            route_link = driver.find_element(By.XPATH, '//*[@class="D117_main D117_container"]/div['+str(i)+']/div/a').get_attribute("href")
            #Clicking Route
            element = driver.find_element(By.XPATH, '//*[@class="D117_main D117_container"]/div['+str(i)+']/div[1]/a')
            driver.execute_script("arguments[0].click();", element)
            time.sleep(5)
            #Click View Buses
            view_seat = driver.find_element(By.XPATH, '//*[@class="button"]')
            view_seat.click()
            time.sleep(5)

            #Looping the Buses
            for j in range(1,20):
                try: #tyr-3
                    print("Test -> 3")
                    bus_name=driver.find_element(By.XPATH, '//*[@class ="bus-items"]/li['+str(j)+']//*[@class ="travels lh-24 f-bold d-color"]').text
                    bus_type=driver.find_element(By.XPATH, '//*[@class ="bus-items"]/li['+str(j)+']//*[@class ="bus-type f-12 m-top-16 l-color evBus"]').text
                    departure_time = driver.find_element(By.XPATH, '//*[@class ="bus-items"]/li['+str(j)+']//*[@class ="dp-time f-19 d-color f-bold"]').text
                    arrival_time = driver.find_element(By.XPATH, '//*[@class ="bus-items"]/li['+str(j)+']//*[@class ="bp-time f-19 d-color disp-Inline"]').text
                    duration = driver.find_element(By.XPATH, '//*[@class ="bus-items"]/li['+str(j)+']//*[@class ="dur l-color lh-24"]').text
                    star_rating = driver.find_element(By.XPATH, '//*[@class ="bus-items"]/li['+str(j)+']//*/span').text
                    price = driver.find_element(By.XPATH, '//*[@class ="bus-items"]/li['+str(j)+']//*[@class ="f-19 f-bold"]').text
                    seat_ava = driver.find_element(By.XPATH, '//*[@class ="bus-items"]/li['+str(j)+']//*[@class ="column-eight w-15 fl"]').text

                    #Appending the values
                    bus_data.append({
                                            "Route Name": route_name,
                                            "Route Link": route_link,
                                            "Bus Name": bus_name,
                                            "Bus Type": bus_type,
                                            "Departing Time": departure_time,
                                            "Reaching Time": arrival_time,
                                            "Duration Time": duration,
                                            "Star Rating": star_rating,
                                            "Price": price,
                                            "Seats Available": seat_ava
                                        })
                except Exception as e: #Catch-3
                    #print("Bus count"+str(j)+ " --Exception: "+str(e))
                    continue
            print("Go one step back")
            #driver.close()
            driver.get(url)
            print("URL Opened")
            time.sleep(5)


        except:#catch-2
            continue
    print("Close")


# Loop through each URL and extract bus details
for url in urls:
    try: #Try-1
        extract_bus_details(url)
    except: #catch-1
        continue

driver.quit()

# Convert the data to a DataFrame and save it to a CSV file
df = pd.DataFrame(data= bus_data)
df.to_csv('Sample_government_state_bus_routes.csv', index=False)

print("Data extracted and saved to 'government_state_bus_routes.csv'")

# Convert the data to a DataFrame and save it to a database file
connection = sqlite3.connect("test1.db")
cursor = connection.cursor()
qry = "CREATE TABLE IF NOT EXISTS data_bus(route_name, route_link, bus_name, bus_type, departure_time, arrival_time, duration, star_rating, price,seat_ava)"
cursor.execute(qry)
for p in range(len(df)):
    cursor.execute("insert into data_bus values(?,?,?,?,?,?,?,?,?,?)",df.iloc[p])

connection.commit()
connection.close()

