from playwright.sync_api import sync_playwright
import time

def test_movies_actions():
    print('=== START ACTIONS TESTS ===')
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto('http://localhost:3000/?category=Popular&page=1', wait_until='domcontentloaded')
        print('Base URL:', page.url)
        print('DOM length:', len(page.content()))
        time.sleep(0.5)

        print('\n--- actions step 1 (scroll) ---')
        try:
            page.mouse.wheel(0, 1000)
            print('SCROLL by 1000')
            print('URL:', page.url)
            print('DOM length:', len(page.content()))
        except Exception as e:
            print('ERROR:', e)
            errors.append(str(e))
        time.sleep(0.5)

        print('\n--- actions step 2 (click) ---')
        try:
            page.click('button:has-text("☀")', timeout=5000)
            print('CLICK button:has-text("☀") OK')
            print('URL:', page.url)
            print('DOM length:', len(page.content()))
        except Exception as e:
            print('ERROR:', e)
            errors.append(str(e))
        time.sleep(0.5)

        print('\n--- actions step 3 (scroll) ---')
        try:
            page.mouse.wheel(0, 1000)
            print('SCROLL by 1000')
            print('URL:', page.url)
            print('DOM length:', len(page.content()))
        except Exception as e:
            print('ERROR:', e)
            errors.append(str(e))
        time.sleep(0.5)

        print('\n--- actions step 4 (click) ---')
        try:
            page.click('button:has-text("☀")', timeout=5000)
            print('CLICK button:has-text("☀") OK')
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
    test_movies_actions()
