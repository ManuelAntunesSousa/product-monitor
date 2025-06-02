import schedule
import time
from monitors.site_checker import MONITORS
from notifications.email_alert import send_email

def monitor():
    print("\n🔍 Starting new check...\n")
    for site in MONITORS:
        name = site["name"]
        url = site["url"]
        check_fn = site["check"]
        try:
            if check_fn():
                print(f"✅ {name}: IN STOCK! Sending email...")
                send_email(name, url)
            else:
                print(f"❌ {name}: Not in stock.")
        except Exception as e:
            print(f"⚠️ Error checking {name}: {e}")

schedule.every(5).minutes.do(monitor)

if __name__ == "__main__":
    print("📦 Product monitor started. Checking every 5 minutes...\n")
    monitor()  # run immediately on start
    while True:
        schedule.run_pending()
        time.sleep(1)
