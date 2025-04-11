# streamlit_index2.py
import streamlit as st

def run():
    # your homepage content goes here
    st.markdown('<div class="hero-title">Explore our Top Categories</div>', unsafe_allow_html=True)
    ...

# streamlit_index2.py
import streamlit as st

# --- Inject Global & Index2 CSS ---
st.markdown("""
<!-- Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #454545;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 700;
        text-transform: capitalize;
        color: #011627;
        margin-bottom: 12px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #767070;
        line-height: 1.6;
        margin-bottom: 24px;
    }
    .category-tag {
        font-size: 28px;
        text-transform: capitalize;
        font-weight: 700;
        color: #4a4947;
        margin-top: 16px;
        margin-bottom: 8px;
    }
    .view-all-btn {
        background-color: #d8d2c2;
        border-radius: 11px;
        padding: 12px 24px;
        font-size: 20px;
        color: #4a4947;
        font-weight: 600;
        text-align: center;
        display: inline-block;
        margin-top: 16px;
    }
    .book-card {
        background-color: #ffffff;
        border: 1px solid #cacaca;
        border-radius: 11px;
        padding: 16px;
        margin: 12px 0;
    }
    .book-title {
        font-size: 22px;
        font-weight: 700;
        text-transform: capitalize;
    }
    .book-author {
        font-size: 16px;
        color: #767070;
    }
    .newsletter-box {
        background: linear-gradient(135deg, #faf7f0, #d8d2c2);
        border-radius: 11px;
        padding: 20px;
        text-align: center;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# --- Content ---
st.markdown('<div class="hero-title">Explore our Top Categories</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Browse through a curated list of educational, financial, and technical reads.</div>', unsafe_allow_html=True)

cols = st.columns(2)
with cols[0]:
    st.markdown('<div class="category-tag">📘 Finance Books</div>', unsafe_allow_html=True)
    st.markdown('<div class="category-tag">📗 Engineering Books</div>', unsafe_allow_html=True)
with cols[1]:
    st.markdown('<div class="category-tag">📙 Management Books</div>', unsafe_allow_html=True)
    st.markdown('<div class="category-tag">📕 Commerce Books</div>', unsafe_allow_html=True)

st.markdown('<div class="view-all-btn">View All</div>', unsafe_allow_html=True)

# --- Featured Book Section ---
st.markdown('<div class="hero-title">Featured Book of the Week</div>', unsafe_allow_html=True)
st.markdown("""
    <div class="book-card">
        <div class="book-title">The Mind Connection</div>
        <div class="book-author">by Joyce Meyer</div>
    </div>
""", unsafe_allow_html=True)

# --- Newsletter Box ---
st.markdown("""
    <div class="newsletter-box">
        <h2>Get over 100 Free Books</h2>
        <p>Subscribe to our newsletter and unlock exclusive book access.</p>
    </div>
""", unsafe_allow_html=True)
