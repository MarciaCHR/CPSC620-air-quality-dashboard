"""
Air Quality Dashboard - Main Streamlit Application

This is the main application file for the UCI Air Quality Dataset dashboard.
Students will work in teams to enhance this dashboard through Git collaboration.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from analysis import (
    load_data,
    clean_data,
    get_data_summary,
    calculate_air_quality_metrics,
    calculate_selected_pollutant_metrics
)
from visualize import (
    plot_co_over_time,
    plot_temperature_vs_humidity,
    plot_pollutant_distribution,
    plot_correlation_heatmap,
    plot_nox_vs_sensor,
    create_summary_metrics_display,
    plot_pollutant_over_time,
    plot_pollutant_vs_sensor
)

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
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2E8B57;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #2E8B57;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">Air Quality Dashboard</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Welcome to the Air Quality Analysis Dashboard!** 
    
    This dashboard analyzes air quality data from an Italian city monitoring station. 
    The dataset includes various air pollutants and weather variables collected over time.
    """)
    
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

        # Global pollutant configuration
    pollutant_options = {
        "Carbon Monoxide (CO)": {
            "column": "CO(GT)",
            "unit": "mg/m³",
            "sensor": "PT08.S1(CO)"
        },
        "Benzene (C6H6)": {
            "column": "C6H6(GT)",
            "unit": "µg/m³",
            "sensor": "PT08.S2(NMHC)"
        },
        "Nitrogen Oxides (NOx)": {
            "column": "NOx(GT)",
            "unit": "ppb",
            "sensor": "PT08.S3(NOx)"
        },
        "Nitrogen Dioxide (NO2)": {
            "column": "NO2(GT)",
            "unit": "µg/m³",
            "sensor": "PT08.S4(NO2)"
        }
    }

    st.markdown(
        '<h2 class="section-header">Global Pollutant Filter</h2>',
        unsafe_allow_html=True
    )

    selected_name = st.selectbox(
        "Select a pollutant to explore:",
        list(pollutant_options.keys())
    )

    selected_config = pollutant_options[selected_name]
    selected_pollutant = selected_config["column"]
    selected_unit = selected_config["unit"]
    selected_sensor = selected_config["sensor"]
    
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
                        st.metric(label=label, value=value)
    
        # Dynamic metrics for the globally selected pollutant
    st.subheader(f"Selected Pollutant Metrics: {selected_name}")

    selected_metrics = calculate_selected_pollutant_metrics(
        df, selected_pollutant
    )

    if selected_metrics is not None:
        metric_cols = st.columns(3)

        metric_cols[0].metric(
            "Average",
            f"{selected_metrics['mean']:.2f} {selected_unit}"
        )

        metric_cols[1].metric(
            "Maximum",
            f"{selected_metrics['max']:.2f} {selected_unit}"
        )

        metric_cols[2].metric(
            "Minimum",
            f"{selected_metrics['min']:.2f} {selected_unit}"
        )
    else:
        st.warning("No valid data available for the selected pollutant.")

    # Data preview table
    st.markdown('<h2 class="section-header">Data Preview</h2>', unsafe_allow_html=True)
    st.dataframe(df.head(10), width="stretch")
    
    # Visualizations
    st.markdown('<h2 class="section-header">Data Visualizations</h2>', unsafe_allow_html=True)
    
    # Base charts as required
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"{selected_name} Concentration Over Time")

        pollutant_time_plot = plot_pollutant_over_time(
            df,
            selected_pollutant,
            selected_unit
        )

        if pollutant_time_plot is not None:
            st.plotly_chart(
                pollutant_time_plot,
                width="stretch",
                config={
                    "displayModeBar": True,
                    "scrollZoom": True,
                    "displaylogo": False
                }
            )
        else:
            st.warning("No valid data available for plotting.")
    
    with col2:
        st.subheader("Temperature vs Absolute Humidity")
        temp_humidity_plot = plot_temperature_vs_humidity(df)
        if temp_humidity_plot:
            st.pyplot(temp_humidity_plot)
        else:
            st.warning("No temperature/humidity data available for plotting")
    
    # Additional visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader(f"{selected_name} Distribution")

        pollutant_plot = plot_pollutant_distribution(
            df,
            selected_pollutant
        )

        if pollutant_plot is not None:
            st.pyplot(pollutant_plot)
            plt.close(pollutant_plot)
        else:
            st.warning("No valid data available for this pollutant.")
    
    with col4:
        st.subheader(f"{selected_name} vs Sensor Reading")

        sensor_plot = plot_pollutant_vs_sensor(
            df,
            selected_pollutant,
            selected_sensor,
            selected_unit
        )

        if sensor_plot is not None:
            st.pyplot(sensor_plot)
            plt.close(sensor_plot)
        else:
            st.warning("No valid sensor data available for this pollutant.")
    
    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    corr_plot = plot_correlation_heatmap(df)
    if corr_plot:
        st.pyplot(corr_plot)

if __name__ == "__main__":
    main()
