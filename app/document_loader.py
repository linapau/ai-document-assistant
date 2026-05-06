from pypdf import PdfReader

def load_document_pages(file_path):
    reader = PdfReader(file_path)
    page_text = ""
    pages = [] # Initialize an empty list to store page information (page number and text)

    for i, page in enumerate(reader.pages): # Iterate through each page in the PDF
        page_text += page.extract_text() or "" # Extract text from the current page and append it to the 'page_text' variable

        pages.append({
            "page_number": i + 1, # Store the page number (starting from 1)
            "text": page_text # Store the extracted text for the current page
        })

    return pages