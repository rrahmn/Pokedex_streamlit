import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd
import requests
import numpy as np

st.title("Pokedex!")

# Display image of pokemon! (latest sprite from front!)
# Add the audio of the latest battle cry!
# Use whole pokedex!
# use the pokemon type to change colour of barchart!
# Make it look better!
# Stretch version -> display the many sprites from the API!

# Decorator makes it run once
# functions are taken as the argument into another function and then called inside the wrapper function.
@st.cache_data
def get_all_links():
    """return list of all pokemon links"""
    url = 'https://pokeapi.co/api/v2/pokemon/?offset=0&limit=1000000000000'
    response = requests.get(url)
    pokemon = response.json()
    pokemon = pokemon['results']
    links = [pok['url'] for pok in pokemon]
    return links

@st.cache_data
def get_details(poke_link):
	try:
		response = requests.get(poke_link)
		pokemon = response.json()
		return pokemon['name'], pokemon['height'], pokemon['weight'], len(pokemon['moves']), pokemon['sprites']['front_default'], pokemon['sprites']['front_shiny'], pokemon['cries']['latest']
	except:
		return 'Error', np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN
	
all_pokemon_links = get_all_links()
pokemon_number = st.slider("Pick a pokemon",
						   min_value=1,
						   max_value=len(all_pokemon_links)
						   )

name, height, weight, moves, sprite, shiny_sprite, cry = get_details(all_pokemon_links[pokemon_number - 1])
height = height * 10


height_data = pd.DataFrame({
	            'Pokemon': ['Weedle', name, 'victreebell'],
	            'Heights': [30, height, 170]
               })

colours = ['gray', 'red', 'gray']

graph = sns.barplot(data = height_data,
					x = 'Pokemon',
					y = 'Heights',
					palette = colours)



# Formatting

	
col1, col2, col3, col4 = st.columns(4)


with col1:
    st.write(f'Name:')
    st.write(f'Height:')
    st.write(f'Weight:')
    st.write(f'Move Count:')
	
with col2:
    st.write(name.title())
    st.write(height)
    st.write(weight)
    st.write(moves)

with col3:
    shine_on = st.toggle("Make it shiny", value = False)

    if shine_on:
        st.image(shiny_sprite, use_column_width = True)
    else:
        st.image(sprite, use_column_width = True)

with col4:
    st.write("Cry")
    st.audio(cry)

st.pyplot(graph.figure)



	

