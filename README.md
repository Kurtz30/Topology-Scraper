# Topology Portal Product Scraper

An automated, high-speed Python scraper built using **Playwright** to extract product metadata, pricing, specifications, and availability directly from the Topology Interiors client portal. 

Optimized for **Ubuntu Desktop (including ARM64 architectures such as Apple Silicon VMs or Raspberry Pi)** by leveraging the host machine's native Chromium package to completely bypass version mismatch constraints.

## Thanks clanker
Note this is a quickly vibe coded tool to solve a very specific problem. Your Mialage may vary and the topology website is likley to change so the code may need to be updated.

## Features

- **Magic Link Authentication Handling:** Implements a two-phase architecture to seamlessly capture and maintain active authentication sessions (`cookies` and `localStorage`).
- **High-Speed DOM Extraction:** Instead of performing slow GUI interactions (like opening and closing modals), it extracts structured data arrays embedded directly inside custom element attributes (`data-name`, `data-brand`, `data-dimensions`, `data-price`, `data-rooms`).
- **Dynamic Text Sanitization:** Features localized JavaScript injection (`Element.evaluate()`) to dynamically filter out responsive frontend layout elements (such as `.client-product-tagline` modifiers) from the primary text descriptions.
- **Data Export:** Outputs structured, clean records directly into a formatted `.csv` file powered by Pandas.

---

## Directory Structure

```text
topology-scraper/
├── README.md            # Project documentation
├── requirements.txt     # Python dependency configuration
├── save_auth.py         # Step 1: Interactive login script
└── scrape_portal.py     # Step 2: Main high-speed scraping engine
```

---

## Prerequisites & Installation

### 1. Install Ubuntu Native Chromium
Because the script avoids typical Playwright browser sandboxes to guarantee hardware architecture compatibility, you must install the native Linux compiler package:

```bash
sudo apt update
sudo apt install chromium-browser -y
```

### 2. Environment Configuration
Set up an isolated Python environment to manage script libraries without impacting your core operating system:

```bash
# Install the environment builder utilities
sudo apt install python3-venv python3-pip -y

# Create and activate the virtual environment
python3 -m venv scraper-env
source scraper-env/bin/activate
```

### 3. Install Python Core Libraries
With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Install Operating System OS/GUI Layer Dependencies
Provide Playwright access to the low-level graphics wrapper utilities required to map interactions to your host display layer:

```bash
sudo ./scraper-env/bin/playwright install-deps
```

---

## Usage Guide

### Step 1: Initialize Your Authentication Session
Because the portal uses email "Magic Links" for login, traditional username/password automated forms will fail. Run the authorization script to record your login token:

```bash
python3 save_auth.py
```

1. A headful browser window will display on your desktop.
2. Enter your email on the portal screen, check your email client, and **click the authorization link**.
3. Let the target workspace fully render on screen inside the automated browser instance.
4. After your browser state settles, the script timer will complete and output a secure snapshot token containing active cookies and localStorage values into `auth.json`.

### Step 2: Execute the High-Speed Scraper Engine
Once your `auth.json` token has been created, run the primary data harvester:

```bash
python3 scrape_portal.py
```

The script will launch the native Chromium binary, automatically inject your localized browser environment state to clear the authentication wall, parse all table rows instantaneously, filter out nested layout taglines, and write the dataset out to a spreadsheet.

---

## Output Data Schema

The resulting `products_expanded.csv` will contain the following structured layout:

| Field Name | Type | Data Description |
| :--- | :--- | :--- |
| **Attribute Name** | String | The core designation label of the product extracted from backend data tags. |
| **Brand** | String | Manufacturer/Supplier name. |
| **Price** | String | Cost item value (pre-formatted with currency symbols). |
| **Dimensions** | String | Structural sizing specifications of the layout item. |
| **Quantity in Room** | Integer | The exact count of items dedicated to the specific project area. |
| **Data Rooms** | String | Delimited structural room classification (e.g., *Kitchen, Living Room*). |
| **Tagline (Small Only)** | String | Targeted small viewport promo/placement subtext notes. |
| **Product Description Cell** | String | Core item copy block, dynamically stripped of nested layout clutter. |
| **Vendor URL** | String | Direct external purchasing link destination tracker. |

---

## Troubleshooting & Maintenance

- **Error: "Could not find product rows / Timeout"**: Your authentication session token saved in `auth.json` has likely expired or been invalidated by the host server security policies. Delete your current token file (`rm auth.json`) and run `python3 save_auth.py` to refresh your login state.
- **Chromium Executable Path Errors**: Depending on whether your system manages packages via canonical APT or Canonical Snaps, your local binary may map to a slight variation. Run `which chromium-browser` or `which chromium` in your system shell and verify that it matches the `CHROMIUM_PATH` global string configuration variable in your script files.
