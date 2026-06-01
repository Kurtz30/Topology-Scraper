import time
from playwright.sync_api import sync_playwright

CHROMIUM_PATH = "/usr/bin/chromium-browser"
URL = "https://portal.topologyinteriors.com/project/698d02b49035c168f2d2cf3b/products"

def capture_session():
    with sync_playwright() as p:
        print("Launching browser. Please log in manually...")
        browser = p.chromium.launch(executable_path=CHROMIUM_PATH, headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto(URL)

        print("\n--> WAITING FOR YOU TO LOG IN INTERACTIVELY <--")
        print("Once you see your product list page fully loaded, just wait...")
        
        # 90 seconds to input email, check mail, and click the magic link
        time.sleep(90) 

        # Save complete session state (Cookies + LocalStorage)
        context.storage_state(path="auth.json")
        print("\nSession successfully captured and saved to 'auth.json'!")
        
        browser.close()

if __name__ == "__main__":
    capture_session()
