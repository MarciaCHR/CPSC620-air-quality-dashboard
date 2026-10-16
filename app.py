"""
Air Quality Dashboard - Main Streamlit Application

This is the main application file for the UCI Air Quality Dataset dashboard.
Students will work in teams to enhance this dashboard through Git collaboration.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analysis import load_data, clean_data, get_data_summary, calculate_air_quality_metrics
from visualize import (plot_co_over_time, plot_temperature_vs_humidity, 
                      plot_pollutant_distribution, plot_correlation_heatmap,
                      plot_nox_vs_sensor, create_summary_metrics_display)

# Configure the page
st.set_page_config(
    page_title="Air Quality Dashboard",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #B9E8D8 !important;
        text-align: center;
        margin-bottom: 0.75rem;
    }
    .intro-copy {
        color: #C6D5D0;
        text-align: center;
        font-size: 1.05rem;
        line-height: 1.6;
        max-width: 900px;
        margin: 0 auto 2rem auto;
    }
    .intro-copy strong {
        color: #E8F5F0;
        font-size: 1.15rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .section-header {
        font-size: 1.5rem;
        color: #5BE2B2 !important;
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
    }
    .metric-label {
        color: #D4DAD8;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 0.45rem;
    }
    .metric-value {
        color: #F4F6F5;
        font-size: 1.3rem;
        text-align: center;
        margin-bottom: 0.75rem;
    }
    div[data-testid="stTable"] th,
    div[data-testid="stTable"] td {
        text-align: center !important;
    }
    .stApp h3 {
        color: #A7DCCB;
        font-size: 1.35rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">Air Quality Dashboard</h1>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="intro-copy">
        <strong>Welcome to the Air Quality Analysis Dashboard</strong><br>
        Explore air pollution and weather measurements collected over time
        at a monitoring station in Italy.
    </div>
    """, unsafe_allow_html=True)
    
    # Load and cache data
    @st.cache_data
    def load_and_clean_data():
        """Load and clean the air quality data."""
        raw_data = load_data("data/AirQualityUCI.csv")
        if raw_data is not None:
            return clean_data(raw_data)
        return None
    
    # Load data
    with st.spinner("Loading air quality data..."):
        df = load_and_clean_data()
    
    if df is None:
        st.error("Could not load the air quality dataset. Please check if 'data/AirQualityUCI.csv' exists.")
        return
    
    # Key Metrics - KPI Boxes
    st.markdown('<h2 class="section-header">Key Metrics</h2>', unsafe_allow_html=True)
    
    # Calculate metrics
    metrics = calculate_air_quality_metrics(df)
    display_metrics = create_summary_metrics_display(metrics)
    
    if display_metrics:
        # Display up to three KPI cards per row.
        metric_items = list(display_metrics.items())
        cards_per_row = 3

        for start in range(0, len(metric_items), cards_per_row):
            cols = st.columns(cards_per_row)
            row_items = metric_items[start:start + cards_per_row]

            for col, (metric_name, metric_values) in zip(cols, row_items):
                with col:
                    st.subheader(metric_name)

                    for label, value in metric_values.items():
                        st.markdown(
                            f'<div class="metric-label">{label}</div>'
                            f'<div class="metric-value">{value}</div>',
                            unsafe_allow_html=True
                        )
    
    # Data preview table
    # Data quality summary
    data_summary = get_data_summary(df)
    sensor_columns = data_summary["numeric_columns"]
    missing_counts = df[sensor_columns].isna().sum()

    st.markdown(
        '<h2 class="section-header">Data Quality Summary</h2>',
        unsafe_allow_html=True
    )

    quality_cols = st.columns(3)
    quality_metrics = [
        ("Records", f"{data_summary['total_records']:,}"),
        (
            "Date range",
            f"{data_summary['date_range']['start']:%Y-%m-%d} to "
            f"{data_summary['date_range']['end']:%Y-%m-%d}"
        ),
        ("Missing sensor values", f"{missing_counts.sum():,}"),
    ]
    for column, (label, value) in zip(quality_cols, quality_metrics):
        with column:
            st.markdown(
                f'<div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div>',
                unsafe_allow_html=True
            )

    missing_summary = pd.DataFrame({
        "Sensor": sensor_columns,
        "Missing values": [
            int(missing_counts[column]) for column in sensor_columns
        ],
        "Missing (%)": [
            f"{data_summary['missing_data_percentage'][column]:.2f}%"
            for column in sensor_columns
        ],
    })
    centered_missing_summary = (
        missing_summary.style
        .set_properties(**{"text-align": "center"})
        .set_table_styles([
            {"selector": "th", "props": [("text-align", "center")]}
        ])
    )
    st.table(centered_missing_summary)
    st.markdown('<h2 class="section-header">Data Preview</h2>', unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True)
    
    # Visualizations
    st.markdown('<h2 class="section-header">Data Visualizations</h2>', unsafe_allow_html=True)
    
    # Base charts as required. Keep both charts the same display height.
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("CO Concentration Over Time")
        co_plot = plot_co_over_time(df)
        if co_plot is not None:
            st.plotly_chart(
                co_plot,
                use_container_width=True,
                config={
                    "displayModeBar": True,
                    "scrollZoom": True,
                    "displaylogo": False
                }
            )
        else:
            st.warning("No CO data available for plotting")
    
    with col2:
        st.subheader("Temperature vs Absolute Humidity")
        temp_humidity_plot = plot_temperature_vs_humidity(df)
        if temp_humidity_plot:
            st.pyplot(temp_humidity_plot, use_container_width=True)
        else:
            st.warning("No temperature/humidity data available for plotting")
    
    # Place the shared selector above the chart row so both plots begin together.
    selected_pollutant = st.selectbox(
        "Select a pollutant:",
        ["CO(GT)", "NOx(GT)", "NO2(GT)"]
    )

    # Additional visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Interactive Pollutant Distribution")

        # Generate the distribution chart
        pollutant_plot = plot_pollutant_distribution(
            df,
            selected_pollutant
        )

        # Display the selected pollutant
        if pollutant_plot is not None:
            st.pyplot(pollutant_plot, use_container_width=True)
        else:
            st.warning("No valid data available for this pollutant.")
    
    with col4:
        st.subheader("NOx(GT) vs Sensor Value")
        nox_plot = plot_nox_vs_sensor(df)
        if nox_plot:
            st.pyplot(nox_plot, use_container_width=True)
        else:
            st.warning("No NOx data available for plotting")
    
    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    corr_plot = plot_correlation_heatmap(df)
    if corr_plot:
        st.pyplot(corr_plot, use_container_width=True)

if __name__ == "__main__":
    main()
