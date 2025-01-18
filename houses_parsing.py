from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

with open('links/houses_links.txt', 'r') as file:
    links = [line.strip() for line in file]

link_beginning = 'https://krisha.kz'
all_property_data = []
counter = 0
driver = webdriver.Chrome()

for link in links:

    print(f"Processing link {counter}: {link_beginning + link}")

    try:

        content = requests.get(link_beginning + link).text
        soup = BeautifulSoup(content, 'html.parser')

        number_of_rooms = soup.find_all('h1', class_='')

        district = soup.find_all('span', class_='')

        area = soup.find_all('div', class_='offer__advert-short-info')

        year_of_construction = area[7]

        floors = area[6]

        plot_area = area[5]

        area = area[3]

        driver.get(link_beginning + link)

        price_element = driver.find_element(By.CLASS_NAME, "offer__price")

        advert_price = price_element.text
        price = ''.join(advert_price.split()[:-1])

        property_data = {'Price': price,
                         'NumberOfRooms': number_of_rooms[0].text.split('· ')[1].split(' ')[0],
                         'District': district[2].text.split(', ')[-1].split(' ')[0],
                         'YearOfConstruction': year_of_construction.text,
                         'Area': area.text.split(' ')[0],
                         'PlotArea': plot_area.text.split(' ')[0],
                         'NumberOfFloors': floors.text.split(' ')[0],
                         'Link': link}
        # print(property_data)

        all_property_data.append(property_data)
    except Exception as e:
        print(f"Error processing link {counter}: {e}")

    finally:
        time.sleep(0.5)
        counter += 1

df = pd.DataFrame(all_property_data)
df.to_csv('datasets/houses_data.csv', index=False)
