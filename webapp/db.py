import json
import os
from pprint import pprint

import streamlit as st
from deta import Deta
import hashlib

DETA_KEY = st.secrets.DETA_KEY
deta = Deta(DETA_KEY)

portfolio = deta.Base("portfolio")
auth = deta.Base("auth")

#---RECIPE FUNCTIONS

def get_portfolio(uuid):
    return portfolio.fetch(query={"uuid": uuid}).items, len(portfolio.fetch().items)

def get_portfolio_total(uuid):
    assets = get_portfolio(uuid)[0]
    return sum([asset["investment"] for asset in assets])

def delete_from_portfolio(uuid):
    return portfolio.delete(uuid)

def add_to_portfolio(ticker, etf_check, etf_provider, investment_amount, metadata, holdings, uuid = None):
    return portfolio.put(
        {
            "ticker" : ticker,
            "etf_check" : etf_check, 
            "etf_provider" : etf_provider,
            "investment" :investment_amount, 
            "metadata": metadata,
            "holdings": holdings,
            "uuid": uuid
        }
    )

       
def register_user(username, email, password):
    return auth.put(
        {
            "key" : username,
            "email" : email, 
            "password" : hashlib.sha256(password.encode('UTF-8')).hexdigest()
        }
    )

def authenticate_user(username, password):
    user = auth.get(username)
    if user:
        return True if hashlib.sha256(password.encode('UTF-8')).hexdigest() == user["password"] else False
    else:
        return False

def check_if_username_available(username):
    user = auth.get(username)
    return True if not user else False