""" Search Wikipedia and get article excerpts. """

import requests
from bs4 import BeautifulSoup
from re import sub



def get_article(article_name):
    """get_article(string) -> string
    
    Searches wikipedia for given article_name string,
    and returns a string with the title and description
    of the first article found.
    """
    try:
        search_results = api_search(article_name)

        for article in search_results:
            if not article['description']:
                article['description'] = first_paragraph(article['url'])

        first_article = search_results[0]
        result = first_article['description']


    except requests.exceptions.ConnectionError:
        result = "Sorry, couldn't connect to Wikipedia."
        
    except ValueError:
        result = "Sorry, didn't find anything for \"{search}\"".format(search=article_name)

    return result
    
        
    
def api_search(article_name, lang='pl', results=3):
    """api_search(string, [string]) -> list

    Using the MediaWiki API, search wikipedia for given article_name
    and return a list of dicts containing the server's response.
    Each dict contains the keys: 'title', 'description', 'url'.
    """
    url = "http://www.wikipedia.org/w/api.php"
    params = search_params(article_name, lang=lang, results=results)

    response = requests.get(url, params)
    if response:
        results_list = response.json()
        results = to_dict(results_list)
        return results
    else:
        raise ValueError



def first_paragraph(article_url):
    """Download the wikipedia article under a given url
    and return its first paragraph."""

    html = requests.get(article_url).text

    page = BeautifulSoup(html, 'html.parser')
    article_body = page.find(id='bodyContent')

    # Removes the tables - they contain <p> elements sometimes,
    # so the search finds that element instead of the article's
    # first paragraph.
    tables = article_body.find_all('table')
    for table in tables:
        table.decompose() # delete from html

    first_paragraph = article_body.p
    paragraph_text = first_paragraph.get_text()

    # Removes the '[10]' citation numbers.
    clean_text = sub(r'\[\d+\]', '', paragraph_text)
    
    return clean_text



def search_params(article_name, lang='pl', results=2):
    """search_params(string, [string, int]) -> dict

    Construct and return a dict containing parameters
    for the Wikipedia MediaWiki API.
    """

    # play around with different parameters or find new ones:
    # https://en.wikipedia.org/wiki/Special:ApiSandbox
    params = {
        'search': article_name,
        'uselang' : lang,
        'limit' : results,
        'action': 'opensearch',
        'format': 'json',
        'namespace': 0,
        'redirects': 'return',
        'suggest': ''
    }
    return params


def to_dict(response_array):
    """to_dict(list) -> dict

    Convert a MediaWiki API JSON response from a messy array to
    a more usable dict format. Expected array format:
    [ search_string, [result_titles], [result_descriptions], [result_urls] ]
    """
    query, titles, descriptions, urls = response_array

    dicted = []
    grouped = zip(titles, descriptions, urls)
    keys = ['title', 'description', 'url']

    for values in grouped:
        element = dict(zip(keys, values))
        dicted.append(element)

    return dicted

