import streamlit as st
from UserGraphs import user_graphs
from LogParser import parse
import sys
import os
from GraphFuncTypes import graph_func_t
from threading import Thread
from typing import List, Tuple
import plotly.graph_objects as go

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("IMC Prosperity Visualizer")
    
    # Perform some checks before parsing the log file and displaying the graphs
    if not len(sys.argv) == 2:
        print("Usage: " + sys.argv[0] + " <log file>")
        st.error("Usage: " + sys.argv[0] + " <log file>")
        sys.exit(1)
    
    if not os.access(sys.argv[1], os.R_OK):
        print("Error: Cannot read file " + sys.argv[1])
        st.error("Error: Cannot read file " + sys.argv[1])
        print("Usage: " + sys.argv[0] + " <log file>")
        st.error("Usage: " + sys.argv[0] + " <log file>")
        sys.exit(1)
    
    # Read and parse the log file
    try:
        with open(sys.argv[1], "r") as f:
            data = parse(f)
    except Exception as e:
        print("Error parsing log file:", e)
        print("Ensure that the correct logger was used to generate the log file.")
        st.error("Error parsing log file: " + str(e))
        st.error("Ensure that the correct logger was used to generate the log file.")
        sys.exit(1)
    
    # Generate the graphs, asynchronously
    graph_tasks: List[Thread] = []
    graphs: List[Tuple[int, go.Figure | str]] = []

    def gen_graph(graph_func: graph_func_t, index: int) -> None:
        """ 
        A simple function that tries to generate a graph, and adds it to the list of graphs,
        or adds an error message if it fails
        """   
        try:
            graphs.append((index, graph_func(data)))
        except Exception as e:
            graphs.append((index, "Error generating graph: " + str(e)))
    
    # Add a task for each graph function and start the thread
    for i, graph_func in enumerate(user_graphs):
        graph_tasks.append(Thread(target=gen_graph, args=(graph_func,i)))
        graph_tasks[-1].start()
        
    # Wait for all the graphs to finish generating
    for task in graph_tasks:
        task.join()
        
    # Sort the graphs by index, so they show up in the desired order
    graphs.sort(key=lambda x: x[0])
    
    # Split the page into two columns
    col1, col2 = st.columns(2)

    # Run each graph function, and display it in alternating columns
    for i, graph in enumerate(graphs):
        column = col1 if i % 2 == 0 else col2
        
        if isinstance(graph[1], str):
            column.error(graph[1])
        else:
            column.plotly_chart(graph[1], use_container_width=True)
