import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # for deployment

# App Layout
app.layout = html.Div([
    html.H1("Gold Price Prediction Dashboard"),
    
    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id='date-range',
        start_date='2020-01-01',
        end_date='2025-01-01'
    ),
    
    html.Button("Fetch & Predict", id='fetch-btn', n_clicks=0),
    
    dcc.Graph(id='historical-graph'),
    dcc.Graph(id='future-graph')
])

# Callback for fetching data and updating graphs
@app.callback(
    [Output('historical-graph', 'figure'),
     Output('future-graph', 'figure')],
    [Input('fetch-btn', 'n_clicks')],
    [dash.dependencies.State('date-range', 'start_date'),
     dash.dependencies.State('date-range', 'end_date')]
)
def update_graphs(n_clicks, start_date, end_date):
    if n_clicks == 0:
        return {}, {}
    
    # Fetch data
    data = yf.download('GC=F', start=start_date, end=end_date)
    data['Date'] = pd.to_datetime(data.index)
    data['Price'] = data['Close']
    data = data[['Date', 'Price']]
    data.ffill(inplace=True)
    data['Day'] = data['Date'].dt.dayofyear
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Moving_Avg_7'] = data['Price'].rolling(7).mean()
    data.dropna(inplace=True)
    
    # Chronological train/test split
    train_size = int(len(data) * 0.8)
    X_train = data[['Day', 'Year', 'Month', 'Moving_Avg_7']].iloc[:train_size]
    y_train = data['Price'].iloc[:train_size]
    X_test = data[['Day', 'Year', 'Month', 'Moving_Avg_7']].iloc[train_size:]
    y_test = data['Price'].iloc[train_size:]
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Smooth predictions
    y_pred_smooth = pd.Series(y_pred).rolling(5, min_periods=1).mean()
    test_dates = data['Date'].iloc[train_size:]
    
    # Historical vs Test Plot
    hist_fig = go.Figure()
    hist_fig.add_trace(go.Scatter(x=data['Date'], y=data['Price'], mode='lines', name='Historical'))
    hist_fig.add_trace(go.Scatter(x=test_dates, y=y_pred_smooth, mode='lines', name='Predicted (Test)'))
    hist_fig.update_layout(title='Historical vs Test Predictions', xaxis_title='Date', yaxis_title='Gold Price')
    
    # Future Prediction
    future_days = pd.DataFrame()
    future_days['Date'] = pd.date_range(start='2025-01-01', periods=366, freq='D')
    future_days['Day'] = future_days['Date'].dt.dayofyear
    future_days['Year'] = future_days['Date'].dt.year
    future_days['Month'] = future_days['Date'].dt.month
    future_days['Moving_Avg_7'] = data['Moving_Avg_7'].iloc[-1]
    future_prices = model.predict(future_days[['Day', 'Year', 'Month', 'Moving_Avg_7']])
    future_days['Predicted_Price'] = future_prices
    
    future_fig = go.Figure()
    future_fig.add_trace(go.Scatter(x=data['Date'], y=data['Price'], mode='lines', name='Historical'))
    future_fig.add_trace(go.Scatter(x=future_days['Date'], y=future_days['Predicted_Price'], mode='lines', name='Future Predicted'))
    future_fig.update_layout(title='Future Gold Price Predictions', xaxis_title='Date', yaxis_title='Gold Price')
    
    return hist_fig, future_fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)
