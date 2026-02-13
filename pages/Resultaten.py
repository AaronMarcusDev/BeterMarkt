import streamlit as st

resultaten = st.session_state.get("zoekresultaten", [])

st.title(f"Resultaten 📑 ({len(resultaten)})")
st.markdown("---")


st.write("") # Behoud voor layout
cols = st.columns([1, 3])
with cols[0]:
    if st.button("⬅️ Terug"):
            st.switch_page("BeterMarkt.py")
with cols[1]:
    st.write("Dit zijn de gevonden resultaten die het beste overeenkomen met de zoekopdracht:")

st.markdown("---")

if resultaten:
    for listing in resultaten:
        title = listing[0]
        description = listing[1]
        seller = listing[2]
        price = str(listing[3])
        location = listing[4]
        image_url = listing[5]
        url = listing[6]

        cols = st.columns([1, 4])
        with cols[0]:
            # Kleine thumbnail, klikbaar
            st.markdown(f"""
            <a href="{url}" target="_blank">
                <img src="{image_url}" width="200" style="border-radius: 5px;" />
            </a>
            """, unsafe_allow_html=True)
            st.markdown(f"##### €{price}")
        with cols[1]:
            st.markdown(f"##### {title}") # 0 = Titel
            st.write(f"Beschrijving: {description}") # 1 = Beschrijving
            st.write(f" Verkoper: {seller}")
            if location.distance == 0:
                st.write(f"📍 {location.city} | <1 km")
            else:
                st.write(f"📍 {location.city} | {location.distance / 1000} km")
            st.link_button(f"Open '{title}' in marktplaats ↗️", url)
        st.markdown("---")
else:
    st.markdown("##### Geen resultaten gevonden 😭")
