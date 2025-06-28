import json 
from playwright.sync_api import sync_playwright

def run_script(json_script):
    actions = json.loads(json_script)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        page = browser.new_page()

        for step in actions:
            match step["action"]:
                case "goto":
                    page.goto(step["url"])
                case "type":
                    page.fill(step["selector"], step["text"])
                case "click":
                    page.click(step["selector"])
                case "press":
                    page.press(step["selector"], step["key"])
                case "wait":
                    page.wait_for_timeout(step.get("seconds", 2) * 1000)
                case "waitForSelector":
                    page.wait_for_selector(step["selector"])
                case "screenshot":
                    page.screenshot(path=step["path"])
                case "extractText":
                    text = page.locator(step["selector"]).inner_text()
                    print("Extracted text:", text)
                case "scrollIntoView":
                    page.locator(step["selector"]).scroll_into_view_if_needed()
                
        browser.close()

        

