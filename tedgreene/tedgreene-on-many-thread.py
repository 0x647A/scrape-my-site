import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

# Main page with PDFs
base_url = 'https://www.tedgreene.com/teaching/default.asp'

# Tabs to search for PDFs
tabs = [
    "Arrangements", "Baroque", "Blues", "Jazz",
    "ChordStudies", "Comping", "Fundamentals",
    "HarmonyAndTheory", "SingleNoteSoloing", "TheVSystem", "Other"
]

# Creating a directory to store PDFs
if not os.path.exists('pdf_files'):
    os.makedirs('pdf_files')

# Function to download and save a PDF file
def download_pdf(url, folder):
    response = requests.get(url)
    filename = os.path.join(folder, url.split('/')[-1])
    with open(filename, 'wb') as file:
        file.write(response.content)

# Function to search the main page and tabs for PDFs
def fetch_pdfs_from_page(url, folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
    
    pdf_urls = [urljoin(url, link['href']) for link in pdf_links]
    return pdf_urls

# Function to process a list of URLs in threads
def download_pdfs_from_urls(urls, folder):
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda url: download_pdf(url, folder), urls)

# Downloading PDFs from the main page
pdf_urls = fetch_pdfs_from_page(base_url, 'pdf_files')
download_pdfs_from_urls(pdf_urls, 'pdf_files')

# Downloading PDFs from the tabs
for tab in tabs:
    tab_url = urljoin(base_url, f"default.asp?study={tab}")
    pdf_urls = fetch_pdfs_from_page(tab_url, 'pdf_files')
    download_pdfs_from_urls(pdf_urls, 'pdf_files')
