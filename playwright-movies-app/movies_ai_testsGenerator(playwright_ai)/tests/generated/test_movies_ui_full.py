import time
import traceback
from playwright.sync_api import sync_playwright

def test_generated():
    print('=== START GENERATED TEST ===')
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        print('Opening base URL...')
        page.goto('http://localhost:5500/dist/index.html')
        print('URL:', page.url)
        print('DOM length:', len(page.content()))

        print("\n--- Step 1: CLICK button:has-text("☀") ---")
        start = time.time()
        try:
            page.click("button:has-text("☀")", timeout=3000)
            duration = round(time.time() - start, 3)
            print('SUCCESS: Clicked button:has-text("☀") in', duration, 'seconds')
            print('New URL:', page.url)
            print('DOM length:', len(page.content()))
        except Exception as e:
            print('ERROR: Failed to click selector:', e)
            errors.append(traceback.format_exc())
            print('Stacktrace logged.')
        print("\n--- Step 2: CLICK button:has-text("☾") ---")
        start = time.time()
        try:
            page.click("button:has-text("☾")", timeout=3000)
            duration = round(time.time() - start, 3)
            print('SUCCESS: Clicked button:has-text("☾") in', duration, 'seconds')
            print('New URL:', page.url)
            print('DOM length:', len(page.content()))
        except Exception as e:
            print('ERROR: Failed to click selector:', e)
            errors.append(traceback.format_exc())
            print('Stacktrace logged.')
        print("\n--- Step 3: CLICK a:has-text("Page 2") ---")
        start = time.time()
        try:
            page.click("a:has-text("Page 2")", timeout=3000)
            duration = round(time.time() - start, 3)
            print('SUCCESS: Clicked a:has-text("Page 2") in', duration, 'seconds')
            print('New URL:', page.url)
            print('DOM length:', len(page.content()))
        except Exception as e:
            print('ERROR: Failed to click selector:', e)
            errors.append(traceback.format_exc())
            print('Stacktrace logged.')

        print('\n=== FINISHED TEST ===')
        if errors:
            print('\n!!! ERRORS OCCURRED DURING TEST !!!')
            for err in errors:
                print(err)

        browser.close()

if __name__ == '__main__':
    test_generated()
