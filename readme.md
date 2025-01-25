
# PDF Spider

PDF Spider is a Python-based web scraping application designed to search for and download PDF files from websites. It features a graphical user interface (GUI) powered by PyQt5, enabling easy interaction with the software. The tool is multi-threaded, highly customizable, and allows you to control the scraping depth and domain traversal options.

## Features

- **PDF File Downloading**: Automatically locates and downloads PDF files from websites.
- **Multi-threading**: Supports concurrent scraping for faster operation.
- **Depth Control**: Allows users to specify the depth of traversal.
- **Domain Restriction**: Option to scrape only within the given domain.
- **GUI Interface**: Easy-to-use interface for non-technical users.
- **CSV Export**: Logs the scraped URLs and filenames to a CSV file for reference.

## Requirements

- Python 3.6 or higher
- PyQt5
- BeautifulSoup4
- Requests

You can install the required packages using:
```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository or download the source code.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. **Start the application**: Run the Python script (`main.py`) to launch the GUI.
2. **Input parameters**:
   - Enter the URL of the website to scrape.
   - Select or specify the directory to save downloaded PDFs.
   - Set the number of threads for multi-threading.
   - Define the scraping depth.
   - Enable or disable domain-only traversal using the checkbox.
3. **Start the process**: Click the "Start" button to begin scraping.
4. **Stop the process**: If needed, click the "Stop" button to halt the operation.
5. **View logs**: Downloaded files and their source URLs are logged in a CSV file saved in the specified directory.

## Example

To scrape a website for PDF files:

1. Enter the website URL (e.g., `https://example.com`).
2. Specify a directory to save the PDFs (e.g., `C:/Downloads`).
3. Set the number of threads (e.g., `5`) and depth (e.g., `2`).
4. Check the "Traverse only within domain" option if you want to limit scraping to the specified domain.
5. Click "Start" to begin.

## Error Handling

- Invalid URLs and unreachable websites will be skipped, and the errors will be logged in the terminal.
- Insecure requests warnings are disabled by default.

## Limitations

- The software relies on website structure; significant deviations in the target website's HTML may require code adjustments.
- Depth and thread count settings may impact performance on larger websites.

## Contributing

If you'd like to contribute to the development of this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
