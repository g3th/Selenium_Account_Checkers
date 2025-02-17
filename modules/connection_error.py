import requests
from socket import gaierror
from bs4 import BeautifulSoup as soup
from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import ConnectionError


def connection_error_try_block(service_name):
    # populate list as more services are added
    services = ['espn', 'directTV']
    country = None
    try:
        get_current_ip = 'https://ipcost.com/'
        request = requests.get(get_current_ip)
        parse_request = soup(request.content, 'html.parser')
        get_IP = parse_request.find('span', attrs={'class': 'dr ipv4'})
        get_Location = parse_request.find_all('div', attrs={'class': 'e'})
        for text in get_Location:
            if 'Country' in str(text):
                country = text.text.replace("\t", "").replace("\n", "").replace("Country", "")
            if 'No location' in str(text):
                print('No Location data was found for current IP.\nEnding')
                exit()
        print('Current IP: {}'.format(get_IP.text))
        print('Current Location: {}'.format(country))
        if [service for service in services if (service_name in service)] and 'US' not in str(country):
            print('Please use a US IP to check accounts.\nEnding.')
            exit()
    except (gaierror, NewConnectionError, ConnectionError):
        print("Can't connect, please check your connection\nEnding")
        exit()


