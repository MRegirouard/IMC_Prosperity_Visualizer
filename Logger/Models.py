from typing import Dict, List, Union

class UserSummary:
    def __init__(self, id: int, firstName: str, lastName: str):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName

class AlgorithmSummary:
    def __init__(self, id: str, content: str, fileName: str, round: str, selectedForRound: bool,
                 status: str, teamId: str, timestamp: str, user: UserSummary):
        self.id = id
        self.content = content
        self.fileName = fileName
        self.round = round
        self.selectedForRound = selectedForRound
        self.status = status
        self.teamId = teamId
        self.timestamp = timestamp
        self.user = user

Time = int
ProsperitySymbol = str
Product = str
Position = int
UserId = str
Observation = int

class ActivityLogRow:
    def __init__(self, day: int, timestamp: int, product: Product, bidPrices: List[float], bidVolumes: List[float],
                 askPrices: List[float], askVolumes: List[float], midPrice: float, profitLoss: float):
        self.day = day
        self.timestamp = timestamp
        self.product = product
        self.bidPrices = bidPrices
        self.bidVolumes = bidVolumes
        self.askPrices = askPrices
        self.askVolumes = askVolumes
        self.midPrice = midPrice
        self.profitLoss = profitLoss

class Listing:
    def __init__(self, symbol: ProsperitySymbol, product: Product, denomination: Product):
        self.symbol = symbol
        self.product = product
        self.denomination = denomination

class Order:
    def __init__(self, symbol: ProsperitySymbol, price: float, quantity: float):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

class OrderDepth:
    def __init__(self, buy_orders: Dict[int, int], sell_orders: Dict[int, int]):
        self.buy_orders = buy_orders
        self.sell_orders = sell_orders

class Trade:
    def __init__(self, symbol: ProsperitySymbol, price: float, quantity: float, buyer: UserId, seller: UserId,
                 timestamp: Time):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
        self.buyer = buyer
        self.seller = seller
        self.timestamp = timestamp

class TradingState:
    def __init__(self, timestamp: Time, listings: Dict[ProsperitySymbol, Listing],
                 order_depths: Dict[ProsperitySymbol, OrderDepth], own_trades: Dict[ProsperitySymbol, List[Trade]],
                 market_trades: Dict[ProsperitySymbol, List[Trade]], position: Dict[Product, Position],
                 observations: Dict[Product, Observation]):
        self.timestamp = timestamp
        self.listings = listings
        self.order_depths = order_depths
        self.own_trades = own_trades
        self.market_trades = market_trades
        self.position = position
        self.observations = observations

class SandboxLogRow:
    def __init__(self, state: TradingState, orders: Dict[ProsperitySymbol, List[Order]], logs: str):
        self.state = state
        self.orders = orders
        self.logs = logs

class Algorithm:
    def __init__(self):
        self.summary: AlgorithmSummary = None
        self.activityLogs: List[ActivityLogRow] = []
        self.sandboxLogs: List[SandboxLogRow] = []
        self.submissionLogs: str = ""


class AlgorithmSummary:
    def __init__(self, id: str, content: str, fileName: str, round: str, selectedForRound: bool,
                 status: str, teamId: str, timestamp: str, user: UserSummary):
        self.id = id
        self.content = content
        self.fileName = fileName
        self.round = round
        self.selectedForRound = selectedForRound
        self.status = status
        self.teamId = teamId
        self.timestamp = timestamp
        self.user = user

class UserSummary:
    def __init__(self, id: int, firstName: str, lastName: str):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName

class ActivityLogRow:
    def __init__(self, day: int, timestamp: int, product: Product, bidPrices: List[float], bidVolumes: List[float],
                 askPrices: List[float], askVolumes: List[float], midPrice: float, profitLoss: float):
        self.day = day
        self.timestamp = timestamp
        self.product = product
        self.bidPrices = bidPrices
        self.bidVolumes = bidVolumes
        self.askPrices = askPrices
        self.askVolumes = askVolumes
        self.midPrice = midPrice
        self.profitLoss = profitLoss

class SandboxLogRow:
    def __init__(self, state: CompressedTradingState, orders: Dict[ProsperitySymbol, List[CompressedOrder]] , logs: str):
        self.state = state
        self.orders = orders
        self.logs = logs

class CompressedListing:
    def __init__(self, symbol: ProsperitySymbol, product: Product, denomination: Product):
        self.symbol = symbol
        self.product = product
        self.denomination = denomination

class CompressedOrderDepth:
    def __init__(self, buy_orders: Dict[int, int], sell_orders: Dict[int, int]):
        self.buy_orders = buy_orders
        self.sell_orders = sell_orders

class CompressedTrade:
    def __init__(self, symbol: ProsperitySymbol, buyer: UserId, seller: UserId,
                 price: float, quantity: float, timestamp: Time):
        self.symbol = symbol
        self.buyer = buyer
        self.seller = seller
        self.price = price
        self.quantity = quantity
        self.timestamp = timestamp

class CompressedTradingState:
    def __init__(self, t: Time, l: List[CompressedListing], od: Dict[ProsperitySymbol, CompressedOrderDepth],
                 ot: List[CompressedTrade], mt: List[CompressedTrade], p: Dict[Product, Position],
                 o: Dict[Product, Observation]):
        self.t = t
        self.l = l
        self.od = od
        self.ot = ot
        self.mt = mt
        self.p = p
        self.o = o

class CompressedOrder:
    def __init__(self, symbol: ProsperitySymbol, price: float, quantity: float):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
