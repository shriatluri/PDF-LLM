import pytesseract
from PIL import Image
import PyPDF2
from pdf2image import convert_from_path

#function to extract the text from PDF
def extract_text(pdf_path):
    #Using PyPDF2 first since it is used to extract text directly from PDF
    try:
        #open in binary since PDF
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfFileReader(file)
            if reader.isEncrypted:
                reader.decrypt('')
            text = []
            #for the pages in the PDF
            for page_num in range(reader.getNumPages()):
                page = reader.getPage(page_num)
                text.append(page.extractText())
            #if there is no text in text extraction
            if not text or not any(text):
                raise ValueError('No text, might be scanned PDF')
            #combines all elements of the text into a single list
            text_output = '\n'.join(text)
            #text is written into text_file
            with open('output_text.txt', 'w') as text_file:
                text_file.write(text_output)
            print('Text extracted using PyPDF2 and written to output_text.txt')
    except Exception as e:
        print(f'Failed with PyPDF due to {e}, OCR in progress')
        #OCR if PyPDF doesn't work
        images = convert_from_path(pdf_path)
        ocr_txt = [pytesseract.image_to_string(image) for image in images]
        ocr_txt_output = '\n'.join(ocr_txt)
        #open as a text file
        with open(ocr_txt_output.txt, 'w') as text_file:
            text_file.write(ocr_txt_output)
        print('Text has been extracted using OCR and writtn in output_text_ocr.txt')
