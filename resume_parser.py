import PyPDF2

def extract_text(pdf_file):

    text = ""

    reader = PyPDF2.PdfReader(pdf_file)

    for page in reader.pages:
        text += page.extract_text()

    return text