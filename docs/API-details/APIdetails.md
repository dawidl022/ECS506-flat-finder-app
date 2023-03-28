# Accessing the APIs
# Things to point out first
Gathered info on 2 APIs which are Zoopla and Zoopla(rapidapi), yes theyre they are both zoopla but its very difficult to find any free APIs which provide the info were looking for. <br>
Zoopla it seems its abit more difficult to get an API key since you must be approved first <br>
Zoopla(rapidapi) - you can get instant access to the API for free <br> <br>

## Zoopla (rapidapi)
### Getting API key
Sign into [rapidapi](https://rapidapi.com/) and subscribe to the [Zoopla API](https://rapidapi.com/apidojo/api/zoopla/) (Basic is free and instant access) and you will be given an API key
### Example HTTP Request
These are the params that we will need to use in our applicaiton when making a request:
<ul>
    <li>area - (like search) which takes a string of the location of interest</li>
    <li>order_by - sort results by either 'price' or 'age' of listings</li>
    <li>ordering - 'descending'(default) or 'ascending' results</li>
    <li>radius - find listings within a certain radius of specified latitude&longitude</li>
    <li>listing_status - set for properites that are either 'sale' or 'rent', we obviously want rent only properties</li>
    <li>page_size - set size of list that is returned max 100</li>
    <li>page_number - set page number of the listings returned</li>
</ul> <br>

This api requires us to make queries using http headers, here is what a request that we would use would look like in python using the requests library:
```python
import requests

url = "https://zoopla.p.rapidapi.com/properties/list"

querystring = {"area":"Whitechapel","order_by":"price","ordering":"descending","radius":"5","listing_status":"rent","page_number":"1","page_size":"1"}

headers = {
	"X-RapidAPI-Key": API_KEY,
	"X-RapidAPI-Host": "zoopla.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
```

response.json() will allow us to use the results and will be in the format:

    {
        "result_count" : NUMBER_OF_LISTINGS,
        "longitude" : LONGITUDE,
        "area_name" : AREA_NAME,
        "listing" : [
            {
                "rental_prices" : {...},
                ...
            },...
        ]
    }
response is quite long so here is a file of an example one:
https://github.com/dawidl022/ECS506-flat-finder-app/blob/docs/19-investigate-uk-accomodation-apis/docs/API-details/rapidapi_sample_response.json


<br> <br>
## Zoopla API
### Getting API key
To get API key you have to both register a Zoopla Developer Account and the application here (it can take time to get a key): <br>
https://developer.zoopla.co.uk/ <br> <br>
### Example HTTP Request
Here is simple API request that will return a list of properties with the postcode E1:

    http://api.zoopla.co.uk/api/v1/property_listings.js?postcode=E1&api_key={API KEY HERE}

This request will return a JSON response in the format:<br>

    {
        "result_count" : NUMBER_OF_LISTINGS,
        "listing" : [
            {
                "listing_id" : ID_OF_LISTING,
                ...
            },...
        ]
    }

To see in details about the listing result set as it is quite long, details are mentioned here at the bottom of the page: <br>

https://developer.zoopla.co.uk/docs/read/Property_listings <br>

The request can be modified further by adding more parameters for more specific requests, the ones that are relevant to our specification are, here is an example of a more specific request that is closer to what we will be using: <br>
(Lets say we want properties in Whitechapel within a 5 mile radius sorted by most recent) <br>

    http://api.zoopla.co.uk/api/v1/property_listings.js?area=Whitechapel&order_by=age&ordering=ascending&radius=5&listing_status=rent&page_size=10&page_number=1&api_key={API KEY HERE}

<br>

### Notes
Zoopla API supports multiple data formats, im using json in the example but they support more incase we should use that instead which are: <br>
<ul>
    <li>JSON</li>
    <li>XML</li>
    <li>RSS</li>
    <li>YAML</li>
    <li>JSONML</li>
    <li>Pearl Dumper</li>
    <li>Pearl Storable</li>
</ul>
See details on all the parameters and making requests here: <br>

https://developer.zoopla.co.uk/docs/read/Property_listings <br> <br>

When using zoopla api we must mention on the page that it is 'powered by Zoopla' as mentioned here: <br>

https://developer.zoopla.co.uk/home