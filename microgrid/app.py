from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import sqlite3
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
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        monthly_kwh = float(request.form["monthly_kwh"])
        if monthly_kwh <= 0:
            flash("Please enter a positive value for monthly kWh usage.")
            return redirect(url_for("index"))

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


if __name__ == "__main__":
    app.run(debug=True)
