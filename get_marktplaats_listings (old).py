from datetime import datetime, timedelta

from marktplaats import SearchQuery, SortBy, SortOrder, Condition, category_from_name


def get_listings(search_term, category, postcode, number_of_listings, max_price, distance_radius, has_included_words: bool, included_words, has_excluded_sellers: bool, excluded_sellers):
    include_words_list = included_words.split(",")
    exclude_sellers_list = excluded_sellers.split(",")

    search = SearchQuery(search_term, # Search query
                        zip_code=postcode, # Zip code to base distance from
                        distance=distance_radius*1000, # Max distance from the zip code for listings
                        price_from=0, # Lowest price to search for
                        price_to=max_price, # Highest price to search for
                        limit=number_of_listings, # Max listings (page size, max 100)
                        offset=0, # Offset for listings (page * limit)
                        sort_by=SortBy.LOCATION, # DATE, PRICE, LOCATION, OPTIMIZED
                        sort_order=SortOrder.ASC, # ASCending or DESCending
                        condition=Condition.USED, # NEW, AS_GOOD_AS_NEW, USED or category-specific
                        offered_since=datetime.now() - timedelta(days=1000), # Filter listings since a point in time
                        category=category_from_name(category)) # Filter in specific category (L1) or subcategory (L2)

    listings = search.get_listings()

    final_listings = [] # What is going to be left after filtering

    listing_number = 1
    for listing in listings:
        skip = False
        
        if has_included_words:
            for item in include_words_list:
                if item.lower().strip() in listing.title.lower() or item in listing.description.lower():
                    skip = False
                else:
                    skip = True

        if has_excluded_sellers:
            for item in exclude_sellers_list:
                if item.lower().strip() in listing.seller.get_seller().name.lower():
                    skip = True

        if skip:
            continue
        
        ## print(' Listing no.' + str(listing_number) + " - " + str(listing.price) + " euro - " + listing.title)
        ## print(" Beschrijving: " + listing.description)
        ## print(" Locatie afstand en stad: " + str(listing.location.distance / 1000) + " km - " + listing.location.city)

    #print(listing.price_as_string(lang="nl"))
    #print(listing.price_type)
        
    # the location object
    # print(listing.location)
        
        # the date object
        #print(listing.date)

        ## print(" Verkoper: " + listing.seller.get_seller().name)
        ## print(" Linkje: " + listing.link)

        #for image in listing.images:
        #print(image.medium)

        ## print("\n" + ("*" * 100) + "\n")

        final_listings.append((
            listing.title, 
            listing.description, 
            listing.seller.get_seller().name, 
            listing.price,
            listing.location, 
            listing.images[0].medium, 
            listing.link
            ))

        listing_number += 1
    
    return final_listings