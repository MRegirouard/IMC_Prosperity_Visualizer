# IMC_Prosperity_Visualizer
A custom visualizer to show graphs and display other data from IMC Prosperity algorithm runs.

![image](https://user-images.githubusercontent.com/46038297/234940290-fdbd26e0-747a-41a4-8b21-047c651c83a1.png)

## Motivation
To create profitable trading algorithms, it is imperative that you understand the nature of the assets that you are trading. One way trading teams have done this is by creating and analyzing graphs to find trading ideas. In a competitive environment it is important to move quickly, but we found generating visuals to be tedious and managing our data became more difficult as the 2023 IMC Prosperity competition went on. <br>
This repository aims to make graphing data easy and fast, so users can focus on analysis rather than generating the graphs.

## Inspiration
This project was inspired by the excellent [imc-prosperity-visualizer](https://jmerle.github.io/imc-prosperity-visualizer/) created by [jmerle](https://github.com/jmerle). View the source code [here on GitHub](https://github.com/jmerle/imc-prosperity-visualizer). We used the same [custom logger](https://github.com/jmerle/imc-prosperity-visualizer/blob/323b7247f995dd2e36fb07147d10c7aa546da91b/src/pages/home/HomePage.tsx#L11-L82) with some slight modifications to enable users to save additional data to the log file, and based our log parsing code on jmerle's as well.

## Usage
First, add our [custom logger](https://github.com/MRegirouard/IMC_Prosperity_Visualizer/blob/main/Visualizer/Logger.py) to your IMC Prosperity algorithm. Ensure that you print the `TradingState`, orders your algorithm makes, and any additional values you would like to save to the log file into your `run` function:
```python
orders = {}
values = {}
logger.flush(state, orders, values)
```

After running, download your log and display it in the visualizer by running: <br>
`streamlit run Visualizer/Visualizer.py <log file>` <br>
Where "`<log file>`" the log file downloaded from the IMC Prosperity website. <br>
Then, Streamlit will display a link in the console, and may automatically navigate your browser to this link. After a few moments, the data will load and your desired graphs will show on the screen, if any are configured. By default, no graphs are configured. See the [Using Predefined Graphs](#using-predefined-graphs) and [Adding Custom Graphs](#adding-custom-graphs) sections to add graphs. <br>
<br>
In the top right of the page in your web browser, Streamlit will prompt you to re-run the page when source code has changed, or do so automatically. This makes it much easier and faster to use instead of stopping and restarting the program each time you wish to make a change.

### Using Predefined Graphs
Several commonly-used predefined graphs exist in [`Visualizer/PredefinedGraphs.py`](https://github.com/MRegirouard/IMC_Prosperity_Visualizer/blob/main/Visualizer/PredefinedGraphs.py). To add a predefined graph to the graphs displayed on the Streamlist page, add the name of the function to the `user_graphs` variable in [`Visualizer/UserGraphs.py`](https://github.com/MRegirouard/IMC_Prosperity_Visualizer/blob/main/Visualizer/UserGraphs.py): <br>
`user_graphs: graph_func_list_t = [summary, pnl, mid_prices]` <br>

### Adding Custom Graphs
To create your own graphs, add graphing functions to the [`Visualizer/UserGraphs.py`](https://github.com/MRegirouard/IMC_Prosperity_Visualizer/blob/main/Visualizer/UserGraphs.py) file, and add these functions to the `user_graphs` list. See [`Visualizer/PredefinedGraphs.py`](https://github.com/MRegirouard/IMC_Prosperity_Visualizer/blob/main/Visualizer/PredefinedGraphs.py) and follow functions there as a template. See [`Visualizer/LogParser.py`](https://github.com/MRegirouard/IMC_Prosperity_Visualizer/blob/main/Visualizer/LogParser.py) for information on how log data is stored. Graph functions should take in one argument, the `LogData` object, and return a Plotly Figure to be displayed.

> **_NOTE:_** Please do not push your custom graphs or your `user_graphs` list to this repository. If you feel a graph would be commonly used by other traders, you may add it to the [`Visualizer/PredefinedGraphs.py`](https://github.com/MRegirouard/IMC_Prosperity_Visualizer/blob/main/Visualizer/PredefinedGraphs.py).

### Using Graph Functions with Additional Parameters
Several predefined graphs use additional parameters to narrow down the data. For example, the `pnl_mid_price_product` graph also takes in a `product` argument, for which it will graph the profit and loss, as well as the mid price. This can be easily added to the `user_graphs` list by a lambda function: <br>
```python
user_graphs: graph_func_list_t = [lambda data: pnl_mid_price_product("BANANAS", data)]
```
This will display data specifically for bananas.

### Logging and Graphing Custom Values
To add custom values to your graphs, first print them using the logger. In the past our team has printed values such as slopes of mid prices, technical indicators, and correlation values between two assets. To save these values to the log file, add them to the `values` dictionary before calling `Logger.flush`:
```python
orders = {}
values = {"slope": calc_slope(state, "BANANAS")}
logger.flush(state, orders, values)
```
Then, graph this data by reading from `LogData.values`, which is a list of the values logged for each timestamp.
