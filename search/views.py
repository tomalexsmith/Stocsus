import requests
import json
from flask import render_template, Blueprint, request, redirect, url_for
from search.forms import SearchForm
import pandas as pd
import ast
import openpyxl # required dependency
"""
This file will not work without the API TOKEN, you need to edit the endpoint variable and add it there
query is the GraphQL query that will be used to extract data using the Octopart API
example part number = CFR50J2K2
"""

search_blueprint = Blueprint('search_blueprint', __name__, template_folder='templates')

endpoint = "https://octopart.com/api/v4/endpoint?token=b02769bc-29c7-413d-9eb0-baf60f016b02"

query = """query {
  search(q: "%s", limit: 1) {
    results {
      part {
        mpn
        manufacturer {
            name
        }
        sellers(include_brokers: false, authorized_only: true) {
          company {
            name
          }
          offers {
          order_multiple
            click_url
            inventory_level
            prices {
              price
              quantity
            }
          }
        }
      }
    }
  }
}"""




@search_blueprint.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit() and request.method == 'POST':
        part_number_input = form.part_number.data
        quantity_input = form.quantity.data
        models_input = form.models.data
        part_number = []
        part_number.append(part_number_input)

        quantity = [quantity_input]
        models = [models_input]
        return redirect(url_for('search_blueprint.results', part_number=[part_number], quantity=[quantity], models=[models]))
    elif request.method == 'POST':
        f = request.files['file']
        data = pd.read_excel(f, 'Sheet1', index_col=None)
        data.to_csv('your_csv.csv', encoding='utf-8')
        part_number = []
        quantity = []
        models = []
        for i in range(len(data['part_no'])):
            part_number.append(str(data['part_no'][i]))
        for i in range(len(data['quantity'])):
            quantity.append(str(data['quantity'][i]))
        for i in range(len(data['models'])):
            models.append(str(data['models'][i]))
        return redirect(url_for('search_blueprint.results', part_number=[part_number], quantity=[quantity], models=[models]))


    return render_template("search.html", form=form)


@search_blueprint.route('/results/<part_number>/<quantity>/<models>/', methods=['GET', 'POST'])
def results(part_number, quantity, models):
    tables = {}
    table_part_numbers = []
    table_manufacturers = []

    # convert string representation of list to an actual list
    part_number = ast.literal_eval(part_number)
    part_numbers = [n.strip() for n in part_number]

    quantity = ast.literal_eval(quantity)
    quantitys = [n.strip() for n in quantity]


    models = ast.literal_eval(models)
    models_final = [n.strip() for n in models]


    for search_no in range(len(part_numbers)):
        part_number = part_numbers[search_no]
        table_part_numbers.append(part_number)
        quantity = quantitys[search_no]
        models = models_final[search_no]
        print(part_number)
        print(quantity)
        print(models)

        r = requests.post(endpoint, json={"query": query % part_number})
        if r.status_code == 200:
            data = json.loads(json.dumps(r.json(), indent=2))  # this data is the api_response

            manufacturer = data['data']['search']['results'][0]['part']['manufacturer']['name']
            table_manufacturers.append(manufacturer)


            quantity = int(quantity) * int(models)
            sellers = {}

            counter = 0  # counter to calculate number of results to be used in other functions.
            for i in range(len(data['data']['search']['results'][0]['part']['sellers'])):
                x = (data['data']['search']['results'][0]['part']['sellers'][i])
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

            # for key, value in sellers_final_check.items():
            #     print(key, ' : ', value)
            for i in list(sellers_final_check):
                if sellers_final_check[i]['offers'][0]['prices'][0]['quantity'] > quantity:
                    sellers_final_check.pop(i)
            # for key, value in sellers_final_check.items():
            #     print(key, ' : ', value)
            # formatting final result
            final_sellers = []
            for i in sellers_final_check:
                name = sellers_final_check[i]['company']['name']
                inventory = str(sellers_final_check[i]['offers'][0]['inventory_level'])
                cost = '$' + str(final_cost_dictionary[i])
                url = sellers_final_check[i]['offers'][0]['click_url']
                temp_list = (name, inventory, cost, url)
                final_sellers.append(temp_list)
                final_data = tuple(final_sellers)
                tables[search_no] = final_data
                print(final_data)
    headings = ("Seller Name", "Inventory", "Calculated Cost", "URL")
    print(tables)
    return render_template("results.html", tables=tables, headings=headings, part_number=table_part_numbers, manufacturer=table_manufacturers)


