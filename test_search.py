from api_response import api_response

"""

Main search file will be committed when it is fully working aka user inputs into search form, and result is returned

The main file has been tested and works by communicating with API and returning what you see in api_response.py

Use this file to test/work on the search function so we don't waste API free tier limit.
apiResponse is what will be returned when we communicate with the API.

Current bugs: 

Everything else seems to be working fine.

"""


# print(type(apiResponse))
# print(len(apiResponse['data']['search']['results'][0]['part']['sellers']))
def test_search(quantity, api_response=api_response):
    sellers = {}
    counter = 0  # counter to calculate number of results to be used in other functions.
    for i in range(len(api_response['data']['search']['results'][0]['part']['sellers'])):
        x = (api_response['data']['search']['results'][0]['part']['sellers'][i])
        counter += 1
        sellers[i + 1] = x

    # check inventory level of each key and make sure it is not equal to zero
    # if seller has 0 inventory level, remove them from result
    sellers_with_stock = {}  # dictionary to store sellers that have stock
    j = 0
    for i in range(len(sellers)):
        if sellers[i + 1]['offers'][0]['inventory_level'] >= quantity:  # check if inventory matches quantity
            j += 1
            sellers_with_stock[j] = sellers[i + 1]

    # check each seller
    # for key, value in sellers_with_stock.items():
    #     print(key, ' : ', value)

    sellers_final_check = {}
    # check each sellers' order multiple = none, if not then check if quantity is bigger than or equal to it
    # order multiple is the min order quantity set by seller
    z = 0
    for i in range(len(sellers_with_stock)):
        if str(sellers_with_stock[i + 1]['offers'][0]['order_multiple']) == "None" or (
                sellers_with_stock[i + 1]['offers'][0]['order_multiple']) <= quantity:
            z += 1
            sellers_final_check[z] = sellers_with_stock[i + 1]

    # algorithm to calculate the cost depending on specified quantity on sellers that passed all checks
    # if quantity/price combo is less than or equal to specified quantity, multiplies quantity by that price
    # lists to be zipped together into a dictionary
    prices_list = []
    quantity_list = []
    prices_quantity = {}  # dictionary to store final zipped lists using same key value as sellers_final_check
    for i in range(len(sellers_final_check)):  # iterate all sellers
        for j in range(len(sellers_final_check[i + 1]['offers'])):  # check how many offers seller has
            for z in range(len(sellers_final_check[i + 1]['offers'][j]['prices'])):  # loop over the prices of offer
                # for y in range(len(sellers_final_check[i + 1]['offers'][j]['prices'][z])):  # loop over prices of offer
                x1 = sellers_final_check[i + 1]['offers'][j]['prices'][z]['quantity']
                if x1 > quantity:
                    pass
                else:
                    price = (sellers_final_check[i + 1]['offers'][j]['prices'][z]['price'])
                    quantity_of_price = (sellers_final_check[i + 1]['offers'][j]['prices'][z]['quantity'])
                    prices_list.append(price)
                    quantity_list.append(quantity_of_price)

                check_case = len(sellers_final_check[i + 1]['offers'])
                if z < check_case:
                    pass
                else:
                    zipped = dict(zip(quantity_list, prices_list))
                    prices_quantity[i + 1] = zipped
        prices_list = []
        quantity_list = []

    # include sellers with only one offer and only one price, adds them to the prices_quantity dictionary
    prices_2 = []
    quantity_2 = []
    for i in range(len(sellers_final_check)):
        x = 1
        if (len(sellers_final_check[i + 1]['offers'][0]['prices'])) == x:
            price_2 = (sellers_final_check[i + 1]['offers'][0]['prices'][0]['price'])
            quantity_price_2 = (sellers_final_check[i + 1]['offers'][0]['prices'][0]['quantity'])
            prices_2.append(price_2)
            quantity_2.append(quantity_price_2)
            zipped_2 = dict(zip(quantity_2, prices_2))
            prices_quantity[i + 1] = zipped_2

    # print(len(sellers_final_check[3]['offers'][0]['prices']))
    # print(sellers_final_check[3]['offers'][0]['prices'][0]['price'])

    # seller has no matching key pair in prices_quantity dictionary? pop it.
    for i in list(sellers_final_check.keys()):
        if i not in list(prices_quantity.keys()):
            sellers_final_check.pop(i)

    final_cost_dictionary = {}
    # calculate final cost for each seller depending on specified quantity
    # loop all keys of keys of prices_quantity in descending order, if value<= quantity, that will be the final cost
    for i in prices_quantity.keys():
        for j in reversed(prices_quantity[i].keys()):
            if j <= quantity:
                final_cost = round(quantity * prices_quantity[i][j])
                final_cost_dictionary[i] = final_cost

    # formatting final result
    final_sellers = []
    for i in sellers_final_check:
        name = sellers_final_check[i]['company']['name']
        inventory = str(sellers_final_check[i]['offers'][0]['inventory_level'])
        cost = str(final_cost_dictionary[i])
        url = sellers_final_check[i]['offers'][0]['click_url']
        temp_list = (name, inventory, cost, url)
        final_sellers.append(temp_list)
    final_data = tuple(final_sellers)
    headings = ("Seller Name", "Inventory", "Calculated Cost", "URL")
    for i in final_data:
        print(i)


test_search(quantity=10000)


