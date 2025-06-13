from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # headless=True to hide UI
        page = browser.new_page()

        # Go to a website
        page.goto("https://www.google.com")

        # Accept cookies if needed (Google sometimes shows a consent popup)
        try:
            page.click("text=Accept all")
        except:
            pass

        # Type into search box
        page.fill("input[name='q']", "rasa chatbot")
        page.keyboard.press("Enter")

        # Wait for search results to load
        page.wait_for_selector("h3")

        # Click the first result
        page.click("h3")

        # Let user see the result
        page.wait_for_timeout(5000)

        # Close browser
        browser.close()

run()
