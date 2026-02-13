import streamlit as st
import pydeck as pdk
import pandas as pd
from datetime import datetime, timedelta
from marktplaats import SearchQuery, SortBy, SortOrder, Condition, category_from_name
from get_postcode_data import postcode_data
from get_marktplaats_listings import get_listings
from categories import category_list

# Titel
st.title("BeterMarkt 🔎")
st.write('###### *Een geoptimaliseerde Marktplaats zoektool*')

# Query's
#query = st.text_input("Zoekterm", placeholder="Fiets")

query = st.text_input("Zoekterm", value=st.session_state.get("query", ""), placeholder="Fiets",)
st.session_state["query"] = query

cat_index = st.session_state.get("category_index", 0)
if not isinstance(cat_index, int) or not (0 <= cat_index < len(category_list)):
    cat_index = 0
category = st.selectbox(
    "Categorie",
    category_list,
    index=cat_index
)
st.session_state["category_index"] = category_list.index(category)

correct_postcode = False
postcode_input = st.text_input("Postcode", value=st.session_state.get("postcode", ""), placeholder="1234AB")
st.session_state["postcode"] = postcode_input

if postcode_data(postcode_input)[0] == "onjuiste postcode":
    st.error("Dit is geen geldige postcode.")
else:
    correct_postcode = True

max_results = st.slider("Aantal advertenties", 1, 100, 30)

st.markdown('---')
st.write('###### Aanvullende opties:')

max_price = 900000
max_price_checkbox = st.checkbox("Maximale prijs", value=st.session_state.get("max_price_checkbox", False))
if max_price_checkbox:
    max_price = st.slider("€", 1, 500, value=st.session_state.get("max_price", 50))
    st.session_state["max_price"] = max_price
st.session_state["max_price_checkbox"] = max_price_checkbox

max_km = 900000
km_limit_checkbox = st.checkbox("Maximale afstand", value=st.session_state.get("km_limit_checkbox", False))
if km_limit_checkbox:
    max_km = st.slider("Kilometer radius:", 1, 100, value=st.session_state.get("max_km", 50))
    st.session_state["max_km"] = max_km
st.session_state["km_limit_checkbox"] = km_limit_checkbox

include_words = "" # Purely for defining
include_words_checkbox = st.checkbox("Moet bepaalde woorden bevatten", value=st.session_state.get("include_words_checkbox", False))
if include_words_checkbox:
    include_words = st.text_area("Zoekwoorden: (splits met komma's)", value=st.session_state.get("include_words", ""))
    st.session_state["include_words"] = include_words
st.session_state["include_words_checkbox"] = include_words_checkbox

exclude_sellers = "" # Purely for defining
exclude_sellers_checkbox = st.checkbox("Verkopers uitsluiten", value=st.session_state.get("exclude_sellers_checkbox", False))
if exclude_sellers_checkbox:
    exclude_sellers = st.text_area("Uit te sluiten verkopers: (splits met komma's)", value=st.session_state.get("exclude_sellers", ""), placeholder="Catawiki")
    st.write("Let op! Schrijf de volledige gebruikersnaam, dus niet een deel van de naam zoals 'a.'")
st.session_state["exclude_sellers_checkbox"] = exclude_sellers_checkbox

st.markdown('---')

if km_limit_checkbox and postcode_input:
    city, lat, lon = postcode_data(postcode_input)

# Als km_limit is geselecteerd, toon de kaart met de zoekradius
try:
    if km_limit_checkbox and lat and lon:
        st.markdown(f"##### 📍 Zoekgebied: {str(max_km)}km radius van {postcode_input}, {city}")
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=lat,
                longitude=lon,
                zoom=8,
                pitch=0,
            ),
            map_style="mapbox://styles/mapbox/light-v9",
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=pd.DataFrame([{"lat": lat, "lon": lon}]),
                    get_position='[lon, lat]',
                    get_color='[0, 100, 255, 160]',
                    get_radius=max_km * 1000,  # radius in meters
                )
            ]
        ))
    elif not km_limit_checkbox:
        pass
    else:
        st.error("Kan locatiegegevens niet ophalen. Klopt de postcode wel?")
except:
            st.error("We konden de locatiegegevens niet ophalen, klopt de postcode wel?")

searching_active = False
if st.button("Zoeken"):
    searching_active = True
    if searching_active:
        st.markdown("### 🔎 Aan het zoeken...")

    #print("\n\n")
    listings = get_listings(query, category, postcode_input, max_results, max_price, max_km, include_words_checkbox, include_words, exclude_sellers_checkbox, exclude_sellers)
    #print(listings)
    st.session_state["zoekresultaten"] = listings

    searching_active = False
    st.switch_page("pages/Resultaten.py")