import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Singapore Residents Analysis",
    page_icon="🇸🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
    }
    h2 {
        color: #ff7f0e;
    }
    .dataframe {
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🇸🇬 Singapore Residents Data Analysis")
st.markdown("---")

# File upload
uploaded_file = st.file_uploader("Upload Singapore_Residents.csv file", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Sidebar
    st.sidebar.header("📊 Analysis Options")
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Overview", "Population Trends", "Gender Ratios", "Growth Rate Analysis"]
    )
    
    # Overview Section
    if analysis_type == "Overview":
        st.header("📈 Data Overview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Years Covered", f"{df['Year'].min()} - {df['Year'].max()}")
        with col3:
            st.metric("Categories", df['Residents'].nunique())
        
        st.subheader("Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True)
        
        st.subheader("Dataset Statistics")
        st.dataframe(df.describe(), use_container_width=True)
    
    # Population Trends
    elif analysis_type == "Population Trends":
        st.header("📊 Population Trends Analysis")
        
        # Total Residents Over Time
        st.subheader("1. Total Residents Trend (2000-2018)")
        total_residents = df[df['Residents'] == 'Total Residents'][['Year', 'Count']]
        
        fig1 = px.line(total_residents, x='Year', y='Count', 
                       title='Total Residents Over Time',
                       markers=True)
        fig1.update_layout(height=400)
        st.plotly_chart(fig1, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("2. Male Residents Trend")
            male_residents = df[df['Residents'] == 'Total Male Residents'][['Year', 'Count']]
            fig2 = px.area(male_residents, x='Year', y='Count',
                          title='Male Residents Over Time')
            fig2.update_traces(fillcolor='lightblue')
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            st.subheader("3. Female Residents Trend")
            female_residents = df[df['Residents'] == 'Total Female Residents'][['Year', 'Count']]
            fig3 = px.area(female_residents, x='Year', y='Count',
                          title='Female Residents Over Time')
            fig3.update_traces(fillcolor='lightpink')
            st.plotly_chart(fig3, use_container_width=True)
        
        # Gender comparison
        st.subheader("4. Gender Comparison")
        gender_comparison = pd.merge(
            male_residents.rename(columns={'Count': 'Male'}),
            female_residents.rename(columns={'Count': 'Female'}),
            on='Year'
        )
        
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(x=gender_comparison['Year'], y=gender_comparison['Male'],
                                 mode='lines+markers', name='Male', line=dict(color='blue')))
        fig4.add_trace(go.Scatter(x=gender_comparison['Year'], y=gender_comparison['Female'],
                                 mode='lines+markers', name='Female', line=dict(color='pink')))
        fig4.update_layout(title='Male vs Female Population Comparison', height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Gender Ratios
    elif analysis_type == "Gender Ratios":
        st.header("⚖️ Gender Ratio Analysis (Female/Male)")
        
        years_selected = [2000, 2003, 2006, 2009, 2012]
        
        # Helper function to calculate ratios
        def calculate_ratio(male_category, female_category, title):
            malm = df[(df['Residents'] == male_category) & 
                     (df['Year'].isin(years_selected))][['Year', 'Residents', 'Count']]
            malf = df[(df['Residents'] == female_category) & 
                     (df['Year'].isin(years_selected))][['Year', 'Residents', 'Count']]
            
            merge_df = pd.merge(malf, malm, on='Year', suffixes=('_Female', '_Male'))
            merge_df['Ratio'] = merge_df['Count_Female'] / merge_df['Count_Male']
            
            return merge_df
        
        # Tabs for different ethnic groups
        tab1, tab2, tab3, tab4 = st.tabs(["Malays", "Chinese", "Indians", "Other Ethnic Groups"])
        
        with tab1:
            st.subheader("Malay Population Ratio")
            malay_ratio = calculate_ratio('Total Male Malays', 'Total Female Malays', 'Malay')
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(malay_ratio[['Year', 'Count_Female', 'Count_Male', 'Ratio']], 
                           use_container_width=True)
            with col2:
                fig = px.line(malay_ratio, x='Year', y='Ratio', markers=True,
                            title='Female/Male Ratio Trend - Malays')
                fig.add_hline(y=1, line_dash="dash", line_color="red", 
                            annotation_text="Equal Ratio")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("Chinese Population Ratio")
            chinese_ratio = calculate_ratio('Total Male Chinese', 'Total Female Chinese', 'Chinese')
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(chinese_ratio[['Year', 'Count_Female', 'Count_Male', 'Ratio']], 
                           use_container_width=True)
            with col2:
                fig = px.line(chinese_ratio, x='Year', y='Ratio', markers=True,
                            title='Female/Male Ratio Trend - Chinese')
                fig.add_hline(y=1, line_dash="dash", line_color="red", 
                            annotation_text="Equal Ratio")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Indian Population Ratio")
            indian_ratio = calculate_ratio('Total Male Indians', 'Total Female Indians', 'Indian')
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(indian_ratio[['Year', 'Count_Female', 'Count_Male', 'Ratio']], 
                           use_container_width=True)
            with col2:
                fig = px.line(indian_ratio, x='Year', y='Ratio', markers=True,
                            title='Female/Male Ratio Trend - Indians')
                fig.add_hline(y=1, line_dash="dash", line_color="red", 
                            annotation_text="Equal Ratio")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            st.subheader("Other Ethnic Groups Ratio")
            other_ratio = calculate_ratio('Other Ethnic Groups (Males)', 
                                         'Other Ethnic Groups (Females)', 'Other')
            
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(other_ratio[['Year', 'Count_Female', 'Count_Male', 'Ratio']], 
                           use_container_width=True)
            with col2:
                fig = px.line(other_ratio, x='Year', y='Ratio', markers=True,
                            title='Female/Male Ratio Trend - Other Ethnic Groups')
                fig.add_hline(y=1, line_dash="dash", line_color="red", 
                            annotation_text="Equal Ratio")
                st.plotly_chart(fig, use_container_width=True)
        
        # Comparison chart
        st.subheader("Ratio Comparison Across All Groups")
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Scatter(x=malay_ratio['Year'], y=malay_ratio['Ratio'],
                                          mode='lines+markers', name='Malays'))
        fig_comparison.add_trace(go.Scatter(x=chinese_ratio['Year'], y=chinese_ratio['Ratio'],
                                          mode='lines+markers', name='Chinese'))
        fig_comparison.add_trace(go.Scatter(x=indian_ratio['Year'], y=indian_ratio['Ratio'],
                                          mode='lines+markers', name='Indians'))
        fig_comparison.add_trace(go.Scatter(x=other_ratio['Year'], y=other_ratio['Ratio'],
                                          mode='lines+markers', name='Other'))
        fig_comparison.add_hline(y=1, line_dash="dash", line_color="red")
        fig_comparison.update_layout(title='Female/Male Ratio Comparison', height=500)
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Growth Rate Analysis
    elif analysis_type == "Growth Rate Analysis":
        st.header("📈 Population Growth Rate Analysis")
        
        # Calculate growth rate
        t1 = df[df['Residents'] == 'Total Residents'][['Year', 'Count']].copy()
        t2 = t1.copy()
        t2['Year'] = t2['Year'] + 1
        t2 = t2.rename(columns={'Count': 'Previous_Count'})
        
        merged_growth = pd.merge(t1, t2, on='Year', how='inner')
        merged_growth['Growth_Rate'] = (
            (merged_growth['Count'] - merged_growth['Previous_Count']) / 
            merged_growth['Previous_Count'] * 100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Growth Rate Statistics")
            st.metric("Average Growth Rate", 
                     f"{merged_growth['Growth_Rate'].mean():.2f}%")
            st.metric("Highest Growth Rate", 
                     f"{merged_growth['Growth_Rate'].max():.2f}% (Year: {merged_growth.loc[merged_growth['Growth_Rate'].idxmax(), 'Year']})")
            st.metric("Lowest Growth Rate", 
                     f"{merged_growth['Growth_Rate'].min():.2f}% (Year: {merged_growth.loc[merged_growth['Growth_Rate'].idxmin(), 'Year']})")
        
        with col2:
            st.subheader("Year-wise Growth Rate Data")
            st.dataframe(merged_growth[['Year', 'Count', 'Growth_Rate']].round(2), 
                        use_container_width=True)
        
        # Growth Rate Chart
        st.subheader("Growth Rate Trend")
        fig_growth = px.bar(merged_growth, x='Year', y='Growth_Rate',
                           title='Annual Population Growth Rate (%)',
                           color='Growth_Rate',
                           color_continuous_scale='RdYlGn')
        fig_growth.add_hline(y=0, line_dash="dash", line_color="black")
        fig_growth.update_layout(height=500)
        st.plotly_chart(fig_growth, use_container_width=True)
        
        # Line chart
        fig_growth_line = px.line(merged_growth, x='Year', y='Growth_Rate',
                                 title='Growth Rate Trend Line',
                                 markers=True)
        fig_growth_line.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_growth_line, use_container_width=True)
        
        # Population with growth rate
        st.subheader("Population vs Growth Rate")
        fig_dual = go.Figure()
        fig_dual.add_trace(go.Bar(x=merged_growth['Year'], y=merged_growth['Count'],
                                 name='Population', yaxis='y', opacity=0.6))
        fig_dual.add_trace(go.Scatter(x=merged_growth['Year'], y=merged_growth['Growth_Rate'],
                                     name='Growth Rate %', yaxis='y2', 
                                     mode='lines+markers', line=dict(color='red', width=3)))
        
        fig_dual.update_layout(
            title='Population Count vs Growth Rate',
            yaxis=dict(title='Population Count'),
            yaxis2=dict(title='Growth Rate (%)', overlaying='y', side='right'),
            height=500
        )
        st.plotly_chart(fig_dual, use_container_width=True)

else:
    st.info("👆 Please upload the Singapore_Residents.csv file to begin analysis")
    st.markdown("""
    ### About this Application
    This application analyzes Singapore resident population data from 2000-2018, providing:
    - **Population Trends**: Visualize total, male, and female population over time
    - **Gender Ratios**: Calculate and compare female-to-male ratios across ethnic groups
    - **Growth Rate Analysis**: Track annual population growth rates and identify trends
    
    Upload your CSV file to get started!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Singapore Residents Data Analysis Dashboard | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
