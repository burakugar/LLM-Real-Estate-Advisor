from IPython.display import IFrame
import pandas as pd
import os

url = "https://public.tableau.com/views/ApartmentListingsinPoland/Dashboard2?:language=en-US&:embed=y&:display_count=yes&:showVizHome=no#5"

IFrame(url, width=1670, height=950)

sale_file_paths = [
    "dataset/apartments_pl_2023_08.csv",
    "dataset/apartments_pl_2023_09.csv",
    "dataset/apartments_pl_2023_10.csv",
    "dataset/apartments_pl_2023_11.csv",
    "dataset/apartments_pl_2023_12.csv",
    "dataset/apartments_pl_2024_01.csv",
    "dataset/apartments_pl_2024_02.csv",
    "dataset/apartments_pl_2024_04.csv",
    "dataset/apartments_pl_2024_05.csv",
    "dataset/apartments_pl_2024_06.csv"
]

rent_file_paths = [
    "dataset/apartments_rent_pl_2023_11.csv",
    "dataset/apartments_rent_pl_2023_12.csv",
    "dataset/apartments_rent_pl_2024_01.csv",
    "dataset/apartments_rent_pl_2024_02.csv",
    "dataset/apartments_rent_pl_2024_03.csv",
    "dataset/apartments_rent_pl_2024_04.csv",
    "dataset/apartments_rent_pl_2024_05.csv",
    "dataset/apartments_rent_pl_2024_06.csv"
]

sale_dfs = []
rent_dfs = []

for path in sale_file_paths:
    if os.path.exists(path):
        df = pd.read_csv(path)
        df = df[df['city'] == 'warszawa']  # Filter data for Warszawa only
        df = df[['id', 'price', 'rooms', 'squareMeters']]  # Select desired columns
        
        # Round square meters to the nearest integer
        df['squareMeters'] = df['squareMeters'].round().astype(int)
        
        # Extract year and month from the file name
        file_name = os.path.basename(path).split('.')[0]  # Remove the file extension
        year, month = map(int, file_name.split('_')[2:4])
        df['year'] = year  # Add the 'year' column
        df['month'] = month  # Add the 'month' column
        
        sale_dfs.append(df)
    else:
        print(f"File not found: {path}")

for path in rent_file_paths:
    if os.path.exists(path):
        df = pd.read_csv(path)
        df = df[df['city'] == 'warszawa']  # Filter data for Warszawa only
        df = df[['id', 'price', 'rooms', 'squareMeters']]  # Select desired columns
        
        # Round square meters to the nearest integer
        df['squareMeters'] = df['squareMeters'].round().astype(int)
        
        # Extract year and month from the file name
        file_name = os.path.basename(path).split('.')[0]  # Remove the file extension
        year, month = map(int, file_name.split('_')[3:5])
        df['year'] = year  # Add the 'year' column
        df['month'] = month  # Add the 'month' column
        
        rent_dfs.append(df)
    else:
        print(f"File not found: {path}")

# Concatenate and save the data for sale and rent separately
if sale_dfs:
    sale_data = pd.concat(sale_dfs)
    sale_data.to_csv("dataset/sale_data.csv", index=False)
    print("Sale data saved to dataset/sale_data.csv")
else:
    print("No sale data found.")

if rent_dfs:
    rent_data = pd.concat(rent_dfs)
    rent_data.to_csv("dataset/rent_data.csv", index=False)
    print("Rent data saved to dataset/rent_data.csv")
else:
    print("No rent data found.")

def get_market_data(number_of_rooms):
    # Calculate and return median prices and standard deviation by room number and square meters for each year and month
    market_data = {}
    for year in [2023, 2024]:
        year_data = {}
        
        # Sale data
        sale_data_year = sale_data[sale_data['year'] == year]
        if not sale_data_year.empty:
            for month in sale_data_year['month'].unique():
                sale_data_month = sale_data_year[sale_data_year['month'] == month]
                median_by_rooms = sale_data_month[sale_data_month['rooms'] == number_of_rooms]['price'].median()
                std_by_rooms = sale_data_month[sale_data_month['rooms'] == number_of_rooms]['price'].std()
                year_data[f'sale_median_price_rooms_{month}'] = median_by_rooms
                year_data[f'sale_std_price_rooms_{month}'] = std_by_rooms
        
        # Rent data
        rent_data_year = rent_data[rent_data['year'] == year]
        if not rent_data_year.empty:
            for month in rent_data_year['month'].unique():
                rent_data_month = rent_data_year[rent_data_year['month'] == month]
                median_by_rooms = rent_data_month[rent_data_month['rooms'] == number_of_rooms]['price'].median()
                std_by_rooms = rent_data_month[rent_data_month['rooms'] == number_of_rooms]['price'].std()
                year_data[f'rent_median_price_rooms_{month}'] = median_by_rooms
                year_data[f'rent_std_price_rooms_{month}'] = std_by_rooms
        
        market_data[str(year)] = year_data
    
    return market_data