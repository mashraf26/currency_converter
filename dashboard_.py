import streamlit as st
import requests
import pycountry

def currency_name(code):
    currency = pycountry.currencies.get(alpha_3=code)
    return currency.name if currency else code


def get_rates():
    try:
      url = "https://api.exchangerate-api.com/v4/latest/USD"
      data = requests.get(url).json()
      return data["rates"]
    except:
      return None

rates = get_rates()

st.set_page_config(page_title="Currency Converter", page_icon="💱")

st.title("💱 Currency Converter Dashboard")

st.write("convert currencies in real-time using live exchange rates")

if rates is None:
   st.error("Error fetching exchange rates, Please try again")
else:
   currencies = sorted(list(rates.keys()))

from_currency = st.selectbox("From Currency", currencies, format_func= lambda x: f"{currency_name(x)} ({x})")
to_currency = st.selectbox("To Currency", currencies, format_func= lambda x: f"{currency_name(x)} ({x})")

amount = st.number_input("Enter Amount", min_value=0.0, format="%.2f")

if st.button("Convert"):
    if from_currency == to_currency:
       st.error("You cannot convert to the same currency")
    elif amount == 0:
       st.warning("Please enter a value greater than zero")
    elif amount < 0:
       st.error("Amount cannot be negative")
    else:
       try:

         usd = amount / rates[from_currency]
         result = usd * rates[to_currency]

         st.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
       except:
         st.error("Something went wrong during conversion")