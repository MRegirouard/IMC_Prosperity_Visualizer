"""
GraphFuncTypes.py

Defines a few types that the graphing functions should adhere to
"""

from typing import Callable, List
import plotly.graph_objects as go
from LogParser import LogData

graph_func_t = Callable[[LogData], go.Figure]
graph_func_list_t = List[graph_func_t]
