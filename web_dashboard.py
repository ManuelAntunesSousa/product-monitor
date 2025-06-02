import streamlit as st
from monitors.site_checker import MONITORS

st.set_page_config(page_title="Product Monitor", page_icon="🛒")
st.title("🛒 ETB Stock Monitor")

if st.button("🔍 Check Stock Now"):
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
