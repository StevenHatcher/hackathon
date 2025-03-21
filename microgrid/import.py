import sqlite3
import pandas as pd
import ast
import constants


def init_db(db_url):
    """
    Create and initialize tables
    """
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS calculations")
    cursor.execute(
        """CREATE TABLE calculations( \\
        id INTEGER PRIMARY KEY AUTOINCREMENT,\\
        total_KWH REAL NOT NULL DEFAULT 0,\\
        monthly_savings REAL NOT NULL DEFAULT 0,\\
        annual_savings REAL NOT NULL DEFAULT 0,\\
        calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,)"""
    )
    cursor.execute("DROP TABLE IF EXISTS devices_specs")
    cursor.execute(
        """CREATE TABLE devices_specs(
        devices_id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_name TEXT,
        power_per_device REAL NOT NULL,
        cost_per_device REAL NOT NULL,)"""
    )
    cursor.execute("DROP TABLE devices_specs")
    cursor.execute(
        """CREATE TABLE device(
        device_id INTEGER PRIMARY KEY AUTOINCREMENT,
        solar_amount INTEGER NOT NULL DEFAULT 0,
        wind_amount INTEGER NOT NULL DEFAULT 0,
        generator INTEGER NOT NULL DEFAULT 0,
        thermal BOOLEAN NOT NULL DEFAULT FALSE,)"""
    )
    cursor.execute("DROP TABLE ur_buildings")
    cursor.execute(
        """CREATE TABLE ur_buildings(
        building_id INTEGER PRIMARY KEY AUTOINCREMENT,
        building_name TEXT,
        cooling_avg REAL NOT NULL,
        heating_avg REAL NOT NULL,
        electrical_avg REAL NOT NULL,
        total_avg REAL NOT NULL,
        total_kwh REAL NOT NULL,)"""
    )

    conn.commit()
    conn.close()


def university_init_db(csv_file_path, db_url):
    # Read the CSV file
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

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    for building in building_usage:
        cooling = building_usage[building]["cooling"]
        heating = building_usage[building]["heating"]
        electrical = building_usage[building]["electrical"]
        total = cooling + heating + electrical
        total_kwh = constants.GIGAJOULE_KWH * total
        cursor.execute(
            """
            INSERT INTO ur_buildings(building_name, cooling_avg, heating_avg, electrical_avg, total_avg, total_kwh) VALUES ((?), (?), (?), (?), (?), (?));
            """,
            building,
            cooling,
            heating,
            electrical,
            total,
            total_kwh,
        )

    return building_usage


# Function to print results in a more readable format
def print_results(building_usage):
    print("Building Average Energy Consumption:")
    print("===================================")

    for building, data in building_usage.items():
        print(f"\nBuilding: {building}")
        for item in data:
            for category, value in item.items():
                print(f"  {category.capitalize()}: {value:.2f}")


if __name__ == "__main__":
    db_url = "microgrid.db"
    init_db(db_url)
    # csv_file_path = "uregina_dashboard/building_consumption.csv"
    # result = university_init_db(csv_file_path, db_url)
    # print_results(result)
