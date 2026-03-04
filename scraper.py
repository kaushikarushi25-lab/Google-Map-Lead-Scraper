import asyncio
import csv
from playwright.async_api import async_playwright

async def scrape_google_maps(query):
    print(f"\n[Scraper] Starting scraping for: '{query}'")
    data = []
    
    async with async_playwright() as p:
        # Launch Chromium (headless=False so you can see the scraper at work)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='en-US'
        )
        page = await context.new_page()
        
        # 1. Go to Google Maps
        await page.goto('https://www.google.com/maps')
        
        # 2. Handle potential cookie popups
        try:
            await page.click('button:has-text("Accept all")', timeout=3000)
        except:
            pass
            
        # 3. Enter search query
        print("[Scraper] Searching...")
        await page.fill('input#searchboxinput', query)
        await page.press('input#searchboxinput', 'Enter')
        
        # 4. Wait for the listings container to load
        try:
            await page.wait_for_selector('a[href*="https://www.google.com/maps/place"]', timeout=15000)
        except Exception:
            print("[Scraper] No search results found or the page didn't load properly.")
            await browser.close()
            return

        # 5. Scroll to load more listings (scrolls the side panel)
        print("[Scraper] Scrolling to load more results...")
        await page.hover('a[href*="https://www.google.com/maps/place"]')
        for i in range(5):  # Change this to scroll more/less
            await page.mouse.wheel(0, 5000)
            await page.wait_for_timeout(2000)
            
        # 6. Gather all listings
        listings = await page.locator('a[href*="https://www.google.com/maps/place"]').all()
        print(f"[Scraper] Found {len(listings)} potential listings. Extracting details...")

        for idx, listing in enumerate(listings):
            try:
                # The name is usually in the aria-label of the link
                name = await listing.get_attribute('aria-label')
                if not name:
                    continue
                
                # Click listing to open the details panel
                await listing.click()
                await page.wait_for_timeout(2000)  # wait for animation
                
                phone = ""
                website = ""
                rating = ""
                
                # Wait up to 2 seconds for detail panel to render content fully
                try: 
                    await page.wait_for_selector('div[role="main"]', timeout=2000)
                except:
                    pass

                # Extract Rating
                try:
                    rating_locator = page.locator('span[aria-label*="stars"]')
                    if await rating_locator.count() > 0:
                        aria = await rating_locator.first.get_attribute('aria-label')
                        rating = aria.split(' ')[0] if aria else ""
                except:
                    pass
                
                # Extract Phone
                try:
                    phone_locator = page.locator('button[data-tooltip*="Copy phone number"]')
                    if await phone_locator.count() > 0:
                        aria = await phone_locator.first.get_attribute('aria-label')
                        phone = aria.replace('Phone number: ', '').strip() if aria else ""
                except:
                    pass
                    
                # Extract Website
                try:
                    web_locator = page.locator('a[data-tooltip*="Open website"]')
                    if await web_locator.count() > 0:
                        website = await web_locator.first.get_attribute('href')
                except:
                    pass
                
                print(f"[{idx+1}/{len(listings)}] Name: {name} | Phone: {phone} | Web: {website} | Rating: {rating}")
                data.append({
                    'Name': name,
                    'Phone': str(phone),
                    'Website': str(website),
                    'Rating': str(rating)
                })
                
            except Exception as e:
                print(f"[Scraper] Error parsing listing {idx+1}: {e}")
                continue

        await browser.close()
        
    # 7. Save to CSV
    if data:
        with open('leads.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Name', 'Phone', 'Website', 'Rating'])
            writer.writeheader()
            writer.writerows(data)
        print(f"\n[Scraper] Successfully extracted and saved {len(data)} leads to 'leads.csv'.")
    else:
        print("\n[Scraper] Completed, but no leads were successfully extracted.")

if __name__ == "__main__":
    search_query = input("Enter your search query (e.g., 'web design agencies in London'): ")
    asyncio.run(scrape_google_maps(search_query))
