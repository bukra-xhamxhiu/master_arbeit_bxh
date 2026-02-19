from playwright.sync_api import sync_playwright
import time

def test_movies_ui_heuristic():
    print('=== START GENERATED TEST ===')
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        print('Opening base URL...')
        page.goto('http://localhost:3000', wait_until='domcontentloaded')
        print('URL:', page.url)
        print('DOM length:', len(page.content()))
        time.sleep(0.5)

        print('\n=== FINISHED TEST ===')
        if errors:
            print('\nSome steps failed:')
            for err in errors:
                print(err)
        browser.close()

if __name__ == '__main__':
    test_movies_ui_heuristic()
