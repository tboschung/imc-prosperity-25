from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order
import random
import json

# data = json.loads(json_string)
# json_string = json.dumps(data)

#init state of the passed on data
TraderData = '{"RAINFOREST_RESIN": 2000, "KELP": 200}'

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        #init useful variables:
        goods = ["RAINFOREST_RESIN", "KELP"]
        position_limit = {
            "RAINFOREST_RESIN" : 50,
            "KELP" : 50
        }

        # use conversions later
        conversions = 0

        # get our "global variables"
        if(state.traderData == ""):
            data = json.loads(TraderData)
        else:
            data = json.loads(state.traderData)

        positions = {good: state.position.get(good, 0) for good in goods}


        # Initialize the method output dict as an empty dict
        result = {}


        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():

            acceptable_price = random.randint(data[product]-1000, data[product]+1000)

            # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
            order_depth: OrderDepth = state.order_depths[product]

            # Initialize the list of Orders to be sent as an empty list
            orders: list[Order] = []

            # Define a fair value 
            print("acceptable price")
            print(acceptable_price)

            # compare sell orders to acceptable price (buy a good to match a sell order)
            buy_order_volume = 0
            buy_price = 0
            sorted_sell_orders = sorted(order_depth.sell_orders.items())
            print(sorted_sell_orders)
            for price, volume in sorted_sell_orders:
                if(price < acceptable_price):
                # if(True):
                    buy_price = price
                    buy_order_volume -= volume #sell orders have negative volume
                #enforce position limit
                if(buy_order_volume > position_limit[product] - positions[product] ):
                    buy_order_volume =  position_limit[product] - positions[product]
                    break
            if(buy_order_volume > 0): 
                orders.append(Order(product, buy_price, buy_order_volume))
                data[product] = buy_price


            #compare buy orders to acceptable price (sell a good to match a buy order)
            sell_order_volume = 0
            sell_price = 0
            sorted_buy_orders = sorted(order_depth.buy_orders.items())
            print(sorted_buy_orders)
            for price, volume in sorted_buy_orders:
                if(price > acceptable_price):
                    sell_price = price
                    sell_order_volume += volume
                #enforce position limit
                if(sell_order_volume > position_limit[product] + positions[product] ):
                    sell_order_volume = position_limit[product] + positions[product]
                    break
            if(sell_order_volume > 0): 
                orders.append(Order(product, sell_price, -sell_order_volume))
                data[product] = sell_price


            result[product] = orders
        print(result)
        print(positions)
        print(conversions)
        return result, conversions, json.dumps(data)