from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import List, Dict

def create_crime_trend_chart(complaints):
    # Process data - count complaints by month
    monthly_counts = {}
    for complaint in complaints:
        date = datetime.strptime(complaint['date'], '%Y-%m-%d')
        month_year = f"{date.year}-{date.month:02d}"
        monthly_counts[month_year] = monthly_counts.get(month_year, 0) + 1
    
    # Sort by date
    sorted_dates = sorted(monthly_counts.items())
    dates = [item[0] for item in sorted_dates]
    counts = [item[1] for item in sorted_dates]
    
    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=counts,
        mode='lines+markers',
        name='Complaints',
        line=dict(color='royalblue', width=2)
    ))
    
    fig.update_layout(
        title='Cyber Crime Complaints Trend',
        xaxis_title='Month',
        yaxis_title='Number of Complaints',
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig.to_html(full_html=False)

def create_crime_by_type_chart(complaints):
    # Count by crime type
    type_counts = {}
    for complaint in complaints:
        crime_type = complaint['crime_type']
        type_counts[crime_type] = type_counts.get(crime_type, 0) + 1
    
    # Prepare data
    types = list(type_counts.keys())
    counts = list(type_counts.values())
    
    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=types,
        values=counts,
        hole=0.3,
        marker_colors=px.colors.qualitative.Plotly
    ))
    
    fig.update_layout(
        title='Distribution by Crime Type',
        template='plotly_white'
    )
    
    return fig.to_html(full_html=False)

def create_geo_distribution_chart(complaints):
    # Count by location
    location_counts = {}
    for complaint in complaints:
        location = complaint['location']
        if location:
            location_counts[location] = location_counts.get(location, 0) + 1
    
    # Prepare data
    locations = list(location_counts.keys())
    counts = list(location_counts.values())
    
    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=locations,
        y=counts,
        marker_color='indianred'
    ))
    
    fig.update_layout(
        title='Geographical Distribution',
        xaxis_title='Location',
        yaxis_title='Number of Complaints',
        template='plotly_white'
    )
    
    return fig.to_html(full_html=False)

def create_time_analysis_chart(complaints):
    # Extract hour from timestamp
    hour_counts = [0] * 24
    for complaint in complaints:
        created_at = datetime.strptime(complaint['created_at'], '%Y-%m-%d %H:%M:%S')
        hour = created_at.hour
        hour_counts[hour] += 1
    
    # Create figure
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=hour_counts,
        theta=[f"{h}:00" for h in range(24)],
        fill='toself',
        line=dict(color='darkgreen')
    ))
    
    fig.update_layout(title='Complaints by Time of Day', polar=dict(radialaxis=dict(visible=True),showlegend=False,template='plotly_white'))
    
    return fig.to_html(full_html=False)