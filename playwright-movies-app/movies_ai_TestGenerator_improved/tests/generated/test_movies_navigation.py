from playwright.sync_api import sync_playwright
import time

def test_movies_navigation():
    print('=== START NAVIGATION TESTS ===')
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto('http://localhost:3000/?category=Popular&page=1', wait_until='domcontentloaded')
        print('Base URL:', page.url)
        print('DOM length:', len(page.content()))
        time.sleep(0.5)

        print('\n--- navigation step 1 (click) ---')
        try:
            page.click('a[href=\'/?category=Popular&page=2\']', timeout=5000)
            print('CLICK a[href=\'/?category=Popular&page=2\'] OK')
            print('URL:', page.url)
            print('DOM length:', len(page.content()))
        except Exception as e:
            print('ERROR:', e)
            errors.append(str(e))
        time.sleep(0.5)

        print('\n=== FINISHED TESTS ===')
        if errors:
            print('\nSome steps failed:')
            for err in errors:
                print(err)
        browser.close()

if __name__ == '__main__':
    test_movies_navigation()
