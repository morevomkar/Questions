import streamlit as st
import pandas as pd

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Singapore Residents Analysis",
    page_icon="📊",
    layout="wide"
)

# ---------------- Title ----------------
st.title("📊 Singapore Residents Data Analysis")
st.markdown("Pandas-based analysis using Streamlit (No Charts Version)")

# ---------------- File Upload ----------------
uploaded_file = st.file_uploader(
    "📂 Upload Singapore_Residents.csv",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ---------------- View Raw Data ----------------
    with st.expander("📄 View Raw Dataset"):
        st.dataframe(df, use_container_width=True)

    # ---------------- Sidebar Filter ----------------
    st.sidebar.header("🔎 Filter Options")

    resident_types = df["Residents"].unique()
    selected_resident = st.sidebar.selectbox(
        "Select Resident Type",
        resident_types
    )

    # ---------------- Filtered Data ----------------
    filtered_df = df[df["Residents"] == selected_resident][["Year", "Count"]]

    st.subheader(f"📌 Year-wise Data for: {selected_resident}")
    st.dataframe(filtered_df, use_container_width=True)

    # ---------------- Growth Rate Calculation ----------------
    st.subheader("📊 Year-wise Growth Rate (%)")

    t1 = filtered_df.copy()
    t2 = filtered_df.copy()

    t2["Year"] = t2["Year"] + 1
    t2 = t2.rename(columns={"Count": "Previous_Count"})

    growth_df = pd.merge(t1, t2, on="Year", how="inner")
    growth_df["Growth_Rate (%)"] = (
        (growth_df["Count"] - growth_df["Previous_Count"])
        / growth_df["Previous_Count"]
    ) * 100

    final_growth = growth_df[["Year", "Growth_Rate (%)"]]

    st.dataframe(
        final_growth.style.format({"Growth_Rate (%)": "{:.2f}"}),
        use_container_width=True
    )

else:
    st.info("⬆ Please upload the CSV file to view the analysis.")

