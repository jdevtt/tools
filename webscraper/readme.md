# Python Web Scraper for Ethical Hacking and Penetration Testing

This project is a powerful, configurable web scraping tool designed for ethical hacking and penetration testing purposes. It can be used in both lab and real-world environments to gather useful information from web applications, detect vulnerabilities like SQL Injection (SQLi) and Cross-Site Scripting (XSS), and export data for further analysis. 

## Features

- **Multi-threaded Web Scraping**: Speeds up the scraping process by scraping multiple URLs simultaneously using threads.
- **Authentication Handling**: Supports logging into web applications and scraping authenticated content.
- **Spider Mode**: Deeply crawls the website, discovering all reachable URLs.
- **SQLi & XSS Detection**: Automatically detects possible SQL Injection and XSS vulnerabilities by injecting common attack payloads.
- **Proxy Support**: Sends requests through a proxy for anonymization or to bypass certain restrictions.
- **User-Agent Rotation**: Rotates user-agents to avoid detection by anti-bot mechanisms.
- **Burp Suite Integration**: Exports scraped URLs in a format compatible with Burp Suite for manual testing.
- **Data Export**: Saves scraped data and detected vulnerabilities in JSON format for analysis.

## Requirements

- Python 3.x
- Required Python Libraries:
  - `requests`
  - `bs4` (BeautifulSoup)
  - `concurrent.futures`
  - `json`

You can install the dependencies using `pip`:

```bash
pip install requests beautifulsoup4
```

## Project Structure

```bash
├── config.json        # Configuration file for target, authentication, SQLi/XSS payloads, and other settings
├── scraper.py         # Main Python script
├── results/           # Directory for logs, exported data, and Burp Suite integration files
├── README.md          # Documentation
```

## Configuration

The tool uses a `config.json` file to define the scraping behavior, including the target URL, login credentials, SQLi/XSS payloads, and proxies. Here's an example configuration:

```json
{
    "target_url": "https://example.com",
    "max_depth": 3,
    "proxies": {
        "http": "http://127.0.0.1:8080"
    },
    "sql_payloads": [
        "' OR 1=1 --", 
        "' OR 'a'='a", 
        "' UNION SELECT NULL, NULL, NULL -- "
    ],
    "xss_payloads": [
        "<script>alert(1)</script>", 
        "\"><img src=x onerror=alert(1)>"
    ],
    "export_format": "json",
    "threads": 5,
    "login_page": "https://example.com/login",
    "login_credentials": {
        "username": "admin",
        "password": "password"
    }
}
```

### Key Configuration Parameters:

- **`target_url`**: The URL of the target web application.
- **`max_depth`**: Defines how deep the scraper will crawl through links.
- **`proxies`**: Optional HTTP proxy settings.
- **`sql_payloads`**: SQL Injection payloads that will be used to test URLs for vulnerabilities.
- **`xss_payloads`**: XSS payloads that will be injected into query parameters.
- **`export_format`**: Format of the export data (currently supports JSON).
- **`threads`**: Number of threads for multi-threaded scraping.
- **`login_page`**: URL of the login page for authentication (if needed).
- **`login_credentials`**: Credentials for login authentication.

## Usage

### 1. Clone the Repository

```bash
git clone https://github.com/jdevtt/webscraper.git
cd webscraper
```

### 2. Edit the `config.json` File

Update the `config.json` file with your target URL, SQLi/XSS payloads, login credentials, and other settings as needed.

### 3. Run the Scraper

```bash
py scraper.py
```

### 4. Exported Data

The results of the scraping and vulnerability detection will be saved in the `results/` directory:

- **`crawled_links.json`**: Contains all crawled URLs.
- **`burp_links.txt`**: Contains all links exported for Burp Suite analysis.

### 5. Output

After running the tool, the output will look like this:

```bash
Starting crawl on https://example.com with depth 3
Crawling: https://example.com/about
Crawling: https://example.com/login
Crawling: https://example.com/products
Found 50 links:
Possible SQLi vulnerability detected at https://example.com/products?id=' OR 1=1 --
Possible XSS vulnerability detected at https://example.com/search?q=<script>alert(1)</script>
```

### 6. Using Burp Suite Integration

The scraper exports a list of all found URLs into `results/burp_links.txt`. You can import this file into Burp Suite for further testing and analysis.

## How It Works

### Multi-threaded Web Scraping
The scraper utilizes Python's `ThreadPoolExecutor` to allow multiple threads to work concurrently, making the process much faster by crawling multiple links at the same time.

### Authentication Handling
If the web application requires login, the scraper handles authentication via the `requests.Session()` method. The credentials and login URL are configured in the `config.json` file.

### SQLi & XSS Detection
The scraper checks each URL for SQL Injection and XSS vulnerabilities by appending specific payloads (configured in `config.json`) to the URL parameters. It looks for error messages or reflected payloads in the response to detect potential vulnerabilities.

### Spider Mode
Spider Mode ensures that the scraper recursively follows all discovered links, up to the specified depth, simulating how an actual web crawler would behave. This allows for deeper discovery of hidden or unlisted pages.

### Burp Suite Integration
For further manual testing, the scraped URLs are saved in a `burp_links.txt` file, which can be easily imported into Burp Suite for deeper analysis.

### Data Export/Exfiltration
All scraped data, including URLs and detected vulnerabilities, is exported to the `results/` directory. This data can be saved in JSON format for easy parsing and analysis.


## **Disclaimer**

This tool is intended for ethical hacking and penetration testing purposes **only**. Ensure you have legal permission before running it against any system. I am not responsible for any misuse of this tool.

---