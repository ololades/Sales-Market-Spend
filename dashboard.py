import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm

# Load your dataset
@st.cache
def load_data():
    # Replace with your dataset path
    df = pd.read_csv(r"C:\Users\Admin\data-analysis\sales-and-marketing-budget\market_data.csv")
    return df

df = load_data()

# Page Title
st.title("Market Spend Dashboard")

# Sidebar
st.sidebar.subheader("Select Data")

# Chart 1: Scatter Plot
st.subheader("Scatter Plot: Total Sales vs. Average Marketing Spend")
fig1 = px.scatter(df, x='Sale', y='InStrSpending', title='Scatter Plot: Sales vs. Marketing Spend')
st.plotly_chart(fig1)

# Chart 2: Pie Chart
st.subheader("Distribution of Total Sums by Marketing Campaign")
total_sum_by_sales = df.groupby('Sale')[['TVSpending', 'Radio', 'OnlineAdsSpending']].sum()
total_sum_by_sales.reset_index(inplace=True)
columns_all = ['TVSpending', 'Radio', 'OnlineAdsSpending']
total_sums = total_sum_by_sales[columns_all].sum()

fig2 = px.pie(names=columns_all, values=total_sums)

# **Update this section to put the charts in a row**
# col1, col2 = st.columns(2)
st.plotly_chart(fig2)

# # Create a row for Charts 3 and 4
# col1, col2 = st.columns(2)

# Chart 3: Heatmap
st.subheader("Correlation Heatmap")
values = df[['Sale', 'TVSpending', 'Radio', 'OnlineAdsSpending']]
correlation_matrix = values.corr()

fig3 = go.Figure(data=go.Heatmap(
    z=correlation_matrix,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    colorscale='Viridis',
))
fig3.update_layout(width=700, height=500)
st.plotly_chart(fig3)

# Chart 4: Regression Analysis
st.subheader("Regression Analysis of Sales by TV Spending")
tv_spending = sm.add_constant(df.TVSpending)
model = sm.OLS(df.Sale, tv_spending).fit()
tv_coefficient = model.params['TVSpending']
tv_se = model.bse['TVSpending']
t_statistic = tv_coefficient / tv_se
p_value = model.pvalues['TVSpending']
r_squared = model.rsquared

# Create a DataFrame with the statistics
df_stat = pd.DataFrame({
    'Statistic': ['Coefficient', 'Standard Error', 'T-statistic', 'P-value', 'R-squared'],
    'Value': [tv_coefficient, tv_se, t_statistic, p_value, r_squared],
})
# Convert p-value to a string without formatting
df_stat['Value'][3] = str(p_value)
st.write(df_stat)
