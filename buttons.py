import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.get("https://dabinmusic.com/pages/tours")
driver.execute_script("window.scrollTo(1,10000)")

time.sleep(5)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

event_month_list = []
event_month = soup.find_all('div', class_="calendar-list-event__date__month")
months = [month.get_text() for month in event_month]
event_month_list.append(months)

event_day_list = []
event_day = soup.find_all('div', class_="calendar-list-event__date__day" )
days = [day.get_text() for day in event_day]
event_day_list.append(days)


location = soup.find_all('div', class_="eca-flex eca-flex__center")
locations = [loc.get_text() for loc in location]
location_list = [loc[14:] for loc in locations]
dates = ([(a,b,c) for a,b,c in zip(event_month_list[0], event_day_list[0], location_list)])
print(dates)
driver.quit()
