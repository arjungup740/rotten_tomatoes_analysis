import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_mojo_table(url, filename):

    response = requests.get(url, verify=False) ## needed the false to get it to work
    tables = pd.read_html(response.content)
    df = tables[0]

    # df.to_pickle('mojo_world_2023.pkl')
    df.to_pickle(f'{filename}.pkl')
    print('pickled')

    return df

df = scrape_mojo_table('https://www.boxofficemojo.com/year/world/2023/', 'mojo_world_2023')
df = scrape_mojo_table('https://www.boxofficemojo.com/year/2023/?grossesOption=calendarGrosses', 'mojo_domestic_calendar_grosses_2023')
df = scrape_mojo_table('https://www.boxofficemojo.com/year/2023/?grossesOption=totalGrosses', 'mojo_domestic_in_year_releases_2023')
