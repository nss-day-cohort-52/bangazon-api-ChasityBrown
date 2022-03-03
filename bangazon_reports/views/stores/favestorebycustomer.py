"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from bangazon_reports.views.helpers import dict_fetch_all


class FaveStoreByCustomerList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
                SELECT
                    f.id,
                    s.name,
                    u.first_name first_name,
                    u.last_name last_name
                FROM bangazon_api_favorite f
                JOIN bangazon_api_store s
                    ON f.store_id = s.id
                JOIN auth_user u
                    ON f.customer_id = u.id
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)
            
            fave_store_by_customer = []

            for row in dataset:
                # TODO: Create a dictionary called event that includes 
                # the name, description, number_of_players, maker,
                # event_type_id, and skill_level from the row dictionary
                fave = {
                    'id': row['id'],
                    'customer': f"{row['first_name']} {row['last_name']}",
                    'store': row['name']
                }
                
                if fave['id'] is not None:
                    # If the user_dict is already in the games_by_user list, append the game to the games list
                    fave_store_by_customer.append(fave)
        
        # The template string must match the file name of the html template
        template = 'stores/list_with_customer_faves.html'
        
        # The context will be a dictionary that the template can access to show data
        context = {
            "favestorebycustomer_list": fave_store_by_customer
        }

        return render(request, template, context)
