import sqlite3
import pandas as pd
import ast


def init_db(db_url):
    """
    Create and initialize tables
    """
    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS calculations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_KWH REAL NOT NULL DEFAULT 0,
        monthly_savings REAL NOT NULL DEFAULT 0,
        annual_savings REAL NOT NULL DEFAULT 0,
        calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS solarpanels(
        solar_id INTEGER PRIMARY KEY AUTOINCREMENT,
        panels_needed INTEGER NOT NULL DEFAULT 0,           
                   )


    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS ur_buildings(
    building_id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_name TEXT,
    cooling_avg REAL NOT NULL,
    heating_avg REAL NOT NULL,
    electrical_avg REAL NOT NULL,
    total_avg REAL NOT NULL,
    start_date DATE,
    end_date DATE;
    )
"""
    )

    conn.commit()
    conn.close()

def university_init_db(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Initialize the dictionary to store building usage data
    building_usage = {}
    
    # Columns to process
    columns = ['cooling', 'heating', 'electrical']
    
    # Process each building
    for building_index, row in df.iterrows():
        building_code = row['building_code']
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

# Function to print results in a more readable format
def print_results(building_usage):
    print("Building Average Energy Consumption:")
    print("===================================")
    
    for building, data in building_usage.items():
        print(f"\nBuilding: {building}")
        for item in data:
            for category, value in item.items():
                print(f"  {category.capitalize()}: {value:.2f}")

if __name__ == '__main__':
    # db_url = "microgrid.db"
    # init_db(db_url)
    csv_file_path = "uregina_dashboard/building_consumption.csv"
    result = university_init_db(csv_file_path)
    print_results(result)
