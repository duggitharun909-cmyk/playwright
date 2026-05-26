from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        # headless=True is what you want for deployment on a server!
        # Set to True so it can run invisibly on GitHub Actions.
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Navigating to employee page...")
        page.goto("https://office-tracker-1.vercel.app/employee")

        # Playwright automatically waits for elements to appear before interacting!
        print("Filling in credentials...")
        page.fill("input[type='email']", "talisetty.tarun@gmail.com")
        page.fill("input[type='password']", "Ttsy@2026$%")
        
        # Playwright's clicks send trusted events, which often avoids React quirks,
        # so we may not even need the "double login" trick anymore!
        print("Clicking Sign In...")
        page.click("button:has-text('Sign In')")

        # Wait to see if it redirects and logs in successfully
        print("Waiting for login to process...")
        
        # Playwright handles dynamic waits well, we just wait for the Check In button
        print("Waiting for Check In button...")
        try:
            # Look for a button containing the text "check in" (case insensitive)
            checkin_btn = page.wait_for_selector("button:has-text('Check In'), button:has-text('check in'), button:has-text('CHECK IN')", timeout=20000)
            
            if checkin_btn:
                checkin_btn.click()
                print("Check In button clicked!")
        except Exception as e:
            print("Timeout waiting for Check In button. The page might have refreshed like in Selenium.")
            print("Taking a screenshot of the failure...")
            #page.screenshot(path="playwright_failed_checkin.png")
            
            # If the page refreshed (the React quirk), let's try entering credentials one more time
            print("Trying double-login trick...")
            page.fill("input[type='email']", "duggitharun909@gmail.com")
            page.fill("input[type='password']", "Td@2023*")
            page.click("button:has-text('Sign In')")
            
            # Wait for Check In again
            checkin_btn = page.wait_for_selector("button:has-text('Check In'), button:has-text('check in'), button:has-text('CHECK IN')", timeout=20000)
            checkin_btn.click()
            print("Check In button clicked on second attempt!")
        
        print(f"Current URL: {page.url}")
        
        # Keep browser open for a few seconds to see result before closing
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    run()
