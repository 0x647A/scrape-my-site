import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

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
    
    for link in pdf_links:
        pdf_url = urljoin(url, link['href'])
        download_pdf(pdf_url, folder)

# Downloading PDFs from the main page
fetch_pdfs_from_page(base_url, 'pdf_files')

# Downloading PDFs from the tabs
for tab in tabs:
    tab_url = urljoin(base_url, f"default.asp?study={tab}")
    fetch_pdfs_from_page(tab_url, 'pdf_files')
