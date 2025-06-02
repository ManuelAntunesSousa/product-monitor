import streamlit as st
from streamlit_autorefresh import st_autorefresh
from monitors.site_checker import MONITORS
import time

# === Settings ===
REFRESH_INTERVAL_MINUTES = 1
REFRESH_INTERVAL_MS = REFRESH_INTERVAL_MINUTES * 60 * 1000

# === Set up Streamlit page ===
st.set_page_config(page_title="Product Monitor", page_icon="🛒")
st.title("🛒 ETB Stock Monitor")

# === Auto-refresh every X minutes ===
count = st_autorefresh(interval=REFRESH_INTERVAL_MS, key="auto_refresh")

# === Countdown Timer ===
remaining = int(REFRESH_INTERVAL_MINUTES * 60)
countdown = st.empty()

def format_time(s):
    mins, secs = divmod(s, 60)
    return f"{mins:02d}:{secs:02d}"

for i in range(remaining, 0, -1):
    countdown.markdown(f"⏳ Refreshing in `{format_time(i)}`", unsafe_allow_html=True)
    time.sleep(1)

# === Show results automatically after refresh ===
st.subheader("🧾 Current Stock Status")

for site in MONITORS:
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

# === Optional: Manual trigger ===
if st.button("🔁 Check Again Now"):
    st.experimental_rerun()
