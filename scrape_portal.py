import json
import time
import pandas as pd
from playwright.sync_api import sync_playwright

# Configuration
URL = "https://portal.topologyinteriors.com/project/698d02b49035c168f2d2cf3b/products"
AUTH_FILE = "auth.json"
OUTPUT_FILE = "products_expanded.csv"
CHROMIUM_PATH = "/usr/bin/chromium-browser"

def clean_text(text):
    """Helper to normalize whitespace and strip messy layout tabs/newlines."""
    if text:
        return " ".join(text.split()).strip()
    return ""

def scrape_portal():
    products_data = []

    with sync_playwright() as p:
        print("Launching Chromium...")
        browser = p.chromium.launch(executable_path=CHROMIUM_PATH, headless=False)
        context = browser.new_context(storage_state=AUTH_FILE)
        page = context.new_page()
        
        print(f"Navigating to: {URL}")
        page.goto(URL, wait_until="networkidle")
        time.sleep(3) 

        ROW_SELECTOR = "#product-table tbody tr"
        
        try:
            page.wait_for_selector(ROW_SELECTOR, timeout=10000)
        except Exception:
            print("❌ Timeout: Could not find product rows.")
            browser.close()
            return

        rows = page.locator(ROW_SELECTOR).all()
        print(f"Found {len(rows)} products to process.")

        for index, row in enumerate(rows):
            try:
                # 1. Standard Attribute Extractions
                attr_name = row.get_attribute("data-name") or "Unknown"
                brand = row.get_attribute("data-brand") or "Unknown"
                dimensions = row.get_attribute("data-dimensions") or ""
                price = row.get_attribute("data-price") or ""
                
                # 2. Extract quantity-in-room using the adjacent sibling selector (+ span)
                qty_in_room_locator = row.locator(".product-room-quantity span:nth-child(2)")
                if qty_in_room_locator.count() > 0:
                    quantity_in_room = qty_in_room_locator.text_content().strip()
                else:
                    quantity_in_room = "N/A" # Default if the quantity badge is absent on certain items

                # 3. Extract and parse data-rooms JSON string into a clean list
                rooms_attr = row.get_attribute("data-rooms")
                rooms_list = []
                if rooms_attr:
                    try:
                        rooms_json = json.loads(rooms_attr)
                        rooms_list = [item.get("room") for item in rooms_json if item.get("room")]
                    except Exception:
                        pass
                data_rooms = ", ".join(rooms_list) if rooms_list else "Unknown"

                # 4. Extract client-product-tagline show-for-small-only
                tagline_locator = row.locator(".client-product-tagline.show-for-small-only")
                tagline_small = tagline_locator.text_content().strip() if tagline_locator.count() > 0 else ""

                # 5. Extract whole text contents of <td class="product-description"> EXCLUDING taglines
                desc_cell_locator = row.locator("td.product-description")
                if desc_cell_locator.count() > 0:
                    raw_description = desc_cell_locator.evaluate("""
                        element => {
                            // Clone the cell element to safely manipulate its content without altering the page
                            const clone = element.cloneNode(true);
                            // Query and remove any tagline elements inside the description cell
                            const taglines = clone.querySelectorAll('.client-product-tagline');
                            taglines.forEach(el => el.remove());
                            return clone.textContent;
                        }
                    """)
                    product_description_cell = clean_text(raw_description)
                else:
                    product_description_cell = ""

                # 6. Action link
                vendor_locator = row.locator("td.client-button-cell a.button")
                vendor_url = vendor_locator.get_attribute("href") if vendor_locator.count() > 0 else ""

                # Build dataset entry (Product Name Column has been removed)
                products_data.append({
                    "Attribute Name": attr_name.strip(),
                    "Brand": brand.strip(),
                    "Price": f"£{price.strip()}" if price else "N/A",
                    "Dimensions": dimensions.strip(),
                    "Quantity in Room": quantity_in_room,
                    "Data Rooms": data_rooms,
                    "Tagline (Small Only)": tagline_small,
                    "Product Description Cell": product_description_cell,
                    "Vendor URL": vendor_url
                })
                print(f" processed {index + 1}/{len(rows)}: {attr_name[:25]}")

            except Exception as e:
                print(f"⚠️ Error on row index {index}: {e}")
                continue

        browser.close()

    # Export out to CSV
    if products_data:
        df = pd.DataFrame(products_data)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n🎉 Clean export successful! Saved {len(products_data)} items to '{OUTPUT_FILE}'")
    else:
        print("\n❌ No data collected.")

if __name__ == "__main__":
    scrape_portal()
