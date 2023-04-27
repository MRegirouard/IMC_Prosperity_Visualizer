import plotly.graph_objects as go
import plotly.express as px
from plotly import subplots as sp
from LogParser import LogData
from datamodel import *

def summary(data: LogData) -> go.Figure:
    """
    Displays the total PnL and the last timestamp using plotly's indicator graph
    """
    fig = sp.make_subplots(rows=1, cols=2, subplot_titles=("Total PnL", "Last Timestamp"),
        specs=[[{"type": "indicator"}, {"type": "indicator"}]])
    total_pnl: float = 0
 
    # Track pnl for each product
    for product in data.activities:
        activity_log = data.activities[product]
        total_pnl += activity_log[-1].profit_and_loss
    
    fig.add_trace(go.Indicator(value=total_pnl), row=1, col=1)
    fig.add_trace(go.Indicator(value=data.trading_states[-1].timestamp,  number={"valueformat": "d"}), row=1, col=2)
    fig.update_layout(title="Log Summary")
    return fig

def pnl(data: LogData) -> go.Figure:
    """
    Graphs the PnL for each product, as well as the total PnL
    """
    fig = go.Figure()
    timestamps = [activity_data.timestamp for activity_data in data.activities[list(data.activities.keys())[0]]]
    total_pnl: List[float] = [0] * len(timestamps)
    
    for product in data.activities:
        activity_log = data.activities[product]
        pnl = [activity_data.profit_and_loss for activity_data in activity_log]
        total_pnl = [total_pnl[i] + pnl[i] for i in range(len(pnl))]
        fig.add_trace(go.Scatter(x=timestamps, y=pnl, name=product))
        
    fig.add_trace(go.Scatter(x=timestamps, y=total_pnl, name="Total PnL"))
    fig.update_layout(title="Profit and Loss", xaxis_title="Timestamp", yaxis_title="PnL")
    return fig

def mid_prices(data: LogData) -> go.Figure:
    """
    Displays the mid price for each product
    """
    fig = go.Figure()
    
    for product in data.activities:
        activity_log = data.activities[product]
        timestamps = [activity_data.timestamp for activity_data in activity_log]
        mid_prices = [activity_data.mid_price for activity_data in activity_log]
        fig.add_trace(go.Scatter(x=timestamps, y=mid_prices, name=product))
        
    fig.update_layout(title="Mid Prices", xaxis_title="Timestamp", yaxis_title="Price")
    return fig

def pnl_mid_price_product(product: Product, data: LogData) -> go.Figure:
    """
    Displays the PnL and mid price for a given product
    """
    activity_log = data.activities[product]
    timestamps = [activity_data.timestamp for activity_data in activity_log]
    mid_prices = [activity_data.mid_price for activity_data in activity_log]
    pnl_values = [activity_data.profit_and_loss for activity_data in activity_log]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timestamps, y=mid_prices, name=product))
    fig.add_trace(go.Scatter(x=timestamps, y=pnl_values, name=product + " PnL"))
    fig.update_layout(title="Mid Price and PnL for " + product, xaxis_title="Timestamp", yaxis_title="Price")
    return fig

def logged_values(values: List[str], data: LogData) -> go.Figure:
    """
    Plots desired values from log file
    """
    fig = go.Figure()
    timestamps = [activity_data.timestamp for activity_data in data.activities[list(data.activities.keys())[0]]]
    
    for value in values:
        logged_values = [data.values[i][value] for i in range(len(data.values))]
        fig.add_trace(go.Scatter(x=timestamps, y=logged_values, name=value))
    
    fig.update_layout(title="Logged Values", xaxis_title="Timestamp", yaxis_title="Value")
    return fig
