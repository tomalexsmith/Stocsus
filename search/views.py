import requests
import json
from flask_login import login_required
from flask import render_template, Blueprint, request, redirect, url_for, flash, jsonify, send_file
from search.forms import SearchForm
import pandas as pd
import ast
import database.models as database
import app
import openpyxl  # required dependency

search_blueprint = Blueprint('search_blueprint', __name__, template_folder='templates')

# This endpoint is used to communicate with the API, you can replace the token if you want
endpoint = "https://octopart.com/api/v4/endpoint?token=3b6dda6b-8d73-4a4f-93ac-eb38c99c16b1"

# This query is sent to the GraphQL API
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
@login_required
def search():
    """
    Presents user with a form to enter part_number, quantity, models.
    Gives user with ability to upload excel file with multiple parts where it transforms it into lists.
    Sends this data to the results function.
    """
    form = SearchForm()
    if form.validate_on_submit() and request.method == 'POST':
        part_number_input = form.part_number.data
        quantity_input = form.quantity.data
        models_input = form.models.data
        part_number = []
        part_number.append(part_number_input)

        quantity = [quantity_input]
        models = [models_input]
        return redirect(
            url_for('search_blueprint.results', part_number=[part_number], quantity=[quantity], models=[models]))
    elif request.method == 'POST':

        try:
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
            return redirect(
                url_for('search_blueprint.results', part_number=[part_number], quantity=[quantity], models=[models]))
        except KeyError:
            flash("File does not match template layout, please check file template and try again.")
        except ValueError:
            flash("File does not match template layout, please check file template and try again.")
        except TypeError:
            flash("File does not match template layout, please check file template and try again.")

    return render_template("search.html", form=form)


@search_blueprint.route('/result/<part_number>/<quantity>/<models>/', methods=['GET', 'POST'])
@login_required
def results(part_number, quantity, models):
    """
    Takes all the input from the user.
    Uses this input to query the GraphQL API for each part number.
    Receives data from the API and transforms it to meet certain requirements.
    Data is ready to be displayed on tables on frontend or exported into an Excel if the user prefers that.

    :param part_number: list of all part numbers entered by user
    :param quantity: list of quantitys entered by user
    :param models: list of all models entered by user
    """

    # checks if database is online
    database.database_check()
    watchlist_check = []
    favourite_check = []
    blacklist_check = []

    # query database to present correct details on frontend
    all_watchlist = database.WatchList.query.all()
    all_favourite = database.Favourite.query.all()
    all_blacklist = database.Blacklist.query.all()

    # adds the most recent data to lists
    for i in all_watchlist:
        watchlist_check.append(i.part_number)
    for i in all_favourite:
        favourite_check.append(i.supplier_name)
    for i in all_blacklist:
        blacklist_check.append(i.supplier_name)

    # global variables
    no_stock_numbers = []
    no_stock = False
    tables = {}
    table_part_numbers = []
    table_manufacturers = []

    # convert string representations of list to an actual list
    part_number = ast.literal_eval(part_number)
    part_numbers = [n.strip() for n in part_number]
    quantity = ast.literal_eval(quantity)
    quantitys = [n.strip() for n in quantity]
    models = ast.literal_eval(models)
    models_final = [n.strip() for n in models]

    # loops every single search, could be one or multiple if the user uploaded an Excel file
    for search_no in range(len(part_numbers)):
        part_number = part_numbers[search_no]
        table_part_numbers.append(part_number)
        quantity = int(quantitys[search_no]) * int(models_final[search_no])

        r = requests.post(endpoint, json={"query": query % part_number})
        if r.status_code == 400:
            flash("Invalid Part Number")
            break
        if r.status_code == 200:
            data = json.loads(json.dumps(r.json(), indent=2))  # this data is the api_response
            if str(data['data']['search']['results']) == "None":
                flash("Invalid Part Number")
                break

            manufacturer = data['data']['search']['results'][0]['part']['manufacturer']['name']
            table_manufacturers.append(manufacturer)

            sellers = {}

            counter = 0  # counter
            for i in range(len(data['data']['search']['results'][0]['part']['sellers'])):
                x = (data['data']['search']['results'][0]['part']['sellers'][i])
                counter += 1
                sellers[i + 1] = x

            # check inventory level of each key and make sure it is not equal to zero
            # if seller has 0 inventory level, remove them from result

            to_continue = True
            sellers_with_stock = {}  # dictionary to store sellers that have stock
            j = 0
            largest_quantity_available = 0
            for i in range(len(sellers)):
                greatest_seller_inventory = sellers[i + 1]['offers'][0]['inventory_level']
                if greatest_seller_inventory > largest_quantity_available:
                    largest_quantity_available = greatest_seller_inventory

                if sellers[i + 1]['offers'][0][
                    'inventory_level'] >= quantity and largest_quantity_available >= quantity:  # check if inventory matches quantity
                    j += 1
                    sellers_with_stock[j] = sellers[i + 1]
                    to_continue = False

                # keep adding each sellers inventory to total, if the total reaches >= quantity,
                # Continue

                # then we will add all these sellers to th

                # elseif  sellers[i + 1]['offers'][0]['inventory_level'] < quantity
                # and largest_quantity_available < quantity:
            if to_continue:
                j = 0
                total = 0
                for i in range(len(sellers)):
                    if sellers[i + 1]['offers'][0]['inventory_level'] < quantity and \
                            largest_quantity_available < quantity:
                        seller_inventory = sellers[i + 1]['offers'][0]['inventory_level']
                        total += seller_inventory
                    for p in range(len(sellers)):
                        if total >= quantity and sellers[p + 1]['offers'][0]['inventory_level'] > 0:
                            j += 1
                            sellers_with_stock[j] = sellers[p + 1]
                        else:
                            if part_number in no_stock_numbers:
                                break
                            else:
                                no_stock_numbers.append(part_number)
                print(no_stock_numbers)
                # if we cannot reach a total that is >= quantity:
                # else:
                # user dialogue box, would you like to add item to watchlist?
                # { jinja }
                # flash("No products in stock/ could not find valid combination", "wishlist") # add item to watchlist
                # Would you like to add to wishlist? button to add
                # { end jinja }

            # check each sellers' order multiple = none, if not then check if quantity is bigger than or equal to it
            # order multiple is the min order quantity set by seller
            sellers_final_check = {}
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
                for j in range(len(sellers_final_check[i + 1]['offers'])):  # check how many offers' seller has
                    for z in range(
                            len(sellers_final_check[i + 1]['offers'][j]['prices'])):  # loop over the prices of offer
                        # for y in range(len(sellers_final_check[i + 1]['offers'][j]['prices'][z])):
                        # loop over prices of offer
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

            print(prices_quantity)

            # seller has no matching key pair in prices_quantity dictionary? pop it.
            for i in list(sellers_final_check.keys()):
                if i not in list(prices_quantity.keys()):
                    sellers_final_check.pop(i)

            final_cost_dictionary = {}
            # calculate final cost for each seller depending on specified quantity loop all keys of keys of
            # prices_quantity in descending order, if value<= quantity, that will be the final cost
            for i in prices_quantity.keys():
                for j in reversed(prices_quantity[i].keys()):
                    if j <= quantity:
                        final_cost = round(quantity * prices_quantity[i][j])
                        final_cost_dictionary[i] = final_cost
                        break

            # for key, value in sellers_final_check.items():
            #     print(key, ' : ', value)
            for i in list(sellers_final_check):
                if sellers_final_check[i]['offers'][0]['prices'][0]['quantity'] > quantity:
                    sellers_final_check.pop(i)
            # for key, value in sellers_final_check.items():
            #     print(key, ' : ', value)
            # formatting final result
            final_sellers = []
            f_dict = {}



            for key in list(sellers_final_check):

                sellers_final_check[key]['company']['name'] = sellers_final_check[key]['company']['name'].replace(
                    " ", "_")

                seller = sellers_final_check[key]['company']['name']
                if seller not in favourite_check:
                    f_dict[key] = sellers_final_check[key]
                    sellers_final_check.pop(key)
                    sellers_final_check[key] = f_dict[key]

            for key in list(sellers_final_check):
                seller = sellers_final_check[key]['company']['name']
                if seller in blacklist_check:
                    sellers_final_check.pop(key)

            if len(sellers_final_check) == 0:
                no_stock_numbers.append(part_number)

            temp_dict = {}
            for i in list(sellers_final_check.keys()):
                name = sellers_final_check[i]['company']['name']
                if name in temp_dict:
                    sellers_final_check.pop(i)
                else:
                    temp_dict[name] = True



            for i in sellers_final_check:
                name = sellers_final_check[i]['company']['name']
                name = name.replace(" ", "_")

                inventory = str(sellers_final_check[i]['offers'][0]['inventory_level'])
                cost = '$' + str(final_cost_dictionary[i])
                url = sellers_final_check[i]['offers'][0]['click_url']

                temp_list = (name, inventory, cost, url)
                final_sellers.append(temp_list)
                final_data = tuple(final_sellers)
                tables[search_no] = final_data

    if len(tables) == 0:
        no_tables_available = True
        # avoids any duplicates being returned on watchlist options
        no_stock_numbers = list(dict.fromkeys(no_stock_numbers))
        return render_template("results.html", no_tables="Could not find any results",
                               no_tables_available=no_tables_available, no_stock_numbers_no_tables=no_stock_numbers, watchlist_check=watchlist_check)

    headings = ("Seller Name", "Inventory", "Calculated Cost")

    if request.method == 'POST':

        supplier_names = []
        inventory_levels = []
        calculated_costs = []
        urls = []
        part_number_column = []

        for i in range(len(tables)):
            for j in range(len(tables[i])):
                part_no = table_part_numbers[i]
                seller_name = tables[i][j][0]
                inventory = tables[i][j][1]
                cost = tables[i][j][2]
                url = tables[i][j][3]

                part_number_column.append(part_no)
                supplier_names.append(seller_name)
                inventory_levels.append(inventory)
                calculated_costs.append(cost)
                urls.append(url)
            # part_number_column.append(' ')
            supplier_names.append(' ')
            inventory_levels.append(' ')
            calculated_costs.append(' ')
            urls.append(' ')
        # 'Part_no': part_number_column,
        data = {
            'Seller': supplier_names,
            'Inventory': inventory_levels,
            'Cost': calculated_costs,
            'URL': urls
        }
        # 'Part_no'
        df = pd.DataFrame(data, columns=['Seller', 'Inventory', 'Cost', 'URL'])

        df.to_excel('results.xlsx', index=False, header=True)

        return send_file('results.xlsx', as_attachment=True)



    if len(tables) != 0:
        no_stock_numbers = list(dict.fromkeys(no_stock_numbers))
        return render_template("results.html", tables=tables, headings=headings, part_number=table_part_numbers,
                               manufacturer=table_manufacturers, no_stock_numbers=no_stock_numbers,
                               watchlist_check=watchlist_check, favourite_check=favourite_check,
                               blacklist_check=blacklist_check)


@search_blueprint.route('/update_watchlist', methods=['POST'])
@login_required
def update_watchlist():
    database.database_check()
    part_number = request.form['part_number']
    new_watchlist_number = database.WatchList(part_number=part_number)
    app.db.session.add(new_watchlist_number)
    app.db.session.commit()
    return jsonify({'result': 'success', 'part_number': part_number})


@search_blueprint.route('/update_favourite', methods=['POST'])
@login_required
def update_favourite():
    database.database_check()
    supplier_name = request.form['supplier_name']
    new_favourite_supplier = database.Favourite(supplier_name=supplier_name)
    app.db.session.add(new_favourite_supplier)
    app.db.session.commit()
    return jsonify({'result': 'success', 'supplier_name': supplier_name})


@search_blueprint.route('/update_blacklist', methods=['POST'])
@login_required
def update_blacklist():
    database.database_check()
    supplier_name = request.form['supplier_name']
    new_blacklist_supplier = database.Blacklist(supplier_name=supplier_name)
    app.db.session.add(new_blacklist_supplier)
    app.db.session.commit()
    return jsonify({'result': 'success', 'supplier_name': supplier_name})
