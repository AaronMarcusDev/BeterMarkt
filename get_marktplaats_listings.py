from datetime import datetime, timedelta
from marktplaats import SearchQuery, SortBy, SortOrder, Condition, category_from_name

category_list = [
    "Antiek en Kunst", 
    "Audio, Tv en Foto", 
    "Auto's",
    "Auto-onderdelen",
    "Auto diversen",
    "Boeken",
    "Caravans en Kamperen",
    "Cd's en Dvd's",
    "Computers en Software",
    "Contacten en Berichten",
    "Diensten en Vakmensen",
    "Dieren en Toebehoren",
    "Doe-het-zelf en Verbouw",
    "Fietsen en Brommers",
    "Hobby en Vrije tijd",
    "Huis en Inrichting",
    "Huizen en Kamers",
    "Kinderen en Baby's",
    "Kleding | Dames",
    "Kleding | Heren",
    "Motoren",
    "Muziek en Instrumenten",
    "Postzegels en Munten",
    "Sieraden, Tassen en Uiterlijk",
    "Spelcomputers en Games",
    "Sport en Fitness",
    "Telecommunicatie",
    "Tickets en Kaartjes",
    "Tuin en Terras",
    "Vacatures",
    "Vakantie",
    "Verzamelen",
    "Watersport en Boten",
    "Witgoed en Apparatuur",
    "Zakelijke goederen",
    "Diversen",
    "Doorzoek alles",
]
    

def get_listings(
    search_term,
    category,
    postcode,
    number_of_listings,
    max_price,
    distance_radius,
    has_included_words: bool,
    included_words,
    has_excluded_sellers: bool,
    excluded_sellers
):
    include_words_list = [w.strip().lower() for w in included_words.split(",") if w.strip()]
    exclude_sellers_list = [w.strip().lower() for w in excluded_sellers.split(",") if w.strip()]

    if category == "Doorzoek alles":
        raw_listings = []
        for cat in category_list:
            if cat == "Doorzoek alles":  # also fixed `is` → `==`
                continue
            curr_search = SearchQuery(
                search_term,
                zip_code=postcode,
                distance=distance_radius, # * 1000,
                price_from=0,
                price_to=max_price,
                limit=number_of_listings,
                offset=0,
                sort_by=SortBy.LOCATION,
                sort_order=SortOrder.ASC,
                condition=Condition.USED,
                offered_since=datetime.now() - timedelta(days=1000),
                category=category_from_name(cat)  # use `cat`, not `category_list[index]`
            )
            raw_listings.extend(curr_search.get_listings())
    else:
        search = SearchQuery(
            search_term,
            zip_code=postcode,
            distance=distance_radius * 1000,
            price_from=0,
            price_to=max_price,
            limit=number_of_listings,
            offset=0,
            sort_by=SortBy.LOCATION,
            sort_order=SortOrder.ASC,
            condition=Condition.USED,
            offered_since=datetime.now() - timedelta(days=1000),
            category=category_from_name(category)
        )
        raw_listings = search.get_listings()

    final_listings = []
    for listing in raw_listings:
        skip = False

        if has_included_words and include_words_list:
            title = listing.title.lower()
            desc = listing.description.lower()
            if not any(word in title or word in desc for word in include_words_list):
                skip = True

        if has_excluded_sellers and exclude_sellers_list:
            seller_name = listing.seller.name.lower()
            if any(bad in seller_name for bad in exclude_sellers_list):
                skip = True

        if skip:
            continue

        image_url = listing.images[0].medium if listing.images else None
        final_listings.append((
            listing.title,
            listing.description,
            listing.seller.name,
            listing.price,
            listing.location,
            image_url,
            listing.link
        ))

    return final_listings