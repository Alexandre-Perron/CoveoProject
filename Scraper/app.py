import urllib3
from bs4 import BeautifulSoup
import csv
import requests
import os
import sys
import time
from coveopush import CoveoPush
from coveopush import Document
from coveopush import CoveoPermissions
from coveopush.CoveoConstants import Constants

url = 'https://pokemondb.net/pokedex/all'
req = urllib3.PoolManager()
res = req.request('GET', url)
soup = BeautifulSoup(res.data, 'html.parser')
pokemons = soup.find('table', {'id': 'pokedex'}).findAll('td', {'class': 'cell-name'})
x=0
for entry in pokemons:
    pokelist = []
    pokelist.append('pokemon_name, pokemon_url')
    name = entry.find('a').text
    link = 'https://pokemondb.net'+entry.find('a')['href']

    url = link
    req = urllib3.PoolManager()
    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')

    pic_url = soup.find('a',{'rel':'lightbox'}).find('img')['src']
    poke_types_entry = soup.find('table',{'class':'vitals-table'}).findAll('tr')[1].findAll('a')
    poke_type = ""
    for pokemon_type in poke_types_entry:
        poke_type += pokemon_type.text+", "
    poke_type = poke_type[:-1]
    try:
        print(name)
    except:
        name = name[:-1]
    pokelist.append([name,link,pic_url,poke_type])

    sourceId = 'alexandreperronpokemonchallenge433qfaz2-tu6fhunq47rndpmxfb3lkvsfpi'
    orgId = 'alexandreperronpokemonchallenge433qfaz2'
    apiKey = 'xx218f6373-c0a7-4a1e-9ea3-b768c6ec1d3b'

    # Setup the push client
    push = CoveoPush.Push(sourceId, orgId, apiKey)

    # First add the document
    mydoc = Document(pokelist[1][1])
    # Set plain text
    mydoc.SetData(pokelist[1][0] +' '+pokelist[1][1])
    # Set FileExtension
    mydoc.FileExtension = ".html"
    # Add Metadata
    mydoc.AddMetadata("connectortype", "HTML")
    mydoc.AddMetadata("pokemon_name", pokelist[1][0])
    mydoc.AddMetadata("pokemon_picture", pokelist[1][2])
    mydoc.AddMetadata("pokemon_type", pokelist[1][3])
    # Set the title
    mydoc.Title = pokelist[1][0]
    # Push the document
    push.AddSingleDocument(mydoc)
    x+=1
    if x >= 25:
        break