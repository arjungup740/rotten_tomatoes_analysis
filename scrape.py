import pandas as pd
import rottentomatoes as rt
import time
import pickle
import requests
############################## Boxoffice mojo 

def scrape_mojo_table(url):

    response = requests.get(url, verify=False) ## needed the false to get it to work
    tables = pd.read_html(response.content)
    df = tables[0]

    # df.to_pickle('mojo_world_2023.pkl')
    # df.to_pickle(f'{filename}.pkl')
    # print('pickled')

    return df

# df = scrape_mojo_table('https://www.boxofficemojo.com/year/world/2023/', 'mojo_world_2023')
# df = scrape_mojo_table('https://www.boxofficemojo.com/year/2023/?grossesOption=totalGrosses', 'mojo_domestic_in_year_releases_2023')

suffix = 'calendar_grosses_domestic_2023'
mojo_df = scrape_mojo_table('https://www.boxofficemojo.com/year/2023/?grossesOption=calendarGrosses')

mojo_df.to_pickle(f'mojo_{suffix}.pkl')

############################## rotten tomatoes from mojo list

######## Read in data from box office mojo

mojo_df = pd.read_pickle(f'mojo_{suffix}.pkl')
mojo_df[['Worldwide', 'Domestic', 'Foreign']] = mojo_df[['Worldwide', 'Domestic', 'Foreign']].apply(lambda x: x.str.replace(',', '').str.replace('$', ''))
mojo_df[['Worldwide', 'Domestic', 'Foreign']] = mojo_df[['Worldwide', 'Domestic', 'Foreign']].apply(lambda x: pd.to_numeric(x, errors='coerce'))


def scrape_rt(scrape_list, filename):

    start = time.time()
    movie_objs_list = []
    error_dict = {}
    for movie_name in scrape_list:
        print(f'beginning {movie_name}')
        try:
            movie = rt.Movie(movie_name)
            movie_objs_list.append(movie)
        except Exception as e:
            print(f'hit error {e} on {movie_name}')
            error_dict[movie_name] = e
        time.sleep(1)
    print(f'pulling {len(scrape_list)} took {time.time() - start}') # 765 

    with open(f'{filename}.pkl', 'wb') as file:
        pickle.dump(movie_objs_list, file)

    return movie_objs_list

# scrape_list = mojo_df['Release Group']
# filename = 'movie_objs_list_world_2023'
# movie_objs_list = scrape_rt(scrape_list, filename)

scrape_list = mojo_df['Release']
filename = f'movie_objs_list_{suffix}'
movie_objs_list = scrape_rt(scrape_list, filename)

with open(f'movie_objs_list_{suffix}.pkl', 'rb') as file:
    # Load the pickled object
    movie_objs_list = pickle.load(file)

data_list = []
# Iterate over each object in the list and extract its attributes
for obj in movie_objs_list:
    data_list.append({
        'movie_title': obj.movie_title,
        'synopsis': obj.synopsis,
        'tomatometer': obj.tomatometer,
        'audience_score': obj.audience_score,
        'weighted_score': obj.weighted_score,
        'genres': obj.genres,
        'rating': obj.rating,
        'duration': obj.duration,
        'year_released': obj.year_released,
        'actors': obj.actors,
        'directors': obj.directors,
        'image': obj.image,
        'url': obj.url,
        'critics_consensus': obj.critics_consensus,
        'num_of_reviews': obj.num_of_reviews
    })

# Convert the list of dictionaries to a DataFrame
rt_df = pd.DataFrame(data_list)

filename = f'rt_df_{suffix}'
with open(f'{filename}.pkl', 'wb') as file:
        pickle.dump(rt_df, file)

###### rescrapes

scrape_list = ["Trolls Band Together", "Renaissance: A Film by Beyoncé", "The Pope's Exorcist", "Pathaan", "The Blind", "Jawan", "Animal", "His Only Son", "After Death", "Demon Slayer: Kimetsu No Yaiba - To the Swords...", "Salaar", "Dunki", "BTS: Yet to Come in Cinemas", "The Chosen Season 3 Finale", "Waitress: The Musical", "Tiger 3", "Mummies", "Ponniyin Selvan: Part Two", "Left Behind: Rise of the Antichrist", "The Journey: A Music Special from Andrea Bocelli", "The Wandering Earth II", "2023 Oscar Nominated Short Films: Live Action", "Tu Jhoothi Main Makkaar", "Come Out in Jesus Name", "Skinamarink", "Winnie-the-Pooh: Blood and Honey", "Fear", "Lost in the Stars", "Creation of the Gods I: Kingdom of Storms", "American Fiction", "The Retirement Plan", "That Time I Got Reincarnated as a Slime the Mo...", "The First Slam Dunk", "Billie Eilish Live at the O2", "Camp Hideout", "Close", "Emily", "Inside",]
filename = 'rescrape'
rescrape = scrape_rt(scrape_list, filename)

movie_name = "Trolls Band Together"
movie = rt.Movie(movie_name)