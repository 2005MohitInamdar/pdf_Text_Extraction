🧾 PDF Structured Text Extractor

A fast, intelligent, and lightweight PDF text extraction utility built using [`pdfplumber`](https://github.com/jsvine/pdfplumber).  
This script goes beyond simple text scraping — it intelligently groups words by spatial relationships on the page to reconstruct meaningful structure, preserving lines, tables, and layout context.

🚀 Features

✅ Dual Extraction Modes
- Automatically detects whether the PDF supports direct text extraction.  
- Falls back to spatial word grouping for scanned or non-standard PDFs.

✅ Smart Word Grouping
- Groups words based on horizontal and vertical distances between their bounding boxes.  
- Rebuilds text lines as they appear visually on the page.

✅ Preserves Readability & Order
- Extracts clean, logically structured text from messy layouts, resumes, invoices, etc.

✅ Faster Than AI APIs
- Unlike AI/NLP-based extraction systems that require cloud requests and processing time, this script runs locally and returns results instantly.

✅ Simple Integration
- One import line, one function call, full text extracted.

🧠 How It Works

This module uses a hybrid approach:
1. Primary extraction – tries to extract text directly using `pdfplumber.page.extract_text()`.  
2. Fallback extraction – when direct text extraction fails (due to scanned, layered, or vector PDFs),  
   it switches to a spatial analysis mode that:
   - Extracts individual word bounding boxes.
   - Calculates horizontal and vertical distances.
   - Groups nearby words intelligently into lines.
   - Joins lines to reconstruct the page text in readable order.

This makes it highly robust across different document formats — from plain PDFs to scanned resumes and reports.

🧩 Installation

You can clone and use it directly:

bash
https://github.com/2005MohitInamdar/pdf_Text_Extraction
cd pdf_Text_Extraction
pip install -r requirements.txt

Or manually install the required dependency:
pip install pdfplumber


🧰 Usage
from extractor import extract_text_from_pdf

pdf_path = "E:/resumes/Ved Devanand Dhanokar Resume.pdf"

text = extract_text_from_pdf(pdf_path)

print(text)

🪄 Function Overview
| Approach                              | Speed              | Internet Required  | Accuracy on Text PDFs  | Accuracy on Scanned PDFs  | Cost    |
| ------------------------------------- | -----------------  | -----------------  | ---------------------  | ------------------------  | ------- |
| This Script (`pdfplumber`)            | ⚡ Fast (Local)   | ❌ No              | ✅ High                | ⚠️ Medium                | 💸 Free |
| AI/NLP APIs (OpenAI, LangChain, etc.) | 🕒 Slower (Cloud) | ✅ Yes             | ✅ High                | ✅ Very High             | 💰 Paid |
| OCR Tools (Tesseract, PyTesseract)    | 🐢 Slower         | ❌ No              | ⚠️ Medium              | ✅ Good                  | 💸 Free |
