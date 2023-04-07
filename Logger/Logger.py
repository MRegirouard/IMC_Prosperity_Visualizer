import json
from datamodel import Order, ProsperityEncoder, Symbol, Trade, TradingState
from typing import Any

class Logger:
    def __init__(self) -> None:
        '''
        Constructor
        effects: Creates Logger object with empty logs
        '''
        self.logs = ""

    # def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
    #     self.logs += sep.join(map(str, objects)) + end

    # values: dict[str, Any]
    def flush(self, state: TradingState, orders: dict[Symbol, list[Order]], 
              values: dict[str, Any]) -> None:
        '''
        state: the current Trading State
        orders: dict with security symbol as key and order-list as key-value
        effects: Formats the orders dict using json and helper functions 
        cls: changes encoder to return dict
        sort_keys: output of orders will be sorted by keys
        '''
        print(json.dumps({
            "state": self.compress_state(state),
            "orders": self.compress_orders(orders),
            "logs": self.logs,
        }, cls=ProsperityEncoder, separators=(",", ":"), sort_keys=True))

        self.logs = ""

    def compress_state(self, state: TradingState) -> dict[str, Any]:
        '''
        listings: Dict[Symbol, Listing]
        listing iterates through listings a list of listings, 
        each containing a [symbol, product, denomination]

        order_depths: Dict[Symbol, OrderDepth]
        OrderDepth: buy_orders = Dict[int, int]
                    sell_orders = Dict[int, int]
                
        order_depths: Creates a dictionary where the key is each symbol,
        the key-value is a two element list containing the buy_orders
        and sell orders

        state: the current trading state
        effects: Creates listings list and order_depths dict
        returns: dictionary with keys and values, uses compress trades to format
        market_trades and own_trades
        '''
        listings = []
        for listing in state.listings.values():
            listings.append([listing["symbol"], listing["product"], listing["denomination"]])

        order_depths = {}
        for symbol, order_depth in state.order_depths.items():
            order_depths[symbol] = [order_depth.buy_orders, order_depth.sell_orders]

        return {
            "t": state.timestamp,
            "l": listings,
            "od": order_depths,
            "ot": self.compress_trades(state.own_trades),
            "mt": self.compress_trades(state.market_trades),
            "p": state.position,
            "o": state.observations,
        }

    def compress_trades(self, trades: dict[Symbol, list[Trade]]) -> list[list[Any]]:
        '''
        trades: dict[Symbol, list[Trade]]

        effects: For each symbol in the trades dict passed in, loop through
        each trade for that symbol and append pertinent info in list
        format to compressed list

        returns: compressed trades list
        '''
        compressed = []
        for arr in trades.values():
            for trade in arr:
                compressed.append([
                    trade.symbol,
                    trade.buyer,
                    trade.seller,
                    trade.price,
                    trade.quantity,
                    trade.timestamp,
                ])
        return compressed

    def compress_orders(self, orders: dict[Symbol, list[Order]]) -> list[list[Any]]:
        '''
        orders: dict[Symbol, list[Order]]

        effects: For each symbol, iterate through each order for that symbol,
        each time appending symbol, price and quantity in list format to 
        compressed list

        returns: compressed orders list
        '''

        compressed = []
        for arr in orders.values():
            for order in arr:
                compressed.append([order.symbol, order.price, order.quantity])

        return compressed

logger = Logger()
class Trader:
    def run(self, state: TradingState) -> dict[Symbol, list[Order]]:
        orders = {}
        values = {}

        # TODO: Add logic

        logger.flush(state, orders, values)
        return orders
