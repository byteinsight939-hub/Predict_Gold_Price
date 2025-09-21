# 🟡 Gold Price Prediction 

This project is a **machine learning-powered** that predicts future gold prices using historical data and visualizes trends using an interactive interface built with **Dash and Plotly**. Users can log in, select date ranges, and get both historical and future price predictions for gold.

---

## 📊 Features

- 🔐 **User Authentication**: Register and login functionality using SQLite.
- 📈 **Historical Analysis**: Visualize gold price trends from Yahoo Finance.
- 🔮 **Future Forecasting**: Predict gold prices using a trained **Random Forest Regressor**.
- 📅 **Date Selection**: Choose custom date ranges for analysis.
- 📉 **Moving Average Smoothing**: Clean and smooth price trends.
- 📊 **Interactive Graphs**: Built with Plotly for better insights.

---

## ⚙️ Technologies Used

| Layer | Tools |
|------|-------|
| Frontend | Dash, Plotly |
| Backend | Python, Flask (via Dash), SQLite |
| ML Model | RandomForestRegressor (Scikit-Learn) |
| Data Source | [Yahoo Finance](https://finance.yahoo.com/) |
| Deployment Ready | ✅ Flask-compatible `server` object |

---

## 🚀 How to Run

### 🔧 Install Requirements

```bash
pip install -r requirements.txt
```

### ▶️ Run the App

```bash
python app.py
```

## 📁 Project Structure

```
📦 gold-price-prediction
├── app.py                # Main Dash + ML code
├── users.db              # SQLite database for auth
├── README.md             # You are here!
├── images/               # Screenshots for README
└── ...
```

---

## 📌 Notes

- The model uses **day, month, year, and 7-day moving average** for predictions.
- Yahoo Finance gold ticker used: `'GC=F'`.
- You can switch to other tickers (like stock prices or ETFs) with minor changes.
- Works best with a consistent internet connection (for live data fetching).

---



