# # import json 
# # from playwright.sync_api import sync_playwright
# # from gpt_parser import new_instructions

# # def run_script(json_script, og_prompt):
# #     actions = json.loads(json_script)
# #     with sync_playwright() as p:
# #         browser = p.chromium.launch(headless=False, slow_mo=600)
# #         page = browser.new_page()

# #         last_url = "https://www.google.com"
# #         last_title = None
# #         step_history = []

# #         for step in actions:
# #             step_history.append(step)
# #             match step["action"]:
# #                 case "goto":
# #                     page.goto(step["url"])
# #                 case "type":
# #                     page.fill(step["selector"], step["text"])
# #                 case "click":
# #                     page.click(step["selector"])
# #                 case "press":
# #                     page.press(step["selector"], step["key"])
# #                 case "wait":
# #                     page.wait_for_timeout(step.get("seconds", 2) * 1000)
# #                 case "waitForSelector":
# #                     page.wait_for_selector(step["selector"])
# #                 case "screenshot":
# #                     page.screenshot(path=step["path"])
# #                 case "extractText":
# #                     text = page.locator(step["selector"]).inner_text()
# #                     print("Extracted text:", text)
# #                 case "scrollIntoView":
# #                     page.locator(step["selector"]).scroll_into_view_if_needed()

# #             curr_url = page.url
# #             curr_title = page.title()

# #             if last_url and (curr_url != last_url or curr_title != last_title):
# #                 print(f"\n🔄 Detected new page: {curr_title} ({curr_url})")
# #                 dom_summary = summarize_dom(page)
# #                 next_json = new_instructions(og_prompt, curr_url, curr_title, dom_summary, step_history)
# #                 run_script(next_json, og_prompt)  # recursive call
# #                 return  # prevent double-close

# #             last_url = curr_url
# #             last_title = curr_title
                
# #         #browser.close()


# # def summarize_dom(page, max_elements=50):
# #     elements = page.locator("body *").all()
# #     summary = []

# #     for el in elements[:max_elements]:
# #         try:
# #             if el.is_visible():
# #                 tag = el.evaluate("el => el.tagName")
# #                 text = el.inner_text().strip()
# #                 attrs = el.evaluate("el => ({ id: el.id, name: el.name, class: el.className, placeholder: el.placeholder })")
# #                 summary.append({ "tag": tag, "text": text, "attrs": attrs })
# #         except:
# #             continue

# #     return summary
   

import json 
from playwright.sync_api import sync_playwright
from gpt_parser import new_instructions


def run_script(json_script, og_prompt):
    from playwright.sync_api import sync_playwright
    import json
    from gpt_parser import new_instructions

    actions = json.loads(json_script)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=600)
        page = browser.new_page()

        last_url = "https://placeholder.local"
        last_title = ""
        step_history = []

        while True:
            for step in actions:
                print("▶️ Executing:", step)
                step_history.append(step)

                try:
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
                except Exception as e:
                    print("Error during step:", e)
                    return

                # Check for page change immediately after this step
                curr_url = page.url
                curr_title = page.title()

                if curr_url != last_url or curr_title != last_title:
                    print(f"\n🔄 Detected new page: {curr_title} ({curr_url})")
                    dom_summary = summarize_dom(page)
                    next_json = new_instructions(og_prompt, curr_url, curr_title, dom_summary, step_history)
                    try:
                        actions = json.loads(next_json)
                        last_url = curr_url
                        last_title = curr_title
                        break  # break out of for-loop and restart with new actions
                    except Exception as e:
                        print("Failed to parse next actions:", e)
                        return
            else:
                #If for-loop finished without breaking (i.e., no new page), stop
                break


        browser.close()


def summarize_dom(page, max_elements=50):
    elements = page.locator("body *").all()
    summary = []

    for el in elements[:max_elements]:
        try:
            if el.is_visible():
                tag = el.evaluate("el => el.tagName")
                text = el.inner_text().strip()
                attrs = el.evaluate("el => ({ id: el.id, name: el.name, class: el.className, placeholder: el.placeholder })")
                summary.append({ "tag": tag, "text": text, "attrs": attrs })
        except:
            continue

    return summary
