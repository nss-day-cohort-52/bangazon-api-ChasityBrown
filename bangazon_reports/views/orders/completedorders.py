"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from bangazon_reports.views.helpers import dict_fetch_all

class CompletedOrderList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
                SELECT
                    o.id,
                    o.payment_type_id,
                    o.completed_on,
                    o.created_on,
                    u.first_name first_name,
                    u.last_name last_name,
                    pt.merchant_name merchant_name,
                    SUM(p.price) as Total
                FROM bangazon_api_order o
                JOIN bangazon_api_orderproduct op
                    ON op.order_id = o.id
                JOIN bangazon_api_product p
                    ON op.product_id = p.id
                JOIN auth_user u
                    ON o.user_id = u.id
                JOIN bangazon_api_paymenttype pt
                    ON o.payment_type_id = pt.id
                GROUP BY o.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            completed_orders = []

            for row in dataset:
                # TODO: Create a dictionary called game that includes 
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                order = {
                    'id': row['id'],
                    'payment_type': row['merchant_name'],
                    'user': f"{row['first_name']} {row['last_name']}",
                    'total': row['Total'],
                    'completed_on': row['completed_on']
                }
                
                # This is using a generator comprehension to find the user_dict in the games_by_user list
                # The next function grabs the dictionary at the beginning of the generator, if the generator is empty it returns None
                # This code is equivalent to:
                # user_dict = None
                # for user_game in games_by_user:
                #     if user_game['gamer_id'] == row['gamer_id']:
                #         user_dict = user_game
                if order['completed_on'] is not None:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    completed_orders.append(order)
        
        # The template string must match the file name of the html template
        template = 'orders/list_with_completed_orders.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "completedorder_list": completed_orders
        }

        return render(request, template, context)
