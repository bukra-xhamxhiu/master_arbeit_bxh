from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:5500/dist/index.html" 

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto(BASE_URL, wait_until="domcontentloaded")
        print("Loaded:", page.url)

        page.wait_for_timeout(3000)  # keep browser open 3 seconds

        browser.close()

if __name__ == "__main__":
    main()
