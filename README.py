readme_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        h1, h2, h3, h4, h5, h6 {
            font-weight: bold;
        }
        ul {
            list-style-type: disc;
            margin-left: 20px;
        }
    </style>
</head>
<body>
    <h1>Interactive Analysis of Great Britain Road Safety Data (2022)</h1>
    <p>The app consists of three main pages:</p>
    <ul>
        <li>Road Collision Map</li>
        <li>Statistical Attribute Analysis</li>
        <li>Attribute Correlation Analysis</li>
    </ul>
    <h2>Features</h2>
    <h3>Road Collision Map</h3>
    <p>The Map View provides a geographic visualization of road safety incidents. Users can filter incidents by local authority, accident severity, and month range. The map view also includes a toggle button to show or hide the left filter panel.</p>
    <ul>
        <li><b>Item Filters:</b>
            <ul>
                <li>Local Authority Dropdown: Select a local authority to filter incidents.</li>
                <li>Severity Dropdown: Select the severity of incidents to display.</li>
                <li>Month Range Slider: Select a range of months to filter incidents.</li>
            </ul>
        </li>
        <li><b>Display Options:</b>
            <ul>
                <li>View All Incidents: Display all incidents.</li>
                <li>Aggregated Data: View aggregated data.</li>
                <li>Total Casualties: Displays the total number of casualties based on the selected filters.</li>
            </ul>
        </li>
        <li><b>Graph Filters:</b>
            <ul>
                <li>Tree Map: Provides deeper analysis opportunities.</li>
                <li>Left Side: Select external conditions to filter collisions.</li>
                <li>Right Side: Select geographical conditions to filter collisions.</li>
                <li>External conditions: weather conditions, road surface conditions, light conditions.</li>
                <li>Geographical conditions: area type, road type, speed limit.</li>
            </ul>
        </li>
    </ul>
    <h3>Statistical Attribute Analysis</h3>
    <h4>Bar Chart View</h4>
    <p>The Bar Chart View displays various categorical attributes of road safety data in a stacked bar chart format. Users can view distributions of data by vehicle attributes, casualty attributes, road attributes, and accident severity.</p>
    <ul>
        <li>Vehicle Attributes Dropdown: Select vehicle-related attributes to display. These are vehicle type, propulsion type, vehicle manoeuvre.</li>
        <li>Collision Attributes Dropdown: Select casualty-related attributes to display. These are casualty class, casualty type, first impact point, hit object in carriageway.</li>
        <li>Road Attributes Dropdown: Select road-related attributes to display. These are road type, first road class, second road class, junction location, junction control, junction detail.</li>
        <li>Data Options: Choose whether to include or exclude missing data.</li>
        
    </ul>
    <p>Note that to be able to use the exclude button, you should first click on the exclude button  and after that 
        you can select the attribute you want to view on the bar chart with the missing values excluded from the 
        dataset. </p>
    <h4>Line Chart View</h4>
    <p>The Line Chart View displays various ordered attributes of road safety data in a stacked line chart format. Users can view distributions of data by:</p>
    <ul>
        <li>Time of the day</li>
        <li>Day of the week</li>
        <li>Month of the year</li>
        <li>Age band of the driver</li>
        <li>Speed limit</li>
        <li>Ordered Attribute Dropdown: Select an ordered attribute to display.</li>
        <li>Data Options: Choose whether to include or exclude missing data.</li>
    </ul>
    <h3>Attribute Correlation Analysis</h3>
    <p>The Heat Map View provides a correlation analysis of different categorical attributes in the form of a heatmap. Users can select attributes for the x and y axes and also have the option to exclude missing data.</p>
    <ul>
        <li>X-axis Attribute Dropdown: Select an attribute for the x-axis.</li>
        <li>Y-axis Attribute Dropdown: Select an attribute for the y-axis.</li>
        <li>Data Options: Choose whether to include or exclude missing data.</li>
        <li>Selectable attributes: first point of impact, pedestrian movement, junction location, junction control, casualty class, vehicle manoeuvre.</li>
    </ul>
    <p><b>Creators:</b></p>
    <ul>
        <li>Efran Razon</li>
        <li>Efsane Yıldız</li>
        <li>Idil Mısra Yılmaz</li>
    </ul>
</body>
</html>
"""
