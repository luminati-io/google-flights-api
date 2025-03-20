from playwright.async_api import async_playwright
from tenacity import retry, stop_after_attempt, wait_fixed
from dataclasses import dataclass
from typing import List
import asyncio
import json
import re


@dataclass
class FlightData:
    """Data class to store individual flight information"""

    airline: str
    departure_time: str
    arrival_time: str
    duration: str
    stops: str
    price: str
    co2_emissions: str
    emissions_variation: str


class FlightScraper:
    """Class to handle Google Flights scraping operations using direct URL"""

    SELECTORS = {
        "airline": "div.sSHqwe.tPgKwe.ogfYpf",
        "departure_time": 'span[aria-label^="Departure time"]',
        "arrival_time": 'span[aria-label^="Arrival time"]',
        "duration": 'div[aria-label^="Total duration"]',
        "stops": "div.hF6lYb span.rGRiKd",
        "price": "div.FpEdX span",
        "co2_emissions": "div.O7CXue",
        "emissions_variation": "div.N6PNV",
    }

    async def _extract_text(self, element) -> str:
        """Extract text content from a page element safely"""
        return (await element.text_content()).strip() if element else "N/A"

    async def _load_all_flights(self, page) -> None:
        """Click 'Show more flights' button until all flights are loaded"""
        while True:
            try:
                more_button = await page.wait_for_selector(
                    'button[aria-label*="more flights"]', timeout=5000
                )
                if more_button:
                    await more_button.click()
                    await page.wait_for_timeout(2000)
                else:
                    break
            except:
                break

    async def _extract_flight_data(self, page) -> List[FlightData]:
        """Extract flight information from search results"""
        try:
            await page.wait_for_selector("li.pIav2d", timeout=30000)
            await self._load_all_flights(page)
            flights = await page.query_selector_all("li.pIav2d")

            flights_data = []
            for flight in flights:
                flight_info = {}
                for key, selector in self.SELECTORS.items():
                    element = await flight.query_selector(selector)
                    flight_info[key] = await self._extract_text(element)
                flights_data.append(FlightData(**flight_info))
            return flights_data
        except Exception as e:
            raise Exception(f"Failed to extract flight data: {str(e)}")

    def _extract_trip_info_from_url(self, url: str) -> dict:
        """Extract trip information from Google Flights URL"""
        trip_info = {}
        airport_match = re.search(r"[?&]tfs=.*?([A-Z]{3}).*?([A-Z]{3})", url)
        if airport_match:
            trip_info["origin"] = airport_match.group(1)
            trip_info["destination"] = airport_match.group(2)

        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", url)
        if date_match:
            trip_info["date"] = date_match.group(1)

        return trip_info

    def save_results(self, flights: List[FlightData], url: str) -> str:
        """Save flight search results to a JSON file"""
        output_data = {
            "search_url": url,
            "flights": [vars(flight) for flight in flights],
        }

        filepath = "flight_results.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        return filepath

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
    async def search_flights(self, url: str) -> List[FlightData]:
        """Execute the flight search with retry capability using a direct URL"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            try:
                await page.goto(url, timeout=60000)
                await page.wait_for_load_state("networkidle")

                flights = await self._extract_flight_data(page)
                filepath = self.save_results(flights, url)
                print(f"Results saved to: {filepath}")
                return flights
            finally:
                await browser.close()


async def main():
    """Main function to demonstrate usage"""
    scraper = FlightScraper()
    url = "https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI1LTA0LTAxagcIARIDREVMcgcIARIDU0ZPQAFIAXABggELCP___________wGYAQI&curr=USD"

    try:
        flights = await scraper.search_flights(url)
        print(f"Successfully found {len(flights)} flights")
    except Exception as e:
        print(f"Error during flight search: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())