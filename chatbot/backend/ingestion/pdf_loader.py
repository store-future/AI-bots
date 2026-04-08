import fitz 

# filepath = "data/uploads/Dhananjay_Resume (2) (1).pdf"

def load_pdf(filepath):
    data = fitz.open(filepath)
    text = ""

    for page in data:
        text += page.get_text()
    print(len(text))
    return text 

# print(load_pdf(filepath))
