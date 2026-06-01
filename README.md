# Topology Portal Product Scraper

An automated, high-speed Python scraper built using **Playwright** to extract product metadata, pricing, specifications, and availability directly from the Topology Interiors client portal. 

Optimized for **Ubuntu Desktop (including ARM64 architectures such as Apple Silicon VMs or Raspberry Pi)** by leveraging the host machine's native Chromium package to completely bypass version mismatch constraints.

## Thanks clanker
Note this is a quickly vibe coded tool to solve a very specific problem. Your Mialage may vary and the topology website is likley to change so the code may need to be updated.

## Features

- **Magic Link Authentication Handling:** Implements a two-phase architecture to seamlessly capture and maintain active authentication sessions (`cookies` and `localStorage`).
- **High-Speed DOM Extraction:** Instead of performing slow GUI interactions (like opening and closing modals), it extracts structured data arrays embedded directly inside custom element attributes.
- **Dynamic Text Sanitization:** Features localized JavaScript injection (`Element.evaluate()`) to dynamically filter out responsive frontend layout elements (such as layout taglines) from the primary text descriptions.
- **Data Export:** Outputs structured, clean records directly into a formatted `.csv` file powered by Pandas.

---

## Directory Structure

```text
topology-scraper/
├── README.md            # Project documentation
├── requirements.txt     # Python dependency configuration
├── save_auth.py         # Step 1: Interactive login script
└── scrape_portal.py     # Step 2: Main high-speed scraping engine
