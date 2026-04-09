from base64 import b64encode
from datetime import datetime
from io import BytesIO
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
LOGO_PATH = STATIC_DIR / "Sustainable growth and innovation logo.png"
QUESTION_PATH = STATIC_DIR / "question.png"

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

REVIEWS = [
    {
        "author": "Blue Hoirzon",
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
    {"name": "Johnson & Johnson", "ticker": "JNJ", "sector": "Healthcare", "mu": 0.072, "sigma": 0.145, "e": 70, "s": 75, "g": 77},
    {"name": "GSK", "ticker": "GSK", "sector": "Healthcare", "mu": 0.065, "sigma": 0.180, "e": 66, "s": 72, "g": 68},
    {"name": "AstraZeneca", "ticker": "AZN", "sector": "Healthcare", "mu": 0.095, "sigma": 0.195, "e": 74, "s": 78, "g": 76},
    {"name": "Novo Nordisk", "ticker": "NVO", "sector": "Healthcare", "mu": 0.185, "sigma": 0.290, "e": 80, "s": 82, "g": 83},
    {"name": "JPMorgan Chase", "ticker": "JPM", "sector": "Financial Services", "mu": 0.110, "sigma": 0.220, "e": 54, "s": 62, "g": 70},
    {"name": "HSBC", "ticker": "HSBC", "sector": "Financial Services", "mu": 0.082, "sigma": 0.195, "e": 58, "s": 60, "g": 65},
    {"name": "BlackRock", "ticker": "BLK", "sector": "Financial Services", "mu": 0.118, "sigma": 0.230, "e": 65, "s": 67, "g": 74},
    {"name": "Unilever", "ticker": "UL", "sector": "Consumer Goods", "mu": 0.060, "sigma": 0.155, "e": 84, "s": 80, "g": 78},
    {"name": "Nestle", "ticker": "NSRGY", "sector": "Consumer Goods", "mu": 0.058, "sigma": 0.148, "e": 72, "s": 70, "g": 74},
    {"name": "Tesla", "ticker": "TSLA", "sector": "Clean Energy", "mu": 0.220, "sigma": 0.580, "e": 85, "s": 52, "g": 48},
    {"name": "Vestas Wind", "ticker": "VWDRY", "sector": "Clean Energy", "mu": 0.090, "sigma": 0.310, "e": 91, "s": 78, "g": 80},
    {"name": "Orsted", "ticker": "DNNGY", "sector": "Clean Energy", "mu": 0.075, "sigma": 0.280, "e": 93, "s": 76, "g": 79},
    {"name": "Siemens", "ticker": "SIEGY", "sector": "Industrials", "mu": 0.098, "sigma": 0.215, "e": 76, "s": 73, "g": 77},
    {"name": "Schneider Electric", "ticker": "SBGSY", "sector": "Industrials", "mu": 0.112, "sigma": 0.225, "e": 88, "s": 80, "g": 82},
    {"name": "Shell", "ticker": "SHEL", "sector": "Fossil Fuels / Energy", "mu": 0.095, "sigma": 0.240, "e": 38, "s": 50, "g": 58},
    {"name": "BP", "ticker": "BP", "sector": "Fossil Fuels / Energy", "mu": 0.088, "sigma": 0.235, "e": 34, "s": 48, "g": 55},
    {"name": "ExxonMobil", "ticker": "XOM", "sector": "Fossil Fuels / Energy", "mu": 0.100, "sigma": 0.250, "e": 30, "s": 45, "g": 52},
    {"name": "Prologis", "ticker": "PLD", "sector": "Real Estate", "mu": 0.092, "sigma": 0.200, "e": 72, "s": 68, "g": 73},
    {"name": "British American Tobacco", "ticker": "BTI", "sector": "Tobacco", "mu": 0.055, "sigma": 0.175, "e": 28, "s": 32, "g": 55},
    {"name": "Diageo", "ticker": "DEO", "sector": "Alcohol", "mu": 0.068, "sigma": 0.170, "e": 65, "s": 60, "g": 70},
    {"name": "Flutter Entertainment", "ticker": "FLTR.L", "sector": "Gambling", "mu": 0.078, "sigma": 0.290, "e": 40, "s": 45, "g": 58},
    {"name": "BAE Systems", "ticker": "BAESY", "sector": "Weapons / Defence", "mu": 0.120, "sigma": 0.230, "e": 35, "s": 55, "g": 62},
    {"name": "Lockheed Martin", "ticker": "LMT", "sector": "Weapons / Defence", "mu": 0.108, "sigma": 0.195, "e": 32, "s": 52, "g": 60},
]

CURATED_BY_TICKER = {asset["ticker"]: asset for asset in CURATED_ASSETS}
CURATED_NAMES = [f'{asset["name"]} ({asset["ticker"]})' for asset in CURATED_ASSETS]


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


def go_home():
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
    clear_query_params()
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
                gap: 0.18rem;
            }

            .hero-logo {
                width: 76px;
                height: 76px;
                object-fit: contain;
                filter: drop-shadow(0 10px 20px rgba(31, 88, 58, 0.16));
                flex-shrink: 0;
                transform: translateY(0);
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

            .hero-brand-copy .hero-kicker {
                margin-bottom: 0.1rem;
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
                font-size: clamp(2.9rem, 5vw, 4.2rem);
                margin: 0.2rem 0 0.5rem;
                line-height: 0.95;
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
                gap: 0.95rem;
                margin-bottom: 0.75rem;
            }

            .hero-action-form {
                margin: 0;
            }

            .hero-button {
                appearance: none;
                text-decoration: none !important;
                color: white !important;
                font-weight: 800;
                padding: 0.95rem 1.45rem;
                border-radius: 18px;
                min-width: 230px;
                text-align: center;
                box-shadow: 0 20px 30px rgba(37, 100, 68, 0.16);
                border: 1px solid rgba(255, 255, 255, 0.46);
                cursor: pointer;
                font-family: "Manrope", "Trebuchet MS", sans-serif;
                font-size: 1.03rem;
            }

            .hero-button.green {
                background: linear-gradient(135deg, #257449 0%, #4eb772 100%);
            }

            .hero-button.blue {
                background: linear-gradient(135deg, #2d76cf 0%, #5cb8ef 100%);
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
                background: linear-gradient(135deg, #256e45, #49a96b);
                color: white;
                font-weight: 700;
                padding: 0.7rem 1rem;
                box-shadow: 0 14px 22px rgba(37, 100, 68, 0.12);
            }

            .stButton > button:hover {
                color: white !important;
                border-color: rgba(46, 123, 83, 0.16);
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
                padding: 1rem 1.05rem;
                box-shadow: 0 14px 24px rgba(24, 60, 43, 0.06);
                margin-top: 1rem;
            }

            .projection-card h4 {
                margin: 0.2rem 0 0.55rem;
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
    st.markdown(
        f"""
        <div class="loader-overlay">
            <img class="loader-logo" src="{LOGO_DATA_URI}" alt="GreenVest logo">
            <div class="loader-title">GreenVest</div>
            <div class="loader-copy">Loading your sustainable investing workspace</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def p_return(w1, mu1, mu2):
    return w1 * mu1 + (1 - w1) * mu2


def p_std(w1, s1, s2, rho):
    return np.sqrt(w1**2 * s1**2 + (1 - w1) ** 2 * s2**2 + 2 * rho * w1 * (1 - w1) * s1 * s2)


def p_esg(w1, e1, e2):
    return w1 * e1 + (1 - w1) * e2


def p_util(mu, sig, esg, gamma, lam):
    return mu - (gamma / 2) * sig**2 + lam * esg


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


def optimise(mu1, mu2, s1, s2, e1, e2, rho, gamma, lam, n=2000, force_w1=None):
    if force_w1 is not None:
        weights = np.array([force_w1])
        mu_grid = p_return(weights, mu1, mu2)
        sigma_grid = p_std(weights, s1, s2, rho)
        esg_grid = p_esg(weights, e1, e2)
        utility_grid = p_util(mu_grid, sigma_grid, esg_grid, gamma, lam)
        return weights, mu_grid, sigma_grid, esg_grid, utility_grid, mu_grid + lam * esg_grid, 0

    weights = np.linspace(0, 1, n)
    mu_grid = p_return(weights, mu1, mu2)
    sigma_grid = p_std(weights, s1, s2, rho)
    esg_grid = p_esg(weights, e1, e2)
    utility_grid = p_util(mu_grid, sigma_grid, esg_grid, gamma, lam)
    idx = np.argmax(utility_grid)
    return weights, mu_grid, sigma_grid, esg_grid, utility_grid, mu_grid + lam * esg_grid, idx


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
    ax.set_ylabel("ESG-adjusted return")
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
            label="Balanced 50 / 50 reference",
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
                f"Recommended allocation: {asset_one['name']} {results['w1'] * 100:.1f}%   |   "
                f"{asset_two['name']} {results['w2'] * 100:.1f}%"
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
        allocation_names = [asset_one["name"], asset_two["name"]]
        allocation_values = [results["w1"] * 100, results["w2"] * 100]
        allocation_colors = ["#2e7b53", "#2f7dca"]
        positions = np.arange(len(allocation_names))
        ax_alloc.barh(positions, allocation_values, color=allocation_colors, height=0.45)
        ax_alloc.set_yticks(positions, allocation_names)
        ax_alloc.set_xlim(0, 100)
        ax_alloc.set_xlabel("Portfolio weight (%)")
        ax_alloc.set_title("Recommended allocation", fontsize=13.5, fontweight="bold", color="#163a2a", pad=12)
        for idx, value in enumerate(allocation_values):
            ax_alloc.text(value + 2, idx, f"{value:.1f}%", va="center", fontsize=10.2, color="#224d38")

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
                label="Balanced 50 / 50 reference",
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
            f"Expected return: {results['mu_opt'] * 100:.2f}%",
            f"Portfolio risk: {results['sigma_opt'] * 100:.2f}%",
            f"Sharpe ratio: {results['sharpe_opt']:.3f}",
            f"ESG score: {results['esg_opt'] * 100:.1f} / 100 [{esg_rating(results['esg_opt'])}]",
            f"Impact score: {results['impact_score']:.1f}",
            f"Trade-off score: {results['tradeoff']:.4f}",
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


def render_investor_charts_section(both_excluded, force_w1, results, a1, a2, invest, title, summary_pdf_bytes):
    st.write("")
    header_cols = st.columns([1.35, 0.65], gap="large")
    with header_cols[0]:
        st.markdown(
            f"""
            <div class="section-kicker">{title}</div>
            <h3 class="section-title">{title}</h3>
            <p class="section-copy">
                These charts highlight the portfolio recommendation and its long-term projection in a cleaner,
                more presentation-ready format.
            </p>
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
            '<div class="chart-caption">Projected values use the current assumptions from the builder below, so investors can compare recommendations instantly.</div>',
            unsafe_allow_html=True,
        )


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


def sync_gamma_input():
    st.session_state.gamma_val = st.session_state._g_ni


def sync_lambda_slider():
    st.session_state.lambda_val = st.session_state._l_sl


def sync_lambda_input():
    st.session_state.lambda_val = st.session_state._l_ni


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
        sector = st.selectbox(
            "Sector",
            SECTORS,
            index=0 if asset_num == 1 else 1,
            key=f"manual_sector_{asset_num}",
        )
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
        "sector": sector,
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
    st.session_state.show_profile_builder = False
    st.session_state.onboarding_step = 1
    st.session_state.generated_signature = None
    st.rerun()


@st.dialog("Investor Preferences", width="large")
def render_profile_builder(editing=False):
    total_steps = 5
    step = st.session_state.onboarding_step
    is_manual_mode = st.session_state.setup_mode == "manual"
    heading = "Investor Preference Builder" if not editing else "Update Investor Preferences"
    if editing:
        body = "Adjust the profile inline and then click generate again to refresh the portfolio."
    elif is_manual_mode:
        body = "Set the investor preferences first, then enter your own expected returns, risk, and ESG assumptions."
    else:
        body = "Complete the investor profile first, then choose eligible assets and generate the portfolio."

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
    content_col, mascot_col = st.columns([1.28, 0.32], gap="large")

    with mascot_col:
        st.markdown(
            f"""
            <div class="guide-mascot-card">
                <div class="section-kicker">Investor guide</div>
                <h4>Preference helper</h4>
                <p>
                    Use this area to guide the investor through the answers that shape risk,
                    sustainability priorities, and sector exclusions.
                </p>
                <img class="guide-mascot-image" src="{QUESTION_DATA_URI}" alt="Question mascot">
            </div>
            """,
            unsafe_allow_html=True,
        )

    with content_col:
        st.progress(step / total_steps)
        st.caption(f"Step {step} of {total_steps}")
        st.write("")

        if step == 1:
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
            )
            st.caption("This tells GreenVest how much short-term volatility feels comfortable for the investor.")
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
            choice = st.radio(
                "How long does the investor plan to stay invested?",
                options=[1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Less than 2 years",
                    2: "2 to 5 years",
                    3: "5 to 10 years",
                    4: "10 years or more",
                }[x],
                index=st.session_state.q3 - 1,
            )
            st.caption(
                "A longer horizon allows GreenVest to tolerate more short-term movement for better long-term upside."
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
            choice = st.radio(
                "What is the investor working toward?",
                options=[1, 2, 3, 4],
                format_func=lambda x: {
                    1: "Retirement - long-term financial security",
                    2: "Long-term growth - compounding wealth over time",
                    3: "Ethical investing - sustainability alongside returns",
                    4: "Short-term profit - stronger near-term gains",
                }[x],
                index=st.session_state.goal - 1,
            )
            st.caption("This final objective helps decide how much explicit weight ESG receives in the utility score.")
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
            st.markdown("#### How much should GreenVest care about each ESG pillar?")
            st.caption("Set each pillar from 0 to 5. These weights shape the composite ESG score.")
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
                            <div class="hero-kicker">Welcome to GreenVest</div>
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
                <h4>What sustainable investing means</h4>
                <p>
                    Sustainable investing looks at financial return alongside environmental, social,
                    and governance performance. Instead of asking only "what could this earn?",
                    it also asks "how is this business being run, and what risks or opportunities does that create?"
                </p>
            </div>
            <div class="fact-card">
                <div class="section-kicker">Why It Matters</div>
                <h4>Why it matters</h4>
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
                    <h3>Scrolling social proof for the welcome page</h3>
                </div>
                <div class="hero-note">Reviews drift left to right and fade softly at the edges.</div>
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
    action = get_query_param("launch")
    if action == "manual":
        st.session_state.entered_app = True
        st.session_state.onboarding_done = False
        st.session_state.setup_mode = "manual"
        st.session_state.show_profile_builder = True
        st.session_state.onboarding_step = 1
        st.session_state.generated_signature = None
        clear_query_params()
        st.rerun()

    if action == "guided":
        st.session_state.entered_app = True
        st.session_state.show_profile_builder = True
        st.session_state.setup_mode = "guided"
        st.session_state.onboarding_step = 1
        st.session_state.onboarding_done = False
        st.session_state.generated_signature = None
        clear_query_params()
        st.rerun()


def render_dashboard():
    setup_mode = st.session_state.setup_mode or "manual"
    is_manual_mode = setup_mode == "manual"
    gamma_used = st.session_state.gamma_val
    lambda_used = st.session_state.lambda_val
    e_w = st.session_state.e_w
    s_w = st.session_state.s_w
    g_w = st.session_state.g_w
    mode_title = "Create your sustainable portfolio" if is_manual_mode else "Generate a portfolio from investor preferences"
    mode_copy = (
        "Enter your own expected returns, standard deviations, and ESG assumptions, then click generate."
        if is_manual_mode
        else "Choose eligible assets, then click generate to turn the investor profile into a recommended portfolio."
    )

    st.markdown(
        f"""
        <section class="dashboard-hero">
            <div class="dashboard-head">
                <div>
                    <h2 class="dashboard-title">{mode_title}</h2>
                    <p class="dashboard-copy">{mode_copy}</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    top_actions = st.columns([1, 1, 1], gap="large")
    with top_actions[0]:
        if st.button("Go Back Home"):
            go_home()
    with top_actions[2]:
        if st.button("Update Preferences"):
            st.session_state.show_profile_builder = True
            st.session_state.onboarding_step = 1
            st.rerun()

    if st.session_state.show_profile_builder:
        render_profile_builder(editing=st.session_state.onboarding_done)

    charts_slot = st.container()
    builder_col, insight_col = st.columns([1.08, 0.92], gap="large")

    current_signature = None
    a1 = None
    a2 = None
    projection_slot = None

    with builder_col:
        builder_heading = "Enter your asset assumptions" if is_manual_mode else "Choose the assets to compare"
        builder_copy = (
            "This path is for investors who want to enter their own expected returns, risk levels, and ESG inputs."
            if is_manual_mode
            else "This path uses the investor profile to guide the optimisation while you choose from eligible assets."
        )
        st.markdown(
            f"""
            <div class="section-kicker">Portfolio builder</div>
            <h3 class="section-title">{builder_heading}</h3>
            <p class="section-copy">{builder_copy}</p>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Advanced controls for gamma and lambda", expanded=False):
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
                    help="Higher gamma means the investor is more sensitive to portfolio risk.",
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
        if is_manual_mode:
            a1 = render_manual_asset_input(1, excluded_sectors)
            st.write("")
            a2 = render_manual_asset_input(2, excluded_sectors)
        else:
            a1 = render_asset_selector(1, excluded_sectors, allowed_modes=["curated", "search"], filter_excluded_curated=True)
            st.write("")
            a2 = render_asset_selector(2, excluded_sectors, allowed_modes=["curated", "search"], filter_excluded_curated=True)

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
            st.info("Complete the investor preferences popup first, then generate the portfolio.")
        elif a1 is None or a2 is None:
            st.info("Complete both asset sections to unlock the portfolio recommendation.")
        elif st.session_state.generated_signature != current_signature:
            st.info("Click Generate Portfolio to show the latest recommendation, projection, and charts.")

        projection_slot = st.container()

    if a1 is None or a2 is None:
        with charts_slot:
            st.markdown(
                """
                <div class="section-kicker">Investor Charts</div>
                <h3 class="section-title">Investor Charts</h3>
                <p class="section-copy">
                    Complete both asset selections to unlock the ESG efficient frontier and future value view.
                </p>
                """,
                unsafe_allow_html=True,
            )
            st.info("Choose two assets first, then click generate to display the charts and recommendation.")
        with insight_col:
            st.markdown(
                """
                <div class="section-kicker">Portfolio recommendation</div>
                <h3 class="section-title">Portfolio output</h3>
                <p class="section-copy">
                    The portfolio recommendation appears here after the investor preferences are complete and both assets have been entered.
                </p>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("How GreenVest scores ESG", expanded=False):
                st.markdown(
                    """
                    1. GreenVest starts with the environmental, social, and governance sub-scores entered for each asset.
                    2. Those pillar scores are combined into one composite ESG score using the investor's own E, S, and G priority weights.
                    3. The final portfolio recommendation is chosen by the utility formula `U = mu - (gamma / 2) * sigma^2 + lambda * ESG`.
                    4. Sector exclusions are enforced so blocked sectors cannot be recommended.
                    """
                )
        return

    generated = st.session_state.generated_signature == current_signature
    if not generated:
        with charts_slot:
            st.markdown(
                """
                <div class="section-kicker">Investor Charts</div>
                <h3 class="section-title">Investor Charts</h3>
                <p class="section-copy">
                    Click generate to show the ESG efficient frontier, future value chart, and export button.
                </p>
                """,
                unsafe_allow_html=True,
            )
            st.info("The charts appear after the investor clicks Generate Portfolio.")
        with insight_col:
            st.markdown(
                """
                <div class="section-kicker">Portfolio recommendation</div>
                <h3 class="section-title">Portfolio output</h3>
                <p class="section-copy">
                    The recommendation, metrics, and narrative appear here after generation.
                </p>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("How GreenVest scores ESG", expanded=False):
                st.markdown(
                    """
                    1. GreenVest starts with the environmental, social, and governance sub-scores entered for each asset.
                    2. Those pillar scores are combined into one composite ESG score using the investor's own E, S, and G priority weights.
                    3. The final portfolio recommendation is chosen by the utility formula `U = mu - (gamma / 2) * sigma^2 + lambda * ESG`.
                    4. Sector exclusions are enforced so blocked sectors cannot be recommended.
                    """
                )
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

    if not both_excluded:
        weights, mu_grid, sigma_grid, esg_grid, utility_grid, esg_adjusted_grid, idx = optimise(
            a1["mu"],
            a2["mu"],
            a1["sigma"],
            a2["sigma"],
            a1["esg_a"],
            a2["esg_a"],
            rho,
            gamma_used,
            lambda_used,
            force_w1=force_w1,
        )

        w1 = float(weights[idx])
        w2 = 1 - w1
        mu_opt = float(mu_grid[idx])
        sigma_opt = float(sigma_grid[idx])
        esg_opt = float(esg_grid[idx])
        utility_opt = float(utility_grid[idx])
        sharpe_opt = (mu_opt - rf) / sigma_opt if sigma_opt > 0 else float("nan")
        esg_sharpe_opt = esg_sharpe(mu_opt, rf, sigma_opt, lambda_used, esg_opt)
        impact_score = round(esg_opt * 100, 1)
        tradeoff = lambda_used * esg_opt - gamma_used * sigma_opt

        benchmark_return = None
        ret_cost = 0.0
        idx_financial = None
        idx_low_risk = None
        mu_50 = None

        if force_w1 is None:
            _, mu_ms, sigma_ms, esg_ms, _, esg_adjusted_ms, idx_financial = optimise(
                a1["mu"],
                a2["mu"],
                a1["sigma"],
                a2["sigma"],
                a1["esg_a"],
                a2["esg_a"],
                rho,
                gamma_used,
                0.0,
            )
            idx_low_risk = int(np.argmin(sigma_grid))
            benchmark_return = p_return(0.5, a1["mu"], a2["mu"])
            mu_50 = benchmark_return
            ret_cost = mu_ms[idx_financial] * 100 - mu_opt * 100
        else:
            mu_ms = sigma_ms = esg_adjusted_ms = None

        results = {
            "weights": weights,
            "mu_grid": mu_grid,
            "sigma_grid": sigma_grid,
            "esg_grid": esg_grid,
            "esg_adjusted_grid": esg_adjusted_grid,
            "idx": idx,
            "w1": w1,
            "w2": w2,
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
            "mu_50": mu_50,
        }

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
            checkpoint_df["50 / 50"] = [
                f"GBP {future_value(invest, results['benchmark_return'], year):,.0f}" for year in checkpoint_years
            ]
            recommendation_30 = future_value(invest, results["mu_opt"], 30)
            benchmark_30 = future_value(invest, results["benchmark_return"], 30)
            if recommendation_30 > benchmark_30:
                benchmark_message_kind = "success"
                benchmark_message_text = (
                    f"GreenVest is projected to outperform the 50 / 50 reference by GBP {recommendation_30 - benchmark_30:,.0f} over 30 years."
                )
            elif benchmark_30 > recommendation_30:
                benchmark_message_kind = "info"
                benchmark_message_text = (
                    f"The 50 / 50 reference projects GBP {benchmark_30 - recommendation_30:,.0f} more over 30 years under the current assumptions."
                )
            else:
                benchmark_message_kind = "info"
                benchmark_message_text = "GreenVest and the 50 / 50 reference project the same 30-year value under the current assumptions."

    with charts_slot:
        if both_excluded:
            st.markdown(
                """
                <div class="section-kicker">Investor Charts</div>
                <h3 class="section-title">Investor Charts</h3>
                <p class="section-copy">
                    The chart area is ready, but both selected assets are blocked by the current sector exclusions.
                </p>
                """,
                unsafe_allow_html=True,
            )
            st.error("Both selected assets are excluded, so GreenVest cannot generate the ESG efficient frontier.")
        else:
            render_investor_charts_section(
                both_excluded,
                force_w1,
                results,
                a1,
                a2,
                invest,
                "Investor Charts",
                summary_pdf_bytes,
            )

    with projection_slot:
        if both_excluded:
            st.markdown(
                """
                <div class="projection-card">
                    <div class="section-kicker">Projection</div>
                    <h4>Projection checkpoints</h4>
                    <p class="section-copy">Projection values will appear here once at least one selected asset is eligible for recommendation.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="projection-card">
                    <div class="section-kicker">Projection</div>
                    <h4>Projection checkpoints</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if benchmark_message_text:
                if benchmark_message_kind == "success":
                    st.success(benchmark_message_text)
                else:
                    st.info(benchmark_message_text)
            st.dataframe(checkpoint_df, use_container_width=True, hide_index=True)

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
                2. Those pillar scores are combined into one composite ESG score using the investor's own E, S, and G priority weights.
                3. The final portfolio recommendation is chosen by the utility formula `U = mu - (gamma / 2) * sigma^2 + lambda * ESG`.
                4. Sector exclusions are enforced so blocked sectors cannot be recommended.
                """
            )

        if both_excluded:
            st.error(
                "Both selected assets sit inside excluded sectors. Update the exclusions or choose different assets."
            )
            return

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

        st.markdown(
            f"""
            <div class="spotlight-card">
                <div class="section-kicker">Recommended mix</div>
                <h3>{a1["name"]}: {results["w1"] * 100:.1f}% | {a2["name"]}: {results["w2"] * 100:.1f}%</h3>
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
        metric_row_1[0].metric("Expected return", f"{results['mu_opt'] * 100:.2f}%")
        metric_row_1[1].metric("Portfolio risk", f"{results['sigma_opt'] * 100:.2f}%")

        metric_row_2 = st.columns(2)
        metric_row_2[0].metric("Sharpe ratio", f"{results['sharpe_opt']:.3f}")
        metric_row_2[1].metric("ESG score", f"{results['esg_opt'] * 100:.1f} / 100")

        metric_row_3 = st.columns(2)
        metric_row_3[0].metric("ESG-adjusted Sharpe", f"{results['esg_sharpe_opt']:.3f}")
        metric_row_3[1].metric("Impact score", f"{results['impact_score']:.1f}")

        metric_row_4 = st.columns(2)
        metric_row_4[0].metric("Trade-off score", f"{results['tradeoff']:.4f}")
        metric_row_4[1].metric("Utility value", f"{results['utility_opt']:.5f}")

        if force_w1 is not None:
            excluded_name = a1["name"] if a1["is_excluded"] else a2["name"]
            remaining_name = a2["name"] if a1["is_excluded"] else a1["name"]
            st.warning(
                f"Hard exclusion applied: {excluded_name} is blocked by the investor rules, so the portfolio moves fully into {remaining_name}."
            )
        elif results["ret_cost"] > 0.5:
            st.info(
                f"Compared with a purely financial benchmark, this sustainable tilt gives up about {results['ret_cost']:.2f}% of expected return."
            )
        else:
            st.success("The current sustainable preference set does not create a meaningful return penalty in this two-asset setup.")


initialize_session_state()
inject_styles()
handle_entry_actions()

if not st.session_state.loader_complete:
    st.session_state.loader_complete = True
    render_loader()

if not st.session_state.entered_app:
    render_landing_page()
    st.stop()


render_dashboard()
