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
AVG_PANEL_OUTPUT = constants.sol_60 * constants.DAYS * constants.HOURS # Average monthly kWh output per panel


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
def calculate_solar_savings(monthly_kwh):
    panels_needed = round(monthly_kwh / AVG_PANEL_OUTPUT)
    if panels_needed < 1:
        panels_needed = 1

    total_solar_output = panels_needed * AVG_PANEL_OUTPUT
    if total_solar_output > monthly_kwh:
        total_solar_output = monthly_kwh  # Can't save more than total usage

    monthly_savings = total_solar_output * COST_PER_KWH
    annual_savings = monthly_savings * 12

    return {
        "monthly_kwh": monthly_kwh,
        "panels_needed": panels_needed,
        "total_solar_output": total_solar_output,
        "monthly_savings": monthly_savings,
        "annual_savings": annual_savings,
    }


# Routes
@app.route("/")
def index():
    buildings = university_init()
    return render_template("index.html", panel_types=buildings)


@app.route("/calculate", methods=["POST"])
def calculate():
    buildings = university_init()
    try:
        monthly_kwh = request.form["monthly_kwh"]
        #building_choice = str(request.form["chooseBuilding"])
        if monthly_kwh is not None:
            monthly_kwh = float(monthly_kwh)
            if monthly_kwh < 0:
                monthly_kwh = 0
        #if monthly_kwh is None:
            #if building_choice is not None:
                #monthly_kwh = buildings[building_choice]['electrical'] * constants.GIGAJOULE_KWH
        
        results = calculate_solar_savings(monthly_kwh)

        # Save to database
        save_calculation(
            results["monthly_kwh"],
            results["panels_needed"],
            results["monthly_savings"],
            results["annual_savings"],
        )
        

        return render_template(
            "results.html", results=results, cost_per_kwh=COST_PER_KWH
        )

    except ValueError:
        flash("Please enter a valid number for monthly kWh usage.")
        return redirect(url_for("index"))


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

                # Calculate average value
                if values and len(values) > 0:
                    avg_value = sum(values) / len(values)
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
