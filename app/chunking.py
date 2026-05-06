def chunk_document_pages(pages, chunk_size=500, overlap=100):
    # now we will use a generator to yield chunks of text instead of returning a list, which can be more memory efficient for large texts
    # ex. if chunk_size is 500 and overlap is 100, the first chunk will be from index 0 to 500, the second chunk will start at index 400 (500 - 100) and end at index 900 (400 + 500), creating an overlap of 100 characters between the two chunks.
    # start = 0, 400, 800, 1200, 1600, ...

    for page in pages:
        start = 0 # Initialize the starting index for chunking the text, starts at the beginning of the text for each page
        text = page["text"] # Get all of the text to current page
        print(text)
        
        while start < len(text): 
            end = start + chunk_size # Calculate the ending index for the current chunk of text

            yield { # Yield a dictionary containing the chunk of text and the corresponding page number
                "text": text[start:end],
                "page": page["page_number"]
            }

            start += chunk_size - overlap # Move the starting index forward by 'chunk_size' minus 'overlap' to create overlapping chunks of text