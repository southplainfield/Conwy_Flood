#to scrape zoopla _NEXT_DATA_ element. A goldmine, get it while you can.
##################################
# Import
from bs4 import BeautifulSoup
import json
import requests
from os import environ, path, curdir, listdir
import csv
from time import sleep, time
from urllib.parse import urlencode, urlunparse
from datetime import datetime
from retry import retry

##################################
# Configurations
csv_path = '<<PATH>>'
location = 'all'
start_time = time()

def get_uprn_list(csv_path, csv_file):
    #open file
    uprn = []
    file = open(path.join(csv_path,csv_file))
    csvreader = csv.reader(file)
    for row in csvreader:
        text = row[0]
        uprn.append(text)
    print(uprn)
    return uprn


@retry()
def get_data(uprn):


    #house_data = {}
    page = requests.get(f"https://www.zoopla.co.uk/property/uprn/{uprn}")
    soup = BeautifulSoup(page.content, 'html.parser')
    core = soup.find(id="__NEXT_DATA__").text
    my_json = json.loads(core)

    if (my_json['props']['pageProps']['data']['property']['address']) is not None:

        house_data = dict({'id': uprn})
        house_data['address'] = (my_json['props']['pageProps']['data']['property']['address']['fullAddress'])
        house_data['longitude'] = (my_json['props']['pageProps']['data']['property']['address']['longitude'])
        house_data['latitude'] = (my_json['props']['pageProps']['data']['property']['address']['latitude'])

        if (my_json['props']['pageProps']['data']['property']['attributes']) is not None:
            house_data['tenure'] = (my_json['props']['pageProps']['data']['property']['attributes']['tenure'])
            house_data['propertyType'] = (my_json['props']['pageProps']['data']['property']['attributes']['propertyType'])
            house_data['bathrooms'] = (my_json['props']['pageProps']['data']['property']['attributes']['bathrooms'])
            house_data['bedrooms'] = (my_json['props']['pageProps']['data']['property']['attributes']['bedrooms'])
            house_data['floorAreaSqM'] = (my_json['props']['pageProps']['data']['property']['attributes']['floorAreaSqM'])
            house_data['livingRooms'] = (my_json['props']['pageProps']['data']['property']['attributes']['livingRooms'])

        if (my_json['props']['pageProps']['data']['property']['saleEstimate']) is not None:
            house_data['currentPrice'] = (my_json['props']['pageProps']['data']['property']['saleEstimate']['currentPrice'])
            # try:
            #     house_data['oldestestimate'] = (
            #     my_json['props']['pageProps']['data']['property']['saleEstimates'][0]['currentPrice'])
            #     house_data['oldestestimatedate'] = (
            #     my_json['props']['pageProps']['data']['property']['saleEstimates'][0]['builtAt'])
            # except TypeError as e:
            #     house_data['oldestestimate'] = ''

        return house_data

    return None

def run_for_one(csv_file):
    data=[]
    for uprn in get_uprn_list(csv_path,csv_file):

        lap_time = time()
        i = 0
        i += 1
        url = urlunparse(['http', 'www.zoopla.co.uk', f'property/uprn/{uprn}', '', '', ''])
        print("Loading", url)
        house_data = get_data(uprn)
        if house_data is not None:
            data += [house_data]
        sleep(0.1)

    print('DONE! ', len(data), f'houses extracted in T: {round((time() - start_time) / 60)}min)')

    columns = ['id','location','address','property_type','longitude','latitude','currentPrice','tenure','propertyType', 'bathrooms','bedrooms','floorAreaSqM','livingRooms']

    try:
        with open(csv_file + 'zoopla' + datetime.now().strftime("%Y%m%d") + '.csv', 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=columns)
            writer.writeheader()
            for key in data:
                print(key)
                writer.writerow(key)
    except IOError:
        print("I/O error")

for file in listdir(csv_path):
    run_for_one(file)