# import fitz  # PyMuPDF
# from googletrans import Translator
# import time

# def extract_text_from_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text

# def split_text(text, max_chars=5000):
#     """Split text into chunks that are under max_chars each"""
#     return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

# def translate_text(text, dest_language):
#     translator = Translator()
#     translated_chunks = []

#     for chunk in split_text(text):
#         try:
#             translated = translator.translate(chunk, dest=dest_language)
#             translated_chunks.append(translated.text)
#             time.sleep(1)  # avoid sending requests too fast
#         except Exception as e:
#             print("Translation error:", e)
#             translated_chunks.append("[Translation Failed]")

#     return "\n".join(translated_chunks)

# def save_translated_text(text, output_path):
#     with open(output_path, 'w', encoding='utf-8') as f:
#         f.write(text)

# def pdf_to_translated_text(pdf_path, output_path, target_language='gu'):
#     print("Extracting text from PDF...")
#     original_text = extract_text_from_pdf(pdf_path)

#     print("Translating text...")
#     translated_text = translate_text(original_text, target_language)

#     print("Saving translated text...")
#     save_translated_text(translated_text, output_path)

#     print("✅ Translation complete. Saved to:", output_path)

# # Example usage:
# pdf_to_translated_text("sample.pdf", "translated_output.txt", target_language="gu")

import fitz  # PyMuPDF
from googletrans import Translator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import time
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def split_text(text, max_chars=4000):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

def translate_text(text, dest_language):
    translator = Translator()
    translated_chunks = []

    for chunk in split_text(text):
        try:
            translated = translator.translate(chunk, dest=dest_language)
            translated_chunks.append(translated.text)
            time.sleep(1)
        except Exception as e:
            print("Translation error:", e)
            translated_chunks.append("[Translation Failed]")

    return "\n".join(translated_chunks)

def save_translated_to_pdf(text, output_pdf_path, font_path, font_name="GujaratiFont"):
    # Register your Gujarati font
    pdfmetrics.registerFont(TTFont(font_name, font_path))
    
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    c.setFont(font_name, 12)

    width, height = letter
    lines = text.split('\n')
    y = height - 40

    for line in lines:
        if y < 40:
            c.showPage()
            c.setFont(font_name, 12)
            y = height - 40
        c.drawString(40, y, line[:90])  # limit line length
        y -= 18

    c.save()

def pdf_to_translated_pdf(pdf_path, output_pdf_path, target_language='gu', font_path='fonts/NotoSansGujarati-Regular.ttf'):
    print("Extracting text from PDF...")
    original_text = extract_text_from_pdf(pdf_path)

    print("Translating text...")
    translated_text = translate_text(original_text, target_language)

    print("Saving translated PDF...")
    save_translated_to_pdf(translated_text, output_pdf_path, font_path)

    print("✅ Done! Saved as:", output_pdf_path)

# Example usage:
pdf_to_translated_pdf(
    pdf_path="sample.pdf",
    output_pdf_path="translated_gujarati.pdf",
    target_language="gu",
    font_path="fonts/NotoSansGujarati-Regular.ttf"
)
