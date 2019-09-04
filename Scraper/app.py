# Dependencies for BeautifulSoup
import urllib3
from bs4 import BeautifulSoup
import requests

# Dependencies for CoveoPush
from coveopush import CoveoPush
from coveopush import Document
from coveopush import CoveoPermissions
from coveopush.CoveoConstants import Constants

# Setup connection to the push api
sourceId = 'alexandreperronpokemonchallenge433qfaz2-tu6fhunq47rndpmxfb3lkvsfpi'
orgId = 'alexandreperronpokemonchallenge433qfaz2'
apiKey = 'xx218f6373-c0a7-4a1e-9ea3-b768c6ec1d3b'
push = CoveoPush.Push(sourceId, orgId, apiKey)

# Strat scraping
url = 'https://pokemondb.net/pokedex/all'
req = urllib3.PoolManager()
res = req.request('GET', url)
soup = BeautifulSoup(res.data, 'html.parser')
pokemons = soup.find('table', {'id': 'pokedex'}).findAll('td', {'class': 'cell-name'})

# Loop trought pokemons found
for entry in pokemons:

    # Find name and link to pokemon page
    name = entry.find('a').text
    link = 'https://pokemondb.net'+entry.find('a')['href']

    # Scrape trought the pokemon page
    url = link
    req = urllib3.PoolManager()
    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')

    # Get the image
    pic_url = soup.find('a',{'rel':'lightbox'}).find('img')['src']

    # Get all pokemon types for this pokemon
    poke_types_entry = soup.find('table',{'class':'vitals-table'}).findAll('tr')[1].findAll('a')

    # Get generation (Generation 1 or Generation 2)
    generation = soup.findAll('div',{'class':'grid-row'})[0].find('abbr').text

    # Get the pokemon number
    number = soup.find('table',{'class':'vitals-table'}).findAll('tr')[0].find('strong').text

    # Make a string with the types separated by semicolumn
    # This is for the multi value facet
    poke_type = ""
    for pokemon_type in poke_types_entry:
        poke_type += pokemon_type.text+";"
    poke_type = poke_type[:-1]

    # This make sure that there are no special characthers
    try:
        print(name)
    except:
        name = name[:-1]

    # First add the document
    mydoc = Document(link)

    # Set plain text
    mydoc.SetData(name +' '+poke_type.replace(";", " ")+' '+generation)

    # Set FileExtension
    mydoc.FileExtension = ".html"

    # Add Metadata
    mydoc.AddMetadata("connectortype", "HTML")
    mydoc.AddMetadata("pokemon_name", name)
    mydoc.AddMetadata("pokemon_picture", pic_url)
    mydoc.AddMetadata("pokemon_type", poke_type)
    mydoc.AddMetadata("pokemon_generation", generation[len(generation)-1:])
    mydoc.AddMetadata("pokemon_number", number)

    # Set the title
    mydoc.Title = name

    # Push the document
    push.AddSingleDocument(mydoc)
