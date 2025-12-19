import streamlit as st
import pandas as pd

# Page configuration for a "beautiful" layout
st.set_page_config(page_title="Singapore Population Analytics", layout="wide")

# Custom CSS to enhance the look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Loading the dataset referenced in your notebook
    df = pd.read_csv('Singapore_Residents.csv')
    return df

try:
    df = load_data()
    
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Total Population", 
        "Ethnic Group Ratios", 
        "Gender Analysis"
    ])

    st.title("🇸🇬 Singapore Resident Population Analytics")
    st.markdown("---")

    if page == "Total Population":
        st.header("Annual Population Overview")
        
        # Displaying total population every year
        pop_df = df[df['Residents'] == 'Total Residents'][['Year', 'Count']].sort_values('Year')
        
        # Key Metrics Row
        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Count (2018)", f"{pop_df['Count'].iloc[-1]:,}")
        col2.metric("Starting Count (2000)", f"{pop_df['Count'].iloc[0]:,}")
        growth = ((pop_df['Count'].iloc[-1] - pop_df['Count'].iloc[0]) / pop_df['Count'].iloc[0]) * 100
        col3.metric("Total Growth", f"{growth:.2f}%")

        st.subheader("Data Summary")
        st.dataframe(pop_df.style.format({"Count": "{:,}"}), use_container_width=True)

    elif page == "Ethnic Group Ratios":
        st.header("Ethnic Group Gender Ratios")
        st.info("Ratio calculation: Female Count / Male Count")

        # Logic for Other Ethnic Groups Ratio
        years_filter = [2000, 2003, 2006, 2009, 2012]
        
        eth_m = df[(df['Residents'] == 'Other Ethnic Groups (Males)') & (df['Year'].isin(years_filter))]
        eth_f = df[(df['Residents'] == 'Other Ethnic Groups (Females)') & (df['Year'].isin(years_filter))]
        
        merge_df = pd.merge(eth_f, eth_m, on='Year', suffixes=('_Female', '_Male'))
        merge_df['Ratio'] = merge_df['Count_Female'] / merge_df['Count_Male']
        
        # Displaying results in a beautiful table
        st.subheader("Other Ethnic Groups (3-Year Intervals)")
        st.table(merge_df[['Year', 'Count_Female', 'Count_Male', 'Ratio']].style.format({
            "Count_Female": "{:,}", 
            "Count_Male": "{:,}", 
            "Ratio": "{:.4f}"
        }))

    elif page == "Gender Analysis":
        st.header("Chinese & Indian Resident Analysis")
        
        tab1, tab2 = st.tabs(["Chinese Residents", "Indian Residents"])
        
        with tab1:
            # Male vs Female Chinese Residents
            c_m = df[df['Residents'] == 'Total Male Chinese']
            c_f = df[df['Residents'] == 'Total Female Chinese']
            c_merge = pd.merge(c_f, c_m, on='Year', suffixes=('_F', '_M'))
            st.dataframe(c_merge[['Year', 'Count_F', 'Count_M']], use_container_width=True)

        with tab2:
            # Indian Resident Ratio Logic
            in_m = df[df['Residents'] == 'Total Male Indians']
            in_f = df[df['Residents'] == 'Total Female Indians']
            in_merge = pd.merge(in_f, in_m, on='Year', suffixes=('_F', '_M'))
            in_merge['Ratio'] = in_merge['Count_F'] / in_merge['Count_M']
            
            st.write("Yearly Gender Breakdown for Indian Residents:")
            st.dataframe(in_merge[['Year', 'Count_F', 'Count_M', 'Ratio']], use_container_width=True)

except FileNotFoundError:
    st.error("Please ensure 'Singapore_Residents.csv' is in the same directory as this script.")
