# Google Flights Scraper API

This repository provides two ways to extract flight data from Google Flights:

1. **Free Google Flights Scraper:** Ideal for small-scale extraction
2. **Google Flights Scraper API:** Designed for high-volume, real-time data extraction with unlimited requests. Part of Bright Data's [SERP Scraping API](https://brightdata.com/products/serp-api).


## Table of Contents
2. [Free Scraper](#free-scraper)
   - [Setup Requirements](#setup-requirements)
   - [Quick Start](#quick-start)
   - [Sample Output](#sample-output)
   - [Limitations](#limitations)
3. [Google Flights Scraper API](#google-flights-scraper-api)
   - [Key Features](#key-features)
   - [Prerequisites](#prerequisites)
   - [Direct API Access](#direct-api-access)
   - [Native Proxy-Based Access](#native-proxy-based-access)
4. [Additional Parameters](#additional-parameters)
   - [Localization Parameters](#localization-parameters)
   - [Currency Parameter](#currency-parameter)
5. [Support & Resources](#support--resources)

## Free Scraper
A quick and simple scraper for limited data extraction from Google Flights.

<img width="800" alt="google-flights-scraper" src="https://github.com/user-attachments/assets/44ae10b1-4974-497e-9a7c-c1a762614f0e" />

### Setup Requirements
- [Python 3.9+](https://www.python.org/downloads/)
- [Playwright](https://playwright.dev/) for browser automation

```bash
pip install playwright
playwright install chromium
```

> **New to web scraping?** Explore our [Beginner's Guide to Web Scraping with Python](https://brightdata.com/blog/how-tos/web-scraping-with-python)
>

### Quick Start
1. Open [google-flights-scraper.py](https://github.com/triposat/Google-Flights-Scraper-API/blob/main/google-flights-scraper/google-flights-scraper.py)
2. Update the following variable:
    - `url`: Paste the Google Flights URL (usually contains `tfs`).
3. Run the script.

💡 Pro Tip: Set `HEADLESS = False` to minimize detection by Google's anti-scraping measures.

### Sample Output
```json
{
  "airline": "Emirates",
  "departure_time": "4:15 AM",
  "arrival_time": "2:00 PM",
  "duration": "22 hr 15 min",
  "stops": "1 stop in DXB",
  "price": "$1,139",
  "co2_emissions": "1,092 kg CO2e",
  "emissions_variation": "+6% emissions"
}
```

👉  [View complete output sample](https://github.com/triposat/Google-Flights-Scraper-API/blob/main/google-flights-results/flight_results.json)


### Limitations
The Free Scraper has several constraints:
- High risk of IP blocking
- Limited request volume
- Frequent CAPTCHAs
- Unreliable for production use

For robust, scalable scraping without these limitations, consider Bright Data's dedicated API below. 👇

## Google Flights Scraper API
[Bright Data's Google Flights Scraper API](https://brightdata.com/products/web-scraper/google-flights) is integrated into the [SERP Scraping API](https://brightdata.com/products/serp-api) and leverages our extensive [proxy network](https://brightdata.com/proxy-types) to extract real-time flight data—including prices, schedules, and airline details—at scale, without CAPTCHAs or IP blocks.

### Key Features

- **Global Accuracy:** Tailored results for specific locations
- **Pay-Per-Success:** Only pay for successful requests
- **Real-Time Data:** Get up-to-date flights data in seconds
- **Unlimited Scalability:** Handle high-volume scraping effortlessly
- **Cost-Efficient:** Eliminates the need for costly infrastructure
- **Reliable Performance:** Built-in anti-blocking technology
- **24/7 Expert Support:** Assistance whenever required

### Prerequisites

1. [Create a Bright Data account](https://brightdata.com/) (new users receive a $5 credit).
2. Generate your [API key](https://docs.brightdata.com/general/account/api-token).
3. Follow our [step-by-step guide](https://github.com/triposat/Google-Flights-Scraper-API/blob/main/setup-serp-api-guide.md) to configure the SERP API and set up your credentials.

### Direct API Access

Make a direct request to the API endpoint.

**cURL Example:**

```bash
curl https://api.brightdata.com/request \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer API_TOKEN" \
  -d '{
        "zone": "ZONE_NAME",
        "url": "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA0LTAxagcIARIDREVMcgwIAxIIL20vMDRqcGxAAUgBcAGCAQsI____________AZgBAg",
        "format": "raw"
      }'
```

**Python Example:**

```python
import requests

url = "https://api.brightdata.com/request"
headers = {"Content-Type": "application/json", "Authorization": "Bearer API_TOKEN"}
payload = {
    "zone": "ZONE_NAME",
    "url": "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA0LTAxagcIARIDREVMcgwIAxIIL20vMDRqcGxAAUgBcAGCAQsI____________AZgBAg",
    "format": "raw",
}

response = requests.post(url, headers=headers, json=payload)

with open("google-flights-data.html", "w", encoding="utf-8") as file:
    file.write(response.text)
print("HTML response saved to 'google-flights-data.html'.")
```

### Native Proxy-Based Access

Alternatively, use Bright Data's proxy routing method.

**cURL Example:**

```bash
curl -i \
  --proxy brd.superproxy.io:33335 \
  --proxy-user "brd-customer-<customer-id>-zone-<zone-name>:<zone-password>" \
  -k \
  "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA0LTAxagcIARIDREVMcgwIAxIIL20vMDRqcGxAAUgBcAGCAQsI____________AZgBAg"
```

**Python Example:**

```python
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = "brd.superproxy.io"
port = 33335
username = "brd-customer-<customer-id>-zone-<zone-name>"
password = "<zone-password>"
proxy_url = f"http://{username}:{password}@{host}:{port}"

proxies = {"http": proxy_url, "https": proxy_url}
url = "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA0LTAxagcIARIDREVMcgwIAxIIL20vMDRqcGxAAUgBcAGCAQsI____________AZgBAg"
response = requests.get(url, proxies=proxies, verify=False)

with open("google-flights-data.html", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Response saved to 'google-flights-data.html'.")
```

👉 View the [full HTML output](https://github.com/triposat/Google-Flights-Scraper-API/blob/main/google-flights-api-output/google-flights-data.html).

**Note:** For production use, load Bright Data's SSL certificate as per the [SSL Certificate Guide](https://docs.brightdata.com/general/account/ssl-certificate).


## Additional Parameters
Fine-tune your Google Flights data extraction with these optional parameters.

### Localization Parameters
<img width="800" alt="bright-data-google-flights-scraper-api-localization" src="https://github.com/user-attachments/assets/e77f10c9-8e44-46aa-be3d-64c756741479" />

Customize search results based on location and language:

| Parameter | Description | Example |
| --- | --- | --- |
| gl | Two-letter country code | `gl=us` (United States) |
| hl | Two-letter language code | `hl=en` (English) |


**Example:** Search for flights from Paris to London in French:

```bash
curl --proxy brd.superproxy.io:33335 --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
"https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA0LTAxagcIARIDQ0RHcgwIAxIIL20vMDRqcGxAAUgBcAGCAQsI____________AZgBAg&hl=fr&gl=fr"
```

### Currency Parameter

<img width="800" alt="bright-data-google-flights-scraper-api-currency" src="https://github.com/user-attachments/assets/c571e99f-b854-449e-abc2-60149611ad5b" />

Define the currency for returned prices using the `curr` parameter.

**Example:** Return prices in USD.

```bash
curl --proxy brd.superproxy.io:33335 --proxy-user brd-customer-<customer-id>-zone-<zone-name>:<zone-password> \
"https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTA0LTAxagcIARIDQ0RHcgwIAxIIL20vMDRqcGxAAUgBcAGCAQsI____________AZgBAg&hl=fr&gl=fr&curr=USD"
```

## Support & Resources

- **Docs:** [SERP API Documentation](https://docs.brightdata.com/scraping-automation/serp-api/)
- **Related APIs:** [Web Unlocker API](https://github.com/luminati-io/web-unlocker-api), [SERP API](https://github.com/luminati-io/serp-api), [Google Search API](https://github.com/luminati-io/google-search-api), [Google News Scraper](https://github.com/luminati-io/Google-News-Scraper), [Google Trends API](https://github.com/luminati-io/google-trends-api), [Google Reviews API](https://github.com/luminati-io/google-reviews-api), [Google Hotels API](https://github.com/luminati-io/google-hotels-api)
- **Google Scraping Tutorials:**
    - [How to Scrape Google Flights](https://brightdata.com/blog/web-data/how-to-scrape-google-flights)
    - [How to Scrape Google Search Results](https://brightdata.com/blog/web-data/scraping-google-with-python)
    - [How to Scrape Google Maps](https://brightdata.com/blog/web-data/how-to-scrape-google-maps)
- **Use Cases:**
    - [SEO & SERP Tracking](https://brightdata.com/use-cases/serp-tracking)
    - [Travel Industry Data](https://brightdata.com/use-cases/travel)
- **Additional Reading:** [Best SERP APIs](https://brightdata.com/blog/web-data/best-serp-apis)
- **Contact Support:** [support@brightdata.com](mailto:support@brightdata.com)
