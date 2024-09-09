import sys
import requests
from bs4 import BeautifulSoup
from collections import Counter
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QScrollArea, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class WebScraperGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Web Scraper')

        # Set up the layout
        layout = QVBoxLayout()

        # Create a font object
        font = QFont("Arial", 20)

        # Create a label for the URL input
        self.url_label = QLabel('Enter the URLs of the websites you want to scrape (separate by commas or new lines):')
        self.url_label.setAlignment(Qt.AlignCenter)
        self.url_label.setFont(font)
        layout.addWidget(self.url_label)

        # Create a text edit for the multiple URL inputs
        self.url_input = QTextEdit()
        self.url_input.setFont(font)
        layout.addWidget(self.url_input)

        # Create a label for the tag input
        self.tag_label = QLabel('Enter the HTML tag you want to scrape for (or leave empty to use checkboxes):')
        self.tag_label.setAlignment(Qt.AlignCenter)
        self.tag_label.setFont(font)
        layout.addWidget(self.tag_label)

        # Create a line edit for the tag input
        self.tag_input = QLineEdit()
        self.tag_input.setFont(font)
        layout.addWidget(self.tag_input)

        # Create checkboxes for different elements to scrape
        self.checkboxes_layout = QHBoxLayout()
        self.headings_checkbox = QCheckBox('Headings')
        self.paragraphs_checkbox = QCheckBox('Paragraphs')
        self.links_checkbox = QCheckBox('Links')
        self.images_checkbox = QCheckBox('Images')

        # Add checkboxes to the layout
        self.checkboxes_layout.addWidget(self.headings_checkbox)
        self.checkboxes_layout.addWidget(self.paragraphs_checkbox)
        self.checkboxes_layout.addWidget(self.links_checkbox)
        self.checkboxes_layout.addWidget(self.images_checkbox)
        layout.addLayout(self.checkboxes_layout)

        # Create a button to start the scraping
        self.scrape_button = QPushButton('Scrape Websites')
        self.scrape_button.setFont(font)
        self.scrape_button.clicked.connect(self.scrape_websites)
        layout.addWidget(self.scrape_button)

        # Create a scrollable area to display the results
        self.scroll_area = QScrollArea()
        self.scroll_area.setFixedSize(1200, 400)
        self.result_area = QTextEdit()
        self.result_area.setFixedSize(1200, 400)
        self.result_area.setReadOnly(True)
        self.result_area.setAlignment(Qt.AlignCenter)

        self.scroll_area.setWidget(self.result_area)
        layout.addWidget(self.scroll_area)

        # Set the layout for the main window
        self.setLayout(layout)

    def scrape_websites(self):
        # Get the URLs from the input and split by commas or new lines
        urls = self.url_input.toPlainText().strip().replace("\n", ",").split(',')
        urls = [url.strip() for url in urls if url.strip()]

        # Get the tag from the input
        tag = self.tag_input.text().strip()

        # Prepare the result string
        result_text = ""

        # Loop through each URL
        for url in urls:
            result_text += f"Scraping URL: {url}\n\n"

            # Send a request to the website
            try:
                response = requests.get(url)

                # Check if the request was successful
                if response.status_code == 200:
                    # Parse the HTML content using BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')

                    if tag:  # If a custom tag is provided, scrape for that tag
                        elements = soup.find_all(tag)
                        if elements:
                            result_text += f"Elements with tag '{tag}':\n"
                            for idx, element in enumerate(elements, start=1):
                                result_text += f"Element {idx}: {element.text.strip()}\n"
                        else:
                            result_text += f"No elements found with tag '{tag}'."
                    else:  # Otherwise, use the checkboxes
                        if self.headings_checkbox.isChecked():
                            headings = []
                            for i in range(1, 7):
                                headings.extend(soup.find_all(f'h{i}'))
                            if headings:
                                result_text += "Headings:\n"
                                for idx, heading in enumerate(headings, start=1):
                                    result_text += f"{heading.name.upper()} {idx}: {heading.text.strip()}\n"
                                result_text += "\n"

                        if self.paragraphs_checkbox.isChecked():
                            paragraphs = soup.find_all('p')
                            if paragraphs:
                                result_text += "Paragraphs:\n"
                                for idx, paragraph in enumerate(paragraphs, start=1):
                                    result_text += f"Paragraph {idx}: {paragraph.text.strip()}\n"
                                result_text += "\n"

                        if self.links_checkbox.isChecked():
                            links = soup.find_all('a')
                            if links:
                                result_text += "Links:\n"
                                link_urls = [link.get('href') for link in links if link.get('href')]
                                link_counts = Counter(link_urls)
                                for idx, (link, count) in enumerate(link_counts.items(), start=1):
                                    result_text += f"Link {idx}: {link} (Used {count} times)\n"
                                result_text += "\n"

                        if self.images_checkbox.isChecked():
                            images = soup.find_all('img')
                            if images:
                                result_text += "Images:\n"
                                for idx, img in enumerate(images, start=1):
                                    result_text += f"Image {idx}: {img.get('src') or 'No source attribute'}\n"
                                result_text += "\n"

                        if not result_text:
                            result_text += "No selected items found on the page."

                else:
                    result_text += f"Failed to retrieve the webpage. Status code: {response.status_code}\n\n"
            except Exception as e:
                result_text += f"Error while scraping {url}: {str(e)}\n\n"

        # Display the results in the text area
        self.result_area.setText(result_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WebScraperGUI()
    window.show()
    sys.exit(app.exec_())

