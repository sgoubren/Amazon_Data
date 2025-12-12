import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import re
import plotly.express as px

amazon_data = pd.read_csv('amazon_anonymized.csv')

st.set_page_config(page_title="Amazon Orders Dashboard", layout="wide")

def orange_header(text):
    st.markdown(f"<h2 style='color:#FF9900'>{text}</h2>", unsafe_allow_html=True)

def orange_title(text):
    st.markdown(f"<h1 style='color:#FF9900'>{text}</h1>", unsafe_allow_html=True)


orange_title('Amazon Orders Personal Dashboard')

# -----------------------------
# KPI On Top
# -----------------------------

total_lifetime_spending = round(amazon_data['total_owed'].sum(), 0)
total_items_purchased = amazon_data['quantity'].sum()
spending_2025 = round(amazon_data[amazon_data['year'] == 2025]['total_owed'].sum(),0)

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Lifetime Spending", f"${total_lifetime_spending}")
col2.metric("🛒 Total Items Purchased", f"{total_items_purchased}")
col3.metric("📅 Total Spending in 2025", f"${spending_2025:,}")

# st.markdown("---")
st.write('')

section = st.sidebar.selectbox(
    "Jump to Section",
    [
        "KPI Overview",
        "Annual Spending with YoY % Change",
        "Spending per Website",
        "Spending Percentage per City in the U.S.",
        "5 Most Expensive Purchases",
        "5 Most Repurchased Items on amazon.com",
        "Monthly Spending Overview Across All Years"
    ]
)


# -------------------------------
# Annual Spending
# -------------------------------
if section == "Annual Spending with YoY % Change":
    orange_header("📈 Annual Spending with YoY % Change")
    st.write("""
    - Until **2021**, annual spending remained below **$300**, indicating occasional ordering.
    - Spending increased sharply beginning in **2021**, then plateaued around **$2,800** from 2023 onward.
    - A major life event in 2021 (e.g., welcoming children) likely contributed to drive up reliance on Amazon for household needs.
    """)

# group by year + aggregate
    yearly_summary = amazon_data.groupby('year').agg(
    total_spending=('total_owed', 'sum'),
    total_items=('quantity', 'sum')
    ).reset_index()

    yearly_summary['total_spending'] = yearly_summary['total_spending'].round(2)
    yearly_summary['YoY_pct'] = yearly_summary['total_spending'].pct_change() * 100
    yearly_summary = yearly_summary.sort_values('year')

# draw the plot
    plt.figure(figsize=(10, 4))
    ax = sns.barplot(
    x='year', 
    y='total_spending', 
    data=yearly_summary, 
    color='#FF9900'  # Amazon orange
)

    ax.set_ylim(0, 3500)

# put pct on top of bar
    for idx, p in enumerate(ax.patches):
        height = p.get_height()
        if idx > 7:
            yoy = yearly_summary['YoY_pct'].iloc[idx]
            ax.text(
            x=p.get_x() + p.get_width() / 2,
            y=height + 0.01 * yearly_summary['total_spending'].max(),
            s=f"{yoy:.1f}%",
            ha='center',
            va='bottom',
            fontsize=12,
            color='darkblue'
            )


    plt.xlabel('Year', fontsize=12)
    plt.ylabel('$ Total Spending', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    st.pyplot(plt, use_container_width=False)  

    st.markdown("---")

# -----
# Spending per website
# -----
elif section == "Spending per Website":
    orange_header("🌐 Spending per Website")
    st.write("""
    - Over **90%** of total spending occurs on **Amazon.com**.
    - **Amazon.fr** and **Whole Foods Market** account for only a small share of spending, likely due to international travel (amazon.fr) and local grocery purchases (Whole Foods).
""")

    fig, ax = plt.subplots(figsize=(3, 3))
    counts = amazon_data['website'].value_counts()
    ax.pie(
    counts,
    labels=counts.index,         # dynamic, order always matches
    colors=['#FF9900', '#146EB4', '#00A8E1'],
    autopct='%.1f%%',
    radius=1
    )

    st.pyplot(fig, use_container_width=False)


# -----
# Spending per city
# -----
elif section == "Spending Percentage per City in the U.S.":
    orange_header("🌎 Spending Percentage per City in the U.S.")
    st.write("""
    - Nearly **90%** of total spending occurs in **San Jose, CA**, the primary delivery location.
    - Smaller shares of spending in other U.S cities likely due to relocation across the years.
""")

# group by cities
    city_spending = amazon_data.groupby('shipping_city')['total_owed'].sum().reset_index()
    city_spending = city_spending.sort_values(by='total_owed', ascending=False)
    city_spending['Percentage'] = (
        city_spending['total_owed'] / city_spending['total_owed'].sum() * 100
    ).round(1)
    city_spending = city_spending.rename(columns={
    'shipping_city': 'city',
    'total_owed': 'total_spend'
    })
    city_spending['total_spend'] = city_spending['total_spend'].round(0)

# cities coordinates
    city_coords = {
    'San Jose': {'lat': 37.3382, 'lon': -121.8863},
    'Portland': {'lat': 45.5152, 'lon': -122.6784},
    'Los Angeles': {'lat': 34.0522, 'lon': -118.2437},
    'France': {'lat': 48.8566, 'lon': 2.3522},
    'Chicago': {'lat': 41.8781, 'lon': -87.6298},
    'Milwaukee': {'lat': 43.0389, 'lon': -87.9065}
    }

    city_spending['lat'] = city_spending['city'].map(lambda x: city_coords.get(x, {}).get('lat'))
    city_spending['lon'] = city_spending['city'].map(lambda x: city_coords.get(x, {}).get('lon'))

# Filter out missing coordinates
    city_spending_map = city_spending.dropna(subset=['lat', 'lon'])

# bubble US map
    fig = px.scatter_geo(
    city_spending_map,
    lat='lat',
    lon='lon',
    scope='usa',
    size='total_spend',
    hover_name='city',
    hover_data={
        'Percentage': ':.1f',
        'total_spend': ':,.0f',
        'lat': False,
        'lon': False
        },
    size_max=60,
    template='plotly_white',
    projection='albers usa',
    color_discrete_sequence=['#FF9900'],
    width=900,
    height=550
    )

    fig.update_layout(
    margin=dict(l=10, r=10, t=40, b=10)
    )

    st.plotly_chart(fig, use_container_width=False)

#----
# 5 Most Expensive Purchases
# ----
elif section == "5 Most Expensive Purchases":
    orange_header("💰 5 Most Expensive Purchases")

    st.write("""
    - The most expensive purchase peaks at **$120**, a moderate spend per order.
    - The top 3 purchases appear to be occasional, possibly for gifts or special occasions.
    - Even the most expensive items are relatively low-cost, showing a pattern of frequent small purchases rather than high-value orders.
        """)

    # Function to shorten product name
    def shorten_name(name):
        match = re.search(r'[,.|]', name)  
        if match:
            return name[:match.start()]   
        else:
            return name                   

    sorted_cost = amazon_data.sort_values(by='total_owed', ascending=False).head(5)
    sorted_cost['total_owed'] = sorted_cost['total_owed'].apply(lambda x: f"{x:,.2f}")
    sorted_cost['product_name']= sorted_cost['product_name'].apply(shorten_name)

    st.dataframe(sorted_cost[['product_name', 'total_owed', 'website', 'month', 'year']].rename(columns={
        'product_name': 'Product',
        'total_owed': 'Total Spent ($)',
        'website': 'Website',
        'month': 'Month',
        'year': 'Year'}).reset_index(drop=True), width=1200)



#----
# 5 most repurchased products
# --- 
elif section == "5 Most Repurchased Items on amazon.com":
    orange_header("🔁 5 Most Repurchased Items on amazon.com")

    st.write("""
    - The most repurchased items correspond to recurring household or personal care needs.
    - High repurchase frequency suggests a reliance on Amazon for daily items.
    - Spending on these articles is moderate, confirming pattern of frequent small purchases rather than occasional large orders.
        """)

        # Function to shorten product name
    def shorten_name(name):
        match = re.search(r'[,.|]', name)  
        if match:
            return name[:match.start()]   
        else:
            return name                  


    amazon_repurchased = amazon_data[amazon_data['website'] != "Whole Foods Market"]
    top5_repurchased = (
        amazon_repurchased
        .groupby('product_name')
        .agg(
            times_purchased=('product_name', 'count'),
            total_spent=('total_owed', 'sum')
        )
        .sort_values(by='times_purchased', ascending=False)
        .head(5)
        .reset_index()
    )

    top5_repurchased['total_spent'] = top5_repurchased['total_spent'].apply(lambda x: f"{x:,.2f}")
    top5_repurchased['product_name'] = top5_repurchased['product_name'].apply(shorten_name)

    st.dataframe (top5_repurchased[['product_name', 'times_purchased','total_spent']].rename(columns={
            'product_name': 'Product',
            'times_purchased': 'Times Purchased',
            'total_spent': 'Total Spent ($)',
            'month': 'Month',
            'year': 'Year'}).reset_index(drop=True),width=1200)

#----
# Spending per Months across the years
#----
elif section == "Monthly Spending Overview Across All Years":
    orange_header('💰 Monthly Spending Overview Across All Years')

    st.write("""
    - Spending is higher in **November**, likely due to seasonal deals (Black Friday) and holiday preparation.
    - Lower spending in **January/February** is consistent with the post-holiday slowdown.
    - Average order value is stable across the months, indicating higher spending is driven by more items ordered, not higher-priced purchases.
        """)

    monthly_spending = amazon_data.groupby(['month', 'month_name'])['total_owed'].sum().reset_index()
    monthly_spending = monthly_spending.sort_values('month')
    monthly_spending['total_owed'] = monthly_spending['total_owed'].round(2)
    monthly_spending_sorted = monthly_spending.sort_values(by='total_owed', ascending=False)

    #  bar charts
    plt.figure(figsize=(10,6))
    sns.barplot(
        y='month_name', 
        x='total_owed', 
        data=monthly_spending_sorted, 
        color='#FF9900'
    )

    plt.ylabel('Month', fontsize=12)
    plt.xlabel('Total Spending ($)', fontsize=12)
    plt.xticks(rotation=0)
    plt.tight_layout()


    # table 
    monthly_summary = amazon_data.groupby('month').agg(
        total_owed=('total_owed', 'sum'),
        items_purchased=('quantity', 'sum')
    ).reset_index()

    monthly_summary['month_name'] = monthly_summary['month'].apply(lambda x: pd.to_datetime(str(x), format='%m').strftime('%b'))
    monthly_summary = monthly_summary.sort_values('month')
    monthly_summary['total_owed'] = monthly_summary['total_owed'].round(2)
    monthly_summary_sorted = monthly_summary.sort_values(by='total_owed', ascending=False)
    monthly_summary_sorted['avg_per_order'] = (monthly_summary_sorted['total_owed'] / monthly_summary_sorted['items_purchased']).round(2)


    # plotting/organizing them 
    col1, col2 = st.columns([2,1])

    with col1:
        st.pyplot(plt, use_container_width=True)

    with col2:
        st.dataframe(monthly_summary_sorted[['month_name', 'items_purchased', 'avg_per_order']].rename(columns={
            'month_name': 'Month',
            'items_purchased': 'Items Purchased',
            'avg_per_order': 'Avg Order Value ($)'
        }).reset_index(drop=True), width=400)