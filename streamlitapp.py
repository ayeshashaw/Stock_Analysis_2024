import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Function to fetch data from the database
def fetch_data_from_db(table_name):
    # Define your database connection string
    db_connection_str = 'mysql+pymysql://root:Ayesha@localhost:3306/stock_analysis'
    db_connection = create_engine(db_connection_str)

    # Fetch data from the specified table
    df = pd.read_sql(f'SELECT * FROM {table_name}', con=db_connection)
    return df

# Function to calculate moving averages and signals
def calculate_signals(df):
    # Calculate moving averages
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_500'] = df['Close'].rolling(window=500).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_5'] = df['Close'].rolling(window=5).mean()

    # Generate buy and sell signals
    df['Buy_Signal'] = np.where(df['SMA_50'] > df['SMA_500'], df['Close'], np.nan)
    df['Sell_Signal'] = np.where(df['SMA_20'] < df['SMA_200'], df['Close'], np.nan)
    df['Close_Buy_Position'] = np.where((df['SMA_10'] < df['SMA_20']) & (df['SMA_10'].shift(1) > df['SMA_20'].shift(1)), df['Close'], np.nan)
    df['Close_Sell_Position'] = np.where((df['SMA_5'] > df['SMA_10']) & (df['SMA_5'].shift(1) < df['SMA_10'].shift(1)), df['Close'], np.nan)

    return df

# Function to plot the dashboard
def plot_dashboard(df):
    fig, axs = plt.subplots(6, 1, figsize=(10, 20))

    # Plot Close Price and Moving Averages (50-day and 500-day)
    axs[0].plot(df.index, df['Close'], label='Close Price', color='black')
    axs[0].plot(df.index, df['SMA_50'], label='50-day SMA', color='blue')
    axs[0].plot(df.index, df['SMA_500'], label='500-day SMA', color='red')
    axs[0].set_title('Close Price and Moving Averages (50-day and 500-day)')
    axs[0].legend()

    # Plot Close Price and Moving Averages (20-day and 200-day)
    axs[1].plot(df.index, df['Close'], label='Close Price', color='black')
    axs[1].plot(df.index, df['SMA_20'], label='20-day SMA', color='orange')
    axs[1].plot(df.index, df['SMA_200'], label='200-day SMA', color='green')
    axs[1].set_title('Close Price and Moving Averages (20-day and 200-day)')
    axs[1].legend()

    # Plot Close Price and 10-day SMA
    axs[2].plot(df.index, df['Close'], label='Close Price', color='black')
    axs[2].plot(df.index, df['SMA_10'], label='10-day SMA', color='purple')
    axs[2].set_title('Close Price and 10-day SMA')
    axs[2].legend()

    # Plot Close Price and 5-day SMA
    axs[3].plot(df.index, df['Close'], label='Close Price', color='black')
    axs[3].plot(df.index, df['SMA_5'], label='5-day SMA', color='brown')
    axs[3].set_title('Close Price and 5-day SMA')
    axs[3].legend()

    # Plot Buy and Sell Signals
    axs[4].plot(df.index, df['Close'], label='Close Price', color='black')
    axs[4].scatter(df.index, df['Buy_Signal'], marker='^', color='green', label='Buy Signal')
    axs[4].scatter(df.index, df['Sell_Signal'], marker='v', color='red', label='Sell Signal')
    axs[4].set_title('Buy and Sell Signals')
    axs[4].legend()

    # Plot Close Buy and Sell Positions
    axs[5].plot(df.index, df['Close'], label='Close Price', color='black')
    axs[5].scatter(df.index, df['Close_Buy_Position'], marker='o', color='blue', label='Close Buy Position')
    axs[5].scatter(df.index, df['Close_Sell_Position'], marker='o', color='orange', label='Close Sell Position')
    axs[5].set_title('Close Buy and Sell Positions')
    axs[5].legend()

    plt.tight_layout()
    st.pyplot(fig)

# Streamlit app
def main():
    st.title('Stock Analysis Dashboard')

    # Select table from the database
    table_name = st.selectbox('Select Table:', ['aapl', 'tsla', 'hdb', 'jiofin', 'mara', 'tatamotors', 'inr'])  # Add more tables as needed

    # Fetch data from the selected table
    df = fetch_data_from_db(table_name)

    # Calculate moving averages and signals
    df = calculate_signals(df)

    # Plot the dashboard
    plot_dashboard(df)

if __name__ == "__main__":
    main()
