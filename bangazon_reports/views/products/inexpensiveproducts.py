"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class InexpensiveProductsList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price,
                    s.name store_name
                FROM bangazon_api_product p
                JOIN bangazon_api_store s
                    ON p.store_id = s.id
                WHERE price <= 1000
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            inexpensive_products = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                product = {
                    'id': row['id'],
                    'name': row['name'],
                    'store': row['store_name'],
                    'price': row['price']                     
                }
                if product['price'] is not None:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    inexpensive_products.append(product)
        
        # The template string must match the file name of the html template
        template = 'products/list_with_inexpensive_products.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "inexpensiveproducts_list": inexpensive_products
        }

        return render(request, template, context)
