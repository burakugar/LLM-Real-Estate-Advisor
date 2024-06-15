import streamlit as st
import os
import requests
from dotenv import load_dotenv
import json
from html_parser import get_median_price
from parser_1 import get_market_data

# Load environment variables from .env file
load_dotenv()

# Initialize Streamlit session state
if 'investment_purpose' not in st.session_state:
    st.session_state.investment_purpose = ''
if 'risk_preference' not in st.session_state:
    st.session_state.risk_preference = ''
if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'min_budget' not in st.session_state:
    st.session_state.min_budget = 0
if 'max_budget' not in st.session_state:
    st.session_state.max_budget = 0
if 'number_of_rooms' not in st.session_state:
    st.session_state.number_of_rooms = 0
if 'should_parse_internet' not in st.session_state:
    st.session_state.should_parse_internet = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Define the real estate advisor class
class RealEstateAdvisor:
    def __init__(self, investment_purpose, risk_preference, market_data, min_budget, max_budget, number_of_rooms, should_parse_internet, chat_history):
        self.investment_purpose = investment_purpose
        self.risk_preference = risk_preference
        self.market_data = market_data
        self.min_budget = min_budget
        self.max_budget = max_budget
        self.number_of_rooms = number_of_rooms
        self.should_parse_internet = should_parse_internet
        self.chat_history = chat_history
        self.api_request = None
        self.prepare_api_request()

    def prepare_api_request(self):
    # Create the system message to define the advisor's role
        system_message = {
            "role": "system",
            "content": (
                "You are a real estate advisor specializing in the Polish market. "
                "Your task is to provide detailed advice based on the client's investment purpose, risk preference, budget, number of rooms, and current market data. "
                "Use the provided market data to give precise and actionable recommendations. "
                "Be professional, detailed, and ensure your advice is practical and based on real data."
            )
        }

        user_message = {
            "role": "user",
            "content": (
                f"Investment Purpose: {self.investment_purpose}\n"
                f"Risk Preference: {self.risk_preference}\n"
                f"Budget: {self.min_budget} to {self.max_budget}\n"
                f"Number of Rooms: {self.number_of_rooms}\n"
                f"Should Parse Internet: {self.should_parse_internet}\n"
                f"Market Data: {json.dumps(self.market_data, indent=2)}"
            )
        }

        messages = [system_message, user_message] + self.chat_history

        api_request = {
            "model": "gpt-4",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2048,
            "n": 1,
            "stream": False,
        }
        self.api_request = api_request


    def send_api_request(self, user_message):
        api_endpoint = "https://api.openai.com/v1/chat/completions"
        api_key = os.getenv("OPENAI_API_KEY")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        self.chat_history.append({"role": "user", "content": user_message})
        self.prepare_api_request()

        try:
            print(self.api_request)
            response = requests.post(api_endpoint, json=self.api_request, headers=headers, verify=False)
            print(response.text)
            response.raise_for_status()
            response_data = response.json()
            assistant_response = response_data['choices'][0]['message']['content']
            self.chat_history.append({"role": "assistant", "content": assistant_response})
            return assistant_response
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

# Streamlit interface
st.title("Real Estate Advisor")

st.header("Enter your preferences:")
investment_purpose_options = [
    "To generate rental income",
    "Long-term investment",
    "Short-term profit",
    "For residency purposes"
]
st.session_state.investment_purpose = st.selectbox("Investment Purpose", investment_purpose_options, index=investment_purpose_options.index(st.session_state.investment_purpose) if st.session_state.investment_purpose else 0)

risk_preference_options = [
    "High risk, high return",
    "Medium risk, medium return",
    "Low risk, low return"
]
st.session_state.risk_preference = st.selectbox("Risk Preference", risk_preference_options, index=risk_preference_options.index(st.session_state.risk_preference) if st.session_state.risk_preference else 0)

st.session_state.min_budget = st.number_input("Minimum Budget", min_value=0, value=st.session_state.min_budget, step=1000)
st.session_state.max_budget = st.number_input("Maximum Budget", min_value=0, value=st.session_state.max_budget, step=1000)

st.session_state.number_of_rooms = st.number_input("Number of Rooms", min_value=0, value=st.session_state.number_of_rooms, step=1)
st.session_state.should_parse_internet = st.checkbox("Should Parse Internet", value=st.session_state.should_parse_internet)

if st.session_state.should_parse_internet:
    base_url = 'https://www.otodom.pl/_next/data/lG7lHcURBL6PPE-_9iij8/pl/wyniki/wynajem/mieszkanie/cala-polska.json'
    search_params = {
        'distanceRadius': '75',
        'limit': '36',
        'ownerTypeSingleSelect': 'ALL',
        'priceMin': str(st.session_state.min_budget),
        'priceMax': str(st.session_state.max_budget),
        'areaMin': '100',
        'areaMax': '250',
        'roomsNumber': f'%5B{st.session_state.number_of_rooms}%5D',
        'by': 'PRICE',
        'direction': 'DESC',
        'viewType': 'listing',
        'page': 1
    }
    median_price = get_median_price(base_url, search_params)
    market_data_internet = {"median_price": median_price}
    market_data_dataset = get_market_data(st.session_state.number_of_rooms)
    print(market_data_dataset)
    st.session_state.market_data = {**market_data_internet, **market_data_dataset}
else:
    st.session_state.market_data = get_market_data(st.session_state.number_of_rooms)

advisor = RealEstateAdvisor(
    st.session_state.investment_purpose,
    st.session_state.risk_preference,
    st.session_state.market_data,
    st.session_state.min_budget,
    st.session_state.max_budget,
    st.session_state.number_of_rooms,
    st.session_state.should_parse_internet,
    st.session_state.chat_history
)

st.header("Chat with the Real Estate Advisor")
user_input = st.text_input("Your message")

if st.button("Send"):
    if user_input:
        advisor_response = advisor.send_api_request(user_input)
        st.write("### Advisor's Response:")
        st.write(advisor_response)

# To run the Streamlit app, save the script and execute: streamlit run app.py
