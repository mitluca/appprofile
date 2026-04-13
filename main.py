from base64 import b64encode
from datetime import datetime
from io import BytesIO
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.collections import LineCollection
from matplotlib.ticker import FuncFormatter


st.set_page_config(
    page_title="GreenVest | Sustainable Investing Workspace",
    layout="wide",
    initial_sidebar_state="collapsed",
)


ROOT = Path(__file__).parent
STATIC_DIR = ROOT / "static"
RESULTS_DIR = ROOT / ".greenvest_results"
LOGO_PATH = STATIC_DIR / "Sustainable growth and innovation logo.png"
QUESTION_PATH = STATIC_DIR / "question.png"
RESULTS_DIR.mkdir(exist_ok=True)

SECTORS = [
    "Clean Energy",
    "Technology",
    "Healthcare",
    "Financial Services",
    "Consumer Goods",
    "Industrials",
    "Real Estate",
    "Tobacco",
    "Weapons / Defence",
    "Gambling",
    "Fossil Fuels / Energy",
    "Alcohol",
]

CORNER_THRESHOLD = 0.002

REVIEWS = [
    {
        "author": "BlueHorizon",
        "quote": (
            "We absolutely love GreenVest. Our own app is striving to become like "
            "this one because the experience feels polished, trustworthy, and easy to follow."
        ),
    },
    {
        "author": "Octavian",
        "quote": (
            "The balance between sustainability and returns is explained so clearly "
            "that I can make decisions with confidence."
        ),
    },
    {
        "author": "Marget",
        "quote": (
            "Beautifully presented and surprisingly simple to use. The charts finally "
            "feel investor-friendly instead of academic."
        ),
    },
    {
        "author": "Anonymous Investor",
        "quote": (
            "I like how GreenVest keeps the important information front and center. "
            "It feels calm, modern, and professional."
        ),
    },
    {
        "author": "Anonymous Investor II",
        "quote": (
            "The journey feels calm and focused. I can talk through sustainable choices "
            "without losing sight of return and risk."
        ),
    },
    {
        "author": "Anonymous Investor III",
        "quote": (
            "GreenVest makes portfolio trade-offs easier to explain. The visuals feel much "
            "more investor-ready than most sustainability tools."
        ),
    },
    {
        "author": "Anonymous Investor IV",
        "quote": (
            "This is one of the few ESG tools that feels polished enough for a real client conversation."
        ),
    },
    {
        "author": "Northlight Capital",
        "quote": (
            "The onboarding flow makes sustainable investing feel approachable without "
            "oversimplifying the strategy."
        ),
    },
    {
        "author": "Willow Ridge",
        "quote": (
            "GreenVest turns a complicated decision into something clear and motivating. "
            "That is rare in finance tools."
        ),
    },
]

CURATED_ASSETS = [
    {"name": "Apple", "ticker": "AAPL", "sector": "Technology", "mu": 0.162, "sigma": 0.248, "e": 82, "s": 74, "g": 78},
    {"name": "Microsoft", "ticker": "MSFT", "sector": "Technology", "mu": 0.148, "sigma": 0.225, "e": 79, "s": 80, "g": 85},
    {"name": "NVIDIA", "ticker": "NVDA", "sector": "Technology", "mu": 0.310, "sigma": 0.510, "e": 64, "s": 68, "g": 72},
    {"name": "Alphabet", "ticker": "GOOGL", "sector": "Technology", "mu": 0.138, "sigma": 0.230, "e": 71, "s": 65, "g": 69},
    {"name": "Meta", "ticker": "META", "sector": "Technology", "mu": 0.175, "sigma": 0.350, "e": 55, "s": 48, "g": 52},
    {"name": "Samsung", "ticker": "005930.KS", "sector": "Technology", "mu": 0.080, "sigma": 0.280, "e": 68, "s": 62, "g": 65},
    {"name": "ASML", "ticker": "ASML", "sector": "Technology", "mu": 0.195, "sigma": 0.310, "e": 78, "s": 76, "g": 80},
    {"name": "Taiwan Semiconductor", "ticker": "TSM", "sector": "Technology", "mu": 0.155, "sigma": 0.340, "e": 70, "s": 64, "g": 72},
    {"name": "Salesforce", "ticker": "CRM", "sector": "Technology", "mu": 0.128, "sigma": 0.295, "e": 76, "s": 78, "g": 74},
    {"name": "Adobe", "ticker": "ADBE", "sector": "Technology", "mu": 0.142, "sigma": 0.285, "e": 74, "s": 72, "g": 76},
    {"name": "SAP", "ticker": "SAP", "sector": "Technology", "mu": 0.118, "sigma": 0.240, "e": 80, "s": 77, "g": 82},
    {"name": "Oracle", "ticker": "ORCL", "sector": "Technology", "mu": 0.132, "sigma": 0.255, "e": 62, "s": 60, "g": 68},
    {"name": "Accenture", "ticker": "ACN", "sector": "Technology", "mu": 0.122, "sigma": 0.220, "e": 82, "s": 84, "g": 80},
    {"name": "Infosys", "ticker": "INFY", "sector": "Technology", "mu": 0.095, "sigma": 0.255, "e": 75, "s": 72, "g": 74},
    {"name": "Qualcomm", "ticker": "QCOM", "sector": "Technology", "mu": 0.138, "sigma": 0.310, "e": 66, "s": 63, "g": 70},
    {"name": "Texas Instruments", "ticker": "TXN", "sector": "Technology", "mu": 0.112, "sigma": 0.230, "e": 69, "s": 65, "g": 72},
    {"name": "Intel", "ticker": "INTC", "sector": "Technology", "mu": 0.042, "sigma": 0.310, "e": 72, "s": 68, "g": 70},
    {"name": "Broadcom", "ticker": "AVGO", "sector": "Technology", "mu": 0.210, "sigma": 0.330, "e": 60, "s": 58, "g": 66},
    {"name": "Shopify", "ticker": "SHOP", "sector": "Technology", "mu": 0.185, "sigma": 0.480, "e": 64, "s": 68, "g": 62},
    {"name": "Capgemini", "ticker": "CGEMY", "sector": "Technology", "mu": 0.108, "sigma": 0.235, "e": 78, "s": 80, "g": 76},

    {"name": "Johnson & Johnson", "ticker": "JNJ", "sector": "Healthcare", "mu": 0.072, "sigma": 0.145, "e": 70, "s": 75, "g": 77},
    {"name": "GSK", "ticker": "GSK", "sector": "Healthcare", "mu": 0.065, "sigma": 0.180, "e": 66, "s": 72, "g": 68},
    {"name": "AstraZeneca", "ticker": "AZN", "sector": "Healthcare", "mu": 0.095, "sigma": 0.195, "e": 74, "s": 78, "g": 76},
    {"name": "Novo Nordisk", "ticker": "NVO", "sector": "Healthcare", "mu": 0.185, "sigma": 0.290, "e": 80, "s": 82, "g": 83},
    {"name": "Roche", "ticker": "RHHBY", "sector": "Healthcare", "mu": 0.068, "sigma": 0.175, "e": 76, "s": 80, "g": 78},
    {"name": "Novartis", "ticker": "NVS", "sector": "Healthcare", "mu": 0.078, "sigma": 0.180, "e": 73, "s": 76, "g": 74},
    {"name": "Pfizer", "ticker": "PFE", "sector": "Healthcare", "mu": 0.048, "sigma": 0.195, "e": 68, "s": 72, "g": 70},
    {"name": "Merck & Co", "ticker": "MRK", "sector": "Healthcare", "mu": 0.092, "sigma": 0.188, "e": 70, "s": 73, "g": 72},
    {"name": "Eli Lilly", "ticker": "LLY", "sector": "Healthcare", "mu": 0.228, "sigma": 0.285, "e": 72, "s": 74, "g": 76},
    {"name": "Abbott Laboratories", "ticker": "ABT", "sector": "Healthcare", "mu": 0.088, "sigma": 0.190, "e": 72, "s": 74, "g": 76},
    {"name": "Medtronic", "ticker": "MDT", "sector": "Healthcare", "mu": 0.058, "sigma": 0.185, "e": 68, "s": 70, "g": 72},
    {"name": "Sanofi", "ticker": "SNY", "sector": "Healthcare", "mu": 0.072, "sigma": 0.178, "e": 72, "s": 74, "g": 70},
    {"name": "Fresenius", "ticker": "FSNUY", "sector": "Healthcare", "mu": 0.038, "sigma": 0.210, "e": 65, "s": 68, "g": 64},
    {"name": "Becton Dickinson", "ticker": "BDX", "sector": "Healthcare", "mu": 0.075, "sigma": 0.185, "e": 70, "s": 72, "g": 74},

    {"name": "JPMorgan Chase", "ticker": "JPM", "sector": "Financial Services", "mu": 0.110, "sigma": 0.220, "e": 54, "s": 62, "g": 70},
    {"name": "HSBC", "ticker": "HSBC", "sector": "Financial Services", "mu": 0.082, "sigma": 0.195, "e": 58, "s": 60, "g": 65},
    {"name": "BlackRock", "ticker": "BLK", "sector": "Financial Services", "mu": 0.118, "sigma": 0.230, "e": 65, "s": 67, "g": 74},
    {"name": "Goldman Sachs", "ticker": "GS", "sector": "Financial Services", "mu": 0.125, "sigma": 0.270, "e": 50, "s": 55, "g": 65},
    {"name": "Morgan Stanley", "ticker": "MS", "sector": "Financial Services", "mu": 0.115, "sigma": 0.255, "e": 55, "s": 60, "g": 68},
    {"name": "Visa", "ticker": "V", "sector": "Financial Services", "mu": 0.148, "sigma": 0.200, "e": 62, "s": 68, "g": 76},
    {"name": "Mastercard", "ticker": "MA", "sector": "Financial Services", "mu": 0.152, "sigma": 0.205, "e": 64, "s": 70, "g": 78},
    {"name": "Allianz", "ticker": "ALIZY", "sector": "Financial Services", "mu": 0.092, "sigma": 0.195, "e": 68, "s": 66, "g": 72},
    {"name": "AXA", "ticker": "AXAHY", "sector": "Financial Services", "mu": 0.085, "sigma": 0.200, "e": 70, "s": 65, "g": 70},
    {"name": "BNP Paribas", "ticker": "BNPQY", "sector": "Financial Services", "mu": 0.078, "sigma": 0.215, "e": 62, "s": 60, "g": 66},
    {"name": "UBS Group", "ticker": "UBS", "sector": "Financial Services", "mu": 0.088, "sigma": 0.225, "e": 60, "s": 58, "g": 68},
    {"name": "American Express", "ticker": "AXP", "sector": "Financial Services", "mu": 0.132, "sigma": 0.240, "e": 60, "s": 65, "g": 72},
    {"name": "S&P Global", "ticker": "SPGI", "sector": "Financial Services", "mu": 0.158, "sigma": 0.230, "e": 72, "s": 70, "g": 78},

    {"name": "Unilever", "ticker": "UL", "sector": "Consumer Goods", "mu": 0.060, "sigma": 0.155, "e": 84, "s": 80, "g": 78},
    {"name": "Nestle", "ticker": "NSRGY", "sector": "Consumer Goods", "mu": 0.058, "sigma": 0.148, "e": 72, "s": 70, "g": 74},
    {"name": "Procter & Gamble", "ticker": "PG", "sector": "Consumer Goods", "mu": 0.088, "sigma": 0.162, "e": 74, "s": 72, "g": 76},
    {"name": "L'Oreal", "ticker": "LRLCY", "sector": "Consumer Goods", "mu": 0.105, "sigma": 0.195, "e": 82, "s": 78, "g": 80},
    {"name": "Colgate-Palmolive", "ticker": "CL", "sector": "Consumer Goods", "mu": 0.075, "sigma": 0.158, "e": 72, "s": 70, "g": 72},
    {"name": "Kering", "ticker": "PPRUY", "sector": "Consumer Goods", "mu": 0.092, "sigma": 0.265, "e": 78, "s": 72, "g": 74},
    {"name": "LVMH", "ticker": "LVMUY", "sector": "Consumer Goods", "mu": 0.115, "sigma": 0.255, "e": 70, "s": 68, "g": 72},
    {"name": "Danone", "ticker": "DANOY", "sector": "Consumer Goods", "mu": 0.042, "sigma": 0.175, "e": 80, "s": 76, "g": 74},
    {"name": "Henkel", "ticker": "HENKY", "sector": "Consumer Goods", "mu": 0.048, "sigma": 0.178, "e": 76, "s": 72, "g": 74},
    {"name": "Beiersdorf", "ticker": "BDRFY", "sector": "Consumer Goods", "mu": 0.085, "sigma": 0.182, "e": 80, "s": 76, "g": 78},
    {"name": "Reckitt Benckiser", "ticker": "RBGLY", "sector": "Consumer Goods", "mu": 0.055, "sigma": 0.185, "e": 72, "s": 68, "g": 70},

    {"name": "Tesla", "ticker": "TSLA", "sector": "Clean Energy", "mu": 0.220, "sigma": 0.580, "e": 85, "s": 52, "g": 48},
    {"name": "Vestas Wind", "ticker": "VWDRY", "sector": "Clean Energy", "mu": 0.090, "sigma": 0.310, "e": 91, "s": 78, "g": 80},
    {"name": "Orsted", "ticker": "DNNGY", "sector": "Clean Energy", "mu": 0.075, "sigma": 0.280, "e": 93, "s": 76, "g": 79},
    {"name": "Enphase Energy", "ticker": "ENPH", "sector": "Clean Energy", "mu": 0.245, "sigma": 0.560, "e": 88, "s": 72, "g": 74},
    {"name": "First Solar", "ticker": "FSLR", "sector": "Clean Energy", "mu": 0.185, "sigma": 0.440, "e": 90, "s": 74, "g": 76},
    {"name": "SolarEdge", "ticker": "SEDG", "sector": "Clean Energy", "mu": 0.125, "sigma": 0.520, "e": 86, "s": 70, "g": 72},
    {"name": "Plug Power", "ticker": "PLUG", "sector": "Clean Energy", "mu": 0.048, "sigma": 0.680, "e": 84, "s": 66, "g": 60},
    {"name": "Brookfield Renewable", "ticker": "BEP", "sector": "Clean Energy", "mu": 0.082, "sigma": 0.260, "e": 90, "s": 75, "g": 78},
    {"name": "NextEra Energy", "ticker": "NEE", "sector": "Clean Energy", "mu": 0.098, "sigma": 0.220, "e": 88, "s": 74, "g": 76},
    {"name": "Iberdrola", "ticker": "IBDRY", "sector": "Clean Energy", "mu": 0.088, "sigma": 0.210, "e": 90, "s": 76, "g": 78},
    {"name": "Enel", "ticker": "ENLAY", "sector": "Clean Energy", "mu": 0.072, "sigma": 0.220, "e": 86, "s": 74, "g": 72},
    {"name": "Acciona Energia", "ticker": "ACXIF", "sector": "Clean Energy", "mu": 0.065, "sigma": 0.285, "e": 88, "s": 72, "g": 70},
    {"name": "Northland Power", "ticker": "NPIFF", "sector": "Clean Energy", "mu": 0.070, "sigma": 0.270, "e": 86, "s": 70, "g": 72},

    {"name": "Siemens", "ticker": "SIEGY", "sector": "Industrials", "mu": 0.098, "sigma": 0.215, "e": 76, "s": 73, "g": 77},
    {"name": "Schneider Electric", "ticker": "SBGSY", "sector": "Industrials", "mu": 0.112, "sigma": 0.225, "e": 88, "s": 80, "g": 82},
    {"name": "ABB", "ticker": "ABB", "sector": "Industrials", "mu": 0.105, "sigma": 0.228, "e": 82, "s": 76, "g": 78},
    {"name": "Honeywell", "ticker": "HON", "sector": "Industrials", "mu": 0.098, "sigma": 0.210, "e": 74, "s": 70, "g": 76},
    {"name": "Caterpillar", "ticker": "CAT", "sector": "Industrials", "mu": 0.132, "sigma": 0.255, "e": 60, "s": 62, "g": 68},
    {"name": "3M", "ticker": "MMM", "sector": "Industrials", "mu": 0.042, "sigma": 0.225, "e": 62, "s": 60, "g": 66},
    {"name": "Rockwell Automation", "ticker": "ROK", "sector": "Industrials", "mu": 0.118, "sigma": 0.240, "e": 76, "s": 72, "g": 74},
    {"name": "Xylem", "ticker": "XYL", "sector": "Industrials", "mu": 0.105, "sigma": 0.235, "e": 86, "s": 78, "g": 78},
    {"name": "Alfa Laval", "ticker": "ALFVY", "sector": "Industrials", "mu": 0.092, "sigma": 0.220, "e": 80, "s": 74, "g": 76},
    {"name": "Danaher", "ticker": "DHR", "sector": "Industrials", "mu": 0.118, "sigma": 0.225, "e": 74, "s": 72, "g": 78},
    {"name": "Legrand", "ticker": "LGRVF", "sector": "Industrials", "mu": 0.102, "sigma": 0.215, "e": 82, "s": 76, "g": 78},
    {"name": "Nibe Industrier", "ticker": "NIBEF", "sector": "Industrials", "mu": 0.085, "sigma": 0.260, "e": 84, "s": 74, "g": 76},
    {"name": "Watts Water Technologies", "ticker": "WTS", "sector": "Industrials", "mu": 0.095, "sigma": 0.225, "e": 80, "s": 72, "g": 74},

    {"name": "Prologis", "ticker": "PLD", "sector": "Real Estate", "mu": 0.092, "sigma": 0.200, "e": 72, "s": 68, "g": 73},
    {"name": "American Tower", "ticker": "AMT", "sector": "Real Estate", "mu": 0.085, "sigma": 0.195, "e": 68, "s": 64, "g": 70},
    {"name": "Segro", "ticker": "SEGXF", "sector": "Real Estate", "mu": 0.098, "sigma": 0.215, "e": 78, "s": 70, "g": 74},
    {"name": "Vonovia", "ticker": "VONOY", "sector": "Real Estate", "mu": 0.040, "sigma": 0.235, "e": 72, "s": 68, "g": 70},
    {"name": "Unibail-Rodamco", "ticker": "UNBLF", "sector": "Real Estate", "mu": 0.045, "sigma": 0.250, "e": 70, "s": 64, "g": 68},
    {"name": "Welltower", "ticker": "WELL", "sector": "Real Estate", "mu": 0.088, "sigma": 0.200, "e": 70, "s": 68, "g": 72},
    {"name": "Digital Realty", "ticker": "DLR", "sector": "Real Estate", "mu": 0.075, "sigma": 0.205, "e": 74, "s": 68, "g": 72},
    {"name": "Klepierre", "ticker": "KLPEF", "sector": "Real Estate", "mu": 0.052, "sigma": 0.235, "e": 68, "s": 62, "g": 66},

    {"name": "Shell", "ticker": "SHEL", "sector": "Fossil Fuels / Energy", "mu": 0.095, "sigma": 0.240, "e": 38, "s": 50, "g": 58},
    {"name": "BP", "ticker": "BP", "sector": "Fossil Fuels / Energy", "mu": 0.088, "sigma": 0.235, "e": 34, "s": 48, "g": 55},
    {"name": "ExxonMobil", "ticker": "XOM", "sector": "Fossil Fuels / Energy", "mu": 0.100, "sigma": 0.250, "e": 30, "s": 45, "g": 52},
    {"name": "Chevron", "ticker": "CVX", "sector": "Fossil Fuels / Energy", "mu": 0.095, "sigma": 0.245, "e": 32, "s": 46, "g": 54},
    {"name": "TotalEnergies", "ticker": "TTE", "sector": "Fossil Fuels / Energy", "mu": 0.088, "sigma": 0.235, "e": 42, "s": 52, "g": 58},
    {"name": "Equinor", "ticker": "EQNR", "sector": "Fossil Fuels / Energy", "mu": 0.085, "sigma": 0.250, "e": 48, "s": 54, "g": 60},
    {"name": "ConocoPhillips", "ticker": "COP", "sector": "Fossil Fuels / Energy", "mu": 0.112, "sigma": 0.270, "e": 30, "s": 44, "g": 52},
    {"name": "Schlumberger (SLB)", "ticker": "SLB", "sector": "Fossil Fuels / Energy", "mu": 0.092, "sigma": 0.285, "e": 36, "s": 48, "g": 54},
    {"name": "Repsol", "ticker": "REPYY", "sector": "Fossil Fuels / Energy", "mu": 0.080, "sigma": 0.238, "e": 44, "s": 50, "g": 56},
    {"name": "Eni", "ticker": "E", "sector": "Fossil Fuels / Energy", "mu": 0.082, "sigma": 0.240, "e": 42, "s": 50, "g": 54},

    {"name": "British American Tobacco", "ticker": "BTI", "sector": "Tobacco", "mu": 0.055, "sigma": 0.175, "e": 28, "s": 32, "g": 55},
    {"name": "Philip Morris", "ticker": "PM", "sector": "Tobacco", "mu": 0.068, "sigma": 0.182, "e": 30, "s": 35, "g": 58},
    {"name": "Altria", "ticker": "MO", "sector": "Tobacco", "mu": 0.052, "sigma": 0.190, "e": 25, "s": 30, "g": 52},
    {"name": "Imperial Brands", "ticker": "IMBBY", "sector": "Tobacco", "mu": 0.060, "sigma": 0.185, "e": 26, "s": 32, "g": 54},
    {"name": "Japan Tobacco", "ticker": "JAPAY", "sector": "Tobacco", "mu": 0.058, "sigma": 0.178, "e": 28, "s": 34, "g": 56},

    {"name": "Diageo", "ticker": "DEO", "sector": "Alcohol", "mu": 0.068, "sigma": 0.170, "e": 65, "s": 60, "g": 70},
    {"name": "AB InBev", "ticker": "BUD", "sector": "Alcohol", "mu": 0.058, "sigma": 0.210, "e": 60, "s": 55, "g": 62},
    {"name": "Heineken", "ticker": "HEINY", "sector": "Alcohol", "mu": 0.062, "sigma": 0.195, "e": 64, "s": 58, "g": 65},
    {"name": "Pernod Ricard", "ticker": "PDRDY", "sector": "Alcohol", "mu": 0.072, "sigma": 0.190, "e": 66, "s": 62, "g": 68},
    {"name": "Remy Cointreau", "ticker": "REMYY", "sector": "Alcohol", "mu": 0.065, "sigma": 0.220, "e": 68, "s": 60, "g": 66},

    {"name": "Flutter Entertainment", "ticker": "FLTR.L", "sector": "Gambling", "mu": 0.078, "sigma": 0.290, "e": 40, "s": 45, "g": 58},
    {"name": "Evolution AB", "ticker": "EVVTY", "sector": "Gambling", "mu": 0.145, "sigma": 0.350, "e": 38, "s": 42, "g": 60},
    {"name": "Entain", "ticker": "GMVHF", "sector": "Gambling", "mu": 0.065, "sigma": 0.310, "e": 44, "s": 48, "g": 60},
    {"name": "MGM Resorts", "ticker": "MGM", "sector": "Gambling", "mu": 0.088, "sigma": 0.390, "e": 42, "s": 50, "g": 55},
    {"name": "Las Vegas Sands", "ticker": "LVS", "sector": "Gambling", "mu": 0.075, "sigma": 0.380, "e": 38, "s": 48, "g": 54},

    {"name": "BAE Systems", "ticker": "BAESY", "sector": "Weapons / Defence", "mu": 0.120, "sigma": 0.230, "e": 35, "s": 55, "g": 62},
    {"name": "Lockheed Martin", "ticker": "LMT", "sector": "Weapons / Defence", "mu": 0.108, "sigma": 0.195, "e": 32, "s": 52, "g": 60},
    {"name": "Raytheon Technologies", "ticker": "RTX", "sector": "Weapons / Defence", "mu": 0.105, "sigma": 0.205, "e": 34, "s": 54, "g": 62},
    {"name": "Northrop Grumman", "ticker": "NOC", "sector": "Weapons / Defence", "mu": 0.115, "sigma": 0.198, "e": 33, "s": 53, "g": 61},
    {"name": "General Dynamics", "ticker": "GD", "sector": "Weapons / Defence", "mu": 0.110, "sigma": 0.192, "e": 34, "s": 52, "g": 60},
    {"name": "Rheinmetall", "ticker": "RNMBY", "sector": "Weapons / Defence", "mu": 0.225, "sigma": 0.320, "e": 32, "s": 50, "g": 58},
    {"name": "Leonardo", "ticker": "FINMY", "sector": "Weapons / Defence", "mu": 0.098, "sigma": 0.245, "e": 35, "s": 54, "g": 60},
    {"name": "Thales", "ticker": "THLLY", "sector": "Weapons / Defence", "mu": 0.105, "sigma": 0.235, "e": 38, "s": 56, "g": 62},
]

CURATED_BY_TICKER = {asset["ticker"]: asset for asset in CURATED_ASSETS}
CURATED_NAMES = [f'{asset["name"]} ({asset["ticker"]})' for asset in CURATED_ASSETS]


def build_curated_asset_profile(asset: dict, e_w: int, s_w: int, g_w: int) -> dict:
    esg_composite = composite_esg(asset["e"], asset["s"], asset["g"], e_w, s_w, g_w) / 100
    return {**asset, "esg_c": esg_composite, "esg_a": esg_composite}


def recommend_guided_asset_pair(
    e_w: int,
    s_w: int,
    g_w: int,
    gamma: float,
    lam: float,
    excluded_sectors: set,
    rf: float = 0.045,
    rho: float = 0.30,
    shortlist_size: int = 18,
    per_sector_limit: int = 2,
):
    eligible_assets = []
    for asset in CURATED_ASSETS:
        if asset["sector"] in excluded_sectors:
            continue
        profiled_asset = build_curated_asset_profile(asset, e_w, s_w, g_w)
        profiled_asset["_guided_score"] = p_util(
            profiled_asset["mu"] - rf,
            profiled_asset["sigma"] ** 2,
            profiled_asset["esg_a"],
            gamma,
            lam,
        )
        eligible_assets.append(profiled_asset)

    if len(eligible_assets) < 2:
        return None

    ranked_assets = sorted(eligible_assets, key=lambda item: item["_guided_score"], reverse=True)
    shortlist = []
    sector_counts = {}
    for asset in ranked_assets:
        sector_total = sector_counts.get(asset["sector"], 0)
        if sector_total >= per_sector_limit:
            continue
        shortlist.append(asset)
        sector_counts[asset["sector"]] = sector_total + 1

    for asset in ranked_assets:
        if len(shortlist) >= shortlist_size:
            break
        if any(existing["ticker"] == asset["ticker"] for existing in shortlist):
            continue
        shortlist.append(asset)

    if len(shortlist) < 2:
        shortlist = ranked_assets[: min(shortlist_size, len(ranked_assets))]

    best_pair = None
    for first_idx, first_asset in enumerate(shortlist[:-1]):
        for second_asset in shortlist[first_idx + 1:]:
            _, x1_grid, x2_grid, _, total_return_grid, sigma_grid, esg_grid, objective_grid, _, idx = optimise(
                first_asset["mu"],
                second_asset["mu"],
                first_asset["sigma"],
                second_asset["sigma"],
                first_asset["esg_a"],
                second_asset["esg_a"],
                rho,
                rf,
                gamma,
                lam,
                n=600,
            )
            objective_value = float(objective_grid[idx])
            if not np.isfinite(objective_value):
                continue

            ranking = (
                objective_value,
                float(total_return_grid[idx]),
                float(esg_grid[idx]),
                -float(sigma_grid[idx]),
            )
            x1 = float(x1_grid[idx])
            x2 = float(x2_grid[idx])
            primary_asset = first_asset
            secondary_asset = second_asset
            primary_weight = x1
            secondary_weight = x2
            if x2 > x1:
                primary_asset, secondary_asset = second_asset, first_asset
                primary_weight, secondary_weight = x2, x1

            if best_pair is None or ranking > best_pair["ranking"]:
                best_pair = {
                    "asset1": primary_asset,
                    "asset2": secondary_asset,
                    "w1": primary_weight,
                    "w2": secondary_weight,
                    "ranking": ranking,
                }

    return best_pair


def image_to_data_uri(path: Path, make_transparent=False) -> str:
    if not path.exists():
        return ""
    if make_transparent:
        image = Image.open(path).convert("RGBA")
        pixels = np.array(image)
        whiteish = (
            (pixels[:, :, 0] > 240)
            & (pixels[:, :, 1] > 240)
            & (pixels[:, :, 2] > 240)
        )
        pixels[:, :, 3] = np.where(whiteish, 0, pixels[:, :, 3])
        cleaned = Image.fromarray(pixels)
        buffer = BytesIO()
        cleaned.save(buffer, format="PNG")
        encoded = b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    encoded = b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


LOGO_DATA_URI = image_to_data_uri(LOGO_PATH, make_transparent=True)
QUESTION_DATA_URI = image_to_data_uri(QUESTION_PATH, make_transparent=True)


def get_query_param(key: str):
    try:
        value = st.query_params.get(key)
        if isinstance(value, list):
            return value[0] if value else None
        return value
    except Exception:
        return st.experimental_get_query_params().get(key, [None])[0]


def clear_query_params():
    try:
        st.query_params.clear()
    except Exception:
        st.experimental_set_query_params()


def reset_home_state():
    reset_prefixes = (
        "manual_",
        "curated_",
        "search_",
        "ticker_input_",
        "radio_mode_",
        "_g_",
        "_l_",
    )
    legacy_keys = {
        "name1", "name2",
        "sector1", "sector2",
        "mu1", "mu2",
        "sigma1", "sigma2",
        "e1", "e2",
        "s1", "s2",
        "g1", "g2",
    }
    for key in list(st.session_state.keys()):
        if key.startswith(reset_prefixes) or key in legacy_keys:
            del st.session_state[key]

    st.session_state.entered_app = False
    st.session_state.show_profile_builder = False
    st.session_state.setup_mode = None
    st.session_state.onboarding_done = False
    st.session_state.onboarding_step = 1
    st.session_state.q1 = 3
    st.session_state.q2 = 3
    st.session_state.q3 = 3
    st.session_state.goal = 2
    st.session_state.e_w = 3
    st.session_state.s_w = 3
    st.session_state.g_w = 3
    st.session_state.excl_tobacco = False
    st.session_state.excl_weapons = False
    st.session_state.excl_gambling = False
    st.session_state.excl_fossil = False
    st.session_state.excl_alcohol = False
    st.session_state.gamma = 4.0
    st.session_state.gamma_val = 4.0
    st.session_state.lambda_esg = 0.06
    st.session_state.lambda_val = 0.06
    st.session_state.profile = "Balanced"
    st.session_state.goal_label = "Long-term growth"
    st.session_state.asset1_mode = "curated"
    st.session_state.asset2_mode = "curated"
    st.session_state.asset1_ticker = "AAPL"
    st.session_state.asset2_ticker = "MSFT"
    st.session_state.generated_signature = None
    st.session_state.loader_context = "launch"
    clear_query_params()


def go_home():
    reset_home_state()
    st.session_state.show_loader = True
    st.rerun()


@st.cache_data(ttl=300, show_spinner=False)
def fetch_live_asset(ticker: str):
    try:
        import yfinance as yf

        instrument = yf.Ticker(ticker.upper())
        info = instrument.info or {}

        history = instrument.history(period="5y", interval="1mo")
        if history.empty or len(history) < 12:
            return None

        monthly_returns = history["Close"].pct_change().dropna()
        mu = float(monthly_returns.mean() * 12)
        sigma = float(monthly_returns.std() * np.sqrt(12))

        sustainability = instrument.sustainability
        e_score = 50.0
        s_score = 50.0
        g_score = 50.0
        if sustainability is not None and not sustainability.empty:
            def get_score(key, default=50.0):
                try:
                    value = sustainability.loc[key].values[0] if key in sustainability.index else default
                    return float(value) * 10 if float(value) <= 10 else float(value)
                except Exception:
                    return default

            e_score = get_score("environmentScore")
            s_score = get_score("socialScore")
            g_score = get_score("governanceScore")

        return {
            "name": info.get("shortName") or info.get("longName") or ticker.upper(),
            "ticker": ticker.upper(),
            "sector": map_sector(info.get("sector", "")),
            "mu": round(mu, 4),
            "sigma": round(sigma, 4),
            "e": round(e_score, 1),
            "s": round(s_score, 1),
            "g": round(g_score, 1),
            "_live": True,
            "_price": info.get("regularMarketPrice") or info.get("currentPrice"),
        }
    except Exception:
        return None


def map_sector(raw_sector: str) -> str:
    mapping = {
        "Technology": "Technology",
        "Consumer Cyclical": "Consumer Goods",
        "Consumer Defensive": "Consumer Goods",
        "Healthcare": "Healthcare",
        "Financial Services": "Financial Services",
        "Industrials": "Industrials",
        "Energy": "Fossil Fuels / Energy",
        "Real Estate": "Real Estate",
        "Communication Services": "Technology",
        "Basic Materials": "Industrials",
        "Utilities": "Clean Energy",
    }
    return mapping.get(raw_sector, "Technology")


def resolve_asset(ticker: str):
    live_asset = fetch_live_asset(ticker)
    if live_asset:
        return live_asset

    curated_asset = CURATED_BY_TICKER.get(ticker.upper())
    if curated_asset:
        return dict(curated_asset, _live=False)
    return None


def inject_styles():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap');

            :root {
                --green-900: #163a2a;
                --green-700: #246847;
                --green-600: #2e7b53;
                --green-500: #46a469;
                --green-200: #d8ecde;
                --green-100: #edf7f0;
                --blue-600: #2f7dca;
                --blue-500: #54a8e8;
                --blue-100: #edf5fc;
                --ink-900: #183427;
                --ink-700: #406854;
                --ink-500: #6a8a77;
                --card: rgba(255, 255, 255, 0.88);
                --border: rgba(46, 123, 83, 0.16);
                --shadow: 0 24px 60px rgba(26, 68, 47, 0.10);
            }

            .stApp,
            [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(circle at top left, rgba(94, 174, 119, 0.16), transparent 28%),
                    radial-gradient(circle at top right, rgba(76, 164, 224, 0.14), transparent 24%),
                    linear-gradient(180deg, #f4fbf6 0%, #edf7f1 34%, #f7fbf8 100%);
                color: var(--ink-900);
                font-family: "Manrope", "Trebuchet MS", sans-serif;
            }

            .block-container {
                padding-top: 1.1rem;
                padding-bottom: 4.5rem;
                max-width: 1220px;
            }

            h1, h2, h3, h4, h5 {
                font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
                color: var(--green-900);
                letter-spacing: -0.02em;
            }

            p, li, label, [data-testid="stMarkdownContainer"] {
                color: var(--ink-700);
            }

            .loader-overlay {
                position: fixed;
                inset: 0;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 0.95rem;
                background:
                    radial-gradient(circle at center, rgba(132, 213, 154, 0.42), transparent 35%),
                    linear-gradient(180deg, #f7fcf8 0%, #eff7f1 100%);
                animation: loader-fade 3.4s ease forwards;
            }

            .loader-logo {
                width: 118px;
                height: 118px;
                object-fit: contain;
                filter: drop-shadow(0 16px 26px rgba(27, 92, 57, 0.16));
                animation: loader-float 1.2s ease-in-out infinite alternate;
            }

            .loader-kicker {
                font-size: 0.82rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.16em;
                color: var(--green-700);
            }

            .loader-title {
                font-family: "Space Grotesk", "Trebuchet MS", sans-serif;
                font-size: 2.3rem;
                font-weight: 700;
                color: var(--green-900);
            }

            .loader-copy {
                font-size: 0.98rem;
                font-weight: 600;
                color: var(--ink-700);
                letter-spacing: 0.02em;
            }

            @keyframes loader-fade {
                0%, 74% { opacity: 1; visibility: visible; }
                100% { opacity: 0; visibility: hidden; pointer-events: none; }
            }

            @keyframes loader-float {
                from { transform: translateY(-4px) scale(1); }
                to { transform: translateY(4px) scale(1.04); }
            }

            .hero-shell,
            .glass-card,
            .review-shell,
            .dashboard-hero,
            .spotlight-card,
            .profile-banner {
                background: var(--card);
                backdrop-filter: blur(10px);
                border: 1px solid var(--border);
                box-shadow: var(--shadow);
                border-radius: 28px;
            }

            .hero-shell {
                padding: 2.4rem 2.5rem;
                overflow: hidden;
                position: relative;
                margin-bottom: 1.4rem;
            }

            .hero-shell::before {
                content: "";
                position: absolute;
                inset: 0 auto auto 0;
                width: 100%;
                height: 10px;
                background: linear-gradient(90deg, var(--green-700), var(--blue-500));
            }

            .hero-grid {
                display: grid;
                grid-template-columns: 1.3fr 0.9fr;
                gap: 1.2rem;
                align-items: center;
            }

            .hero-main {
                display: flex;
                flex-direction: column;
                justify-content: center;
                min-height: 100%;
                padding: 0.35rem 0 0.2rem;
                width: 100%;
                max-width: 820px;
                margin: 0 auto;
            }

            .hero-brand-row {
                display: flex;
                gap: 1.05rem;
                align-items: center;
                margin: 0.15rem 0 1rem;
            }

            .hero-brand-copy {
                display: flex;
                flex-direction: column;
                justify-content: center;
            }

            .hero-logo {
                width: 76px;
                height: 76px;
                object-fit: contain;
                filter: drop-shadow(0 10px 20px rgba(31, 88, 58, 0.16));
                flex-shrink: 0;
                transform: translateY(2px);
            }

            .hero-kicker,
            .section-kicker {
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                font-size: 0.74rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.12em;
                color: var(--green-700);
            }

            .hero-kicker::before,
            .section-kicker::before {
                content: "";
                width: 12px;
                height: 12px;
                border-radius: 999px;
                background: linear-gradient(135deg, var(--green-500), var(--blue-500));
            }

            .hero-title {
                font-family: "Manrope", "Trebuchet MS", sans-serif;
                font-size: clamp(4.1rem, 6.6vw, 5.8rem);
                font-weight: 800;
                letter-spacing: -0.035em;
                margin: 0;
                line-height: 0.94;
            }

            .hero-brand-row .hero-title {
                margin: 0;
            }

            .hero-copy {
                font-size: 1.05rem;
                line-height: 1.7;
                max-width: 38ch;
                margin: 0 0 1.15rem;
            }

            .hero-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 1.1rem;
                margin-bottom: 0.95rem;
            }

            .hero-action-form {
                margin: 0;
                flex: 1 1 290px;
            }

            .hero-button {
                appearance: none;
                text-decoration: none !important;
                color: #ffffff !important;
                font-weight: 800;
                letter-spacing: 0.01em;
                padding: 1.12rem 1.85rem;
                border-radius: 20px;
                min-width: 290px;
                text-align: center;
                box-shadow: 0 20px 30px rgba(37, 100, 68, 0.16);
                border: 1px solid rgba(255, 255, 255, 0.46);
                cursor: pointer;
                font-family: "Manrope", "Trebuchet MS", sans-serif;
                font-size: 1.14rem;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.28);
                width: 100%;
            }

            .hero-button.green {
                background: linear-gradient(135deg, #1f633d 0%, #43a364 100%);
            }

            .hero-button.blue {
                background: linear-gradient(135deg, #225ea9 0%, #4c9ddb 100%);
            }

            .hero-button:hover {
                transform: translateY(-1px);
            }

            .hero-note {
                font-size: 0.92rem;
                color: var(--ink-500);
                font-weight: 600;
                max-width: 52ch;
                margin-top: 1.2rem;
                line-height: 1.65;
            }

            .hero-panel {
                background: linear-gradient(180deg, rgba(235, 247, 238, 0.9), rgba(238, 246, 252, 0.92));
                border-radius: 24px;
                border: 1px solid rgba(46, 123, 83, 0.12);
                padding: 1.4rem;
                position: relative;
                overflow: hidden;
                min-height: 100%;
            }

            .hero-panel h4 {
                margin: 0 0 0.55rem;
                font-size: 1.12rem;
            }

            .hero-panel-copy {
                max-width: 100%;
            }

            .hero-points {
                display: grid;
                gap: 0.75rem;
                margin-top: 1rem;
            }

            .hero-point {
                background: rgba(255, 255, 255, 0.76);
                border: 1px solid rgba(46, 123, 83, 0.11);
                border-radius: 18px;
                padding: 0.9rem 1rem;
            }

            .hero-point strong {
                display: block;
                color: var(--green-900);
                margin-bottom: 0.2rem;
            }

            .fact-grid {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 1rem;
                margin: 1.35rem 0 1.1rem;
            }

            .fact-card {
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid rgba(46, 123, 83, 0.12);
                border-radius: 22px;
                padding: 1.15rem 1.2rem;
                min-height: 170px;
            }

            .fact-card h4 {
                margin: 0 0 0.6rem;
                font-size: 1.08rem;
            }

            .fact-card p {
                margin: 0;
                line-height: 1.75;
                font-size: 0.98rem;
            }

            .review-shell {
                padding: 1.4rem 1.55rem 1.6rem;
                overflow: hidden;
                position: relative;
                margin-top: 1.1rem;
            }

            .review-intro {
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                align-items: end;
                margin-bottom: 1rem;
            }

            .review-intro h3 {
                margin: 0.2rem 0 0;
                font-size: 1.7rem;
            }

            .review-rail {
                overflow: hidden;
                mask-image: linear-gradient(to right, transparent, black 12%, black 88%, transparent);
                -webkit-mask-image: linear-gradient(to right, transparent, black 12%, black 88%, transparent);
            }

            .review-track {
                display: flex;
                gap: 1rem;
                width: max-content;
                animation: reviews-left-to-right 30s linear infinite;
            }

            .review-card {
                width: 320px;
                min-height: 190px;
                padding: 1.15rem 1.2rem;
                border-radius: 22px;
                border: 1px solid rgba(46, 123, 83, 0.12);
                background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(240,248,243,0.94));
                box-shadow: 0 18px 28px rgba(24, 60, 43, 0.08);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }

            .review-stars {
                color: #f3b31d;
                letter-spacing: 0.08em;
                font-size: 0.9rem;
                margin-bottom: 0.65rem;
            }

            .review-card p {
                color: var(--ink-700);
                line-height: 1.68;
                font-size: 0.95rem;
                margin: 0 0 0.9rem;
            }

            .reviewer {
                font-weight: 800;
                color: var(--green-900);
                font-size: 0.95rem;
            }

            @keyframes reviews-left-to-right {
                0% { transform: translateX(-52%); }
                100% { transform: translateX(0); }
            }

            .dashboard-hero {
                padding: 1.75rem 1.85rem;
                margin-bottom: 1.35rem;
            }

            .dashboard-head {
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                align-items: start;
                flex-wrap: wrap;
            }

            .dashboard-title {
                font-size: 2.2rem;
                margin: 0;
            }

            .dashboard-copy {
                max-width: 58ch;
                line-height: 1.75;
                margin: 0;
                color: var(--ink-700);
            }

            .chip-row {
                display: flex;
                gap: 0.6rem;
                flex-wrap: wrap;
                margin-top: 1rem;
            }

            .chip {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.52rem 0.82rem;
                border-radius: 999px;
                font-size: 0.84rem;
                font-weight: 700;
                border: 1px solid rgba(46, 123, 83, 0.14);
                background: rgba(255, 255, 255, 0.85);
                color: var(--green-900);
            }

            .chip.blue {
                border-color: rgba(47, 125, 202, 0.18);
                color: #235f9b;
                background: rgba(240, 247, 255, 0.95);
            }

            .profile-banner {
                padding: 1.35rem 1.45rem;
                margin: 0 0 1rem;
                background: linear-gradient(180deg, rgba(241, 248, 244, 0.98), rgba(234, 244, 252, 0.96));
            }

            .guide-mascot-card {
                background: linear-gradient(180deg, rgba(241, 248, 244, 0.98), rgba(234, 244, 252, 0.96));
                border: 1px solid rgba(46, 123, 83, 0.12);
                border-radius: 24px;
                padding: 1rem 0.95rem 0.95rem;
                box-shadow: 0 16px 28px rgba(24, 60, 43, 0.06);
            }

            .guide-mascot-card h4 {
                margin: 0.25rem 0 0.45rem;
                font-size: 1.2rem;
            }

            .guide-mascot-card p {
                margin: 0;
                line-height: 1.72;
                font-size: 0.95rem;
            }

            .guide-mascot-image {
                display: block;
                width: min(176px, 100%);
                margin: 0.8rem auto 0;
                filter: drop-shadow(0 12px 22px rgba(24, 60, 43, 0.12));
            }

            .spotlight-card {
                padding: 1.45rem 1.4rem;
                margin-bottom: 1rem;
                background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(237,247,241,0.92));
            }

            .spotlight-card h3 {
                margin: 0.3rem 0 0.55rem;
                font-size: 1.45rem;
            }

            .spotlight-card p {
                margin: 0;
                line-height: 1.74;
            }

            .asset-card {
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid rgba(46, 123, 83, 0.14);
                border-radius: 22px;
                padding: 1.1rem 1.15rem 0.85rem;
                margin-bottom: 0.5rem;
                box-shadow: 0 12px 24px rgba(24, 60, 43, 0.06);
            }

            .asset-card-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 0.65rem;
                margin-bottom: 0.35rem;
            }

            .asset-card-name {
                font-weight: 800;
                font-size: 1.12rem;
                color: var(--green-900);
            }

            .asset-card-badges {
                display: flex;
                gap: 0.4rem;
                align-items: center;
                flex-wrap: wrap;
                justify-content: flex-end;
            }

            .asset-card-ticker,
            .asset-card-live,
            .asset-card-static {
                font-size: 0.78rem;
                font-weight: 700;
                border-radius: 999px;
                padding: 0.2rem 0.6rem;
            }

            .asset-card-ticker {
                color: var(--ink-500);
                background: rgba(46, 123, 83, 0.08);
            }

            .asset-card-live {
                color: #1b6e42;
                background: rgba(70, 164, 105, 0.12);
            }

            .asset-card-static {
                color: #5b7a8c;
                background: rgba(47, 125, 202, 0.10);
            }

            .asset-card-meta {
                font-size: 0.88rem;
                color: var(--ink-500);
                margin-bottom: 0.6rem;
            }

            .asset-pill-row {
                display: flex;
                gap: 0.4rem;
                flex-wrap: wrap;
                margin-top: 0.45rem;
            }

            .asset-pill {
                font-size: 0.78rem;
                font-weight: 700;
                border-radius: 999px;
                padding: 0.18rem 0.55rem;
                border: 1px solid rgba(46, 123, 83, 0.12);
                background: rgba(237, 247, 241, 0.85);
                color: var(--green-700);
            }

            .esg-bar-wrap {
                margin-top: 0.7rem;
            }

            .esg-bar-label {
                display: flex;
                justify-content: space-between;
                gap: 1rem;
                font-size: 0.8rem;
                color: var(--ink-500);
                margin-bottom: 0.2rem;
            }

            .esg-bar-track {
                height: 7px;
                border-radius: 999px;
                background: rgba(46, 123, 83, 0.10);
                overflow: hidden;
            }

            .esg-bar-fill {
                height: 100%;
                border-radius: 999px;
                background: linear-gradient(90deg, #2e7b53, #54c87a);
            }

            div[data-testid="metric-container"] {
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid rgba(46, 123, 83, 0.12);
                border-radius: 18px;
                padding: 1rem 1.05rem;
                box-shadow: 0 12px 24px rgba(24, 60, 43, 0.06);
            }

            [data-testid="metric-container"] label {
                color: var(--ink-500);
            }

            .section-title {
                margin: 0.35rem 0 0.7rem;
                font-size: 1.75rem;
            }

            .section-copy {
                margin: 0;
                line-height: 1.72;
                color: var(--ink-700);
            }

            .stButton > button {
                width: 100%;
                border-radius: 16px;
                border: 1px solid rgba(46, 123, 83, 0.12);
                background: linear-gradient(135deg, #469f6b, #78c995);
                color: #ffffff !important;
                font-weight: 800;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.18);
                padding: 0.7rem 1rem;
                box-shadow: 0 14px 22px rgba(37, 100, 68, 0.12);
            }

            .stButton > button:hover {
                color: #ffffff !important;
                background: linear-gradient(135deg, #53ad78, #88d2a2) !important;
                border-color: rgba(46, 123, 83, 0.16);
            }

            .output-launch {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                border-radius: 16px;
                border: 1px solid rgba(46, 123, 83, 0.12);
                background: linear-gradient(135deg, #469f6b, #78c995);
                color: #ffffff !important;
                font-weight: 800;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.18);
                padding: 0.78rem 1rem;
                box-shadow: 0 14px 22px rgba(37, 100, 68, 0.12);
                text-decoration: none !important;
                text-align: center;
                transition: transform 0.14s ease, opacity 0.14s ease, background 0.14s ease;
            }

            .output-launch:hover {
                color: #ffffff !important;
                background: linear-gradient(135deg, #53ad78, #88d2a2);
                transform: translateY(-1px);
            }

            .output-launch.disabled {
                opacity: 0.55;
                pointer-events: none;
            }

            .results-note {
                font-size: 0.9rem;
                color: var(--ink-500);
                margin-top: 0.55rem;
                line-height: 1.6;
            }

            .info-note {
                padding: 1rem 1.05rem;
                border-radius: 18px;
                background: rgba(236, 247, 240, 0.92);
                border: 1px solid rgba(46, 123, 83, 0.12);
                line-height: 1.7;
                margin: 0.8rem 0 0.3rem;
            }

            .stExpander {
                border: 1px solid rgba(46, 123, 83, 0.12) !important;
                border-radius: 18px !important;
                background: rgba(255, 255, 255, 0.88) !important;
            }

            .stExpander details summary p {
                font-weight: 700;
                color: var(--green-900);
            }

            div[data-baseweb="select"] > div,
            div[data-baseweb="input"] > div,
            textarea,
            input {
                border-radius: 14px !important;
            }

            .stSlider [data-baseweb="slider"] {
                padding-top: 0.4rem;
                padding-bottom: 0.1rem;
            }

            [data-testid="stDataFrame"] {
                border: 1px solid rgba(46, 123, 83, 0.12);
                border-radius: 18px;
                overflow: hidden;
                box-shadow: 0 12px 24px rgba(24, 60, 43, 0.06);
            }

            .chart-card {
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid rgba(46, 123, 83, 0.12);
                border-radius: 24px;
                padding: 1rem 1rem 0.2rem;
                box-shadow: 0 20px 35px rgba(24, 60, 43, 0.07);
            }

            .chart-caption {
                font-size: 0.92rem;
                color: var(--ink-500);
                margin-top: -0.4rem;
                margin-bottom: 0.8rem;
            }

            .projection-card {
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid rgba(46, 123, 83, 0.12);
                border-radius: 22px;
                padding: 0.75rem 0.95rem 0.85rem;
                box-shadow: 0 14px 24px rgba(24, 60, 43, 0.06);
                margin-top: 0.9rem;
            }

            .projection-card h4 {
                font-size: 0.92rem;
                margin: 0.08rem 0 0.28rem;
            }

            .projection-copy {
                font-size: 0.88rem;
                color: var(--ink-500);
                margin: 0 0 0.55rem;
            }

            .dashboard-utility {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                margin: 0.15rem 0 1rem;
            }

            .dashboard-home-link {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 64px;
                height: 64px;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(46, 123, 83, 0.12);
                box-shadow: 0 12px 24px rgba(24, 60, 43, 0.08);
            }

            .dashboard-home-link img {
                width: 40px;
                height: 40px;
                object-fit: contain;
            }

            div[data-testid="stDialog"] [role="dialog"] {
                background: linear-gradient(180deg, rgba(241, 248, 244, 0.98), rgba(234, 244, 252, 0.98));
                border: 1px solid rgba(46, 123, 83, 0.12);
                border-radius: 28px;
                box-shadow: 0 24px 60px rgba(26, 68, 47, 0.16);
            }

            div[data-testid="stDialog"] .block-container {
                padding-top: 0.85rem;
                padding-bottom: 1.1rem;
            }

            div[data-testid="stDialog"] [data-testid="stRadio"] label p,
            div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] p,
            div[data-testid="stDialog"] label,
            div[data-testid="stDialog"] .stCaptionContainer {
                color: var(--ink-700);
            }

            .profile-step-card {
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(46, 123, 83, 0.1);
                border-radius: 22px;
                padding: 1rem 1.05rem;
                margin-bottom: 0.85rem;
            }

            .profile-question-title {
                font-size: 1.42rem;
                font-weight: 800;
                color: var(--green-900);
                line-height: 1.28;
                margin: 0 0 0.35rem;
            }

            .mascot-answer {
                margin-top: 0.75rem;
                padding: 0.7rem 0.8rem;
                border-radius: 16px;
                background: rgba(255, 255, 255, 0.72);
                border: 1px solid rgba(46, 123, 83, 0.1);
                color: var(--ink-700);
                line-height: 1.6;
            }

            @media (max-width: 980px) {
                .hero-grid {
                    grid-template-columns: 1fr;
                }

                .fact-grid {
                    grid-template-columns: 1fr;
                }

                .hero-button {
                    width: 100%;
                    min-width: 0;
                }

                .hero-panel-copy {
                    max-width: 100%;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <style>
            .hero-kicker::before,
            .section-kicker::before {{
                width: 25px;
                height: 25px;
                border-radius: 0;
                background: url("{LOGO_DATA_URI}") center / contain no-repeat;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_loader():
    loader_context = st.session_state.get("loader_context", "launch")
    if loader_context == "home":
        kicker_html = '<div class="loader-kicker">Back to investing?</div>'
        title = "GreenVest"
        copy = "Returning you to the home page"
    elif loader_context == "launch":
        kicker_html = '<div class="loader-kicker">Welcome to GreenVest</div>'
        title = "GreenVest"
        copy = "Loading your sustainable investing workspace"
    else:
        kicker_html = ""
        title = "GreenVest"
        copy = "Preparing your investing workspace"

    st.markdown(
        f"""
        <div class="loader-overlay">
            <img class="loader-logo" src="{LOGO_DATA_URI}" alt="GreenVest logo">
            {kicker_html}
            <div class="loader-title">{title}</div>
            <div class="loader-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def p_return(w1, mu1, mu2):
    return w1 * mu1 + (1 - w1) * mu2


def p_variance(w1, s1, s2, rho):
    return w1**2 * s1**2 + (1 - w1) ** 2 * s2**2 + 2 * rho * w1 * (1 - w1) * s1 * s2


def p_std(w1, s1, s2, rho):
    return np.sqrt(p_variance(w1, s1, s2, rho))


def p_esg(w1, e1, e2):
    return w1 * e1 + (1 - w1) * e2


def p_util(excess_return, variance, esg, gamma, lam):
    return excess_return - (gamma / 2) * variance + lam * esg


def composite_esg(e, s, g, we, ws, wg):
    total_weight = we + ws + wg
    return (we * e + ws * s + wg * g) / total_weight if total_weight > 0 else 0


def esg_rating(score):
    for thresh, rating in [
        (0.85, "AAA"),
        (0.70, "AA"),
        (0.55, "A"),
        (0.40, "BBB"),
        (0.25, "BB"),
        (0.10, "B"),
    ]:
        if score >= thresh:
            return rating
    return "CCC"


def esg_sharpe(mu, rf, sig, lam, esg):
    return (mu - rf + lam * esg) / sig if sig > 0 else float("nan")


def future_value(pv, r, years):
    return pv * (1 + r) ** years


def optimal_risky_share(excess_return, variance, gamma):
    if variance <= 0 or gamma <= 0:
        return 0.0
    return max(excess_return / (gamma * variance), 0.0)


def optimise(mu1, mu2, s1, s2, e1, e2, rho, rf, gamma, lam, n=2000, force_w1=None):
    if force_w1 is not None:
        mix_grid = np.array([force_w1], dtype=float)
    else:
        mix_grid = np.linspace(0, 1, n)

    sleeve_return_grid = p_return(mix_grid, mu1, mu2)
    sleeve_excess_grid = sleeve_return_grid - rf
    sleeve_variance_grid = p_variance(mix_grid, s1, s2, rho)
    sleeve_sigma_grid = np.sqrt(sleeve_variance_grid)
    esg_grid = p_esg(mix_grid, e1, e2)

    risky_share_grid = np.zeros_like(mix_grid, dtype=float)
    valid_variance = sleeve_variance_grid > 0
    risky_share_grid[valid_variance] = np.maximum(
        sleeve_excess_grid[valid_variance] / (gamma * sleeve_variance_grid[valid_variance]),
        0.0,
    )

    x1_grid = risky_share_grid * mix_grid
    x2_grid = risky_share_grid * (1 - mix_grid)
    sigma_grid = risky_share_grid * sleeve_sigma_grid
    excess_contribution_grid = risky_share_grid * sleeve_excess_grid
    total_return_grid = rf + excess_contribution_grid
    objective_grid = (
        excess_contribution_grid
        - (gamma / 2) * (sigma_grid ** 2)
        + np.where(risky_share_grid > 1e-10, lam * esg_grid, 0.0)
    )
    esg_adjusted_grid = total_return_grid + np.where(risky_share_grid > 1e-10, lam * esg_grid, 0.0)
    idx = int(np.argmax(objective_grid))
    return (
        mix_grid,
        x1_grid,
        x2_grid,
        risky_share_grid,
        total_return_grid,
        sigma_grid,
        esg_grid,
        objective_grid,
        esg_adjusted_grid,
        idx,
    )


def derive_lambda(e_w, s_w, g_w, excl_count, goal_lam):
    base = ((e_w + s_w + g_w) / 3 / 5) * 0.11 + 0.01
    lam = min(base + 0.005 * excl_count + goal_lam, 0.20)
    return round(lam, 3)


def style_axis(ax):
    ax.set_facecolor("#fcfffd")
    ax.set_axisbelow(True)
    ax.grid(True, color="#d6e7d9", linewidth=0.85, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_color("#cddfd2")
        spine.set_linewidth(1.0)
    ax.tick_params(colors="#406854", labelsize=10)
    ax.xaxis.label.set_color("#406854")
    ax.yaxis.label.set_color("#406854")


def build_frontier_chart(
    sigma_grid,
    esg_adjusted_grid,
    esg_grid,
    sigma_opt,
    esg_adjusted_opt,
    sigma_financial,
    esg_adjusted_financial,
    sigma_low_risk,
    esg_adjusted_low_risk,
):
    fig, ax = plt.subplots(figsize=(8.2, 5.7))
    fig.patch.set_facecolor("#fcfffd")
    style_axis(ax)

    points = np.array([sigma_grid, esg_adjusted_grid]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    collection = LineCollection(segments, cmap="YlGn", linewidth=4.2)
    collection.set_array(esg_grid)
    ax.add_collection(collection)
    ax.autoscale()

    ax.plot(
        sigma_grid,
        esg_adjusted_grid,
        color="#afcdb7",
        linestyle="--",
        linewidth=1.3,
        alpha=0.9,
        label="Traditional frontier path",
    )
    ax.scatter(
        sigma_opt,
        esg_adjusted_opt,
        s=86,
        color="#1f6844",
        edgecolors="#ffffff",
        linewidths=1.8,
        label="GreenVest optimum",
        zorder=5,
    )
    ax.scatter(
        sigma_financial,
        esg_adjusted_financial,
        s=54,
        color="#2f7dca",
        edgecolors="#e8f3fd",
        linewidths=1.1,
        label="Financial-only benchmark",
        zorder=4,
    )

    ax.annotate(
        "GreenVest recommendation",
        xy=(sigma_opt, esg_adjusted_opt),
        xytext=(16, 16),
        textcoords="offset points",
        fontsize=9.2,
        color="#173b2b",
        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="#d6e7d9", alpha=0.96),
        arrowprops=dict(arrowstyle="-", color="#4c8f68", lw=1.2),
    )
    ax.scatter(
        sigma_low_risk,
        esg_adjusted_low_risk,
        s=54,
        color="#5d9b79",
        edgecolors="#edf7f0",
        linewidths=1.1,
        label="Lowest-risk mix",
        zorder=4,
    )

    colorbar = fig.colorbar(collection, ax=ax, pad=0.02, shrink=0.88)
    colorbar.set_label("ESG score", color="#406854")
    colorbar.ax.tick_params(labelsize=9, colors="#406854")

    ax.set_title("ESG Efficient Frontier", fontsize=15, fontweight="bold", color="#163a2a", pad=14)
    ax.set_xlabel("Portfolio risk (std deviation)")
    ax.set_ylabel("Expected return + ESG tilt")
    ax.legend(
        loc="lower right",
        fontsize=8.6,
        frameon=True,
        facecolor="white",
        edgecolor="#d6e7d9",
        framealpha=0.95,
        markerscale=0.8,
        borderpad=0.55,
        labelspacing=0.55,
        handlelength=1.4,
    )
    fig.tight_layout(pad=1.4)
    return fig


def build_future_value_chart(invest, opt_return, benchmark_return=None, selected_label="GreenVest"):
    years = np.arange(0, 31)
    fig, ax = plt.subplots(figsize=(7.8, 5.7))
    fig.patch.set_facecolor("#fcfffd")
    style_axis(ax)

    opt_values = [future_value(invest, opt_return, year) for year in years]
    ax.plot(
        years,
        opt_values,
        color="#1f6844",
        linewidth=3.2,
        label=f"{selected_label} strategy",
    )
    ax.fill_between(years, opt_values, color="#d9efdf", alpha=0.4)
    ax.scatter(years[-1], opt_values[-1], color="#1f6844", s=70, edgecolors="white", linewidths=1.6, zorder=5)

    if benchmark_return is not None:
        benchmark_values = [future_value(invest, benchmark_return, year) for year in years]
        ax.plot(
            years,
            benchmark_values,
            color="#2f7dca",
            linewidth=2.4,
            linestyle="--",
            label="50 / 50 risky-sleeve reference",
        )
        ax.scatter(
            years[-1],
            benchmark_values[-1],
            color="#2f7dca",
            s=60,
            edgecolors="white",
            linewidths=1.4,
            zorder=5,
        )

    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"GBP {x:,.0f}"))
    ax.set_xlabel("Years invested")
    ax.set_ylabel("Projected portfolio value")
    ax.set_title("Future Value Projection", fontsize=15, fontweight="bold", color="#163a2a", pad=14)
    ax.annotate(
        f"GBP {opt_values[-1]:,.0f}",
        xy=(years[-1], opt_values[-1]),
        xytext=(-74, 16),
        textcoords="offset points",
        fontsize=9,
        color="#173b2b",
        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="#d6e7d9", alpha=0.96),
    )
    if benchmark_return is not None:
        ax.annotate(
            f"GBP {benchmark_values[-1]:,.0f}",
            xy=(years[-1], benchmark_values[-1]),
            xytext=(-70, -28),
            textcoords="offset points",
            fontsize=8.7,
            color="#235f9b",
            bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="#d6e7d9", alpha=0.96),
        )
    ax.legend(
        loc="upper left",
        fontsize=8.8,
        frameon=True,
        facecolor="white",
        edgecolor="#d6e7d9",
        framealpha=0.95,
        borderpad=0.55,
        labelspacing=0.55,
        handlelength=1.8,
    )
    fig.tight_layout(pad=1.4)
    return fig


def build_summary_pdf_bytes(
    asset_one,
    asset_two,
    results,
    invest,
    profile,
    goal_label,
    gamma_used,
    lambda_used,
    e_w,
    s_w,
    g_w,
    excluded_summary,
):
    buffer = BytesIO()
    years = np.arange(0, 31)
    future_values = [future_value(invest, results["mu_opt"], year) for year in years]
    benchmark_values = None
    if results["benchmark_return"] is not None:
        benchmark_values = [future_value(invest, results["benchmark_return"], year) for year in years]

    checkpoints = [5, 10, 20, 30]
    checkpoint_lines = [
        f"{year}y: GBP {future_value(invest, results['mu_opt'], year):,.0f}"
        for year in checkpoints
    ]

    with PdfPages(buffer) as pdf:
        fig = plt.figure(figsize=(11.69, 8.27))
        fig.patch.set_facecolor("#f7fbf8")
        grid = fig.add_gridspec(
            2,
            3,
            height_ratios=[0.88, 1.12],
            width_ratios=[1.05, 1.1, 1.05],
            hspace=0.28,
            wspace=0.28,
        )

        ax_header = fig.add_subplot(grid[0, :])
        ax_alloc = fig.add_subplot(grid[1, 0])
        ax_growth = fig.add_subplot(grid[1, 1])
        ax_notes = fig.add_subplot(grid[1, 2])

        ax_header.axis("off")
        ax_header.text(
            0.0,
            0.96,
            "GreenVest - One-page Portfolio Summary",
            fontsize=23,
            fontweight="bold",
            color="#163a2a",
            transform=ax_header.transAxes,
        )
        ax_header.text(
            0.0,
            0.80,
            f"Prepared on {datetime.now().strftime('%B %d, %Y')} for investor meetings and submissions.",
            fontsize=11.2,
            color="#4f7461",
            transform=ax_header.transAxes,
        )
        ax_header.text(
            0.0,
            0.56,
            (
                f"Investor profile: {profile}   |   Goal: {goal_label}   |   "
                f"gamma: {gamma_used:.1f}   |   lambda: {lambda_used:.3f}"
            ),
            fontsize=11.4,
            color="#224d38",
            transform=ax_header.transAxes,
        )
        ax_header.text(
            0.0,
            0.41,
            (
                f"Risky positions: {asset_one['name']} {results['w1'] * 100:.1f}%   |   "
                f"{asset_two['name']} {results['w2'] * 100:.1f}%   |   "
                f"Risk-free {results['rf_weight'] * 100:.1f}%"
            ),
            fontsize=13.5,
            fontweight="bold",
            color="#173b2b",
            transform=ax_header.transAxes,
        )
        ax_header.text(
            0.0,
            0.22,
            (
                f"ESG priorities: E {e_w}/5, S {s_w}/5, G {g_w}/5   |   "
                f"Excluded sectors: {excluded_summary}"
            ),
            fontsize=10.8,
            color="#4f7461",
            transform=ax_header.transAxes,
        )
        ax_header.text(
            0.0,
            0.04,
            (
                "Method note: GreenVest combines weighted E, S, and G pillar scores into one ESG score "
                "and then blends that score into the portfolio utility calculation."
            ),
            fontsize=10.4,
            color="#5b7d69",
            transform=ax_header.transAxes,
        )

        style_axis(ax_alloc)
        allocation_names = [asset_one["name"], asset_two["name"], "Risk-free"]
        allocation_values = [results["w1"] * 100, results["w2"] * 100, results["rf_weight"] * 100]
        allocation_colors = ["#2e7b53", "#2f7dca", "#9ab7a7"]
        positions = np.arange(len(allocation_names))
        ax_alloc.barh(positions, allocation_values, color=allocation_colors, height=0.45)
        ax_alloc.set_yticks(positions, allocation_names)
        lower_bound = min(-50.0, min(allocation_values) - 10)
        upper_bound = max(100.0, max(allocation_values) + 15)
        ax_alloc.set_xlim(lower_bound, upper_bound)
        ax_alloc.axvline(0, color="#cddfd2", linewidth=1.0)
        ax_alloc.set_xlabel("Position (% of wealth)")
        ax_alloc.set_title("Recommended positions", fontsize=13.5, fontweight="bold", color="#163a2a", pad=12)
        for idx, value in enumerate(allocation_values):
            x_position = value + 2 if value >= 0 else value - 18
            ax_alloc.text(x_position, idx, f"{value:.1f}%", va="center", fontsize=10.2, color="#224d38")

        style_axis(ax_growth)
        ax_growth.plot(years, future_values, color="#1f6844", linewidth=3.0, label="GreenVest strategy")
        ax_growth.fill_between(years, future_values, color="#d9efdf", alpha=0.34)
        if benchmark_values is not None:
            ax_growth.plot(
                years,
                benchmark_values,
                color="#2f7dca",
                linewidth=2.0,
                linestyle="--",
                label="50 / 50 risky-sleeve reference",
            )
        ax_growth.set_title("Future value outlook", fontsize=13.5, fontweight="bold", color="#163a2a", pad=12)
        ax_growth.set_xlabel("Years invested")
        ax_growth.set_ylabel("Projected value")
        ax_growth.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"GBP {x:,.0f}"))
        ax_growth.legend(
            loc="upper left",
            fontsize=7.8,
            frameon=True,
            facecolor="white",
            edgecolor="#d6e7d9",
            framealpha=0.96,
        )

        ax_notes.axis("off")
        ax_notes.text(0.0, 0.96, "Key portfolio facts", fontsize=14, fontweight="bold", color="#163a2a")
        note_lines = [
            f"Risk-free weight: {results['rf_weight'] * 100:.2f}%",
            f"Expected return: {results['mu_opt'] * 100:.2f}%",
            f"Portfolio risk: {results['sigma_opt'] * 100:.2f}%",
            f"Sharpe ratio: {results['sharpe_opt']:.3f}",
            f"ESG score: {results['esg_opt'] * 100:.1f} / 100 [{esg_rating(results['esg_opt'])}]",
            f"Impact score: {results['impact_score']:.1f}",
            f"Objective value: {results['utility_opt']:.4f}",
            "",
            "Projection checkpoints",
            *checkpoint_lines,
        ]
        y_pos = 0.86
        for line in note_lines:
            if line == "":
                y_pos -= 0.08
                continue
            style = dict(fontsize=10.8, color="#355843")
            if line == "Projection checkpoints":
                style = dict(fontsize=11.5, fontweight="bold", color="#163a2a")
            ax_notes.text(0.0, y_pos, line, transform=ax_notes.transAxes, **style)
            y_pos -= 0.085

        pdf.savefig(fig, facecolor=fig.get_facecolor(), bbox_inches="tight")
        plt.close(fig)

    buffer.seek(0)
    return buffer.getvalue()


def render_investor_charts_section(
    both_excluded,
    force_w1,
    results,
    a1,
    a2,
    invest,
    title,
    summary_pdf_bytes,
    checkpoint_df,
    benchmark_message_kind,
    benchmark_message_text,
):
    st.write("")
    header_cols = st.columns([1.35, 0.65], gap="large")
    with header_cols[0]:
        st.markdown(
            f"""
            <div class="section-kicker">{title}</div>
            <h3 class="section-title">{title}</h3>
            """,
            unsafe_allow_html=True,
        )
    with header_cols[1]:
        st.write("")
        st.write("")
        if summary_pdf_bytes is not None:
            st.download_button(
                "Export PDF",
                data=summary_pdf_bytes,
                file_name="greenvest-portfolio-summary.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    chart_cols = st.columns(2, gap="large")
    if both_excluded:
        with chart_cols[0]:
            st.error("Frontier chart unavailable until at least one asset falls outside the excluded sectors.")
        with chart_cols[1]:
            st.info("Future value projection will appear again once the portfolio becomes investable.")
        return

    if force_w1 is None:
        frontier_fig = build_frontier_chart(
            results["sigma_grid"],
            results["esg_adjusted_grid"],
            results["esg_grid"],
            results["sigma_opt"],
            results["esg_adjusted_grid"][results["idx"]],
            results["sigma_ms"][results["idx_financial"]],
            results["esg_adjusted_ms"][results["idx_financial"]],
            results["sigma_grid"][results["idx_low_risk"]],
            results["esg_adjusted_grid"][results["idx_low_risk"]],
        )
        with chart_cols[0]:
            st.markdown("#### ESG efficient frontier")
            st.pyplot(frontier_fig)
            plt.close(frontier_fig)
            st.markdown(
                '<div class="chart-caption">The frontier now highlights the recommendation more clearly and keeps the benchmark markers lighter.</div>',
                unsafe_allow_html=True,
            )
    else:
        with chart_cols[0]:
            st.markdown("#### ESG efficient frontier")
            st.info(
                "The ESG efficient frontier only appears when both assets remain investable. Remove the exclusion to compare mixes again."
            )

    selected_label = a1["name"] if results["w1"] >= results["w2"] else a2["name"]
    future_fig = build_future_value_chart(
        invest,
        results["mu_opt"],
        benchmark_return=results["benchmark_return"],
        selected_label=selected_label,
    )
    with chart_cols[1]:
        st.markdown("#### Future value projection")
        st.pyplot(future_fig)
        plt.close(future_fig)
        st.markdown(
            '<div class="chart-caption">Projected values use the current assumptions from the builder on this page, so investors can compare scenarios instantly.</div>',
            unsafe_allow_html=True,
        )

    if both_excluded:
        st.markdown(
            """
            <div class="projection-card">
                <div class="section-kicker">Projection</div>
                <h4>Projection checkpoints</h4>
                <p class="projection-copy">Projection values will appear here once at least one selected asset is eligible for recommendation.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="projection-card">
            <div class="section-kicker">Projection</div>
            <p class="projection-copy">{benchmark_message_text or "Projected values below reflect the current assumptions."}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(checkpoint_df, use_container_width=True, hide_index=True)


def get_excluded_sectors():
    mapping = [
        ("Tobacco", st.session_state.excl_tobacco),
        ("Weapons / Defence", st.session_state.excl_weapons),
        ("Gambling", st.session_state.excl_gambling),
        ("Fossil Fuels / Energy", st.session_state.excl_fossil),
        ("Alcohol", st.session_state.excl_alcohol),
    ]
    return {name for name, enabled in mapping if enabled}


def excluded_sector_labels():
    mapping = [
        ("Tobacco", st.session_state.excl_tobacco),
        ("Weapons", st.session_state.excl_weapons),
        ("Gambling", st.session_state.excl_gambling),
        ("Fossil Fuels", st.session_state.excl_fossil),
        ("Alcohol", st.session_state.excl_alcohol),
    ]
    labels = [name for name, enabled in mapping if enabled]
    return labels if labels else ["None"]


def sync_gamma_slider():
    st.session_state.gamma_val = st.session_state._g_sl
    st.session_state._g_ni = st.session_state._g_sl


def sync_gamma_input():
    st.session_state.gamma_val = st.session_state._g_ni
    st.session_state._g_sl = st.session_state._g_ni


def sync_lambda_slider():
    st.session_state.lambda_val = st.session_state._l_sl
    st.session_state._l_ni = st.session_state._l_sl


def sync_lambda_input():
    st.session_state.lambda_val = st.session_state._l_ni
    st.session_state._l_sl = st.session_state._l_ni


def render_asset_card_html(asset: dict) -> str:
    price_text = ""
    if asset.get("_price") is not None:
        price_text = f"  ·  Last price {asset['_price']:,.2f}"

    if asset.get("_source") == "custom":
        source_badge = '<span class="asset-card-static">Custom input</span>'
    elif asset.get("_live"):
        source_badge = '<span class="asset-card-live">Live data</span>'
    else:
        source_badge = '<span class="asset-card-static">Curated profile</span>'
    asset_ticker = asset.get("ticker") or "Custom"
    esg_composite = composite_esg(asset["e"], asset["s"], asset["g"], 1, 1, 1) / 100
    score_value = int(round(esg_composite * 100))

    pills = "".join(
        [
            f'<span class="asset-pill">E: {asset["e"]:.0f}</span>',
            f'<span class="asset-pill">S: {asset["s"]:.0f}</span>',
            f'<span class="asset-pill">G: {asset["g"]:.0f}</span>',
            f'<span class="asset-pill">Expected return: {asset["mu"] * 100:.1f}%</span>',
            f'<span class="asset-pill">Standard deviation: {asset["sigma"] * 100:.1f}%</span>',
        ]
    )

    return f"""
    <div class="asset-card">
        <div class="asset-card-header">
            <span class="asset-card-name">{asset["name"]}</span>
            <span class="asset-card-badges">
                <span class="asset-card-ticker">{asset_ticker}</span>
                {source_badge}
            </span>
        </div>
        <div class="asset-card-meta">{asset["sector"]}{price_text}</div>
        <div class="esg-bar-wrap">
            <div class="esg-bar-label">
                <span>ESG quality</span>
                <span>{score_value}/100 [{esg_rating(esg_composite)}]</span>
            </div>
            <div class="esg-bar-track">
                <div class="esg-bar-fill" style="width:{score_value}%"></div>
            </div>
        </div>
        <div class="asset-pill-row">{pills}</div>
    </div>
    """


def render_manual_asset_input(asset_num: int, excluded_sectors: set):
    e_w = st.session_state.e_w
    s_w = st.session_state.s_w
    g_w = st.session_state.g_w

    st.markdown(
        f"""
        <div class="section-kicker">Asset {asset_num}</div>
        <h4 style="margin:0.2rem 0 0.55rem;">Asset {asset_num} — enter your own assumptions</h4>
        """,
        unsafe_allow_html=True,
    )

    columns = st.columns([1.05, 1], gap="large")
    with columns[0]:
        name = st.text_input("Name", value=f"Asset {asset_num}", key=f"manual_name_{asset_num}")
        mu = st.number_input(
            "Expected return (%)",
            -100.0,
            500.0,
            8.0 if asset_num == 1 else 5.0,
            0.1,
            key=f"manual_mu_{asset_num}",
        ) / 100
        sigma = st.number_input(
            "Standard deviation (%)",
            0.01,
            500.0,
            15.0 if asset_num == 1 else 10.0,
            0.1,
            key=f"manual_sigma_{asset_num}",
        ) / 100

    with columns[1]:
        st.caption("ESG pillar scores")
        e_score = st.slider("Environmental", 0.0, 100.0, 70.0 if asset_num == 1 else 50.0, key=f"manual_e_{asset_num}")
        s_score = st.slider("Social", 0.0, 100.0, 65.0 if asset_num == 1 else 55.0, key=f"manual_s_{asset_num}")
        g_score = st.slider("Governance", 0.0, 100.0, 60.0 if asset_num == 1 else 45.0, key=f"manual_g_{asset_num}")

    asset_data = {
        "name": name,
        "ticker": "Custom",
        "sector": "Self-directed input",
        "mu": mu,
        "sigma": sigma,
        "e": e_score,
        "s": s_score,
        "g": g_score,
        "_live": False,
        "_source": "custom",
    }

    esg_composite = composite_esg(asset_data["e"], asset_data["s"], asset_data["g"], e_w, s_w, g_w) / 100
    is_excluded = asset_data["sector"] in excluded_sectors

    st.markdown(render_asset_card_html(asset_data), unsafe_allow_html=True)
    st.caption(
        f"Composite ESG used in the optimiser: {esg_composite * 100:.1f} [{esg_rating(esg_composite)}]"
    )

    if esg_composite >= 0.60 and asset_data["g"] / 100 < 0.35:
        st.warning(
            f"Greenwashing alert: {asset_data['name']} has a strong overall ESG score but weak governance."
        )

    if is_excluded:
        st.error(
            f"{asset_data['name']} sits inside an excluded sector ({asset_data['sector']}), so GreenVest will force its allocation to 0%."
        )

    return {
        **asset_data,
        "esg_c": esg_composite,
        "esg_a": esg_composite,
        "is_excluded": is_excluded,
    }


def render_asset_selector(asset_num: int, excluded_sectors: set, allowed_modes=None, filter_excluded_curated=False):
    mode_key = f"asset{asset_num}_mode"
    ticker_key = f"asset{asset_num}_ticker"
    e_w = st.session_state.e_w
    s_w = st.session_state.s_w
    g_w = st.session_state.g_w
    mode_options = allowed_modes or ["curated", "search", "custom"]

    if st.session_state[mode_key] not in mode_options:
        st.session_state[mode_key] = mode_options[0]

    st.markdown(
        f"""
        <div class="section-kicker">Asset {asset_num}</div>
        <h4 style="margin:0.2rem 0 0.55rem;">Asset {asset_num} — choose an eligible asset</h4>
        """,
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Input method",
        options=mode_options,
        format_func=lambda value: {
            "curated": "Pick from curated list",
            "search": "Search by ticker",
            "custom": "Enter manually",
        }[value],
        key=f"radio_mode_{asset_num}",
        index=mode_options.index(st.session_state[mode_key]),
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state[mode_key] = mode

    asset_data = None

    if mode == "curated":
        curated_pool = [
            asset for asset in CURATED_ASSETS
            if not filter_excluded_curated or asset["sector"] not in excluded_sectors
        ]
        if not curated_pool:
            st.error("No curated assets remain after the exclusion rules. Relax the exclusions or search a different ticker.")
            return None

        default_ticker = st.session_state[ticker_key]
        available_tickers = {asset["ticker"] for asset in curated_pool}
        if default_ticker not in available_tickers:
            default_ticker = curated_pool[0]["ticker"]
            st.session_state[ticker_key] = default_ticker

        default_idx = next(
            (idx for idx, asset in enumerate(curated_pool) if asset["ticker"] == default_ticker),
            0,
        )
        curated_names = [f'{asset["name"]} ({asset["ticker"]})' for asset in curated_pool]
        chosen_label = st.selectbox(
            "Select an asset",
            options=curated_names,
            index=default_idx,
            key=f"curated_sel_{asset_num}",
        )
        selected_asset = dict(curated_pool[curated_names.index(chosen_label)])
        st.session_state[ticker_key] = selected_asset["ticker"]
        with st.expander("Override ESG scores (optional)", expanded=False):
            st.caption("The curated values are pre-filled. Adjust them only if you have better data.")
            columns = st.columns(3)
            selected_asset["e"] = columns[0].slider(
                "Environmental",
                0.0,
                100.0,
                float(selected_asset["e"]),
                key=f"curated_e_{asset_num}",
            )
            selected_asset["s"] = columns[1].slider(
                "Social",
                0.0,
                100.0,
                float(selected_asset["s"]),
                key=f"curated_s_{asset_num}",
            )
            selected_asset["g"] = columns[2].slider(
                "Governance",
                0.0,
                100.0,
                float(selected_asset["g"]),
                key=f"curated_g_{asset_num}",
            )
        asset_data = dict(selected_asset, _live=False, _source="curated")

    elif mode == "search":
        ticker_input = st.text_input(
            "Enter ticker (for example AAPL, TSLA, NVDA)",
            value=st.session_state[ticker_key],
            key=f"ticker_input_{asset_num}",
            placeholder="Ticker symbol",
        ).strip().upper()

        if ticker_input:
            with st.spinner(f"Fetching {ticker_input}..."):
                fetched_asset = resolve_asset(ticker_input)

            if fetched_asset:
                st.session_state[ticker_key] = ticker_input
                with st.expander("Override ESG scores (optional)", expanded=False):
                    st.caption("These values come from live data when available, otherwise from the curated fallback profile.")
                    columns = st.columns(3)
                    fetched_asset["e"] = columns[0].slider(
                        "Environmental",
                        0.0,
                        100.0,
                        float(fetched_asset["e"]),
                        key=f"search_e_{asset_num}",
                    )
                    fetched_asset["s"] = columns[1].slider(
                        "Social",
                        0.0,
                        100.0,
                        float(fetched_asset["s"]),
                        key=f"search_s_{asset_num}",
                    )
                    fetched_asset["g"] = columns[2].slider(
                        "Governance",
                        0.0,
                        100.0,
                        float(fetched_asset["g"]),
                        key=f"search_g_{asset_num}",
                    )
                fetched_asset["_source"] = "live" if fetched_asset.get("_live") else "curated"
                asset_data = fetched_asset
                if not fetched_asset.get("_live"):
                    st.info(f"Live lookup was unavailable for {ticker_input}, so GreenVest is using the curated fallback profile instead.")
            else:
                st.warning(f"GreenVest could not find data for {ticker_input}. Check the ticker or switch to manual entry.")

    else:
        return render_manual_asset_input(asset_num, excluded_sectors)

    if asset_data is None:
        return None

    esg_composite = composite_esg(asset_data["e"], asset_data["s"], asset_data["g"], e_w, s_w, g_w) / 100
    is_excluded = asset_data["sector"] in excluded_sectors

    st.markdown(render_asset_card_html(asset_data), unsafe_allow_html=True)
    st.caption(
        f"Composite ESG used in the optimiser: {esg_composite * 100:.1f} [{esg_rating(esg_composite)}]"
    )

    if esg_composite >= 0.60 and asset_data["g"] / 100 < 0.35:
        st.warning(
            f"Greenwashing alert: {asset_data['name']} has a strong overall ESG score but weak governance."
        )

    if is_excluded:
        st.error(
            f"{asset_data['name']} sits inside an excluded sector ({asset_data['sector']}), so GreenVest will force its allocation to 0%."
        )

    return {
        **asset_data,
        "esg_c": esg_composite,
        "esg_a": esg_composite,
        "is_excluded": is_excluded,
    }


def build_generation_signature(setup_mode, rf, invest, rho, gamma_used, lambda_used, a1, a2):
    exclusions = tuple(sorted(get_excluded_sectors()))
    return repr(
        {
            "mode": setup_mode,
            "rf": round(rf, 6),
            "invest": round(float(invest), 2),
            "rho": round(rho, 4),
            "gamma": round(gamma_used, 4),
            "lambda": round(lambda_used, 4),
            "exclusions": exclusions,
            "asset_1": None if a1 is None else {
                key: a1.get(key)
                for key in ["name", "ticker", "sector", "mu", "sigma", "e", "s", "g", "is_excluded"]
            },
            "asset_2": None if a2 is None else {
                key: a2.get(key)
                for key in ["name", "ticker", "sector", "mu", "sigma", "e", "s", "g", "is_excluded"]
            },
        }
    )


def serialize_asset_for_snapshot(asset: dict):
    if asset is None:
        return None

    return {
        "name": str(asset.get("name", "")),
        "ticker": str(asset.get("ticker", "")),
        "sector": str(asset.get("sector", "")),
        "mu": float(asset.get("mu", 0.0)),
        "sigma": float(asset.get("sigma", 0.0)),
        "e": float(asset.get("e", 0.0)),
        "s": float(asset.get("s", 0.0)),
        "g": float(asset.get("g", 0.0)),
        "esg_c": float(asset.get("esg_c", 0.0)),
        "esg_a": float(asset.get("esg_a", 0.0)),
        "is_excluded": bool(asset.get("is_excluded", False)),
        "_live": bool(asset.get("_live", False)),
        "_source": str(asset.get("_source", "")),
        "_price": None if asset.get("_price") is None else float(asset.get("_price")),
    }


def build_result_snapshot(setup_mode, rf, invest, rho, gamma_used, lambda_used, e_w, s_w, g_w, profile, goal_label, excluded_labels, a1, a2):
    return {
        "setup_mode": setup_mode,
        "rf": float(rf),
        "invest": float(invest),
        "rho": float(rho),
        "gamma": float(gamma_used),
        "lambda": float(lambda_used),
        "e_w": int(e_w),
        "s_w": int(s_w),
        "g_w": int(g_w),
        "profile": str(profile),
        "goal_label": str(goal_label),
        "excluded_labels": list(excluded_labels),
        "asset1": serialize_asset_for_snapshot(a1),
        "asset2": serialize_asset_for_snapshot(a2),
    }


def persist_result_snapshot(snapshot: dict):
    payload = json.dumps(snapshot, sort_keys=True, separators=(",", ":"))
    snapshot_id = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:24]
    snapshot_path = RESULTS_DIR / f"{snapshot_id}.json"
    snapshot_path.write_text(payload, encoding="utf-8")
    return snapshot_id


def load_result_snapshot(snapshot_id: str):
    if not snapshot_id:
        return None

    snapshot_path = RESULTS_DIR / f"{snapshot_id}.json"
    if not snapshot_path.exists():
        return None

    try:
        return json.loads(snapshot_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def compute_portfolio_package(snapshot: dict):
    a1 = snapshot["asset1"]
    a2 = snapshot["asset2"]
    rf = float(snapshot["rf"])
    invest = float(snapshot["invest"])
    rho = float(snapshot["rho"])
    gamma_used = float(snapshot["gamma"])
    lambda_used = float(snapshot["lambda"])
    e_w = int(snapshot["e_w"])
    s_w = int(snapshot["s_w"])
    g_w = int(snapshot["g_w"])
    profile = snapshot["profile"]
    goal_label = snapshot["goal_label"]
    excluded_labels = snapshot.get("excluded_labels", [])
    excluded_summary = ", ".join(excluded_labels) if excluded_labels else "None"

    both_excluded = a1["is_excluded"] and a2["is_excluded"]
    force_w1 = None
    if a1["is_excluded"] and not a2["is_excluded"]:
        force_w1 = 0.0
    elif a2["is_excluded"] and not a1["is_excluded"]:
        force_w1 = 1.0

    results = {}
    summary_pdf_bytes = None
    benchmark_message_kind = "info"
    benchmark_message_text = ""
    checkpoint_df = pd.DataFrame()
    corner_solution_message = None

    if not both_excluded:
        (
            mix_grid,
            x1_grid,
            x2_grid,
            risky_share_grid,
            mu_grid,
            sigma_grid,
            esg_grid,
            objective_grid,
            esg_adjusted_grid,
            idx,
        ) = optimise(
            a1["mu"],
            a2["mu"],
            a1["sigma"],
            a2["sigma"],
            a1["esg_a"],
            a2["esg_a"],
            rho,
            rf,
            gamma_used,
            lambda_used,
            force_w1=force_w1,
        )

        w1 = float(x1_grid[idx])
        w2 = float(x2_grid[idx])
        risky_share = float(risky_share_grid[idx])
        rf_weight = 1 - risky_share
        mu_opt = float(mu_grid[idx])
        sigma_opt = float(sigma_grid[idx])
        esg_opt = float(esg_grid[idx])
        utility_opt = float(objective_grid[idx])
        sharpe_opt = (mu_opt - rf) / sigma_opt if sigma_opt > 0 else float("nan")
        esg_sharpe_opt = esg_sharpe(mu_opt, rf, sigma_opt, lambda_used, esg_opt)
        impact_score = round(esg_opt * 100, 1)
        tradeoff = lambda_used * esg_opt - (gamma_used / 2) * (sigma_opt ** 2)

        benchmark_return = None
        ret_cost = 0.0
        idx_financial = None
        idx_low_risk = None
        mu_50 = None
        sigma_ms = None
        esg_adjusted_ms = None
        x1_ms = None
        x2_ms = None
        risky_share_ms = None
        mu_ms = None

        if force_w1 is None:
            (
                _,
                x1_ms,
                x2_ms,
                risky_share_ms,
                mu_ms,
                sigma_ms,
                _esg_ms,
                _objective_ms,
                esg_adjusted_ms,
                idx_financial,
            ) = optimise(
                a1["mu"],
                a2["mu"],
                a1["sigma"],
                a2["sigma"],
                a1["esg_a"],
                a2["esg_a"],
                rho,
                rf,
                gamma_used,
                0.0,
            )
            positive_risky_mask = risky_share_grid > 1e-8
            if np.any(positive_risky_mask):
                idx_low_risk = int(np.argmin(np.where(positive_risky_mask, sigma_grid, np.inf)))
            else:
                idx_low_risk = int(np.argmin(sigma_grid))

            (
                _,
                _x1_50,
                _x2_50,
                _risky_share_50,
                mu_50_grid,
                _sigma_50_grid,
                _esg_50_grid,
                _objective_50_grid,
                _esg_adjusted_50_grid,
                idx_50,
            ) = optimise(
                a1["mu"],
                a2["mu"],
                a1["sigma"],
                a2["sigma"],
                a1["esg_a"],
                a2["esg_a"],
                rho,
                rf,
                gamma_used,
                0.0,
                force_w1=0.5,
            )
            benchmark_return = float(mu_50_grid[idx_50])
            mu_50 = benchmark_return
            ret_cost = mu_ms[idx_financial] * 100 - mu_opt * 100

        results = {
            "mix_grid": mix_grid,
            "x1_grid": x1_grid,
            "x2_grid": x2_grid,
            "risky_share_grid": risky_share_grid,
            "mu_grid": mu_grid,
            "sigma_grid": sigma_grid,
            "esg_grid": esg_grid,
            "esg_adjusted_grid": esg_adjusted_grid,
            "idx": idx,
            "w1": w1,
            "w2": w2,
            "rf_weight": rf_weight,
            "risky_share": risky_share,
            "mu_opt": mu_opt,
            "sigma_opt": sigma_opt,
            "esg_opt": esg_opt,
            "utility_opt": utility_opt,
            "sharpe_opt": sharpe_opt,
            "esg_sharpe_opt": esg_sharpe_opt,
            "impact_score": impact_score,
            "tradeoff": tradeoff,
            "benchmark_return": benchmark_return,
            "ret_cost": ret_cost,
            "idx_financial": idx_financial,
            "idx_low_risk": idx_low_risk,
            "mu_ms": mu_ms,
            "sigma_ms": sigma_ms,
            "esg_adjusted_ms": esg_adjusted_ms,
            "x1_ms": x1_ms,
            "x2_ms": x2_ms,
            "risky_share_ms": risky_share_ms,
            "mu_50": mu_50,
        }

        if force_w1 is None and results["risky_share"] > 0:
            corner_asset = None
            if results["w1"] < CORNER_THRESHOLD * results["risky_share"]:
                corner_asset = a2["name"]
                zero_asset = a1["name"]
            elif results["w2"] < CORNER_THRESHOLD * results["risky_share"]:
                corner_asset = a1["name"]
                zero_asset = a2["name"]

            if corner_asset is not None:
                corner_solution_message = (
                    f"**Corner solution detected.** At your current ESG preference "
                    f"(λ = {lambda_used:.3f}), holding any allocation in "
                    f"**{zero_asset}** reduces portfolio utility. The optimiser has "
                    f"placed the entire risky sleeve in **{corner_asset}**. "
                    f"This is economically meaningful: your sustainability preference "
                    f"is strong enough that diversification into the lower-ESG asset "
                    f"is not worth the trade-off. To restore a mixed portfolio, lower λ "
                    f"or choose an asset pair with more similar ESG scores."
                )

        summary_pdf_bytes = build_summary_pdf_bytes(
            a1,
            a2,
            results,
            invest,
            profile,
            goal_label,
            gamma_used,
            lambda_used,
            e_w,
            s_w,
            g_w,
            excluded_summary,
        )

        checkpoint_years = [5, 10, 20, 30]
        checkpoint_df = pd.DataFrame(
            {
                "Horizon": [f"{year} years" for year in checkpoint_years],
                "GreenVest": [f"GBP {future_value(invest, results['mu_opt'], year):,.0f}" for year in checkpoint_years],
            }
        )
        if results["benchmark_return"] is not None:
            checkpoint_df["50 / 50 risky mix"] = [
                f"GBP {future_value(invest, results['benchmark_return'], year):,.0f}"
                for year in checkpoint_years
            ]
            recommendation_30 = future_value(invest, results["mu_opt"], 30)
            benchmark_30 = future_value(invest, results["benchmark_return"], 30)
            if recommendation_30 > benchmark_30:
                benchmark_message_kind = "success"
                benchmark_message_text = (
                    f"GreenVest is projected to outperform the 50 / 50 risky-mix reference by GBP {recommendation_30 - benchmark_30:,.0f} over 30 years."
                )
            elif benchmark_30 > recommendation_30:
                benchmark_message_kind = "info"
                benchmark_message_text = (
                    f"The 50 / 50 risky-mix reference projects GBP {benchmark_30 - recommendation_30:,.0f} more over 30 years under the current assumptions."
                )
            else:
                benchmark_message_kind = "info"
                benchmark_message_text = (
                    "GreenVest and the 50 / 50 risky-mix reference project the same 30-year value under the current assumptions."
                )

    return {
        "setup_mode": snapshot["setup_mode"],
        "profile": profile,
        "goal_label": goal_label,
        "rf": rf,
        "invest": invest,
        "rho": rho,
        "gamma_used": gamma_used,
        "lambda_used": lambda_used,
        "e_w": e_w,
        "s_w": s_w,
        "g_w": g_w,
        "excluded_labels": excluded_labels,
        "excluded_summary": excluded_summary,
        "a1": a1,
        "a2": a2,
        "both_excluded": both_excluded,
        "force_w1": force_w1,
        "results": results,
        "summary_pdf_bytes": summary_pdf_bytes,
        "benchmark_message_kind": benchmark_message_kind,
        "benchmark_message_text": benchmark_message_text,
        "checkpoint_df": checkpoint_df,
        "corner_solution_message": corner_solution_message,
    }


def render_portfolio_output_panel(package: dict):
    a1 = package["a1"]
    a2 = package["a2"]
    both_excluded = package["both_excluded"]
    force_w1 = package["force_w1"]
    results = package["results"]
    gamma_used = package["gamma_used"]
    lambda_used = package["lambda_used"]
    corner_solution_message = package["corner_solution_message"]

    st.markdown(
        """
        <div class="section-kicker">Portfolio recommendation</div>
        <h3 class="section-title">Portfolio output</h3>
        <p class="section-copy">
            The recommendation below explains the mix, the core metrics, and the sustainability trade-off.
        </p>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("How GreenVest scores ESG", expanded=False):
        st.markdown(
            """
            1. GreenVest starts with the environmental, social, and governance sub-scores entered for each asset.
            2. Those pillar scores are combined into one composite ESG score using your own E, S, and G priority weights.
            3. The optimiser chooses risky positions `x1` and `x2`, not weights that must sum to 100%, so the remainder can stay in the risk-free asset.
            4. The final recommendation maximises `x'(mu - rf) - (gamma / 2) x'Sigma x + lambda * ESG_average`.
            5. Sector exclusions are enforced so blocked sectors cannot be recommended.
            """
        )

    if both_excluded:
        st.error(
            "Both selected assets sit inside excluded sectors. Update the exclusions or choose different assets."
        )
        return

    if corner_solution_message:
        st.info(corner_solution_message)

    high_esg_asset = a1["name"] if a1["esg_a"] >= a2["esg_a"] else a2["name"]
    high_return_asset = a1["name"] if a1["mu"] >= a2["mu"] else a2["name"]
    gamma_desc = (
        "high risk aversion" if gamma_used >= 7 else "moderate risk aversion" if gamma_used >= 4 else "lower risk aversion"
    )
    lambda_desc = (
        "strong sustainability preference"
        if lambda_used >= 0.12
        else "balanced sustainability preference"
        if lambda_used >= 0.06
        else "lighter sustainability preference"
    )
    rf_position_label = (
        f"Borrowing at rf: {abs(results['rf_weight']) * 100:.1f}%"
        if results["rf_weight"] < 0
        else f"Risk-free: {results['rf_weight'] * 100:.1f}%"
    )

    st.markdown(
        f"""
        <div class="spotlight-card">
            <div class="section-kicker">Recommended positions</div>
            <h3>{a1["name"]}: {results["w1"] * 100:.1f}% | {a2["name"]}: {results["w2"] * 100:.1f}% | {rf_position_label}</h3>
            <p>
                GreenVest leans toward <strong>{high_esg_asset}</strong> for sustainability strength while
                preserving return support from <strong>{high_return_asset}</strong>. With
                <strong>{gamma_desc}</strong> and a <strong>{lambda_desc}</strong>, the optimiser searches for a cleaner balance between return, risk, and ESG quality.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_row_1 = st.columns(2)
    metric_row_1[0].metric(f"{a1['name']} position", f"{results['w1'] * 100:.2f}%")
    metric_row_1[1].metric(f"{a2['name']} position", f"{results['w2'] * 100:.2f}%")

    metric_row_2 = st.columns(2)
    metric_row_2[0].metric("Risk-free position", f"{results['rf_weight'] * 100:.2f}%")
    metric_row_2[1].metric("Expected return", f"{results['mu_opt'] * 100:.2f}%")

    metric_row_3 = st.columns(2)
    metric_row_3[0].metric("Portfolio risk", f"{results['sigma_opt'] * 100:.2f}%")
    metric_row_3[1].metric("Sharpe ratio", f"{results['sharpe_opt']:.3f}")

    metric_row_4 = st.columns(2)
    metric_row_4[0].metric("ESG score", f"{results['esg_opt'] * 100:.1f} / 100")
    metric_row_4[1].metric("ESG-adjusted Sharpe", f"{results['esg_sharpe_opt']:.3f}")

    metric_row_5 = st.columns(2)
    metric_row_5[0].metric("Objective value", f"{results['utility_opt']:.5f}")
    metric_row_5[1].metric("Impact score", f"{results['impact_score']:.1f}")

    if force_w1 is not None:
        excluded_name = a1["name"] if a1["is_excluded"] else a2["name"]
        held_name = a2["name"] if a1["is_excluded"] else a1["name"]
        st.warning(
            f"Hard exclusion applied: {excluded_name} is blocked, so the risky sleeve moves fully into {held_name}."
        )
    elif results["benchmark_return"] is not None and results["ret_cost"] > 0.5:
        st.info(
            f"Compared with a purely financial benchmark, this sustainable tilt gives up about {results['ret_cost']:.2f}% of expected return."
        )
    else:
        st.success(
            "The current sustainable preference set does not create a meaningful return penalty in this two-asset setup."
        )


def render_results_page(snapshot: dict):
    package = compute_portfolio_package(snapshot)
    setup_label = "Create Your Own" if package["setup_mode"] == "manual" else "Generate For Me"

    utility_cols = st.columns([0.14, 0.62, 0.24], gap="large")
    with utility_cols[0]:
        st.markdown(
            f'<div class="dashboard-utility"><a class="dashboard-home-link" href="?nav=home" target="_self"><img src="{LOGO_DATA_URI}" alt="Go back home"></a></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <section class="dashboard-hero">
            <div class="dashboard-head">
                <div>
                    <div class="section-kicker">{setup_label}</div>
                    <h2 class="dashboard-title">Portfolio Results</h2>
                    <p class="dashboard-copy">Everything from the GreenVest recommendation is collected here in one clean output view.</p>
                    <div class="chip-row">
                        <span class="chip">{package["profile"]}</span>
                        <span class="chip blue">{package["goal_label"]}</span>
                        <span class="chip">gamma = {package["gamma_used"]:.1f}</span>
                        <span class="chip">lambda = {package["lambda_used"]:.3f}</span>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    render_investor_charts_section(
        package["both_excluded"],
        package["force_w1"],
        package["results"],
        package["a1"],
        package["a2"],
        package["invest"],
        "Investor Charts",
        package["summary_pdf_bytes"],
        package["checkpoint_df"],
        package["benchmark_message_kind"],
        package["benchmark_message_text"],
    )

    result_cols = st.columns([1.05, 0.95], gap="large")
    with result_cols[0]:
        render_portfolio_output_panel(package)
    with result_cols[1]:
        st.markdown(
            """
            <div class="section-kicker">Selected assets</div>
            <h3 class="section-title">Assets in this result</h3>
            <p class="section-copy">These are the two risky assets used in the optimisation shown above.</p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(render_asset_card_html(package["a1"]), unsafe_allow_html=True)
        st.markdown(render_asset_card_html(package["a2"]), unsafe_allow_html=True)

def apply_profile_results(e_w, s_w, g_w, excl_tobacco, excl_weapons, excl_gambling, excl_fossil, excl_alcohol):
    st.session_state.e_w = e_w
    st.session_state.s_w = s_w
    st.session_state.g_w = g_w
    st.session_state.excl_tobacco = excl_tobacco
    st.session_state.excl_weapons = excl_weapons
    st.session_state.excl_gambling = excl_gambling
    st.session_state.excl_fossil = excl_fossil
    st.session_state.excl_alcohol = excl_alcohol

    q1 = st.session_state.q1
    q2 = st.session_state.q2
    q3 = st.session_state.q3
    score = ((5 - q1) + (5 - q2) + q3) / 3
    gamma_base = round(2 + (score - 1) * (8 / 3), 1)
    profile = "Conservative" if gamma_base >= 7 else "Balanced" if gamma_base >= 4 else "Aggressive"
    goal = st.session_state.goal
    gamma = round(max(1.0, gamma_base + {1: 2, 2: 0, 3: 0, 4: -1}[goal]), 1)
    goal_lam = {1: 0, 2: 0, 3: 0.02, 4: 0}[goal]
    excl_count = sum([excl_tobacco, excl_weapons, excl_gambling, excl_fossil, excl_alcohol])
    lambda_esg = derive_lambda(e_w, s_w, g_w, excl_count, goal_lam)

    goal_labels = {
        1: "Retirement",
        2: "Long-term growth",
        3: "Ethical investing",
        4: "Short-term profit",
    }

    st.session_state.gamma = gamma
    st.session_state.gamma_val = gamma
    st.session_state.lambda_esg = lambda_esg
    st.session_state.lambda_val = lambda_esg
    st.session_state.profile = profile
    st.session_state.goal_label = goal_labels[goal]
    st.session_state.onboarding_done = True
    st.session_state.entered_app = True
    st.session_state.setup_mode = st.session_state.setup_mode or "guided"
    if st.session_state.setup_mode == "guided":
        excluded_sectors = {
            sector_name
            for sector_name, enabled in [
                ("Tobacco", excl_tobacco),
                ("Weapons / Defence", excl_weapons),
                ("Gambling", excl_gambling),
                ("Fossil Fuels / Energy", excl_fossil),
                ("Alcohol", excl_alcohol),
            ]
            if enabled
        }
        guided_pair = recommend_guided_asset_pair(
            e_w,
            s_w,
            g_w,
            gamma,
            lambda_esg,
            excluded_sectors,
        )
        if guided_pair is not None:
            asset1 = guided_pair["asset1"]
            asset2 = guided_pair["asset2"]
            st.session_state.asset1_mode = "curated"
            st.session_state.asset2_mode = "curated"
            st.session_state.asset1_ticker = asset1["ticker"]
            st.session_state.asset2_ticker = asset2["ticker"]
            st.session_state.radio_mode_1 = "curated"
            st.session_state.radio_mode_2 = "curated"
            st.session_state.curated_sel_1 = f'{asset1["name"]} ({asset1["ticker"]})'
            st.session_state.curated_sel_2 = f'{asset2["name"]} ({asset2["ticker"]})'
    st.session_state.show_profile_builder = False
    st.session_state.onboarding_step = 1
    st.session_state.generated_signature = None
    st.rerun()


@st.dialog("Your Investor Preferences", width="large")
def render_profile_builder(editing=False):
    total_steps = 5
    step = st.session_state.onboarding_step
    is_manual_mode = st.session_state.setup_mode == "manual"
    heading = "Set Your Investor Preferences" if not editing else "Update Your Preferences"
    if editing:
        body = "Refine your answers here, then generate again to refresh your portfolio without leaving the workspace."
    elif is_manual_mode:
        body = "Answer these questions first, then enter your own expected returns, risk, and ESG assumptions."
    else:
        body = "Answer these questions first, then choose from the eligible assets and generate your portfolio."

    mascot_answers = {
        1: "This answer sets how defensive or adventurous your portfolio should feel if markets become volatile.",
        2: "Your objective tells GreenVest whether to lean more toward stability, income, or long-term growth.",
        3: "Your time horizon affects how much short-term movement GreenVest can tolerate for stronger long-term upside.",
        4: "Your goal helps decide how strongly the recommendation should balance growth with sustainability.",
        5: "These priorities tell GreenVest how much environmental, social, governance, and sector exclusions should shape the final mix.",
    }
    step_summaries = {
        1: "Start by telling GreenVest how you react to losses.",
        2: "Next, define what success looks like for your portfolio.",
        3: "Then set the time horizon GreenVest should plan around.",
        4: "Now choose the outcome you care about most.",
        5: "Finish by setting your ESG priorities and any sector exclusions.",
    }

    st.markdown(
        f"""
        <div class="profile-banner">
            <div class="section-kicker">Guided setup</div>
            <h3 class="section-title" style="margin-bottom:0.35rem;">{heading}</h3>
            <p class="section-copy">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    content_col, mascot_col = st.columns([1.18, 0.38], gap="large")

    with mascot_col:
        st.markdown(
            f"""
            <div class="guide-mascot-card">
                <div class="section-kicker">GreenVest guide</div>
                <div class="mascot-answer"><strong>Guide note:</strong> {mascot_answers[step]}</div>
                <img class="guide-mascot-image" src="{QUESTION_DATA_URI}" alt="Question mascot">
            </div>
            """,
            unsafe_allow_html=True,
        )

    with content_col:
        st.markdown(
            f"""
            <div class="profile-step-card">
                <div class="section-kicker">Step overview</div>
                <p class="section-copy">{step_summaries[step]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(step / total_steps)
        st.caption(f"Step {step} of {total_steps}")
        st.write("")

        if step == 1:
            st.markdown(
                '<div class="profile-question-title">If your portfolio dropped 25%, what would you do?</div>',
                unsafe_allow_html=True,
            )
            choice = st.radio(
                "If your portfolio dropped 25%, what would you do?",
                options=[1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Sell everything - I cannot afford to lose more",
                    2: "Reduce exposure - I want to limit further losses",
                    3: "Hold steady - I trust the market will recover",
                    4: "Buy more - downturns are buying opportunities",
                }[x],
                index=st.session_state.q1 - 1,
                label_visibility="collapsed",
            )
            st.caption("This tells GreenVest how much short-term volatility feels comfortable for you.")
            left, _, right = st.columns([1, 1.4, 1])
            if editing:
                with left:
                    if st.button("Cancel", key="profile_cancel_1"):
                        st.session_state.show_profile_builder = False
                        st.session_state.onboarding_step = 1
                        st.rerun()
            with right:
                if st.button("Next", key="profile_next_1"):
                    st.session_state.q1 = choice
                    st.session_state.onboarding_step = 2
                    st.rerun()

        elif step == 2:
            st.markdown(
                '<div class="profile-question-title">What is the primary investment objective?</div>',
                unsafe_allow_html=True,
            )
            choice = st.radio(
                "What is the primary investment objective?",
                options=[1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Preserve capital - protect what is already there",
                    2: "Generate income - steady, reliable returns",
                    3: "Long-term growth - grow wealth steadily",
                    4: "Maximise growth - seek the highest return potential",
                }[x],
                index=st.session_state.q2 - 1,
                label_visibility="collapsed",
            )
            st.caption("This shifts the balance between stability, growth, and sustainability tilt.")
            left, _, right = st.columns([1, 1.4, 1])
            with left:
                if st.button("Back", key="profile_back_2"):
                    st.session_state.q2 = choice
                    st.session_state.onboarding_step = 1
                    st.rerun()
            with right:
                if st.button("Next", key="profile_next_2"):
                    st.session_state.q2 = choice
                    st.session_state.onboarding_step = 3
                    st.rerun()

        elif step == 3:
            st.markdown(
                '<div class="profile-question-title">How long do you plan to stay invested?</div>',
                unsafe_allow_html=True,
            )
            choice = st.radio(
                "How long do you plan to stay invested?",
                options=[1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Less than 2 years",
                    2: "2 to 5 years",
                    3: "5 to 10 years",
                    4: "10 years or more",
                }[x],
                index=st.session_state.q3 - 1,
                label_visibility="collapsed",
            )
            st.caption(
                "Your time horizon tells GreenVest how much short-term movement you can tolerate for long-term upside."
            )
            left, _, right = st.columns([1, 1.4, 1])
            with left:
                if st.button("Back", key="profile_back_3"):
                    st.session_state.q3 = choice
                    st.session_state.onboarding_step = 2
                    st.rerun()
            with right:
                if st.button("Next", key="profile_next_3"):
                    st.session_state.q3 = choice
                    st.session_state.onboarding_step = 4
                    st.rerun()

        elif step == 4:
            st.markdown(
                '<div class="profile-question-title">What are you working toward?</div>',
                unsafe_allow_html=True,
            )
            choice = st.radio(
                "What are you working toward?",
                options=[1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Retirement - long-term financial security",
                    2: "Long-term growth - compounding wealth over time",
                    3: "Ethical investing - sustainability alongside returns",
                    4: "Short-term profit - stronger near-term gains",
                }[x],
                index=st.session_state.goal - 1,
                label_visibility="collapsed",
            )
            st.caption("Your goal helps decide how much explicit weight ESG receives in the utility score.")
            left, _, right = st.columns([1, 1.4, 1])
            with left:
                if st.button("Back", key="profile_back_4"):
                    st.session_state.goal = choice
                    st.session_state.onboarding_step = 3
                    st.rerun()
            with right:
                if st.button("Next", key="profile_next_4"):
                    st.session_state.goal = choice
                    st.session_state.onboarding_step = 5
                    st.rerun()

        else:
            st.markdown(
                '<div class="profile-question-title">How much should GreenVest care about each ESG pillar?</div>',
                unsafe_allow_html=True,
            )
            st.caption("Set each pillar from 0 to 5. These weights shape your composite ESG score.")
            e_w = st.slider("Environmental priority", 0, 5, st.session_state.e_w)
            s_w = st.slider("Social priority", 0, 5, st.session_state.s_w)
            g_w = st.slider("Governance priority", 0, 5, st.session_state.g_w)
            st.write("")
            st.caption("Exclude any sectors from the portfolio universe?")
            c1, c2, c3, c4, c5 = st.columns(5)
            excl_tobacco = c1.checkbox("Tobacco", value=st.session_state.excl_tobacco)
            excl_weapons = c2.checkbox("Weapons", value=st.session_state.excl_weapons)
            excl_gambling = c3.checkbox("Gambling", value=st.session_state.excl_gambling)
            excl_fossil = c4.checkbox("Fossil Fuels", value=st.session_state.excl_fossil)
            excl_alcohol = c5.checkbox("Alcohol", value=st.session_state.excl_alcohol)

            left, _, right = st.columns([1, 1.4, 1])
            with left:
                if st.button("Back", key="profile_back_5"):
                    st.session_state.e_w = e_w
                    st.session_state.s_w = s_w
                    st.session_state.g_w = g_w
                    st.session_state.onboarding_step = 4
                    st.rerun()
            with right:
                if st.button("Build My GreenVest Profile", key="profile_done_5"):
                    apply_profile_results(
                        e_w,
                        s_w,
                        g_w,
                        excl_tobacco,
                        excl_weapons,
                        excl_gambling,
                        excl_fossil,
                        excl_alcohol,
                    )


def render_landing_page():
    review_cards = REVIEWS + REVIEWS
    review_html = "".join(
        f"""
        <div class="review-card">
            <div>
                <div class="review-stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>
                <p>{review['quote']}</p>
            </div>
            <div class="reviewer">{review['author']}</div>
        </div>
        """
        for review in review_cards
    )

    st.markdown(
        f"""
        <section class="hero-shell">
            <div class="hero-grid">
                <div class="hero-main">
                    <div class="hero-brand-row">
                        <img class="hero-logo" src="{LOGO_DATA_URI}" alt="GreenVest logo">
                        <div class="hero-brand-copy">
                            <h1 class="hero-title">GreenVest</h1>
                        </div>
                    </div>
                    <p class="hero-copy">
                        Sustainable investing, made clearer.
                        GreenVest brings return, risk, and ESG into one clean view.
                    </p>
                    <div class="hero-actions">
                        <form class="hero-action-form" method="get" target="_self">
                            <button class="hero-button green" type="submit" name="launch" value="manual">Create Your Own</button>
                        </form>
                        <form class="hero-action-form" method="get" target="_self">
                            <button class="hero-button blue" type="submit" name="launch" value="guided">Generate For Me</button>
                        </form>
                    </div>
                    <div class="hero-note">
                        Use the green path for a self-directed portfolio build, or the blue path to generate
                        a portfolio from investor preferences.
                    </div>
                </div>
                <div class="hero-panel">
                    <div class="hero-panel-copy">
                        <h4>What GreenVest does better</h4>
                        <div class="hero-points">
                            <div class="hero-point">
                                <strong>More transparent sustainability scoring</strong>
                                GreenVest shows how ESG is built from weighted E, S, and G inputs,
                                rather than hiding the methodology behind a vague label.
                            </div>
                            <div class="hero-point">
                                <strong>Real assets and live ticker lookup</strong>
                                GreenVest now lets investors pick from a curated asset library or search real
                                tickers, so the portfolio conversation feels closer to an actual investment workflow.
                            </div>
                            <div class="hero-point">
                                <strong>Better outputs for real conversations</strong>
                                The app now supports cleaner charts, clearer explanations, and a one-page
                                PDF summary that is easier to use in meetings and submissions.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="fact-grid">
            <div class="fact-card">
                <div class="section-kicker">What It Is</div>
                <p>
                    Sustainable investing looks at financial return alongside environmental, social,
                    and governance performance. Instead of asking only "what could this earn?",
                    it also asks "how is this business being run, and what risks or opportunities does that create?"
                </p>
            </div>
            <div class="fact-card">
                <div class="section-kicker">Why It Matters</div>
                <p>
                    Investors often use sustainable strategies to align with their values, manage long-run
                    regulatory and reputational risk, and back companies that may be better positioned for
                    future policy, consumer, and market shifts.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <section class="review-shell">
            <div class="review-intro">
                <div>
                    <div class="section-kicker">Investor reactions</div>
                </div>
            </div>
            <div class="review-rail">
                <div class="review-track">
                    {review_html}
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    defaults = {
        "entered_app": False,
        "show_profile_builder": False,
        "setup_mode": None,
        "loader_complete": False,
        "show_loader": False,
        "loader_context": "launch",
        "onboarding_done": False,
        "onboarding_step": 1,
        "q1": 3,
        "q2": 3,
        "q3": 3,
        "goal": 2,
        "e_w": 3,
        "s_w": 3,
        "g_w": 3,
        "excl_tobacco": False,
        "excl_weapons": False,
        "excl_gambling": False,
        "excl_fossil": False,
        "excl_alcohol": False,
        "gamma": 4.0,
        "lambda_esg": 0.06,
        "gamma_val": 4.0,
        "lambda_val": 0.06,
        "profile": "Balanced",
        "goal_label": "Long-term growth",
        "asset1_mode": "curated",
        "asset2_mode": "curated",
        "asset1_ticker": "AAPL",
        "asset2_ticker": "MSFT",
        "generated_signature": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def handle_entry_actions():
    nav = get_query_param("nav")
    if nav == "home":
        reset_home_state()
        st.session_state.show_loader = True
        st.session_state.loader_context = "home"
        return

    action = get_query_param("launch")
    if action == "manual":
        st.session_state.show_loader = True
        st.session_state.loader_context = "enter"
        st.session_state.entered_app = True
        st.session_state.onboarding_done = False
        st.session_state.setup_mode = "manual"
        st.session_state.show_profile_builder = True
        st.session_state.onboarding_step = 1
        st.session_state.generated_signature = None
        clear_query_params()
        return

    if action == "guided":
        st.session_state.show_loader = True
        st.session_state.loader_context = "enter"
        st.session_state.entered_app = True
        st.session_state.show_profile_builder = True
        st.session_state.setup_mode = "guided"
        st.session_state.onboarding_step = 1
        st.session_state.onboarding_done = False
        st.session_state.generated_signature = None
        clear_query_params()
        return


def _legacy_render_dashboard_unused():
    setup_mode = st.session_state.setup_mode or "manual"
    is_manual_mode = setup_mode == "manual"
    gamma_used = st.session_state.gamma_val
    lambda_used = st.session_state.lambda_val
    e_w = st.session_state.e_w
    s_w = st.session_state.s_w
    g_w = st.session_state.g_w

    utility_cols = st.columns([0.14, 0.62, 0.24], gap="large")
    with utility_cols[0]:
        st.markdown(
            f'<div class="dashboard-utility"><a class="dashboard-home-link" href="?nav=home" target="_self"><img src="{LOGO_DATA_URI}" alt="Go back home"></a></div>',
            unsafe_allow_html=True,
        )
    with utility_cols[2]:
        if st.button("Update Preferences"):
            st.session_state.show_profile_builder = True
            st.session_state.onboarding_step = 1
            st.rerun()

    if st.session_state.show_profile_builder:
        render_profile_builder(editing=st.session_state.onboarding_done)

    top_results_slot = st.container()
    builder_col, insight_col = st.columns([1.34, 0.66], gap="large")

    current_signature = None
    a1 = None
    a2 = None

    with builder_col:
        if is_manual_mode:
            st.markdown(
                """
                <div class="section-kicker">Portfolio builder</div>
                <h3 class="section-title">Enter your asset assumptions</h3>
                """,
                unsafe_allow_html=True,
            )

        with st.expander("Advanced controls for gamma and lambda", expanded=False):
            if "_g_sl" not in st.session_state:
                st.session_state._g_sl = st.session_state.gamma_val
            if "_g_ni" not in st.session_state:
                st.session_state._g_ni = st.session_state.gamma_val
            if "_l_sl" not in st.session_state:
                st.session_state._l_sl = st.session_state.lambda_val
            if "_l_ni" not in st.session_state:
                st.session_state._l_ni = st.session_state.lambda_val

            st.caption(
                "Use these only if you want to override the profile-derived risk aversion and ESG preference values."
            )

            gamma_cols = st.columns([4, 1])
            with gamma_cols[0]:
                    st.slider(
                        "Risk aversion",
                        1.0,
                        10.0,
                        st.session_state.gamma_val,
                        0.1,
                        key="_g_sl",
                        on_change=sync_gamma_slider,
                        help="Higher gamma means you are more sensitive to portfolio risk.",
                    )
            with gamma_cols[1]:
                st.number_input(
                    "gamma exact",
                    1.0,
                    10.0,
                    st.session_state.gamma_val,
                    0.1,
                    key="_g_ni",
                    on_change=sync_gamma_input,
                    label_visibility="collapsed",
                )

            lambda_cols = st.columns([4, 1])
            with lambda_cols[0]:
                st.slider(
                    "ESG preference",
                    0.01,
                    0.20,
                    st.session_state.lambda_val,
                    0.005,
                    key="_l_sl",
                    on_change=sync_lambda_slider,
                    help="Higher lambda gives sustainability a stronger role in the utility score.",
                )
            with lambda_cols[1]:
                st.number_input(
                    "lambda exact",
                    0.01,
                    0.20,
                    st.session_state.lambda_val,
                    0.005,
                    key="_l_ni",
                    on_change=sync_lambda_input,
                    format="%.3f",
                    label_visibility="collapsed",
                )

            st.info(
                f"Active values -> gamma = {st.session_state.gamma_val:.1f} | "
                f"lambda = {st.session_state.lambda_val:.3f}"
            )

        st.write("")
        market_cols = st.columns(2)
        with market_cols[0]:
            rf = st.number_input(
                "Risk-free rate (%)",
                min_value=0.0,
                max_value=20.0,
                value=4.5,
                step=0.1,
            ) / 100
        with market_cols[1]:
            invest = st.number_input(
                "Investment amount (GBP)",
                min_value=100.0,
                max_value=1_000_000.0,
                value=10_000.0,
                step=500.0,
            )

        st.markdown(
            f"""
            <div class="info-note">
                Excluded sectors: <strong>{", ".join(excluded_sector_labels())}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

        excluded_sectors = get_excluded_sectors()
        asset_cols = st.columns(2, gap="medium")
        with asset_cols[0]:
            if is_manual_mode:
                a1 = render_manual_asset_input(1, excluded_sectors)
            else:
                a1 = render_asset_selector(
                    1,
                    excluded_sectors,
                    allowed_modes=["curated", "search"],
                    filter_excluded_curated=True,
                )
        with asset_cols[1]:
            if is_manual_mode:
                a2 = render_manual_asset_input(2, excluded_sectors)
            else:
                a2 = render_asset_selector(
                    2,
                    excluded_sectors,
                    allowed_modes=["curated", "search"],
                    filter_excluded_curated=True,
                )

        if not is_manual_mode and st.session_state.onboarding_done and a1 is not None and a2 is not None:
            st.info(
                f"GreenVest has pre-selected {a1['name']} and {a2['name']} from your preferences. "
                "You can keep them or swap them before generating the portfolio."
            )

        st.write("")
        rho = st.slider(
            "Correlation between the two assets",
            -1.0,
            1.0,
            0.3,
            0.01,
            help="-1 means the assets move opposite to each other. 1 means they move together.",
        )

        if a1 is not None and a2 is not None:
            current_signature = build_generation_signature(
                setup_mode,
                rf,
                invest,
                rho,
                gamma_used,
                lambda_used,
                a1,
                a2,
            )

        generate_disabled = not st.session_state.onboarding_done or a1 is None or a2 is None
        if st.button("Generate Portfolio", use_container_width=True, disabled=generate_disabled):
            st.session_state.generated_signature = current_signature
            st.rerun()

        if not st.session_state.onboarding_done:
            st.info("Complete your investor preferences popup first, then generate your portfolio.")
        elif a1 is None or a2 is None:
            st.info("Complete both asset sections to unlock the portfolio recommendation.")

    if a1 is None or a2 is None:
        return

    generated = st.session_state.generated_signature == current_signature
    if not generated:
        return

    both_excluded = a1["is_excluded"] and a2["is_excluded"]
    force_w1 = None
    if a1["is_excluded"] and not a2["is_excluded"]:
        force_w1 = 0.0
    elif a2["is_excluded"] and not a1["is_excluded"]:
        force_w1 = 1.0

    results = {}
    summary_pdf_bytes = None
    benchmark_message_kind = "info"
    benchmark_message_text = ""
    checkpoint_df = pd.DataFrame()
    corner_solution_message = None

    if not both_excluded:
        mix_grid, x1_grid, x2_grid, risky_share_grid, mu_grid, sigma_grid, esg_grid, objective_grid, esg_adjusted_grid, idx = optimise(
            a1["mu"],
            a2["mu"],
            a1["sigma"],
            a2["sigma"],
            a1["esg_a"],
            a2["esg_a"],
            rho,
            rf,
            gamma_used,
            lambda_used,
            force_w1=force_w1,
        )

        w1 = float(x1_grid[idx])
        w2 = float(x2_grid[idx])
        risky_share = float(risky_share_grid[idx])
        rf_weight = 1 - risky_share
        mu_opt = float(mu_grid[idx])
        sigma_opt = float(sigma_grid[idx])
        esg_opt = float(esg_grid[idx])
        utility_opt = float(objective_grid[idx])
        sharpe_opt = (mu_opt - rf) / sigma_opt if sigma_opt > 0 else float("nan")
        esg_sharpe_opt = esg_sharpe(mu_opt, rf, sigma_opt, lambda_used, esg_opt)
        impact_score = round(esg_opt * 100, 1)
        tradeoff = lambda_used * esg_opt - (gamma_used / 2) * (sigma_opt ** 2)

        benchmark_return = None
        ret_cost = 0.0
        idx_financial = None
        idx_low_risk = None
        mu_50 = None
        sigma_ms = None
        esg_adjusted_ms = None
        x1_ms = None
        x2_ms = None
        risky_share_ms = None

        if force_w1 is None:
            _, x1_ms, x2_ms, risky_share_ms, mu_ms, sigma_ms, esg_ms, objective_ms, esg_adjusted_ms, idx_financial = optimise(
                a1["mu"],
                a2["mu"],
                a1["sigma"],
                a2["sigma"],
                a1["esg_a"],
                a2["esg_a"],
                rho,
                rf,
                gamma_used,
                0.0,
            )
            positive_risky_mask = risky_share_grid > 1e-8
            if np.any(positive_risky_mask):
                idx_low_risk = int(np.argmin(np.where(positive_risky_mask, sigma_grid, np.inf)))
            else:
                idx_low_risk = int(np.argmin(sigma_grid))

            _, x1_50, x2_50, risky_share_50, mu_50_grid, sigma_50_grid, esg_50_grid, objective_50_grid, _, idx_50 = optimise(
                a1["mu"],
                a2["mu"],
                a1["sigma"],
                a2["sigma"],
                a1["esg_a"],
                a2["esg_a"],
                rho,
                rf,
                gamma_used,
                0.0,
                force_w1=0.5,
            )
            benchmark_return = float(mu_50_grid[idx_50])
            mu_50 = benchmark_return
            ret_cost = mu_ms[idx_financial] * 100 - mu_opt * 100

        results = {
            "mix_grid": mix_grid,
            "x1_grid": x1_grid,
            "x2_grid": x2_grid,
            "risky_share_grid": risky_share_grid,
            "mu_grid": mu_grid,
            "sigma_grid": sigma_grid,
            "esg_grid": esg_grid,
            "esg_adjusted_grid": esg_adjusted_grid,
            "idx": idx,
            "w1": w1,
            "w2": w2,
            "rf_weight": rf_weight,
            "risky_share": risky_share,
            "mu_opt": mu_opt,
            "sigma_opt": sigma_opt,
            "esg_opt": esg_opt,
            "utility_opt": utility_opt,
            "sharpe_opt": sharpe_opt,
            "esg_sharpe_opt": esg_sharpe_opt,
            "impact_score": impact_score,
            "tradeoff": tradeoff,
            "benchmark_return": benchmark_return,
            "ret_cost": ret_cost,
            "idx_financial": idx_financial,
            "idx_low_risk": idx_low_risk,
            "mu_ms": mu_ms,
            "sigma_ms": sigma_ms,
            "esg_adjusted_ms": esg_adjusted_ms,
            "x1_ms": x1_ms,
            "x2_ms": x2_ms,
            "risky_share_ms": risky_share_ms,
            "mu_50": mu_50,
        }

        if force_w1 is None and results["risky_share"] > 0:
            corner_asset = None
            if results["w1"] < CORNER_THRESHOLD * results["risky_share"]:
                corner_asset = a2["name"]
                zero_asset = a1["name"]
            elif results["w2"] < CORNER_THRESHOLD * results["risky_share"]:
                corner_asset = a1["name"]
                zero_asset = a2["name"]

            if corner_asset is not None:
                corner_solution_message = (
                    f"**Corner solution detected.** At your current ESG preference "
                    f"(λ = {lambda_used:.3f}), holding any allocation in "
                    f"**{zero_asset}** reduces portfolio utility. The optimiser has "
                    f"placed the entire risky sleeve in **{corner_asset}**. "
                    f"This is economically meaningful: your sustainability preference "
                    f"is strong enough that diversification into the lower-ESG asset "
                    f"is not worth the trade-off. To restore a mixed portfolio, lower λ "
                    f"or choose an asset pair with more similar ESG scores."
                )

        summary_pdf_bytes = build_summary_pdf_bytes(
            a1,
            a2,
            results,
            invest,
            st.session_state.profile,
            st.session_state.goal_label,
            gamma_used,
            lambda_used,
            e_w,
            s_w,
            g_w,
            ", ".join(excluded_sector_labels()),
        )

        checkpoint_years = [5, 10, 20, 30]
        checkpoint_df = pd.DataFrame(
            {
                "Horizon": [f"{year} years" for year in checkpoint_years],
                "GreenVest": [f"GBP {future_value(invest, results['mu_opt'], year):,.0f}" for year in checkpoint_years],
            }
        )
        if results["benchmark_return"] is not None:
            checkpoint_df["50 / 50 risky mix"] = [
                f"GBP {future_value(invest, results['benchmark_return'], year):,.0f}" for year in checkpoint_years
            ]
            recommendation_30 = future_value(invest, results["mu_opt"], 30)
            benchmark_30 = future_value(invest, results["benchmark_return"], 30)
            if recommendation_30 > benchmark_30:
                benchmark_message_kind = "success"
                benchmark_message_text = (
                    f"GreenVest is projected to outperform the 50 / 50 risky-mix reference by GBP {recommendation_30 - benchmark_30:,.0f} over 30 years."
                )
            elif benchmark_30 > recommendation_30:
                benchmark_message_kind = "info"
                benchmark_message_text = (
                    f"The 50 / 50 risky-mix reference projects GBP {benchmark_30 - recommendation_30:,.0f} more over 30 years under the current assumptions."
                )
            else:
                benchmark_message_kind = "info"
                benchmark_message_text = "GreenVest and the 50 / 50 risky-mix reference project the same 30-year value under the current assumptions."

    with top_results_slot:
        if not both_excluded:
            render_investor_charts_section(
                both_excluded,
                force_w1,
                results,
                a1,
                a2,
                invest,
                "Investor Charts",
                summary_pdf_bytes,
                checkpoint_df,
                benchmark_message_kind,
                benchmark_message_text,
            )

    with insight_col:
        st.markdown(
            """
            <div class="section-kicker">Portfolio recommendation</div>
            <h3 class="section-title">Portfolio output</h3>
            <p class="section-copy">
                The recommendation below explains the mix, the core metrics, and the sustainability trade-off.
            </p>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("How GreenVest scores ESG", expanded=False):
            st.markdown(
                """
                1. GreenVest starts with the environmental, social, and governance sub-scores entered for each asset.
                2. Those pillar scores are combined into one composite ESG score using your own E, S, and G priority weights.
                3. The optimiser chooses risky positions `x1` and `x2`, not weights that must sum to 100%, so the remainder can stay in the risk-free asset.
                4. The final recommendation maximises `x'(mu - rf) - (gamma / 2) x'Sigma x + lambda * ESG_average`.
                5. Sector exclusions are enforced so blocked sectors cannot be recommended.
                """
            )

        if both_excluded:
            st.error(
                "Both selected assets sit inside excluded sectors. Update the exclusions or choose different assets."
            )
            return

        if corner_solution_message:
            st.info(corner_solution_message)

        high_esg_asset = a1["name"] if a1["esg_a"] >= a2["esg_a"] else a2["name"]
        high_return_asset = a1["name"] if a1["mu"] >= a2["mu"] else a2["name"]
        gamma_desc = (
            "high risk aversion" if gamma_used >= 7 else "moderate risk aversion" if gamma_used >= 4 else "lower risk aversion"
        )
        lambda_desc = (
            "strong sustainability preference"
            if lambda_used >= 0.12
            else "balanced sustainability preference"
            if lambda_used >= 0.06
            else "lighter sustainability preference"
        )
        rf_position_label = (
            f"Borrowing at rf: {abs(results['rf_weight']) * 100:.1f}%"
            if results["rf_weight"] < 0
            else f"Risk-free: {results['rf_weight'] * 100:.1f}%"
        )

        st.markdown(
            f"""
            <div class="spotlight-card">
                <div class="section-kicker">Recommended positions</div>
                <h3>{a1["name"]}: {results["w1"] * 100:.1f}% | {a2["name"]}: {results["w2"] * 100:.1f}% | {rf_position_label}</h3>
                <p>
                    GreenVest leans toward <strong>{high_esg_asset}</strong> for sustainability strength while
                    preserving return support from <strong>{high_return_asset}</strong>. With
                    <strong>{gamma_desc}</strong> and a <strong>{lambda_desc}</strong>, the optimiser searches for a cleaner balance between return, risk, and ESG quality.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        metric_row_1 = st.columns(2)
        metric_row_1[0].metric(f"{a1['name']} position", f"{results['w1'] * 100:.2f}%")
        metric_row_1[1].metric(f"{a2['name']} position", f"{results['w2'] * 100:.2f}%")

        metric_row_2 = st.columns(2)
        metric_row_2[0].metric("Risk-free position", f"{results['rf_weight'] * 100:.2f}%")
        metric_row_2[1].metric("Expected return", f"{results['mu_opt'] * 100:.2f}%")

        metric_row_3 = st.columns(2)
        metric_row_3[0].metric("Portfolio risk", f"{results['sigma_opt'] * 100:.2f}%")
        metric_row_3[1].metric("Sharpe ratio", f"{results['sharpe_opt']:.3f}")

        metric_row_4 = st.columns(2)
        metric_row_4[0].metric("ESG score", f"{results['esg_opt'] * 100:.1f} / 100")
        metric_row_4[1].metric("ESG-adjusted Sharpe", f"{results['esg_sharpe_opt']:.3f}")

        metric_row_5 = st.columns(2)
        metric_row_5[0].metric("Objective value", f"{results['utility_opt']:.5f}")
        metric_row_5[1].metric("Impact score", f"{results['impact_score']:.1f}")

        if force_w1 is not None:
            excluded_name = a1["name"] if a1["is_excluded"] else a2["name"]
            remaining_name = a2["name"] if a1["is_excluded"] else a1["name"]
            st.warning(
                f"Hard exclusion applied: {excluded_name} is blocked by the investor rules, so all risky exposure shifts into {remaining_name}."
            )
        elif results["ret_cost"] > 0.5:
            st.info(
                f"Compared with a purely financial benchmark, this sustainable tilt gives up about {results['ret_cost']:.2f}% of expected return."
            )
        else:
            st.success("The current sustainable preference set does not create a meaningful return penalty in this two-asset setup.")
def render_dashboard():
    setup_mode = st.session_state.setup_mode or "manual"
    is_manual_mode = setup_mode == "manual"
    gamma_used = st.session_state.gamma_val
    lambda_used = st.session_state.lambda_val
    e_w = st.session_state.e_w
    s_w = st.session_state.s_w
    g_w = st.session_state.g_w

    utility_cols = st.columns([0.14, 0.62, 0.24], gap="large")
    with utility_cols[0]:
        st.markdown(
            f'<div class="dashboard-utility"><a class="dashboard-home-link" href="?nav=home" target="_self"><img src="{LOGO_DATA_URI}" alt="Go back home"></a></div>',
            unsafe_allow_html=True,
        )
    with utility_cols[2]:
        if st.button("Update Preferences"):
            st.session_state.show_profile_builder = True
            st.session_state.onboarding_step = 1
            st.rerun()

    if st.session_state.show_profile_builder:
        render_profile_builder(editing=st.session_state.onboarding_done)

    top_results_slot = st.container()
    builder_col, insight_col = st.columns([1.34, 0.66], gap="large")
    a1 = None
    a2 = None
    current_signature = None
    snapshot = None

    with builder_col:
        if is_manual_mode:
            st.markdown(
                """
                <div class="section-kicker">Portfolio builder</div>
                <h3 class="section-title">Enter your asset assumptions</h3>
                """,
                unsafe_allow_html=True,
            )

        with st.expander("Advanced controls for gamma and lambda", expanded=False):
            if "_g_sl" not in st.session_state:
                st.session_state._g_sl = st.session_state.gamma_val
            if "_g_ni" not in st.session_state:
                st.session_state._g_ni = st.session_state.gamma_val
            if "_l_sl" not in st.session_state:
                st.session_state._l_sl = st.session_state.lambda_val
            if "_l_ni" not in st.session_state:
                st.session_state._l_ni = st.session_state.lambda_val

            st.caption(
                "Use these only if you want to override the profile-derived risk aversion and ESG preference values."
            )

            gamma_cols = st.columns([4, 1])
            with gamma_cols[0]:
                st.slider(
                    "Risk aversion",
                    1.0,
                    10.0,
                    st.session_state.gamma_val,
                    0.1,
                    key="_g_sl",
                    on_change=sync_gamma_slider,
                    help="Higher gamma means you are more sensitive to portfolio risk.",
                )
            with gamma_cols[1]:
                st.number_input(
                    "gamma exact",
                    1.0,
                    10.0,
                    st.session_state.gamma_val,
                    0.1,
                    key="_g_ni",
                    on_change=sync_gamma_input,
                    label_visibility="collapsed",
                )

            lambda_cols = st.columns([4, 1])
            with lambda_cols[0]:
                st.slider(
                    "ESG preference",
                    0.01,
                    0.20,
                    st.session_state.lambda_val,
                    0.005,
                    key="_l_sl",
                    on_change=sync_lambda_slider,
                    help="Higher lambda gives sustainability a stronger role in the utility score.",
                )
            with lambda_cols[1]:
                st.number_input(
                    "lambda exact",
                    0.01,
                    0.20,
                    st.session_state.lambda_val,
                    0.005,
                    key="_l_ni",
                    on_change=sync_lambda_input,
                    format="%.3f",
                    label_visibility="collapsed",
                )

            st.info(
                f"Active values -> gamma = {st.session_state.gamma_val:.1f} | "
                f"lambda = {st.session_state.lambda_val:.3f}"
            )

        st.write("")
        market_cols = st.columns(2)
        with market_cols[0]:
            rf = st.number_input(
                "Risk-free rate (%)",
                min_value=0.0,
                max_value=20.0,
                value=4.5,
                step=0.1,
            ) / 100
        with market_cols[1]:
            invest = st.number_input(
                "Investment amount (GBP)",
                min_value=100.0,
                max_value=1_000_000.0,
                value=10_000.0,
                step=500.0,
            )

        st.markdown(
            f"""
            <div class="info-note">
                Excluded sectors: <strong>{", ".join(excluded_sector_labels())}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

        excluded_sectors = get_excluded_sectors()
        asset_cols = st.columns(2, gap="medium")
        with asset_cols[0]:
            if is_manual_mode:
                a1 = render_manual_asset_input(1, excluded_sectors)
            else:
                a1 = render_asset_selector(
                    1,
                    excluded_sectors,
                    allowed_modes=["curated", "search"],
                    filter_excluded_curated=True,
                )
        with asset_cols[1]:
            if is_manual_mode:
                a2 = render_manual_asset_input(2, excluded_sectors)
            else:
                a2 = render_asset_selector(
                    2,
                    excluded_sectors,
                    allowed_modes=["curated", "search"],
                    filter_excluded_curated=True,
                )

        if not is_manual_mode and st.session_state.onboarding_done and a1 is not None and a2 is not None:
            st.info(
                f"GreenVest has pre-selected {a1['name']} and {a2['name']} from your preferences. "
                "You can keep them or swap them before generating the portfolio."
            )

        st.write("")
        rho = st.slider(
            "Correlation between the two assets",
            -1.0,
            1.0,
            0.3,
            0.01,
            help="-1 means the assets move opposite to each other. 1 means they move together.",
        )

        if st.session_state.onboarding_done and a1 is not None and a2 is not None:
            snapshot = build_result_snapshot(
                setup_mode,
                rf,
                invest,
                rho,
                gamma_used,
                lambda_used,
                e_w,
                s_w,
                g_w,
                st.session_state.profile,
                st.session_state.goal_label,
                excluded_sector_labels(),
                a1,
                a2,
            )
            current_signature = json.dumps(snapshot, sort_keys=True)

        generate_disabled = current_signature is None
        if st.button("Generate Portfolio", use_container_width=True, disabled=generate_disabled):
            st.session_state.generated_signature = current_signature
            st.rerun()

        if not st.session_state.onboarding_done:
            st.info("Complete your investor preferences popup first, then generate your portfolio.")
        elif a1 is None or a2 is None:
            st.info("Complete both asset sections to unlock the portfolio recommendation.")

    generated = snapshot is not None and st.session_state.generated_signature == current_signature
    package = compute_portfolio_package(snapshot) if generated else None

    with top_results_slot:
        if generated and package is not None:
            render_investor_charts_section(
                package["both_excluded"],
                package["force_w1"],
                package["results"],
                package["a1"],
                package["a2"],
                package["invest"],
                "Investor Charts",
                package["summary_pdf_bytes"],
                package["checkpoint_df"],
                package["benchmark_message_kind"],
                package["benchmark_message_text"],
            )

    with insight_col:
        if generated and package is not None:
            render_portfolio_output_panel(package)
        else:
            st.markdown(
                """
                <div class="section-kicker">Output preview</div>
                <h3 class="section-title">Ready to generate</h3>
                <p class="section-copy">
                    GreenVest will show the full results in a dedicated section above, with the charts, projection table, recommendation, and export materials together.
                </p>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("How GreenVest scores ESG", expanded=False):
                st.markdown(
                    """
                    1. GreenVest starts with the environmental, social, and governance sub-scores entered for each asset.
                    2. Those pillar scores are combined into one composite ESG score using your own E, S, and G priority weights.
                    3. The optimiser chooses risky positions `x1` and `x2`, not weights that must sum to 100%, so the remainder can stay in the risk-free asset.
                    4. The final recommendation maximises `x'(mu - rf) - (gamma / 2) x'Sigma x + lambda * ESG_average`.
                    5. Sector exclusions are enforced so blocked sectors cannot be recommended.
                    """
                )

            if a1 is not None and a2 is not None:
                st.markdown(render_asset_card_html(a1), unsafe_allow_html=True)
                st.markdown(render_asset_card_html(a2), unsafe_allow_html=True)
            elif not st.session_state.onboarding_done:
                st.info("Set your investor preferences first, then complete both assets to unlock the result view.")
            else:
                st.info("Complete both asset sections to prepare the portfolio output section.")


initialize_session_state()
inject_styles()

if get_query_param("view") == "results":
    snapshot = load_result_snapshot(get_query_param("snapshot"))
    if snapshot is None:
        utility_cols = st.columns([0.14, 0.62, 0.24], gap="large")
        with utility_cols[0]:
            st.markdown(
                f'<div class="dashboard-utility"><a class="dashboard-home-link" href="?nav=home" target="_self"><img src="{LOGO_DATA_URI}" alt="Go back home"></a></div>',
                unsafe_allow_html=True,
            )
        st.error("This portfolio result could not be loaded. Generate it again from the builder.")
    else:
        render_results_page(snapshot)
    st.stop()

handle_entry_actions()

if not st.session_state.loader_complete:
    st.session_state.loader_complete = True
    render_loader()
    st.session_state.loader_context = "enter"
elif st.session_state.show_loader:
    render_loader()
    st.session_state.show_loader = False
    st.session_state.loader_context = "enter"

if not st.session_state.entered_app:
    render_landing_page()
    st.stop()


render_dashboard()
