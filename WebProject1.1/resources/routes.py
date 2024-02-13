from .resources import  OrdersApi

def initialize_routes(api):
    api.add_resource(OrdersApi, '/api/order_details')
    