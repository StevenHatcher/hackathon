from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
import pandas as pd
import ast
import csv
import io
from datetime import datetime
import constants
app = Flask(__name__)

# Constants

COST_PER_KWH = 0.14705  # Cost per kWh in dollars
AVG_PANEL_OUTPUT = constants.sol_72 * constants.BILLING_PERIOD * constants.HOURS # Average monthly kWh output per panel


# Function to save calculation to database
def save_calculation(monthly_kwh, monthly_savings, panels_needed, annual_savings):
    conn = sqlite3.connect("microgrid.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO calculations (total_kwh, monthly_savings, annual_savings, panels_needed)
    VALUES (?, ?, ?, ?)
    """,
        (monthly_kwh, monthly_savings, annual_savings, panels_needed),
    )
    conn.commit()
    conn.close()


# Function to get all calculations
def get_all_calculations():
    conn = sqlite3.connect("microgrid.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM calculations")
    calculations = cursor.fetchall()
    conn.close()
    return calculations


# Function to calculate solar savings
def calculate_solar_savings(monthly_kwh=None, selected_buildings=None, buildings_data=None):
    """
    Calculate solar savings based on either direct kWh input or selected buildings
    
    Parameters:
    monthly_kwh (float): Direct input of monthly kWh usage
    selected_buildings (list): List of selected building codes
    buildings_data (dict): Dictionary of building energy data
    
    Returns:
    dict: Dictionary with calculation results
    """
    # If selected buildings provided, calculate total kWh from buildings
    total_kwh = monthly_kwh
    
    if selected_buildings and buildings_data:
        # Calculate total kWh from selected buildings
        total_kwh = 0
        for building_code in selected_buildings:
            if building_code in buildings_data:
                # Sum up electrical usage for each building
                building_electrical = 0
                for energy_dict in buildings_data[building_code]:
                    if 'electrical' in energy_dict:
                        building_electrical += energy_dict['electrical']
                
                total_kwh += building_electrical
    
    # If no kWh value was provided or calculated, return error
    if not total_kwh or total_kwh <= 0:
        return None
    
    # Continue with regular calculations
    panels_needed = round(total_kwh / AVG_PANEL_OUTPUT)
    if panels_needed < 1:
        panels_needed = 1
    
    total_solar_output = panels_needed * AVG_PANEL_OUTPUT
    if total_solar_output > total_kwh:
        total_solar_output = total_kwh  # Can't save more than total usage
    
    monthly_savings = total_solar_output * COST_PER_KWH
    annual_savings = monthly_savings * 12
    
    return {
        "monthly_kwh": total_kwh,
        "panels_needed": panels_needed,
        "total_solar_output": total_solar_output,
        "monthly_savings": monthly_savings,
        "annual_savings": annual_savings,
    }


# Routes
@app.route("/")
def index():
    buildings = university_init()
    return render_template("index.html", panel_options=buildings)


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get buildings data
        buildings_data = university_init()
        
        # Check if user entered kWh directly
        monthly_kwh = None
        if 'monthly_kwh' in request.form and request.form['monthly_kwh']:
            monthly_kwh = float(request.form['monthly_kwh'])
        
        # Get selected buildings
        selected_buildings = request.form.getlist('selected_buildings')
        
        # If neither kWh nor buildings selected, show error
        if not monthly_kwh and not selected_buildings:
            flash('Please either enter monthly kWh usage or select at least one building.')
            return redirect(url_for('index'))
        
        # Calculate total kWh from selected buildings
        buildings_kwh = 0
        if selected_buildings:
            for building_code in selected_buildings:
                if building_code in buildings_data:
                    # Sum up electrical usage for the building
                    for energy_dict in buildings_data[building_code]:
                        if 'electrical' in energy_dict:
                            buildings_kwh += energy_dict['electrical']
        
        # Use either direct input or calculated value
        total_kwh = monthly_kwh if monthly_kwh else buildings_kwh
        
        # Calculate results using the total kWh
        results = calculate_solar_savings(total_kwh)
        
        # Save to database
        save_calculation(
            results['monthly_kwh'],
            results['panels_needed'],
            results['monthly_savings'],
            results['annual_savings']
        )
        
        return render_template('results.html', 
                             results=results, 
                             cost_per_kwh=COST_PER_KWH, 
                             selected_buildings=selected_buildings)
    
    except ValueError as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'An unexpected error occurred: {str(e)}')
        return redirect(url_for('index'))


@app.route("/history")
def history():
    calculations = get_all_calculations()
    return render_template("history.html", calculations=calculations)


@app.route("/export")
def export():
    try:
        calculations = get_all_calculations()

        # Create a CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(
            [
                "ID",
                "Monthly kWh",
                "Panels Needed",
                "Monthly Savings ($)",
                "Annual Savings ($)",
                "Calculation Date",
            ]
        )

        # Write data
        for calc in calculations:
            writer.writerow(
                [
                    calc["id"],
                    calc["monthly_kwh"],
                    calc["panels_needed"],
                    calc["monthly_savings"],
                    calc["annual_savings"],
                    calc["calculation_date"],
                ]
            )

        # Prepare the CSV for download
        output.seek(0)

        # Create an in-memory file-like object
        mem = io.BytesIO()
        mem.write(output.getvalue().encode("utf-8"))
        mem.seek(0)
        output.close()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return send_file(
            mem,
            mimetype="text/csv",
            as_attachment=True,
            download_name=f"solar_savings_{timestamp}.csv",
        )

    except Exception as e:
        flash(f"Error exporting data: {str(e)}")
        return redirect(url_for("history"))

def university_init():
    # Read the CSV file
    csv_file_path = "uregina_dashboard/building_consumption.csv"
    df = pd.read_csv(csv_file_path)

    # Initialize the dictionary to store building usage data
    building_usage = {}

    # Columns to process
    columns = ["cooling", "heating", "electrical"]

    # Process each building
    for building_index, row in df.iterrows():
        building_code = row["building_code"]
        temp = []

        # Process each energy type (cooling, heating, electrical)
        for item in columns:
            # The data is stored as a string representation of a list
            # Convert it to an actual list of values
            try:
                # Using ast.literal_eval to safely convert string to list
                values = ast.literal_eval(row[item])

                # Calculate average value for a 30 day billing cycle
                if values and len(values) > 0:
                    avg_value = (sum(values) / len(values))*constants.GIGAJOULE_KWH*constants.BILLING_PERIOD
                else:
                    avg_value = 0

                # Add to temporary list
                temp.append({item: avg_value})
            except (ValueError, SyntaxError) as e:
                print(f"Error processing {item} for {building_code}: {e}")
                temp.append({item: 0})  # Default to 0 if there's an error

        # Add this building's data to the result dictionary
        building_usage[building_code] = temp
    return building_usage

if __name__ == "__main__":
    app.run(debug=True)
