# Download all PDFs from the Ted Greene teaching website at once

## Project Overview

This project was created for a friend who plays in a band and asked for help in downloading all PDFs from the Ted Greene teaching website at once. The goal was to create a script that can fetch all PDFs from the main page and various tabs on the site, saving them locally. Two versions of the script were developed: a single-threaded version and a multi-threaded version to improve download speed.

## Single-Threaded Script

The single-threaded script downloads PDFs from the main page and specified tabs on the Ted Greene teaching website. It searches for all links ending with .pdf, constructs the full URL, and downloads each file sequentially.

### Usage

1. **Import necessary libraries**:
    - `os`: For creating directories.
    - `requests`: For making HTTP requests.
    - `BeautifulSoup`: For parsing HTML content.
    - `urljoin`: For constructing full URLs from relative paths.

2.  **Set the main URL and tabs to search**:
```python
base_url = 'https://www.tedgreene.com/teaching/default.asp'
tabs = [
    "Arrangements", "Baroque", "Blues", "Jazz",
    "ChordStudies", "Comping", "Fundamentals",
    "HarmonyAndTheory", "SingleNoteSoloing", "TheVSystem", "Other"
]
```

3. **Create a directory to store the PDFs**:
```python
if not os.path.exists('pdf_files'):
    os.makedirs('pdf_files')
```

4. **Define functions to download and save PDFs**:
```python
def download_pdf(url, folder):
    response = requests.get(url)
    filename = os.path.join(folder, url.split('/')[-1])
    with open(filename, 'wb') as file:
        file.write(response.content)
```

5. **Fetch and download PDFs from the main page and tabs**:
```python
def fetch_pdfs_from_page(url, folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
    
    for link in pdf_links:
        pdf_url = urljoin(url, link['href'])
        download_pdf(pdf_url, folder)

fetch_pdfs_from_page(base_url, 'pdf_files')

for tab in tabs:
    tab_url = urljoin(base_url, f"default.asp?study={tab}")
    fetch_pdfs_from_page(tab_url, 'pdf_files')
```

## Multi-Threaded Script

The multi-threaded script improves download speed by using multiple threads to fetch PDFs concurrently. It follows the same basic steps as the single-threaded version but uses ThreadPoolExecutor to manage concurrent downloads.

### Usage

1. **Import necessary libraries**:
    - Same as the single-threaded script, with the addition of `ThreadPoolExecutor` for managing threads.

2. **Set the main URL and tabs to search**:
    - Same as the single-threaded script.

3. **Create a directory to store the PDFs**:
    - Same as the single-threaded script.

4. **Define functions to download and save PDFs, and to process URLs in threads**:
```python
def download_pdf(url, folder):
    response = requests.get(url)
    filename = os.path.join(folder, url.split('/')[-1])
    with open(filename, 'wb') as file:
        file.write(response.content)

def fetch_pdfs_from_page(url, folder):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))
    
    pdf_urls = [urljoin(url, link['href']) for link in pdf_links]
    return pdf_urls

def download_pdfs_from_urls(urls, folder):
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda url: download_pdf(url, folder), urls)
```

5. **Fetch and download PDFs from the main page and tabs using threads**:
```python
pdf_urls = fetch_pdfs_from_page(base_url, 'pdf_files')
download_pdfs_from_urls(pdf_urls, 'pdf_files')

for tab in tabs:
    tab_url = urljoin(base_url, f"default.asp?study={tab}")
    pdf_urls = fetch_pdfs_from_page(tab_url, 'pdf_files')
    download_pdfs_from_urls(pdf_urls, 'pdf_files')
```

## Differences

- **Execution Speed**:
    - The single-threaded script processes PDF downloads sequentially, which can be slow for a large number of files.
    - The multi-threaded script uses four threads to download PDFs concurrently, significantly improving download speed.

- **Complexity**:
    - The single-threaded script is simpler and easier to understand for basic use cases.
    - The multi-threaded script introduces additional complexity with threading but provides better performance for larger tasks.