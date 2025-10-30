import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# ---------------------- DATABASE CONNECTION ----------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",                # 🔹 your MySQL username
        password="Mysql@123",   # 🔹 your MySQL password
        database="phonepe_db"
    )

# ---------------------- LOAD DATA ----------------------
def load_table(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# ---------------------- STREAMLIT SETUP ----------------------
st.set_page_config(layout="wide")
st.title("📊 PhonePe Data Visualization Dashboard (MySQL Version)")

menu = st.sidebar.radio("Choose Section", ["Home", "Data Preview", "Analysis"])

# ---------------------- HOME PAGE ----------------------
if menu == "Home":
    st.header("Welcome to the PhonePe Analysis Dashboard")
    st.write("""
    This dashboard visualizes PhonePe Pulse data directly from your MySQL database.

    - Explore **Transaction Trends, Insurance, and User Metrics**
    - Analyze by **Year, State, and Brand**
    - Powered by **Streamlit + MySQL + Plotly**
    """)
    st.image("https://www.phonepe.com/images/page-banner.png", use_container_width=True)

# ---------------------- DATA PREVIEW ----------------------
elif menu == "Data Preview":
    st.subheader(" View Raw Data from MySQL")

    table = st.selectbox(
        "Select a Table",
        [
            "aggregated_insurance",
            "aggregated_transaction",
            "aggregated_user",
            "map_insurance",
            "map_transaction",
            "map_user",
            "top_insurance",
            "top_transaction",
            "top_user"
        ]
    )

    df = load_table(table)
    st.write(f"✅ Loaded `{table}` with {len(df)} rows and {len(df.columns)} columns")
    st.dataframe(df.head(10))

# ---------------------- ANALYSIS PAGE ----------------------
elif menu == "Analysis":
    st.subheader("📈 Analyze Transactions & Users")

    table = st.selectbox(
        "Choose Dataset for Analysis",
        [
            "aggregated_insurance",
            "aggregated_transaction",
            "aggregated_user",
            "map_transaction",
            "map_user",
            "top_transaction",
            "top_user"
        ]
    )

    df = load_table(table)
    st.success(f"✅ Data loaded from `{table}` ({len(df)} rows)")

    # Common Year Filter
    if "year" in df.columns:
        year = st.selectbox("Select Year", sorted(df["year"].unique()))
        df = df[df["year"] == year]

    st.markdown("---")

    # ========== AGGREGATED INSURANCE ==========
    if table == "aggregated_insurance":
        st.write(f"### 📊 Aggregated Insurance Data - {year}")
        fig1 = px.bar(df, x="name", y="amount", title="Transaction Amount by Name", color="name")
        fig2 = px.bar(df, x="name", y="count", title="Transaction Count by Name", color="name")
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)

    # ========== AGGREGATED TRANSACTION ==========
    elif table == "aggregated_transaction":
        st.write(f"### 💳 Aggregated Transactions - {year}")
        fig1 = px.bar(df, x="category", y="amount", color="type",
                      title="Transaction Amount by Category")
        fig2 = px.bar(df, x="category", y="count", color="type",
                      title="Transaction Count by Category")
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)

    # ========== AGGREGATED USER ==========
    elif table == "aggregated_user":
        st.write(f"### 👤 User Statistics - {year}")
        fig1 = px.bar(df, x="brand", y="count", title="Transactions by Brand", color="brand")
        fig2 = px.line(df, x="brand", y="registered_users",
                       title="Registered Users by Brand", markers=True)
        fig3 = px.line(df, x="brand", y="app_opens",
                       title="App Opens by Brand", markers=True)
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)

    # ========== MAP TRANSACTION / INSURANCE ==========
    elif table in ["map_transaction", "map_insurance"]:
        st.write(f"### 🗺️ Map Data - {year}")
        fig1 = px.bar(df, x="state", y="amount", title="Transaction Amount by State")
        fig2 = px.bar(df, x="state", y="count", title="Transaction Count by State")
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)

    # ========== MAP USER ==========
    elif table == "map_user":
        st.write(f"### 🧭 Map User Data - {year}")
        fig1 = px.bar(df, x="state", y="registered_users", title="Registered Users by State")
        fig2 = px.line(df, x="state", y="app_opens", title="App Opens by State", markers=True)
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)

    # ========== TOP TRANSACTION / INSURANCE ==========
    elif table in ["top_transaction", "top_insurance"]:
        st.write(f"### 🏆 Top Performing Entities - {year}")
        fig1 = px.bar(df, x="entity", y="amount", title="Top Entities by Amount", color="entity")
        fig2 = px.bar(df, x="entity", y="count", title="Top Entities by Count", color="entity")
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig2, use_container_width=True)

    # ========== TOP USER ==========
    elif table == "top_user":
        st.write(f"### 🏅 Top Users - {year}")
        fig1 = px.bar(df, x="entity", y="registered_users",
                      title="Top Entities by Registered Users", color="entity")
        st.plotly_chart(fig1, use_container_width=True)
