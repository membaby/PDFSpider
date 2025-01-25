from bs4 import BeautifulSoup
import requests
import os
import urllib3
import csv
import datetime
import traceback
import concurrent.futures
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PDFSpider:
    def __init__(self, url, directory, threads, depth, domainOnly, parent):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15',
            'Connection': 'keep-alive'
        }
        self.base_url = url
        self.directory = directory
        self.threads = threads
        self.domain = url.split('/')[2].replace('www.', '').split('/')[0]
        self.parent = parent
        self.depth = depth
        self.domainOnly = domainOnly
        os.makedirs(self.directory, exist_ok=True)
        self.history = []

        filename = f'pdfs_{parent.version}_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
        writer_filename = os.path.join(self.directory, filename)
        self.file = open(writer_filename, 'w', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=['depth', 'url', 'filename'])
        self.writer.writeheader()

    def get_cases(self, url, links=False, depth=0):
        if self.parent.running == False or not isinstance(url, str):
            return [], [], []
        if 'http' not in url:
            url = 'https://www.' + self.domain + url

        self.parent.info = 'Scraping ' + url + '...'
        try:
            response = requests.request("GET", url, headers=self.headers, timeout=60, verify=False)
        except Exception as err:
            print('[ERROR] (1)', url, err)
            return [], [], []
        soup = BeautifulSoup(response.text, 'html.parser')
        next_page = soup.find('a', class_='usa-pagination__next-page')
        if next_page: next_page = url.split('?')[0] + next_page['href']
        
        cases_holder = soup.find('div', class_='cases-multi-defendant')
        cases_links = []
        if cases_holder:
            for case in cases_holder.find('table').find('tbody').find_all('tr'):
                link = case.find('a')['href']
                cases_links.append(link)

        links = []
        for link in soup.find_all('a', href=True):
            if '/dl' in link['href'] or '.pdf' in link['href']:
                try:
                    self.download_pdf(link['href'], depth)
                except Exception:
                    traceback.print_exc()
            elif self.domainOnly and self.domain in link['href'].split('?')[0] or not self.domainOnly:
                links.append(link['href'])

        return next_page, cases_links, links
    
    def get_case_pdf(self, url, depth=0):
        print('[DEBUG] Getting', url)
        self.parent.info = 'Scraping ' + url
        if 'http' not in url:
            url = 'https://www.' + self.domain + url
        for i in range(5):
            try:
                response = requests.request("GET", url, headers=self.headers)
                break
            except Exception:
                print('[ERROR] (2) Failed to get', url)
            finally:
                if i == 4: return
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            if '/dl' in link['href'] or '.pdf' in link['href']:
                try:
                    self.download_pdf(link['href'], depth)
                except Exception:
                    traceback.print_exc()

    def handle_page(self, url, depth=0):
        if depth == self.depth: 
            return
        if url in self.history: 
            return
        self.history.append(url)
        print(f'[DEBUG] Depth: {depth+1} URL: {url}')
        next_page, case_links, page_links = self.get_cases(url, True, depth+1)
        for case_link in case_links:
            self.get_case_pdf(case_link)

        while next_page:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.threads)
            next_page, case_links, page_links = self.get_cases(next_page, False, depth+1)
            for case_link in case_links:
                executor.submit(self.get_case_pdf, case_link, depth+1)
            executor.shutdown(wait=True)
        
        for page_link in page_links:
            self.handle_page(page_link, depth+1)

    def start_process(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.threads)

        next_page, case_links, page_links = self.get_cases(self.base_url, True, 0)
        for case_link in case_links:
            executor.submit(self.get_case_pdf, case_link, 0)
        
        for page_link in page_links:
            print('[DEBUG] Handling', page_link)
            executor.submit(self.handle_page, page_link)

        executor.shutdown(wait=True)
        d = 1
        while next_page:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.threads)
            next_page, case_links, page_links = self.get_cases(next_page, False, d)
            for case_link in case_links:
                executor.submit(self.get_case_pdf, case_link, d)
            executor.shutdown(wait=True)
            d += 1
        self.parent.info = 'Finished'

    def download_pdf(self, pdf_link, depth):
        if 'http' not in pdf_link:
            pdf_link = 'https://www.' + self.domain + pdf_link
        filename = pdf_link.split('/')[-1]
        if not filename.endswith('.pdf'):
            filename = pdf_link.split('/')[-2] + '.pdf'
        filename = os.path.join(self.directory, filename)
        if os.path.exists(filename):
            print('[DEBUG] Skipping', pdf_link, filename)
            return
        self.parent.info = 'Downloading ' + pdf_link + '...'
        print('[DEBUG] Downloading', pdf_link, 'to', self.directory)
        try:
            response = requests.request("GET", pdf_link, headers=self.headers, verify=False, timeout=60)
            if response.status_code != 200:
                print('[ERROR] (3) Invalid PDF', pdf_link, response.status_code)
                return
        except Exception as err:
            print('[ERROR] (4)', pdf_link, err)
            return
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        self.writer.writerow({'url': pdf_link, 'filename': filename, 'depth': depth})
        self.file.flush()