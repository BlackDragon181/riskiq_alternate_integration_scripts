# Use json to dump data to send in request
import json

# Use requests to make and send request
import requests

# This line is to disable warning when you send request
requests.packages.urllib3.disable_warnings()

# THis is the host to send request
host = "https://ws.riskiq.net/v1/"


# Use this header in request to get response in json format
headers = {"Accept": "application/json", "Content-Type": "application/json", "Accept-Encoding": "gzip"}

token = "put_here_token"  # String Token
key = "put_here_key"  # String Key

# I instantiate a session object
session = requests.Session()

# Set token and key in session to make request
session.auth = requests.auth.HTTPBasicAuth(token, key)

# Set header in session to make request
session.headers.update(headers)


def requester(url, parameters=None, input_timeout=60):

    conecction_error = False
    timeout = input_timeout

    # I make the url to send response, with url to serach and host
    api_url = "{0}{1}".format(host, url)

    response = {}
    response['data'] = None
    response['scroll'] = None
    response['status'] = 0

    # I make and send the request
    try:
        if parameters is None:
            parameters = {}
        # To Debug_________________________________________________
        print("Parameters is: {}".format(json.dumps(parameters)))
        print("Send POST Request ,to {}".format(api_url))
        # _________________________________________________________

        res = session.post(api_url, data=json.dumps(parameters), timeout=timeout, stream=False)
        # To Debug_________________________________________________
        print("Response of Request POST obtain")
        # _________________________________________________________

    except requests.Timeout as e:
        print("ERROR: {}".format(e))
        response['status'] = -2
        conecction_error = True
    except requests.ConnectionError as e:
        print("ERROR: {}".format(e))
        response['status'] = -1
        conecction_error = True

    # If don't have any error in connection:
    if not conecction_error:

        # If response is 200, parse json
        if res.status_code == 200:
            if res.text != '':
                response['data'] = res.json()

        # But if response is another code, i print the response to see error
        else:
            response['status'] = -1
            try:
                print("Response is:{}".format(res.json()))
            except json.decoder.JSONDecodeError:
                print("Response is:{}".format(res.text))

    return response


# filetr: filter to make search
# limit: amount of assets you want get, default is all assets
# retry: amount of retry you want make, if fail request
def search_assets(filters, limit=None, retry=5):
    count_retry = retry
    while count_retry > 0:
        # Variables to make search
        # empty list to save assets
        assets_list = []
        # string to save id of search(scroll)
        scroll = None
        # limit of assets to get in a response
        MAX_QUERY = 1000
        query_limit = MAX_QUERY

        while True:
            # Calculate the amount of assets to request in the request
            if limit is not None:
                left_to_retrieve = limit - len(assets_list)
                if left_to_retrieve <= 0:
                    count_retry = 0
                    break
                if left_to_retrieve > MAX_QUERY:
                    query_limit = MAX_QUERY
                else:
                    query_limit = left_to_retrieve

            # Make url to send request
            if scroll is None:
                base_url = "/inventory/search?results={0}&scroll".format(query_limit)
            else:
                base_url = "/inventory/search?results={0}&scroll={1}".format(query_limit, scroll)

            # # Debug______________________________________________________________________________________________________________________
            # count = count + 1
            # print("Send Request {} to search. Base url: '{}' . And Filters is: '{}'".format(count, base_url, filters))
            # # ___________________________________________________________________________________________________________________________
            response = requester(base_url, parameters=filters)
            # # ____________________________________________________________________________________________________________________________
            # print("The status of request is: '{}'".format(response['status']))
            # # ____________________________________________________________________________________________________________________________

            if response['status'] != 0:
                count_retry = count_retry - 1
                break

            scroll = response['data']['scroll']
            # print("The scroll is: {}".format(scroll))
            total_to_retrieve = response['data']['totalResults']
            # print("The total to retrive is: {}".format(total_to_retrieve))
            assets_list = assets_list + response['data']['inventoryAsset']
            # print("The List of Assets is: {}".format(assets_list))

            if len(assets_list) >= total_to_retrieve:
                count_retry = 0
                break

    # if result is 0 asset ,returned None
    if len(assets_list) == 0:
        return None
    return assets_list


def main():
    # Here I make filter to search: Organization !empty | Status in ("Confirmed") | Type in ("Host") | Tag !in ("App - Cloud", "Deloitte Subcontractor", "Affiliate", "IP-HOP", "InQualys")
    filter_param = {
        "filters": [
            {
                "filters": [
                    {
                        "field": "organization",
                        "value": True,
                        "type": "NOT_NULL",
                    }
                ]
            }, {
                "filters": [
                    {
                        "field": "inventoryState",
                        "value": "CONFIRMED",
                        "type": "IN"
                    }
                ]
            }, {
                "filters": [
                    {
                        "field": "assetType",
                        "type": "IN",
                        "value": "HOST"
                    }
                ]
            }, {
                "filters": [
                    {
                        "field": "tag",
                        "value": '"App - Cloud","Deloitte Subcontractor","Affiliate","IP-HOP","InQualys"',
                        "type": "NOT_IN"
                    }
                ]
            }
        ]
    }

    # Call search_assets funtion to make search of assets with thtat filter
    assets = search_assets(filter_param)

    # print(assets)
    print(len(assets))


if __name__ == '__main__':
    main()
