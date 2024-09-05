import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv("food_orders_new_delhi.csv")

# Load data and perform necessary cleaning
food_orders = load_data()

# Convert 'Order Date and Time' to datetime, coerce errors
food_orders['Order Date and Time'] = pd.to_datetime(food_orders['Order Date and Time'], errors='coerce')

# Create 'Discount Percentage' column for percentage discounts
food_orders['Discount Percentage'] = food_orders['Discounts and Offers'].str.extract(r'(\d+)%')[0].astype(float)

# Create 'Fixed Discount' column for fixed amount discounts
food_orders['Fixed Discount'] = food_orders['Discounts and Offers'].str.extract(r'(\d+)\s*off')[0].astype(float)

# Fill missing discount values with 0
food_orders['Discount Percentage'] = food_orders['Discount Percentage'].fillna(0)
food_orders['Fixed Discount'] = food_orders['Fixed Discount'].fillna(0)

# Calculate 'Discount Amount'
food_orders['Discount Amount'] = np.where(
    food_orders['Discount Percentage'] > 0,
    food_orders['Order Value'] * food_orders['Discount Percentage'] / 100,
    food_orders['Fixed Discount']
)

# Calculate Revenue, Costs, and Profit
food_orders['Revenue'] = food_orders['Order Value'] + food_orders['Delivery Fee']
food_orders['Costs'] = (food_orders['Commission Fee'] +
                        food_orders['Payment Processing Fee'] +
                        food_orders['Refunds/Chargebacks'])
food_orders['Profit'] = food_orders['Revenue'] - food_orders['Costs']

# Total calculations
total_revenue = food_orders['Revenue'].sum()
total_cost = food_orders['Costs'].sum()
total_profit = food_orders['Profit'].sum()

# Streamlit Dashboard
st.title("Food Delivery Data Analysis Dashboard")

# Show a preview of the data
st.write("### Data Preview")
st.write(food_orders.head())

# Show key metrics
st.write("### Key Metrics")
st.write(f"**Total Revenue**: ₹{total_revenue:,.2f}")
st.write(f"**Total Costs**: ₹{total_cost:,.2f}")
st.write(f"**Total Profit**: ₹{total_profit:,.2f}")

# Visualizations
st.write("### Visualizations")

# Order Value Distribution
st.write("#### Order Value Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(food_orders['Order Value'], kde=True, color='blue', bins=30, ax=ax1)
ax1.set_title('Distribution of Order Value')
st.pyplot(fig1)

# Profit Distribution
st.write("#### Profit Distribution")
fig2, ax2 = plt.subplots()
sns.histplot(food_orders['Profit'], kde=True, color='green', bins=30, ax=ax2)
ax2.set_title('Distribution of Profit')
st.pyplot(fig2)

# Discount Amount Distribution
st.write("#### Discount Amount Distribution")
fig3, ax3 = plt.subplots()
sns.histplot(food_orders['Discount Amount'], kde=True, color='orange', bins=30, ax=ax3)
ax3.set_title('Distribution of Discount Amount')
st.pyplot(fig3)

# Correlation Heatmap
st.write("#### Correlation Heatmap")
fig4, ax4 = plt.subplots()
correlation_matrix = food_orders[['Order Value', 'Delivery Fee', 'Revenue', 'Costs', 'Profit']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax4)
ax4.set_title('Correlation Heatmap of Financial Variables')
st.pyplot(fig4)

# Profit by Payment Method
st.write("#### Profit by Payment Method")
fig5, ax5 = plt.subplots()
sns.boxplot(data=food_orders, x='Payment Method', y='Profit', palette='Set2', ax=ax5)
ax5.set_title('Profit by Payment Method')
plt.xticks(rotation=45)
st.pyplot(fig5)

# Scatter plot: Order Value vs Profit with regression line
st.write("#### Order Value vs Profit")
fig6, ax6 = plt.subplots()
sns.regplot(data=food_orders, x='Order Value', y='Profit', scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'}, ax=ax6)
ax6.set_title('Order Value vs Profit')
st.pyplot(fig6)

# Average profit per restaurant
st.write("#### Top 10 Restaurants by Average Profit")
avg_profit_per_restaurant = food_orders.groupby('Restaurant ID')['Profit'].mean().reset_index().sort_values(by='Profit', ascending=False)
fig7, ax7 = plt.subplots()
sns.barplot(data=avg_profit_per_restaurant.head(10), x='Restaurant ID', y='Profit', palette='Blues_d', ax=ax7)
ax7.set_title('Top 10 Restaurants by Average Profit')
plt.xticks(rotation=45)
st.pyplot(fig7)
