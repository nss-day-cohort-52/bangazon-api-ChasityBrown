"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class ProductPriceList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
                SELECT
                    p.id,
                    p.name,
                    s.name
                FROM bangazon_product p
                JOIN bangazon_store s
                    ON p.store = s.id
                WHERE price >= 1000
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_user list:
            #
            # [
            #   {
            #     "id": 1,
            #     "full_name": "Admina Straytor",
            #     "games": [
            #       {
            #         "id": 1,
            #         "title": "Foo",
            #         "maker": "Bar Games",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       },
            #       {
            #         "id": 2,
            #         "title": "Foo 2",
            #         "maker": "Bar Games 2",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       }
            #     ]
            #   },
            # ]

            products_by_price = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                product = {
                    'id': row['id'],
                    'name': row['name'],
                    'price': row['price'],
                    'description': row['description'],
                    'quantity': row['quantity'],
                    'location': row['location'],
                    'category': row['category'],
                    'store': row['store'],
                    'image_path': row['image_path']                     
                }
                
                # This is using a generator comprehension to find the user_dict in the games_by_user list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # user_dict = None
                # for user_game in games_by_user:
                #     if user_game['gamer_id'] == row['gamer_id']:
                #         user_dict = user_game
                
                price_dict = next(
                    (
                        price_product for price_product in products_by_price
                        if price_product['gamer_id'] == row['gamer_id']
                    ),
                    None
                )
                
                if price_dict:
                    # If the price_dict is already in the games_by_price list, append the game to the games list
                    price_dict['games'].append(game)
                else:
                    # If the user is not on the games_by_user list, create and add the user to the list
                    games_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": f"{row['first_name']} {row['last_name']}",
                        "games": [game]
                    })
        
        # The template string must match the file name of the html template
        template = 'users/list_with_games.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "usergame_list": games_by_user
        }

        return render(request, template, context)
