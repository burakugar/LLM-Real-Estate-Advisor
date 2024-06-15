from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page containing the inflation rates
url = "https://ycharts.com/indicators/poland_inflation_rate"

# Function to get inflation rates
def get_inflation_rates(url):
    # Set up the Selenium webdriver (make sure you have the appropriate driver installed)
    driver = webdriver.Chrome()  # Use the appropriate driver for your browser
    driver.get(url)
    
    # Wait for the page to load and render the data (adjust the timeout as needed)
    driver.implicitly_wait(10)
    
    # Get the page source after JavaScript execution
    page_source = driver.page_source
    
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    
    print("Parsed HTML:")
    print(soup.prettify())  # Print the parsed HTML for debugging
    
    # Find the table with the class 'vc'
    table = soup.find('table', class_='vc')
    
    if table is None:
        print("Could not find the table with class 'vc'.")
        driver.quit()
        return None
    
    # Prepare lists to hold date and value
    dates = []
    values = []
    
    # Extract date and value from the table
    tbody = table.find('tbody')
    if tbody is None:
        print("Could not find tbody in the table.")
        driver.quit()
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
    
    # Close the Selenium webdriver
    driver.quit()
    
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