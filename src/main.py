import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timedelta

# --- CONFIGURATION ---
ROUTES = [
    {"from": "YYZ", "to": "NKG"}, # Toronto to Nanjing
    {"from": "YUL", "to": "NKG"}  # Montreal to Nanjing
]
# Passenger Mix: 2 Adults + 12yo (Adult) + 10yo (Child) = 3 Adults, 1 Child
ADULTS = 3 
CHILDREN = 1
AIRLINES = ["Cathay Pacific", "Singapore Airlines", "Etihad", "Emirates"]
START_DATE = datetime(2027, 1, 29)
DAYS_TO_CHECK = 5 # To create the "Price per Day" grid feature

async def scrape_google_flights(origin, dest, date):
    async with async_playwright() as p:
        # Launch browser (headless=False lets you see it work)
        browser = await p.chromium.launch(headless=False) 
        page = await browser.new_page()
        
        # Construct a targeted Google Flights URL
        # Note: Google Flights URLs use Base64 for parameters; 
        # For a simple scraper, we use the query-string method.
        formatted_date = date.strftime("%Y-%m-%d")
        url = f"https://www.google.com/travel/flights?q=Flights%20to%20{dest}%20from%20{origin}%20on%20{formatted_date}%20with%20{ADULTS}%20adults%20and%20{CHILDREN}%20children"
        
        print(f"Checking {origin} to {dest} for {formatted_date}...")
        await page.goto(url)
        
        # Wait for flight results to load
        try:
            await page.wait_for_selector('.pI9WCe', timeout=10000) # Selector for flight rows
        except:
            print(f"No results found for {formatted_date} (Window might not be open yet).")
            await browser.close()
            return None

        # Extract Flight Data
        flights = await page.query_selector_all('.pI9WCe')
        results = []

        for flight in flights:
            text = await flight.inner_text()
            # Simple check for your preferred airlines
            if any(airline.lower() in text.lower() for airline in AIRLINES):
                # Extracting price (usually starts with $)
                lines = text.split('\n')
                price = [l for l in lines if '$' in l]
                results.append({
                    "date": formatted_date,
                    "airline": lines[0], # Rough estimate of position
                    "price": price[0] if price else "N/A"
                })
        
        await browser.close()
        return results

async def main():
    price_grid = {}

    for route in ROUTES:
        print(f"\n--- Analyzing Route: {route['from']} to {route['to']} ---")
        for i in range(DAYS_TO_CHECK):
            check_date = START_DATE + timedelta(days=i)
            data = await scrape_google_flights(route['from'], route['to'], check_date)
            
            if data:
                price_grid[check_date.strftime("%Y-%m-%d")] = data
    
    # Display the "Price per Day" Summary
    print("\n--- DAILY PRICE GRID ---")
    for day, info in price_grid.items():
        for flight in info:
            print(f"{day} | {flight['airline']} | {flight['price']}")

if __name__ == "__main__":
    asyncio.run(main())