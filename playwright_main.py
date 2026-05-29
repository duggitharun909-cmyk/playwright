from playwright.sync_api import sync_playwright
import time
import json
import datetime

def check_in_user(email, password):
    with sync_playwright() as p:
        # For testing locally, headless=False lets you see the browser.
        # Change it back to True when you deploy to PythonAnywhere!
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print(f"\nNavigating to employee page for {email}...")
        page.goto("https://office-tracker-1.vercel.app/employee")

        # Playwright automatically waits for elements to appear before interacting!
        print("Filling in credentials...")
        page.fill("input[type='email']", email)
        page.fill("input[type='password']", password)
        
        # Playwright's clicks send trusted events, which often avoids React quirks,
        # so we may not even need the "double login" trick anymore!
        print("Clicking Sign In...")
        page.click("button:has-text('Sign In')")

        # Wait to see if it redirects and logs in successfully
        print("Waiting for login to process...")
        
        # Playwright handles dynamic waits well, we just wait for the Check In button
        print("Waiting for Check In button...")
        try:
            # Wait for EITHER the Check In OR Check Out button
            btn_selector = "button:has-text('Check In'), button:has-text('check in'), button:has-text('Check Out'), button:has-text('check out')"
            action_btn = page.wait_for_selector(btn_selector, timeout=20000)
            
            if action_btn:
                btn_text = action_btn.inner_text().lower()
                if "out" in btn_text:
                    print(f"[{email}] is already checked in! Skipping click to avoid checking out.")
                else:
                    action_btn.click()
                    print(f"[{email}] Check In button clicked!")
        except Exception as e:
            print("Timeout waiting for buttons. The page might have refreshed like in Selenium.")
            
            # If the page refreshed (the React quirk), try entering credentials one more time
            print("Trying double-login trick...")
            page.fill("input[type='email']", email)
            page.fill("input[type='password']", password)
            page.click("button:has-text('Sign In')")
            
            # Wait for buttons again
            action_btn = page.wait_for_selector(btn_selector, timeout=20000)
            if action_btn:
                btn_text = action_btn.inner_text().lower()
                if "out" in btn_text:
                    print(f"[{email}] is already checked in on second attempt! Skipping click.")
                else:
                    action_btn.click()
                    print(f"[{email}] Check In button clicked on second attempt!")
        
        print(f"Finished processing. Current URL: {page.url}")
        
        # Keep browser open for a few seconds to see result before closing
        time.sleep(2)
        browser.close()

def run():
    # Check if it's Saturday (5) or Sunday (6)
    if datetime.datetime.now().weekday() >= 5:
        print("It is the weekend (Saturday or Sunday). Enjoy your day off! Skipping check-ins.")
        return

    print("Loading credentials from credentials.json...")
    try:
        with open('credentials.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        print("Error: credentials.json file not found!")
        return
        
    total_users = len(users)
    print(f"Found {total_users} users to check in.")

    for index, user in enumerate(users):
        name = user.get('name')
        email = user.get('email')
        password = user.get('password')
        
        print(f"\n======================================")
        print(f"Starting check-in process for: {name}")
        print(f"======================================")
        
        try:
            check_in_user(email, password)
        except Exception as e:
            print(f"Failed to check in {name} ({email}): {str(e)}")
            
        # If it's not the last user, wait 2 minutes before doing the next one
        if index < total_users - 1:
            print(f"\nCheck-in for {name} complete. Waiting 2 minutes before the next person...")
            # Wait for 120 seconds (2 minutes)
            time.sleep(30)

    print("\nAll check-ins complete!")

if __name__ == "__main__":
    run()
