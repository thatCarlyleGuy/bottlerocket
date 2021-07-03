# Datatypes
import pandas as pd
# Plotting
from plotly.subplots import make_subplots
import plotly.graph_objects as go

class IPlot(object):
    def __init__(self, pandas_df, vertical_spacing=0.01, shared_xaxes=True, cols = 1, **kwargs):
        self.df = pandas_df
        self.x_axis = self.df.axes[0].date
        self.fig = make_subplots(
            vertical_spacing=vertical_spacing,
            shared_xaxes=shared_xaxes,
            cols = cols,
            **kwargs
        )
   
    def add_simple_plot(self, go_plot, df_key, title = None, row = 3, col = 2, **kwargs):
        if title is None:
            title = df_key
        
        self.fig.append_trace(go_plot(
            x = self.x_axis,
            y = self.df[df_key],
            name = title,
            **kwargs
        ), row = row, col = col)
        
        return self 
    
    def add_ohcl(self, name = 'OHCL', row = 1, col = 1):
        self.fig.append_trace(go.Candlestick(
            x = self.x_axis,
            open = self.df['open'],
            high = self.df['high'],
            low = self.df['low'],
            close = self.df['close'],
            name = name
        ), row = row, col = col)
        
        return self
    
    def add_volume(self, name = 'Volume', row = 2, col = 1):
        return self.add_simple_plot(go.Bar, 'volume', name, row, col)
    
    def add_scatter(self, df_key, title = None, row = 3, col = 1, **kwargs):
        return self.add_simple_plot(go.Scatter, df_key, title, row, col, **kwargs)
    
    def add_lines(self, lines):
        default_args = {'row': 3, 'col': 1}
        with_default_args = lambda args: {**default_args, **args}
        
        for line_args in lines:
            self.add_scatter(**with_default_args(line_args))
    
        return self
    
    def add_histogram(self, df_key, title = None, row = 3, col = 1, **kwargs):
        return self.add_simple_plot(go.Bar, df_key, title, row, col, **kwargs)
    
    def add_fill_between_lines(self, from_line, to_line, fill_color, row = 1, col = 1):
        from_args = from_line['args'] if 'args' in from_line else {} 
        to_args = to_line['args'] if 'args' in to_line else {} 
        
        self.fig.append_trace(go.Scatter(
            x = self.x_axis,
            y = pd.concat([
                self.df[from_line['df_key']],
                self.df[to_line['df_key']]
            ]),
            name = from_line['name'],
            fill = None,
            mode = 'lines',
            **from_args
        ), row = row, col = col)

        self.fig.append_trace(go.Scatter(
            x = self.x_axis,
            y = pd.concat([
                self.df[to_line['df_key']],
                self.df[to_line['df_key']]
            ]),
            name = to_line['name'],
            fill = fill_color,
            mode = 'lines',
            **to_args
        ), row = row, col = col)
        
        return self
    
    def show_plot(self, title = '', height = 900, xaxis_rangeslider_visible = False, **kwargs):
        self.fig.update_layout(
            height = height,
            xaxis_rangeslider_visible = xaxis_rangeslider_visible,
            title_text = title,
            **kwargs
        )
        self.fig.show()
        
        return self