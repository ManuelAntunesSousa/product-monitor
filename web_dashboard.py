import streamlit as st
from streamlit_autorefresh import st_autorefresh
from monitors.site_checker import PRODUCTS
import datetime

# === Config ===
REFRESH_INTERVAL_MINUTES = 1
REFRESH_INTERVAL_MS = REFRESH_INTERVAL_MINUTES * 60 * 1000

# === Streamlit Setup ===
st.set_page_config(page_title="Product Monitor", page_icon="🛒")
st.title("🛒 ETB Scarlet & Violet - White Flare Stock Monitor")

# === Trigger auto-refresh ===
st_autorefresh(interval=REFRESH_INTERVAL_MS, key="auto_refresh")

# === Show next refresh time ===
now = datetime.datetime.now()
next_refresh = now + datetime.timedelta(minutes=REFRESH_INTERVAL_MINUTES)
st.info(f"🔄 Auto-refreshing at **{next_refresh.strftime('%H:%M:%S')}**")

# === Stock Check Results ===
for product, sites in PRODUCTS.items():
    st.subheader(f"📦 {product}")
    for site in sites:
        name = site["name"]
        url = site["url"]
        check_fn = site["check"]
        try:
            if check_fn():
                st.success(f"✅ {name}: IN STOCK!")
                st.markdown(f"[Buy Now]({url})")
            else:
                st.warning(f"❌ {name}: Not in stock.")
        except Exception as e:
            st.error(f"⚠️ Error checking {name}: {e}")

# === Manual Refresh Button ===
if st.button("🔁 Check Again Now"):
    st.experimental_rerun()
