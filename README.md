# GB Road Safety Visualization Tool

An interactive web-based dashboard for exploring road safety incidents across Great Britain in 2022.  
The app is built with Python, Dash, and Plotly, and consists of three main pages:
- Road Collision Map
- Statistical Attribute Analysis
- Attribute Correlation Analysis

---

## Features

### Road Collision Map

Provides a geographic visualization of road safety incidents.  
Users can filter by local authority, accident severity, and month.

**Filters:**
- Local Authority Dropdown
- Severity Dropdown
- Month Range Slider

**Display Options:**
- View All Incidents
- Aggregated Data
- Total Casualties display

**Graph Filters:**
- **External Conditions:** Weather, Road Surface, Lighting  
- **Geographical Conditions:** Area Type, Road Type, Speed Limit

---

### Statistical Attribute Analysis

#### Bar Chart View

Visualizes categorical attributes such as vehicle, casualty, and road characteristics.

**Attributes:**
- Vehicle Attributes: vehicle type, propulsion type, manoeuvre
- Casualty Attributes: casualty class, casualty type, impact point
- Road Attributes: road type, junction type, junction control

**Options:**
- Include or exclude missing data  
*Note: To use the exclude button, click it first, then select the attribute.*

#### Line Chart View

Displays trends in:
- Time of Day
- Day of Week
- Month of Year
- Age Band of Driver
- Speed Limit

---

### Attribute Correlation Analysis

Displays a heatmap of correlations between selected categorical features.

**Filters:**
- X-axis attribute
- Y-axis attribute
- Option to exclude missing data

**Selectable Attributes:**
- First Point of Impact
- Pedestrian Movement
- Junction Location
- Junction Control
- Casualty Class
- Vehicle Manoeuvre

---

## Tech Stack

- Python
- Dash
- Plotly
- Pandas

---

## Project Structure

```
datasets/
plots/
assets/
data_cleaning_and_merging.ipynb
imageCreate.py
main.py
README.md
.gitignore
```

---

## Setup

```bash
git clone https://github.com/idilmy/GB-road-safety-visualization-tool.git
pip install -r requirements.txt
python main.py
```

---

## Dataset

The full dataset (`merged_collision_data.csv`, ~214 MB) is not stored in this repository due to GitHub's file size limits.

You can download it here:  
[Download from Google Drive](https://drive.google.com/file/d/1GIqEmN-E5jnBK9QFbDjZqwpLz8lSM1b_/view?usp=sharing)

After downloading, place the file in the root of the project directory (alongside `main.py`) before running the app.
