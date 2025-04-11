# streamlit_index1.py
import streamlit as st

def run():
    # everything here stays the same...
    st.sidebar.title("User")
    ...

# streamlit_index1.py
import streamlit as st

# --- Inject CSS for styling ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #454545;
    }
    .section-header {
        font-size: 24px;
        font-weight: 600;
        color: #2a2a2a;
        margin-top: 1.5rem;
    }
    .product-title {
        font-size: 18px;
        font-weight: 600;
        color: #4a4947;
    }
    .status-available {
        color: #23a149;
        font-weight: bold;
    }
    .status-out {
        color: #ea3030;
        font-weight: bold;
    }
    .custom-button {
        background-color: #4a4947;
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        text-align: center;
        font-weight: 500;
        display: inline-block;
    }
    .product-card {
        background-color: #f6f6f6;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("User")
st.sidebar.markdown("**Mariangel Rivero**")
st.sidebar.markdown("### Menu")
st.sidebar.markdown("- Dashboard")
st.sidebar.markdown("- Product (119)")
st.sidebar.markdown("  - Books\n  - E-Books\n  - Borrowed\n  - Loans")
st.sidebar.markdown("- Transaction (441)")
st.sidebar.markdown("- Customers")
st.sidebar.markdown("- Sales Report")
st.sidebar.markdown("### Tools")
st.sidebar.markdown("- Account & Settings")
st.sidebar.markdown("- Help")
st.sidebar.markdown("- Dark Mode")

# --- Page Title ---
st.markdown("## Product")
st.caption("Dashboard > Product > Books")

# --- Search and New Product Button ---
col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("Search for ID or Product Name", "")
with col2:
    st.markdown('<div class="custom-button">New Product</div>', unsafe_allow_html=True)

# --- Filter and Export Buttons ---
filter_col, export_col = st.columns(2)
with filter_col:
    st.markdown('<div class="custom-button">Filter</div>', unsafe_allow_html=True)
with export_col:
    st.markdown('<div class="custom-button">Export</div>', unsafe_allow_html=True)

# --- Tabs ---
tabs = st.tabs(["Books (50)", "E-Books (26)", "Borrowed (121)", "Loaned (21)"])

with tabs[0]:  # Books tab
    st.markdown('<div class="section-header">Book Inventory</div>', unsafe_allow_html=True)

    book_data = [
        {
            "ID": "021231",
            "Name": "My Book Cover",
            "Type": "Borrow",
            "Price": 40,
            "Qty": 234,
            "Date": "04/17/23 at 8:25 PM",
            "Status": "Available",
        },
        {
            "ID": "021232",
            "Name": "Another Book",
            "Type": "Loan",
            "Price": 40,
            "Qty": 234,
            "Date": "04/17/23 at 8:25 PM",
            "Status": "Out of Stock",
        },
    ]

    for book in book_data:
        status_class = "status-available" if book["Status"] == "Available" else "status-out"
        st.markdown(f"""
        <div class="product-card">
            <div class="product-title">{book['Name']} — ${book['Price']}</div>
            <div>ID: {book['ID']} | Type: {book['Type']} | QTY: {book['Qty']}</div>
            <div>Date: {book['Date']}</div>
            <div>Status: <span class="{status_class}">{book['Status']}</span></div>
        </div>
        """, unsafe_allow_html=True)
