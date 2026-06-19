#for parsing the pdf we get

from pypdf import PdfReader

def extract_text_from_pdf(file_address):
        
    reader = PdfReader(file_address)
    number_of_page=len(reader.pages)
    text =[]
    for i in range(number_of_page):
        page = reader.pages[i]
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return " ".join(text)
