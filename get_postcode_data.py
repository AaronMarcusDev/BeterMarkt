import requests

def postcode_data(postcode: str):
    url = f"https://free.bedrijfsdata.nl/v1.1/postcode?country_code=NL&postcode={postcode}"
    response = requests.get(url)

    if response.json()["wrong_postcode"] == 1:
        return "onjuiste postcode", "", ""

    try:
        return (response.json()["postcode"][0]["city"], response.json()["postcode"][0]["lat"], response.json()["postcode"][0]["lon"])
        #                       ^-- Stad                                    ^-- Latitude                            ^-- Longitute
    except:
        return "error", "", ""

#Example response:
#
#{
#    "status": "ok",
#    "success": 1,
#    "wrong_postcode": 0,
#    "message": "good postcode",
#    "found": 1,
#    "postcode": [
#        {
#            "postcode": "1013PN",
#            "city": "Amsterdam", # <-- Nodig!
#            "admin1": "Noord-Holland",
#            "admin2": "Gemeente Amsterdam",
#            "admin3": null,
#            "lat": 52.3893, # <-- Nodig!
#            "lon": 4.8871   # <-- Nodig!
#        }
#    ]
#}