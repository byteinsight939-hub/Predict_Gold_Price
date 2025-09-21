import sqlite3
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import getpass

def initialize_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def register():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful! You can now log in.")
    except sqlite3.IntegrityError:
        print("Username already exists. Try a different one.")
    conn.close()

def login():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# -------------------------------
# Fetch and Process Gold Price Data
# -------------------------------
def fetch_gold_data():
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    print("Fetching gold price data...")
    data = yf.download('GC=F', start=start_date, end=end_date)
    data['Date'] = data.index
    data['Price'] = data['Close']
    data = data[['Date', 'Price']]
    data.ffill(inplace=True)

    # Feature Engineering
    data['Day'] = data['Date'].dt.dayofyear
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Moving_Avg_7'] = data['Price'].rolling(window=7).mean()
    data.dropna(inplace=True)

    return data

# -------------------------------
# Train Model and Plot Trends
# -------------------------------
def predict_and_plot(data):
    X = data[['Day', 'Year', 'Month', 'Moving_Avg_7']]
    y = data['Price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")

    # Plot Historical vs Predicted Prices
    plt.figure(figsize=(14, 7))
    plt.plot(data['Date'], data['Price'], label='Actual Price', color='blue')
    plt.plot(data['Date'].iloc[-len(y_test):], y_pred, label='Predicted Price', color='red')
    plt.xlabel('Date')
    plt.ylabel('Gold Price')
    plt.title('Gold Price Prediction using Random Forest (Historical Data)')
    plt.legend()
    plt.show()

    # Future Prediction
    future_days = pd.DataFrame({
        'Day': range(1, 367),
        'Year': [2025] * 366,
        'Month': [(i % 12) + 1 for i in range(366)],
        'Moving_Avg_7': [data['Moving_Avg_7'].iloc[-1]] * 366
    })

    future_days['Date'] = pd.date_range(start='2025-01-01', periods=366, freq='D')
    future_prices = model.predict(future_days[['Day', 'Year', 'Month', 'Moving_Avg_7']])
    future_days['Predicted_Price'] = future_prices

    # Plot Historical and Future Predictions
    plt.figure(figsize=(14, 7))
    plt.plot(data['Date'], data['Price'], label='Historical Price', color='blue')
    plt.plot(future_days['Date'], future_days['Predicted_Price'], label='Future Predicted Price', color='green')
    plt.xlabel('Date')
    plt.ylabel('Gold Price')
    plt.title('Gold Price Prediction (Future Trend)')
    plt.legend()
    plt.show()

    print(future_days[['Date', 'Predicted_Price']].head())

# -------------------------------
# Main Program
# -------------------------------
def main():
    initialize_db()
    while True:
        print("\n1️.Register\n2️. Login\n3️. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                print(f"Welcome, {user[1]}!")
                data = fetch_gold_data()
                predict_and_plot(data)
            else:
                print("Invalid username or password.")
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")
            
if __name__ == '__main__':
    main()