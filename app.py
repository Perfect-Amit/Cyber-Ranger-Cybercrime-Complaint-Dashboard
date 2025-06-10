from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_db, add_complaint, get_all_complaints, get_complaints_by_type
from utils.visualization import create_crime_trend_chart, create_crime_by_type_chart, create_geo_distribution_chart, create_time_analysis_chart
import os

app = Flask(__name__)
app.config['DATABASE'] = 'cybercrimes.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize database
init_db(app)

@app.route('/')
def dashboard():
    # Get data for visualizations
    complaints = get_all_complaints()
    
    # Create visualizations
    trend_chart = create_crime_trend_chart(complaints)
    type_chart = create_crime_by_type_chart(complaints)
    geo_chart = create_geo_distribution_chart(complaints)
    time_chart = create_time_analysis_chart(complaints)
    
    return render_template('dashboard.html', 
                         trend_chart=trend_chart,
                         type_chart=type_chart,
                         geo_chart=geo_chart,
                         time_chart=time_chart)

@app.route('/add', methods=['GET', 'POST'])
def add_complaint():
    if request.method == 'POST':
        # Get form data
        crime_type = request.form['crime_type']
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']
        status = request.form['status']
        
        # Add to database
        add_complaint(crime_type, description, location, date, status)
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_complaint.html')

@app.route('/data')
def view_data():
    complaints = get_all_complaints()
    return render_template('view_data.html', complaints=complaints)

if __name__ == '__main__':
    app.run(debug=True)