
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page containing the inflation rates
url = "https://ycharts.com/indicators/poland_inflation_rate"

# Function to get inflation rates
def get_inflation_rates(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("Parsed HTML:")
    print(soup.prettify())  # Print the parsed HTML for debugging
    
    # Find the table with the class 'vc'
    table = soup.find('table', class_='vc')
    
    if table is None:
        print("Could not find the table with class 'vc'.")
        return None
    
    # Prepare lists to hold date and value
    dates = []
    values = []
    
    # Extract date and value from the table
    tbody = table.find('tbody')
    if tbody is None:
        print("Could not find tbody in the table.")
        return None
    
    rows = tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            date = cols[0].text.strip()
            value = cols[1].text.strip().replace('%', '')  # Remove the percentage sign
            dates.append(date)
            values.append(float(value))
    
    # Create a DataFrame
    data = {
        'Date': dates,
        'Inflation Rate (%)': values
    }
    df = pd.DataFrame(data)
    
    return df

# Get the inflation rates
inflation_df = get_inflation_rates(url)

if inflation_df is not None:
    # Save the DataFrame to a CSV file
    csv_file_path = 'inflation_rates.csv'
    inflation_df.to_csv(csv_file_path, index=False)
    
    print(f"Inflation rates have been saved to {csv_file_path}")
    
    # Optionally, display the DataFrame
    print(inflation_df)
else:
    print("Failed to retrieve inflation rates.")