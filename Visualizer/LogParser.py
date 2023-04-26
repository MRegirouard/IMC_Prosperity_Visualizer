"""
LogParser.py

Contains functions and classes to parse the log files generated by IMC using a modified version of 
jmerle's logger.
"""

from datamodel import *
from typing import Dict, List, Any, Tuple, TextIO
import json
import csv

"""
A class to store data from the activity logs, specifically, all the data for one product on one timpestamp.
"""
class ProductActivityLog:
    def __init__(self, product: Product, day: int, timestamp: int, bids: List[Tuple[int, Position]] = [],
        asks: List[Tuple[int, Position]] = [], mid_price: float = 0, profit_and_loss: float = 0):
        self.product = product
        self.day = day
        self.timestamp = timestamp
        self.bids = bids
        self.asks = asks
        self.mid_price = mid_price
        self.profit_and_loss = profit_and_loss

"""
A class to store all data parsed from the log file.
"""
class LogData:
    def __init__(self, trading_states: List[TradingState], orders: List[Dict[Symbol, List[Order]]], logs: List[str],
        values: List[Dict[str, Any]], submission_logs: List[str], activities: Dict[Product, List[ProductActivityLog]]):
        
        self.trading_states = trading_states
        self.orders = orders
        self.logs = logs
        self.values = values
        self.submission_logs = submission_logs
        self.activities = activities

"""
Parse the given log file, and return a LogData object.

Parameters:
log_file (TextIO): The log file to parse, as an open file object.

Returns:
LogData: The parsed data from the log file.
"""
def parse(log_file: TextIO) -> LogData:
    # Find the start of each section of the log file:
    lines = log_file.read().split('\n')
    sandboxStart = lines.index('Sandbox logs:')
    submissionStart = lines.index('Submission logs:')
    activitiesStart = lines.index('Activities log:')
    
    # Parse each section of the logs separately:
    sandbox_logs = parse_sandbox_logs(lines[sandboxStart + 1:submissionStart])
    submission_logs = parse_submission_logs(lines[submissionStart + 1:activitiesStart])
    activities_log = parse_activities_log(lines[activitiesStart + 1:])
    return LogData(*sandbox_logs, submission_logs, activities_log)

"""
Parse the "sandbox logs" section of the log file, and return a tuple of the parsed data.

Parameters:
lines (List[str]): The lines of the log file to parse.

Returns:
Tuple[List[TradingState], List[Dict[Symbol, List[Order]]], List[str], List[Dict[str, Any]]]: The parsed data from the
log file. In the following order: A list of the trading states, the orders, the user log messages, and the user values.
"""
def parse_sandbox_logs(lines: List[str]) -> Tuple[List[TradingState], List[Dict[Symbol, List[Order]]],
    List[str], List[Dict[str, Any]]]:
    
    trading_states: List[TradingState] = []
    orders: List[Dict[Symbol, List[Order]]] = []
    logs: List[str] = []
    values: List[Dict[str, Any]] = []
    
    for line in lines:        
        if line.startswith('{'):
            unparsedLine = line        
        elif line == '' or line.endswith(' ') or not line[0].isdigit():
            # Discard lines that are empty, end with a space, or do not start with a digit        
            continue
        else:
            unparsedLine = line[line.index(' ') + 1:]
            
        if not unparsedLine.startswith('{\"logs\":\"'):
            continue
        
        jsonParsed = json.loads(unparsedLine)
        
        # Parse user logs:
        user_logs = jsonParsed['logs']
        
        # Parse orders:
        user_orders: Dict[Symbol, List[Order]] = {}
        for order in jsonParsed['orders']:
            user_orders.setdefault(order[0], [])
            user_orders[order[0]].append(Order(*order))
        
        # Parse trading state:
        # Parse listings:
        listings: Dict[Symbol, Listing] = {}
        for listing in jsonParsed['state']['l']:
            listings[listing[0]] = Listing(*listing)
        
        # Parse market trades:
        market_trades: Dict[Symbol, List[Trade]] = {}
        for mt in jsonParsed['state']['mt']:
            symbol, price, quantity, buyer, seller, timestamp = mt[0], mt[3], mt[4], mt[1], mt[2], mt[5]            
            market_trades.setdefault(symbol, [])
            market_trades[symbol].append(Trade(symbol, price, quantity, buyer, seller, timestamp))
            
        # Parse observations:
        observations: Dict[Symbol, Observation] = {}
        for observation in jsonParsed['state']['o']:
            observations[observation] = jsonParsed['state']['o'][observation]
        
        # Parse order depths:
        order_depths: Dict[Symbol, OrderDepth] = {}
        for symbol in jsonParsed['state']['od']:
            od = jsonParsed['state']['od'][symbol]
            order_depths.setdefault(symbol, OrderDepth())

            for buy_order_price in od[0]:
                # Convert to float first: Logs often store numbers as "1198.0" even if they are integers
                order_depths[symbol].buy_orders[int(float(buy_order_price))] = od[0][buy_order_price]
            
            for sell_order_price in od[1]:
                order_depths[symbol].sell_orders[int(float(sell_order_price))] = od[1][sell_order_price]
                
        # Parse own trades:
        own_trades: Dict[Symbol, List[Trade]] = {}
        for ot in jsonParsed['state']['ot']:
            symbol, price, quantity, buyer, seller, timestamp = ot[0], ot[3], ot[4], ot[1], ot[2], ot[5]            
            own_trades.setdefault(symbol, [])
            own_trades[symbol].append(Trade(symbol, price, quantity, buyer, seller, timestamp))
            
        # Parse position:
        position: Dict[Product, Position] = {}
        for product in jsonParsed['state']['p']:
            position[product] = jsonParsed['state']['p'][product]
            
        # Parse timestamp:
        timestamp = jsonParsed['state']['t']
            
        # Parse values:
        user_values: Dict[str, Any] = {}
        
        if "values" in jsonParsed:
            for value in jsonParsed['values']:
                user_values[value] = jsonParsed['values'][value]
            
        trading_states.append(TradingState(timestamp, listings, order_depths,
            own_trades, market_trades, position, observations))
        logs.append(user_logs)
        values.append(user_values)
        orders.append(user_orders)
        
    return (trading_states, orders, logs, values)

"""
Parse the "submission logs" section of the log file, and return a list of the parsed data.
For now, this function simply returns the lines of the log file.

Parameters:
lines (List[str]): The lines of the log file to parse.

Returns:
List[str]: The parsed data from the log file.
"""
def parse_submission_logs(lines: List[str]) -> List[str]:
    # Submission logs mostly contain error messages, etc.
    # Simply return the lines in this section of the log file for now
    return lines

"""
Parse the "activities log" section of the log file, and return a dictionary of the parsed data.

Parameters:
lines (List[str]): The lines of the log file to parse.

Returns:
A dictionary of the product to a list of the product's activity for each timestamp.
"""
def parse_activities_log(lines: List[str]) -> Dict[Product, List[ProductActivityLog]]:
    reader = csv.reader(lines, delimiter=';')
    header = next(reader)
   
    data: Dict[Product, List[ProductActivityLog]] = {}
    
    for row in reader:
        if len(row) == 0:
            continue
        
        day, timestamp, product, mid_price, pnl = int(row[0]), int(row[1]), row[2], float(row[15]), float(row[16])
        prod_log = ProductActivityLog(product, day, timestamp, mid_price=mid_price, profit_and_loss=pnl)
        
        # Parse each of the three bid and ask prices/volumes
        
        for bid_num in range(3):
            bid_price = row[3 + bid_num * 2]
            bid_vol = row[4 + bid_num * 2]
            
            if bid_price is None or bid_vol is None or bid_price == '' or bid_vol == '':
                break
            
            prod_log.bids.append((int(float(bid_price)), int(float(bid_vol))))
            
        for ask_num in range(3):
            ask_price = row[9 + ask_num * 2]
            ask_vol = row[10 + ask_num * 2]
            
            if ask_price is None or ask_vol is None or ask_price == '' or ask_vol == '':
                break
            
            prod_log.asks.append((int(float(ask_price)), int(float(ask_vol))))
            
        data.setdefault(product, [])
        data[product].append(prod_log)
        
    return data
