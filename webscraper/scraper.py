import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import time
import threading
import json
import os
from concurrent.futures import ThreadPoolExecutor

# Load configuration from external JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
]

# Function to make HTTP requests with random user agents and optional proxies
def make_request(url, session=None):
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    proxies = config.get('proxies')
    try:
        if session:
            response = session.get(url, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response
        else:
            print(f"Failed to fetch {url}: Status Code {response.status_code}")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return None

# Function to handle authentication (if needed)
def authenticate():
    session = requests.Session()
    login_url = config.get("login_page")
    credentials = config.get("login_credentials")
    if login_url and credentials:
        print(f"Logging in to {login_url}...")
        response = session.post(login_url, data=credentials)
        if response.status_code == 200:
            print("Authentication successful.")
            return session
        else:
            print("Authentication failed.")
    return None

# Function to parse URLs and subdomains from a page
def scrape_links(url, session=None):
    response = make_request(url, session)
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()  # To avoid duplicate links
        for anchor in soup.find_all('a', href=True):
            link = urljoin(url, anchor['href'])
            links.add(link)
        return links
    return []

# Multi-threaded crawler with spider mode
def crawl(url, max_depth, session=None):
    visited = set()
    to_visit = {url}
    depth = 0

    def worker(next_url):
        if next_url not in visited:
            print(f"Crawling: {next_url}")
            links = scrape_links(next_url, session)
            visited.add(next_url)
            to_visit.update(links)

    with ThreadPoolExecutor(max_workers=config.get("threads")) as executor:
        while to_visit and depth < max_depth:
            futures = [executor.submit(worker, next_url) for next_url in to_visit.copy()]
            for future in futures:
                future.result()  # Block until all tasks are done
            depth += 1
    return visited

# SQLi and XSS detection functions
def check_sqli(url):
    for payload in config.get("sql_payloads", []):
        sqli_url = f"{url}?id={payload}"
        response = make_request(sqli_url)
        if response and "error" in response.text.lower():
            print(f"Possible SQLi vulnerability detected at {sqli_url}")

def check_xss(url):
    for payload in config.get("xss_payloads", []):
        xss_url = f"{url}?q={payload}"
        response = make_request(xss_url)
        if response and payload in response.text:
            print(f"Possible XSS vulnerability detected at {xss_url}")

# Data export/exfiltration
def export_data(data, file_name='export'):
    export_format = config.get('export_format', 'json')
    file_path = f"results/{file_name}.{export_format}"

    if not os.path.exists('results/'):
        os.makedirs('results/')

    if export_format == 'json':
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        print(f"Unsupported export format: {export_format}")

# Function to integrate with Burp Suite
def export_to_burp(links):
    burp_file = 'results/burp_links.txt'
    with open(burp_file, 'w') as file:
        for link in links:
            file.write(f"{link}\n")
    print(f"Links exported to {burp_file} for Burp Suite analysis.")

# Main function
if __name__ == "__main__":
    target_url = config.get("target_url")
    session = authenticate()  # Handle authentication if required
    max_depth = config.get("max_depth", 2)

    print(f"Starting crawl on {target_url} with depth {max_depth}")
    all_links = crawl(target_url, max_depth, session)

    print(f"Found {len(all_links)} links:")
    for link in all_links:
        print(link)
        check_sqli(link)  # Check for SQLi
        check_xss(link)   # Check for XSS

    # Export the found links
    export_data(list(all_links), 'crawled_links')

    # Optionally, export links for Burp Suite
    export_to_burp(all_links)
