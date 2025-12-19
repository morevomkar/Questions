import streamlit as st
import pandas as pd

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Singapore Residents Analysis",
    page_icon="🇸🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Custom Styling ----------------
st.markdown("""
<style>
.main { padding: 0rem 1rem; }
h1 { text-align: center; color: #1f77b4; }
h2 { color: #ff7f0e; }
.stMetric {
    background-color: #f5f7fb;
    padding: 15px;
    border-radius: 10px;
}
.dataframe { font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ---------------- Title ----------------
st.title("🇸🇬 Singapore Residents Data Analysis")
st.markdown("---")

# ---------------- File Upload ----------------
uploaded_file = st.file_uploader(
    "📂 Upload Singapore_Residents.csv file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ---------------- Sidebar ----------------
    st.sidebar.header("📊 Analysis Options")
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        [
            "Overview",
            "Population Trends",
            "Gender Ratios",
            "Growth Rate Analysis"
        ]
    )

    # ================= OVERVIEW =================
    if analysis_type == "Overview":
        st.header("📈 Dataset Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(df))
        col2.metric("Years Covered", f"{df['Year'].min()} - {df['Year'].max()}")
        col3.metric("Resident Categories", df['Residents'].nunique())

        st.subheader("📄 Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True)

        st.subheader("📊 Statistical Summary")
        st.dataframe(df.describe(), use_container_width=True)

    # ================= POPULATION TRENDS =================
    elif analysis_type == "Population Trends":
        st.header("👥 Population Trends (Table View)")

        total = df[df["Residents"] == "Total Residents"][["Year", "Count"]]
        male = df[df["Residents"] == "Total Male Residents"][["Year", "Count"]]
        female = df[df["Residents"] == "Total Female Residents"][["Year", "Count"]]

        st.subheader("Total Residents Over Years")
        st.dataframe(total, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Male Residents")
            st.dataframe(male, use_container_width=True)
        with col2:
            st.subheader("Female Residents")
            st.dataframe(female, use_container_width=True)

        st.subheader("👫 Male vs Female Comparison")
        comparison = pd.merge(
            male.rename(columns={"Count": "Male"}),
            female.rename(columns={"Count": "Female"}),
            on="Year"
        )
        st.dataframe(comparison, use_container_width=True)

    # ================= GENDER RATIOS =================
    elif analysis_type == "Gender Ratios":
        st.header("⚖️ Gender Ratio Analysis (Female / Male)")

        years_selected = [2000, 2003, 2006, 2009, 2012]

        def calculate_ratio(male_cat, female_cat):
            m = df[(df["Residents"] == male_cat) & (df["Year"].isin(years_selected))]
            f = df[(df["Residents"] == female_cat) & (df["Year"].isin(years_selected))]
            merged = pd.merge(
                f[["Year", "Count"]],
                m[["Year", "Count"]],
                on="Year",
                suffixes=("_Female", "_Male")
            )
            merged["Ratio"] = (merged["Count_Female"] / merged["Count_Male"]).round(3)
            return merged

        tab1, tab2, tab3, tab4 = st.tabs(
            ["Malays", "Chinese", "Indians", "Other Ethnic Groups"]
        )

        with tab1:
            st.subheader("Malay Population Ratio")
            st.dataframe(
                calculate_ratio("Total Male Malays", "Total Female Malays"),
                use_container_width=True
            )

        with tab2:
            st.subheader("Chinese Population Ratio")
            st.dataframe(
                calculate_ratio("Total Male Chinese", "Total Female Chinese"),
                use_container_width=True
            )

        with tab3:
            st.subheader("Indian Population Ratio")
            st.dataframe(
                calculate_ratio("Total Male Indians", "Total Female Indians"),
                use_container_width=True
            )

        with tab4:
            st.subheader("Other Ethnic Groups Ratio")
            st.dataframe(
                calculate_ratio(
                    "Other Ethnic Groups (Males)",
                    "Other Ethnic Groups (Females)"
                ),
                use_container_width=True
            )

    # ================= GROWTH RATE =================
    elif analysis_type == "Growth Rate Analysis":
        st.header("📈 Population Growth Rate Analysis")

        t1 = df[df["Residents"] == "Total Residents"][["Year", "Count"]].copy()
        t2 = t1.copy()
        t2["Year"] += 1
        t2.rename(columns={"Count": "Previous_Count"}, inplace=True)

        growth = pd.merge(t1, t2, on="Year")
        growth["Growth_Rate (%)"] = (
            (growth["Count"] - growth["Previous_Count"])
            / growth["Previous_Count"] * 100
        ).round(2)

        col1, col2, col3 = st.columns(3)
        col1.metric("Average Growth Rate", f"{growth['Growth_Rate (%)'].mean():.2f}%")
        col2.metric("Highest Growth", f"{growth['Growth_Rate (%)'].max():.2f}%")
        col3.metric("Lowest Growth", f"{growth['Growth_Rate (%)'].min():.2f}%")

        st.subheader("📊 Year-wise Growth Rate Table")
        st.dataframe(
            growth[["Year", "Count", "Growth_Rate (%)"]],
            use_container_width=True
        )

else:
    st.info("👆 Upload the Singapore_Residents.csv file to begin analysis")
    st.markdown("""
    ### About This Application
    ✔ Population overview  
    ✔ Gender-based analysis  
    ✔ Ethnic group ratio calculation  
    ✔ Growth rate analysis  
    ✔ No charts – clean, fast & professional  
    """)

# ---------------- Footer ----------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center'>Singapore Residents Data Analysis | Streamlit App</div>",
    unsafe_allow_html=True
)
