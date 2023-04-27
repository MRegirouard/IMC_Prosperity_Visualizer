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

