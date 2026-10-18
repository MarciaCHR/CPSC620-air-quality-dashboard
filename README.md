# Air Quality Dashboard

This repository is designed for **CPSC 620: Agile Software Development** course at the University of Niagara Falls Canada. The primary objective is to train students in Git and GitHub workflows, collaborative development practices, and version control systems through hands-on project experience.

Students will work in teams to enhance this Streamlit dashboard for analyzing the UCI Air Quality Dataset, by forking the repository, creating feature branches, making pull requests, and merging changes while improving the air quality data visualization and analysis capabilities.


## About the Dataset

This project uses the **UCI Air Quality Dataset** from an Italian city monitoring station. The dataset contains hourly measurements of various air pollutants and weather variables collected over approximately one year.

### Dataset Features:
- **Air Pollutants**: CO (Carbon Monoxide), NOx (Nitrogen Oxides), NO2 (Nitrogen Dioxide), NMHC (Non-methane Hydrocarbons), Benzene
- **Weather Variables**: Temperature, Relative Humidity, Absolute Humidity
- **Time Period**: March 2004 - February 2005
- **Frequency**: Hourly measurements
- **Missing Data**: Some measurements marked as -200 (handled in the code)

### Dataset Source:
- **Original Dataset**: [UCI Machine Learning Repository - Air Quality](https://archive.ics.uci.edu/dataset/360/air+quality)
- **Citation**: S. De Vito, E. Massera, M. Piga, L. Martinotto, G. Di Francia, On field calibration of an electronic nose for benzene estimation in an urban pollution monitoring scenario, Sensors and Actuators B: Chemical, Volume 129, Issue 2, 22 February 2008, Pages 750-757, ISSN 0925-4005

### Column Descriptions:
- **Date**: Measurement date
- **Time**: Measurement time
- **CO(GT)**: Carbon Monoxide concentration (mg/m³)
- **PT08.S1(CO)**: CO sensor reading
- **NMHC(GT)**: Non-methane hydrocarbons (µg/m³)
- **C6H6(GT)**: Benzene concentration (µg/m³)
- **PT08.S2(NMHC)**: NMHC sensor reading
- **NOx(GT)**: Nitrogen oxides concentration (µg/m³)
- **PT08.S3(NOx)**: NOx sensor reading
- **NO2(GT)**: Nitrogen dioxide concentration (µg/m³)
- **PT08.S4(NO2)**: NO2 sensor reading
- **PT08.S5(O3)**: Ozone sensor reading
- **T**: Temperature (°C)
- **RH**: Relative Humidity (%)
- **AH**: Absolute Humidity

## Quick Start

### Prerequisites
- Python 3.11–3.15 (check the [current Streamlit installation guide](https://docs.streamlit.io/get-started/installation/command-line) for supported versions)
- pip package manager
- PyCharm or Visual Studio Code (optional, if you prefer an IDE)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone https://github.com/MarciaCHR/CPSC620-air-quality-dashboard.git
   cd CPSC620-air-quality-dashboard
   ```

2. **Download the dataset**
   
   **Important**: For privacy and data protection reasons, the actual dataset files are not included in this repository. After cloning, you need to download the dataset separately.
   
   - Download the **Air Quality Dataset** from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/360/air+quality)
   - Save the downloaded file as `AirQualityUCI.csv` in the `data/` folder
   - The `data/` folder structure is preserved in git, but the CSV files are excluded via `.gitignore`
   
   ```bash
   # After downloading, your data folder should look like:
   data/
   ├── .gitkeep
   └── AirQualityUCI.csv  # Downloaded separately
   ```

3. **Create and activate a virtual environment**

   Create a separate environment for this project. Do not copy a `.venv` folder between Windows and macOS.

   **Windows (PowerShell):**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell does not allow the activation script to run, use **Command Prompt** instead:
   ```bat
   py -m venv .venv
   .venv\Scripts\activate.bat
   ```

   **macOS:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install all required packages**

   With the virtual environment activated, run:
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

   The `requirements.txt` file includes the dashboard dependencies, including Plotly.

5. **Select the virtual environment in your IDE (optional)**

   - **PyCharm:** In the project’s Python Interpreter settings, select the interpreter inside `.venv`.
     - Windows: `.venv\Scripts\python.exe`
     - macOS: `.venv/bin/python`
   - **Visual Studio Code:** Open the Command Palette, choose **Python: Select Interpreter**, and select the interpreter inside this project’s `.venv`.

6. **Run the dashboard**
   ```bash
   python -m streamlit run app.py
   ```

7. **Open your browser** and navigate to `http://localhost:8501`

## About Streamlit

**Streamlit** is a powerful Python framework for building interactive web applications and data dashboards. It's particularly well-suited for data science and machine learning projects because it allows developers to create beautiful, interactive web apps with minimal code.

### Key Streamlit Features:
- **Simple Python API**: Write web apps using only Python - no HTML, CSS, or JavaScript required
- **Interactive Widgets**: Built-in components like sliders, dropdowns, file uploaders, and more
- **Automatic Rerun**: Apps automatically update when you modify the code
- **Data Visualization**: Seamless integration with popular libraries like Matplotlib, Plotly, and Altair
- **Caching**: Built-in caching mechanisms for improved performance
- **Deployment**: Easy deployment to cloud platforms

### Important Streamlit Concepts:
- **st.write()**: Display text, data, and charts
- **st.columns()**: Create multi-column layouts
- **st.sidebar**: Add sidebar elements for controls
- **@st.cache_data**: Cache expensive computations
- **st.session_state**: Maintain state across reruns
- **st.file_uploader()**: Handle file uploads
- **st.selectbox()**, **st.slider()**: Interactive widgets

### How Streamlit Works:
1. **Run Command**: Execute `streamlit run app.py` to start the development server
2. **Auto-Reload**: Streamlit watches your files and automatically reloads when changes are detected
3. **Browser Interface**: The app runs in your web browser at `http://localhost:8501`
4. **Widget Interaction**: User interactions trigger script reruns with updated values
5. **State Management**: Use `st.session_state` to maintain data between reruns

## Project Structure

```
air_quality/
├── app.py              # Main Streamlit application
├── analysis.py         # Data cleaning and analysis functions
├── visualize.py        # Chart and visualization functions
├── data/
│   ├── .gitkeep        # Ensures data folder is tracked by git
│   └── AirQualityUCI.csv  # Air quality dataset (downloaded separately)
├── .gitignore          # Excludes sensitive data files from version control
└── README.md           # This file
```

**Note**: The `AirQualityUCI.csv` file is not included in the repository for privacy reasons. See the Installation section above for download instructions.

## Current Issues & Backlog

### Issue #1: Handle Missing Data Values (-200)
**Reference**: [Issue #1: Handle Missing Data Values (-200)](https://github.com/alamdari/CPSC620-air-quality-dashboard/issues/1)

The dataset contains missing values represented as -200, which need to be properly handled in the data processing pipeline. This affects data visualization accuracy and analysis results.

**For Students**: When your team forks this repository, **create the same issue** in your fork and work collaboratively to resolve it. This models a real Agile backlog item and helps you practice issue tracking, branching, and pull-request workflows.

## Development Workflow

### 1. **Setup Team Repository**
```bash
# One team member forks the repository
# Other members clone the fork
git clone <forked-repo-url>
cd air_quality
```

### 2. **Create Feature Branches**
```bash
# Create a new branch for each feature
git checkout -b feature/add-date-filters
git checkout -b feature/enhance-visualizations
git checkout -b feature/add-metrics
```

### 3. **Development Process**
```bash
# Make changes to files
# Test your changes
streamlit run app.py

# Stage and commit changes
git add .
git commit -m "feat: add date range filter to dashboard"

# Push to your branch
git push origin feature/add-date-filters
```

### 4. **Collaboration**
- Create **Pull Requests** for team review
- **Review** team members' code
- **Merge** approved changes
- **Resolve conflicts** when they arise

### 5. **Best Practices**
- Write **descriptive commit messages**
- Create **small, focused pull requests**
- **Test** your changes before submitting
- **Communicate** with your team

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/stable/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)
- [GitHub Pull Request Guide](https://docs.github.com/en/pull-requests)

---

**Happy Coding!** Work together to build an amazing air quality analysis dashboard!
