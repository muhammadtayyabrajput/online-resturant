from flask import request, Response, jsonify
from flask_restful import Resource
from models import orders,orders_items
from SMDBHandler import SMDBHandler
import json
from decimal import Decimal

class OrdersApi(Resource):
    def get(self):
        try: 
            print("here in api")
            handler = SMDBHandler("localhost", "root", "mysql123", "web_project_food")
            orders_details=handler.order_details()
            # print(orders_details)
            # Restructure the data into a list of dictionaries
            restaurants_list = []
            for restaurant_tuple in orders_details:
                for restaurant_info in restaurant_tuple:
                    restaurant_dict = {
                        "id": restaurant_info[0],
                        "name": restaurant_info[1],
                        "price": str(restaurant_info[2]),  # Convert Decimal to string for JSON serialization
                        "quantity": restaurant_info[3]
                    }
                    restaurants_list.append(restaurant_dict)

            # Convert the list of dictionaries to JSON format
            json_data = json.dumps(restaurants_list, indent=2)

            print(json_data)
            print("here in api2")
            return Response(json_data, mimetype="application/json", status=200)
        except Exception as e:
            return Response(status=404)
    

