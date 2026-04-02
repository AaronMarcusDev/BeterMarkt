from datetime import datetime, timedelta
from marktplaats import SearchQuery, SortBy, SortOrder, Condition, category_from_name


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
    # Prepare filters
    include_words_list = [w.strip().lower() for w in included_words.split(",") if w.strip()]
    exclude_sellers_list = [w.strip().lower() for w in excluded_sellers.split(",") if w.strip()]

    # Build search query
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

    listings = search.get_listings()
    final_listings = []

    for listing in listings:
        skip = False

        # --- Include words filter ---
        if has_included_words and include_words_list:
            title = listing.title.lower()
            desc = listing.description.lower()

            # must match at least ONE include word
            if not any(word in title or word in desc for word in include_words_list):
                skip = True

        # --- Excluded sellers filter ---
        if has_excluded_sellers and exclude_sellers_list:
            seller_name = listing.seller.name.lower()

            if any(bad in seller_name for bad in exclude_sellers_list):
                skip = True

        if skip:
            continue

        # --- Safe image access ---
        image_url = listing.images[0].medium if listing.images else None

        # --- Build tuple (7 items, same as before) ---
        final_listings.append((
            listing.title,
            listing.description,
            listing.seller.name,   # NO get_seller() anymore
            listing.price,
            listing.location,
            image_url,
            listing.link
        ))

    return final_listings
