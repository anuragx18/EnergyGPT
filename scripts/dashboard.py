import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Ensure Streamlit Page Config is the First Command
st.set_page_config(page_title="Energy Dashboard", page_icon="⚡", layout="wide")

# ✅ Define Paths for Data
forecast_data_path = "/Users/anurag/Documents/EnergyGPT/data/processed/forecasted_energy_data.csv"

# ✅ Load Forecast Data
try:
    df_forecast = pd.read_csv(forecast_data_path, parse_dates=["ds"])
    
except Exception as e:
    st.error(f"❌ Error loading forecast dataset: {e}")
    df_forecast = pd.DataFrame(columns=["ds", "yhat", "yhat_lower", "yhat_upper"])  # Empty placeholder

# ✅ Custom Styling
def set_custom_style():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;600;700&display=swap');
            html, body, [class*="css"] {
                font-family: 'SF Pro Display', sans-serif;
                background-color: #f5f5f7;
                color: #1d1d1f;
            }
            .stTitle, .stSubheader, .stMarkdown {
                color: #1d1d1f;
            }
            .stSidebar {
                background-color: #e5e5ea;
            }
            .stMetric {
                color: #0071e3;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

set_custom_style()

def main():
    st.title("📊 Energy Consumption Forecast Dashboard")
    st.markdown("This dashboard provides **forecasted electricity consumption trends**.")

    # ✅ Sidebar for Filters
    st.sidebar.header("📏 Filter Options")
    if not df_forecast.empty:
        date_range = st.sidebar.date_input("Select Date Range",
                                           [df_forecast["ds"].min(), df_forecast["ds"].max()],
                                           key='date_range')

        # ✅ Filter Data
        if date_range and len(date_range) == 2:
            df_filtered = df_forecast[(df_forecast["ds"] >= pd.to_datetime(date_range[0])) &
                                      (df_forecast["ds"] <= pd.to_datetime(date_range[1]))]
        else:
            df_filtered = df_forecast  # Show full data if no date selected
    else:
        df_filtered = pd.DataFrame()  # Empty DataFrame if forecast data isn't available

    # ✅ Main Section Layout
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("📈 Forecasted Electricity Consumption")
        if not df_filtered.empty:
            fig = px.line(df_filtered, x="ds", y="yhat", title="Electricity Consumption Forecast",
                          labels={"ds": "Date", "yhat": "Predicted Consumption (kWh)"}, markers=True)
            fig.update_traces(line_color="#0071e3")  # Apple Blue Theme
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠ No forecast data available.")

    with col2:
        st.subheader("📊 Quick Stats")
        if not df_filtered.empty:
            st.metric(label="🔹 Min Forecast", value=f"{df_filtered['yhat'].min():.2f} kWh")
            st.metric(label="🔹 Max Forecast", value=f"{df_filtered['yhat'].max():.2f} kWh")
            st.metric(label="🔹 Avg Forecast", value=f"{df_filtered['yhat'].mean():.2f} kWh")
        else:
            st.write("⚠ No forecast data available.")

    # ✅ Display Data Table
    st.divider()
    st.subheader("📊 Forecast Data Table")
    if not df_filtered.empty:
        df_display = df_filtered[["ds", "yhat", "yhat_lower", "yhat_upper"]]
        df_display.columns = ["Date", "Forecast (kWh)", "Lower Bound", "Upper Bound"]
        st.dataframe(df_display, use_container_width=True)
    else:
        st.warning("⚠ No forecast data available.")

if __name__ == "__main__":
    main()
