from playwright.sync_api import sync_playwright
import time
import os
import json

def _write_json_log(test_name, step_results):
    """Write step_results as JSON into ../logs/<test_name>.json"""
    # __file__ points to tests/generated/test_*.py
    root_dir = os.path.dirname(os.path.dirname(__file__))  # .../playwright_ai
    logs_dir = os.path.join(root_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, f'{test_name}.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(step_results, f, indent=2)
    print(f'JSON log written to: {log_path}')

def test_generated_ui():
    # Use the filename (without .py) as the name for the JSON log.
    test_name = os.path.splitext(os.path.basename(__file__))[0]
    step_results = []  # one entry per click step
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto('http://127.0.0.1:5500/dist/index.html', wait_until='domcontentloaded')
        print('=== START GENERATED COFFEE SHOP TEST ===')
        print('Opening base URL...')
        print('URL:', page.url)
        print('DOM length:', len(page.content()))
        time.sleep(0.5)

        print('\n--- Step 1: CLICK a:has-text(\'Sign In\') ---')
        selector = 'a:has-text(\'Sign In\')'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 1,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n--- Step 2: CLICK a:has-text(\'Sign In\') ---')
        selector = 'a:has-text(\'Sign In\')'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 2,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n--- Step 3: CLICK a:has-text(\'Services\') ---')
        selector = 'a:has-text(\'Services\')'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 3,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n--- Step 4: CLICK a:has-text(\'Services\') ---')
        selector = 'a:has-text(\'Services\')'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 4,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n--- Step 5: CLICK a ---')
        selector = 'a'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 5,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n--- Step 6: CLICK a ---')
        selector = 'a'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 6,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n--- Step 7: CLICK a:has-text(\'Home\') ---')
        selector = 'a:has-text(\'Home\')'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 7,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n--- Step 8: CLICK a:has-text(\'Contact\') ---')
        selector = 'a:has-text(\'Contact\')'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 8,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n--- Step 9: CLICK a:has-text(\'Services\') ---')
        selector = 'a:has-text(\'Services\')'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 9,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n--- Step 10: CLICK a ---')
        selector = 'a'
        start = time.time()
        try:
            page.click(selector, timeout=5000)
            status = 'passed'
            error = ''
        except Exception as e:
            status = 'failed'
            error = str(e)
        duration = time.time() - start
        url = page.url
        dom_length = len(page.content())
        print('STATUS:', status)
        if error:
            print('ERROR:', error)
        print('New URL:', url)
        print('DOM length:', dom_length)
        step_results.append({
            'step': 10,
            'action': 'click',
            'selector': selector,
            'status': status,
            'error': error,
            'duration': duration,
            'url': url,
            'dom_length': dom_length,
        })
        time.sleep(0.5)

        print('\n=== FINISHED GENERATED COFFEE SHOP TEST ===')
        _write_json_log(test_name, step_results)
        browser.close()

if __name__ == '__main__':
    test_generated_ui()
