import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

# Base URL for the website
base_url = "https://www.uregina.ca"
# Ajax endpoint that provides the data
ajax_url = base_url + "/energy-dashboard/inc/ajax.php"

# Get building codes from the HTML page
def get_building_codes():
    # Get the main page
    response = requests.get(base_url + "/energy-dashboard/index.html")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all div elements with data-building attribute
    building_divs = soup.find_all('div', attrs={'data-building': True})
    
    # Extract building codes
    building_codes = [div['data-building'] for div in building_divs]
    return building_codes

# Get overview data
def get_overview_data():
    params = {'overview': 'true'}
    response = requests.get(ajax_url, params=params)
    return response.json()

# Get energy intensity data
def get_energy_intensity_data():
    params = {'overview_intesity': 'true'}
    response = requests.get(ajax_url, params=params)
    return response.json()

# Get building-specific consumption data
def get_building_consumption(building_code):
    params = {
        'building_rankings': building_code,
        'type': 'consuption'  # Note: this is the spelling used in the original code
    }
    response = requests.get(ajax_url, params=params)
    return response.json()

# Get building-specific greenhouse data
def get_building_greenhouse(building_code):
    params = {
        'building_rankings': building_code,
        'type': 'greenhouse'
    }
    response = requests.get(ajax_url, params=params)
    return response.json()

# Get today's consumption data
def get_todays_consumption():
    params = {'todays_consumption': ''}
    response = requests.get(ajax_url, params=params)
    return response.json()

# Main function to collect all data
def collect_all_data():
    # Container for all our data
    all_data = {}
    
    # Get building codes
    building_codes = get_building_codes()
    print(f"Found {len(building_codes)} buildings: {building_codes}")
    
    # Get overview data
    try:
        all_data['overview'] = get_overview_data()
        print("Successfully retrieved overview data")
    except Exception as e:
        print(f"Error retrieving overview data: {e}")
    
    # Get energy intensity data
    try:
        all_data['energy_intensity'] = get_energy_intensity_data()
        print("Successfully retrieved energy intensity data")
    except Exception as e:
        print(f"Error retrieving energy intensity data: {e}")
    
    # Get today's consumption
    try:
        all_data['todays_consumption'] = get_todays_consumption()
        print("Successfully retrieved today's consumption data")
    except Exception as e:
        print(f"Error retrieving today's consumption data: {e}")
    
    # Get building-specific data
    all_data['buildings'] = {}
    for code in building_codes:
        all_data['buildings'][code] = {}
        
        # Add small delay to avoid overloading the server
        time.sleep(1)
        
        try:
            all_data['buildings'][code]['consumption'] = get_building_consumption(code)
            print(f"Successfully retrieved consumption data for building {code}")
        except Exception as e:
            print(f"Error retrieving consumption data for building {code}: {e}")
        
        time.sleep(1)
        
        try:
            all_data['buildings'][code]['greenhouse'] = get_building_greenhouse(code)
            print(f"Successfully retrieved greenhouse data for building {code}")
        except Exception as e:
            print(f"Error retrieving greenhouse data for building {code}: {e}")
    
    # Save all data to a JSON file
    with open('uregina_energy_data.json', 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print("All data saved to uregina_energy_data.json")
    
    return all_data

# Process the data into a more readable format (optional)
def process_data(all_data):
    # Example: Convert building consumption data to a DataFrame
    buildings_data = []
    
    for code, data in all_data['buildings'].items():
        if 'consumption' in data and 'data' in data['consumption']:
            consumption = data['consumption']['data']
            
            # Extract relevant information
            building_info = {
                'building_code': code,
                'date': consumption.get('date', ''),
                'labels': consumption.get('labels', []),
                'cooling': consumption.get('cooling', []),
                'heating': consumption.get('heating', []),
                'electrical': consumption.get('electrical', [])
            }
            
            buildings_data.append(building_info)
    
    # Save to CSV
    df = pd.DataFrame(buildings_data)
    df.to_csv('building_consumption.csv', index=False)
    print("Building consumption data saved to building_consumption.csv")

# Run the data collection
if __name__ == "__main__":
    all_data = collect_all_data()
    process_data(all_data)