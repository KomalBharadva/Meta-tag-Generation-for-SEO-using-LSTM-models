###############################
# IMPORTS
import numpy as np
from bs4 import BeautifulSoup  # Parse HTML data
import requests  # Get data from servers on the web
from requests.exceptions import Timeout
import concurrent.futures  # Enables threading or multiprocessing
import pickle
import time
###############################

###############################
# USEFUL FUNCTIONS
###############################


def read_file(file_path):
    """Parse a file and returns a Python list splitting in every new line.

    Args:
        file_path (str): path to the file.

    Output:
        lines_list: list with each line of the file being a item.
    """
    try:
        with open(file_path, 'r') as f:
            file_text = f.read()
            # json.loads() read the json text from a string
            lines_list = file_text.split('\n')
            return lines_list
    # From Python 3.3 IOError is an alias for OSError. Also, file_pathNotFoundError
    # is a subclass of OSError
    except OSError:
        print(f'Could not open or read from {f}')


def get_metadata(url):
    print(url)
    try:
        r = requests.get(url, timeout=(3, 10))
        soup = BeautifulSoup(r.content, features="lxml")
        meta = soup.find_all('meta')
        content = []
        for tag in meta:
            if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
                content.append(tag.attrs['content'])
        print(content)
    except Timeout:
        content = ['Connection timed out']
        print(content)
    except:
        content = ["Link blocked"]
        print(content)
    return content

###############################
# GET THE METATAGS FROM THE LINKS
###############################


file_names = ['links_list_bigrams2_lemmed.txt',
              'links_list_bigrams2_lemmed.txt',
              'links_list_trigrams1_lemmed.txt',
              'links_list_trigrams2_lemmed.txt',
              'links_list_trigrams3_lemmed.txt',
              'links_list_trigrams4_lemmed.txt',
              'links_list_trigrams5_lemmed.txt',
              'links_list_trigrams6_lemmed.txt']

names_to_save = ['bigrams1',
                 'bigrams2',
                 'trigrams1',
                 'trigrams2',
                 'trigrams3',
                 'trigrams4',
                 'trigrams5',
                 'trigrams6']

path_linux = '/home/marcelo/Dropbox/Marcelo/Mestrado/NCI/Data_Mining_and_Machine_Learning_2/project/'
# path_windows = "C:\\Users\\marce\\Dropbox\\Marcelo\\Mestrado\\NCI\\Data_Mining_and_Machine_Learning_2\\project\\"

for i, file in enumerate(file_names):
    links_list = read_file(path_linux + f'{file}')

    start = time.time()
    # Run the function in different threads so that it doesn't wait until the
    # previous one is finished to start the next one on the list.
    # It returns a generator object which has to be casted to list.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        metatags_generator = executor.map(get_metadata, links_list)
    end = time.time()

    metatags_lst = list(metatags_generator)
    print(metatags_lst)
    print(f'\nTook {(end-start)/60} minutes to complete.\n')

    print(f'Saving the file metatags_lst as a pkl file...\n')
    # Save the metatags list object
    pickle.dump(metatags_lst, open(
        path_linux + f'pickles/metatags_{names_to_save[i]}_linux.pkl', 'wb'))

    print(f'Saving complete. Starting the next list if it exists...\n')
