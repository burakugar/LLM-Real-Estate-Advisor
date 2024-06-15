import requests
import time
import random

def send_request(url, headers):
    try:
        print(url)  # For debugging purposes
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while sending request: {e}")
        return None

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43'
    ]
    return random.choice(user_agents)

def get_random_referer():
    referers = [
        'https://www.google.com',
        'https://yandex.com',
        'https://www.bing.com',
        'https://duckduckgo.com',
        'https://www.baidu.com'
    ]
    return random.choice(referers)

def search_apartments(base_url, params):
    url = base_url + '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': get_random_referer(),
        'Origin': get_random_referer()
    }
    data = send_request(url, headers)
    return data

def get_median_price(base_url, search_params):
    # First request to get the total page count
    data = search_apartments(base_url, search_params)
    if data:
        total_pages = data['pageProps']['data']['searchAds']['pagination']['totalPages']
        print(f"Total pages: {total_pages}")

        # Calculate the median page
        median_page = (total_pages // 2) + 1
        print(f"Median page: {median_page}")

        # Modify search_params to go to the median page
        search_params['page'] = median_page

        # Wait for 10 seconds before making the second request
        time.sleep(10)

        # Second request to get the median page results
        median_data = search_apartments(base_url, search_params)
        
        if median_data:
            items = median_data['pageProps']['data']['searchAds']['items']
            prices = [item['totalPrice']['value'] for item in items if 'totalPrice' in item and 'value' in item['totalPrice']]
            average_price = sum(prices) / len(prices) if prices else 0
            print(f"Average price on median page: {average_price} PLN")
            return average_price
        else:
            print("Failed to retrieve data for the median page.")
            return None
    else:
        print("Failed to retrieve initial data.")
        return None