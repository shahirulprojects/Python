# error handling in web scraping operations
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from typing import Any, Dict, List, Optional, Union
import logging
import time
from dataclasses import dataclass
from urllib.parse import urljoin
import json
from pathlib import Path
import re
from functools import wraps
import random

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# custom exceptions
class ScrapingError(Exception):
    """base class for scraping errors."""
    pass

class RequestError(ScrapingError):
    """error for request failures."""
    pass

class ParsingError(ScrapingError):
    """error for parsing failures."""
    pass

class ValidationError(ScrapingError):
    """error for data validation failures."""
    pass

@dataclass
class ScrapedData:
    """container for scraped data."""
    url: str
    timestamp: str
    content: Dict[str, Any]
    metadata: Dict[str, Any]

class RateLimiter:
    """rate limiter for web requests."""
    
    def __init__(self, requests_per_second: float):
        self.delay = 1.0 / requests_per_second
        self.last_request = 0.0
    
    def wait(self):
        """wait appropriate time before next request."""
        now = time.time()
        elapsed = now - self.last_request
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request = time.time()

class RequestManager:
    """manage web requests with error handling."""
    
    def __init__(self, rate_limit: float = 1.0, 
                 max_retries: int = 3, 
                 timeout: int = 30):
        self.rate_limiter = RateLimiter(rate_limit)
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """make GET request with error handling."""
        for attempt in range(self.max_retries):
            try:
                self.rate_limiter.wait()
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    **kwargs
                )
                response.raise_for_status()
                return response
            
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    raise RequestError(f"page not found: {url}")
                elif e.response.status_code == 429:
                    wait_time = int(e.response.headers.get('Retry-After', 60))
                    logging.warning(f"rate limited, waiting {wait_time} seconds")
                    time.sleep(wait_time)
                elif attempt == self.max_retries - 1:
                    raise RequestError(f"HTTP error: {str(e)}")
            
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise RequestError(f"request failed: {str(e)}")
                
                wait_time = 2 ** attempt  # exponential backoff
                logging.warning(f"attempt {attempt + 1} failed, retrying in {wait_time}s")
                time.sleep(wait_time)

class SeleniumWrapper:
    """wrapper for Selenium with error handling."""
    
    def __init__(self, headless: bool = True):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
    
    def get_page(self, url: str, wait_time: int = 10) -> str:
        """get page content with JavaScript rendering."""
        try:
            self.driver.get(url)
            return self.driver.page_source
        except WebDriverException as e:
            raise RequestError(f"selenium error: {str(e)}")
    
    def wait_for_element(self, selector: str, 
                        by: str = By.CSS_SELECTOR, 
                        timeout: int = 10) -> Any:
        """wait for element to be present."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, selector))
            )
            return element
        except TimeoutException:
            raise RequestError(f"element not found: {selector}")
        except WebDriverException as e:
            raise RequestError(f"selenium error: {str(e)}")

class Parser:
    """HTML parser with error handling."""
    
    @staticmethod
    def create_soup(content: str) -> BeautifulSoup:
        """create BeautifulSoup object."""
        try:
            return BeautifulSoup(content, 'html.parser')
        except Exception as e:
            raise ParsingError(f"failed to parse HTML: {str(e)}")
    
    @staticmethod
    def extract_text(element: Any, selector: str) -> str:
        """extract text from element."""
        try:
            result = element.select_one(selector)
            return result.text.strip() if result else ""
        except Exception as e:
            raise ParsingError(f"failed to extract text: {str(e)}")
    
    @staticmethod
    def extract_attribute(element: Any, selector: str, 
                         attribute: str) -> str:
        """extract attribute from element."""
        try:
            result = element.select_one(selector)
            return result.get(attribute, "") if result else ""
        except Exception as e:
            raise ParsingError(f"failed to extract attribute: {str(e)}")

class DataValidator:
    """validate scraped data."""
    
    @staticmethod
    def validate_text(text: str, min_length: int = 1, 
                     max_length: int = 1000) -> str:
        """validate text content."""
        if not isinstance(text, str):
            raise ValidationError(f"expected string, got {type(text)}")
        
        text = text.strip()
        if len(text) < min_length:
            raise ValidationError(f"text too short: {len(text)} chars")
        if len(text) > max_length:
            raise ValidationError(f"text too long: {len(text)} chars")
        
        return text
    
    @staticmethod
    def validate_url(url: str) -> str:
        """validate URL."""
        if not isinstance(url, str):
            raise ValidationError(f"expected string, got {type(url)}")
        
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            raise ValidationError(f"invalid URL: {url}")
        
        return url

class Scraper:
    """web scraper with error handling."""
    
    def __init__(self, output_dir: str = "scraped_data"):
        self.request_manager = RequestManager()
        self.parser = Parser()
        self.validator = DataValidator()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def scrape_page(self, url: str) -> ScrapedData:
        """scrape single page."""
        try:
            # validate URL
            url = self.validator.validate_url(url)
            
            # get page content
            response = self.request_manager.get(url)
            
            # parse content
            soup = self.parser.create_soup(response.text)
            
            # extract data (example)
            title = self.parser.extract_text(soup, 'h1')
            description = self.parser.extract_text(soup, 'meta[name="description"]')
            links = [
                self.parser.extract_attribute(a, 'a', 'href')
                for a in soup.select('a[href]')
            ]
            
            # validate data
            title = self.validator.validate_text(title)
            description = self.validator.validate_text(description)
            links = [
                urljoin(url, link)
                for link in links
                if self.validator.validate_url(urljoin(url, link))
            ]
            
            # create result
            return ScrapedData(
                url=url,
                timestamp=datetime.now().isoformat(),
                content={
                    'title': title,
                    'description': description,
                    'links': links
                },
                metadata={
                    'status_code': response.status_code,
                    'content_type': response.headers.get('content-type'),
                    'encoding': response.encoding
                }
            )
            
        except (RequestError, ParsingError, ValidationError):
            raise
        except Exception as e:
            raise ScrapingError(f"scraping failed: {str(e)}")
    
    def save_data(self, data: ScrapedData) -> None:
        """save scraped data."""
        try:
            filename = re.sub(r'[^\w\-_.]', '_', data.url) + '.json'
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data.__dict__, f, indent=2)
        
        except Exception as e:
            raise ScrapingError(f"failed to save data: {str(e)}")

# example usage
def main():
    """demonstrate web scraping error handling."""
    scraper = Scraper()
    
    # 1. basic scraping
    print("1. testing basic scraping:")
    try:
        data = scraper.scrape_page("https://example.com")
        print(f"scraped data: {json.dumps(data.__dict__, indent=2)}")
        scraper.save_data(data)
    except ScrapingError as e:
        print(f"scraping error: {e}")
    
    # 2. selenium scraping
    print("\n2. testing selenium scraping:")
    try:
        with SeleniumWrapper() as browser:
            # wait for dynamic content
            browser.get_page("https://example.com")
            element = browser.wait_for_element("h1")
            print(f"found element: {element.text}")
    except RequestError as e:
        print(f"selenium error: {e}")
    
    # 3. error handling
    print("\n3. testing error handling:")
    try:
        # invalid URL
        scraper.scrape_page("invalid-url")
    except ValidationError as e:
        print(f"validation error: {e}")
    
    try:
        # non-existent page
        scraper.scrape_page("https://example.com/nonexistent")
    except RequestError as e:
        print(f"request error: {e}")

if __name__ == "__main__":
    main()

# practice exercises:
# 1. create a web crawler that:
#    - follows links recursively
#    - respects robots.txt
#    - handles rate limiting
#    - saves site structure

# 2. create a data extractor that:
#    - handles different page layouts
#    - extracts structured data
#    - validates against schema
#    - handles missing data

# 3. create a monitoring system that:
#    - tracks scraping success rate
#    - detects site changes
#    - handles IP blocking
#    - rotates proxies 