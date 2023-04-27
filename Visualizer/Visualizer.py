import streamlit as st
from UserGraphs import user_graphs
from LogParser import parse
import sys
import os

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
    
    # Split the page into two columns
    col1, col2 = st.columns(2)

    # Run each graph function, and display it in alternating columns
    for i, graph_fn in enumerate(user_graphs):
        try:
            graph = graph_fn(data)
            if i % 2 == 0:
                col1.plotly_chart(graph, use_container_width=True)
            else:
                col2.plotly_chart(graph, use_container_width=True)
        except Exception as e:
            if i % 2 == 0:
                col1.warning("Graph " + str(i+1) + " failed to load because of error: " + str(e))
            else:
                col2.warning("Graph " + str(i+1) + " failed to load because of error: " + str(e))
