# Instructions: How to Run the Google Maps Lead Scraper

Follow these steps to set up your environment and run the scraping script.

## 1. Prerequisites
- Enure you have **Python 3.8** or newer installed. You can check your version by running `python --version` in your terminal.

## 2. Setup a Virtual Environment (Recommended)
It is always good practice to use a virtual environment so the project dependencies do not interfere with other projects.
1. Open your terminal in the project directory (`Google-Map-Lead-Scraper`).
2. Run the following command to create the environment:
   ```bash
   python -m venv venv
   ```
3. Activate the environment:
   - On **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

## 3. Install Dependencies
With your virtual environment activated, install the required packages (Playwright) by executing:
```bash
pip install -r requirements.txt
```

## 4. Install Playwright Browsers
Playwright requires you to download the actual browser binaries before it can automate them. Run:
```bash
playwright install chromium
```

## 5. Run the Scraper
You are all set! Run the script with:
```bash
python scraper.py
```

- You will be prompted to enter a **search query** (e.g., *Plumbers in New York, NY*).
- A browser window will visually open, search Google Maps, and scroll down to load listings.
- Once finished, all extracted data will be saved inside the `leads.csv` file in the same folder.
