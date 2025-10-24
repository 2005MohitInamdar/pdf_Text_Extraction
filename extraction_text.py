"""
PDF Text Extraction Script
--------------------------
This module provides a robust method for extracting structured text
from PDF files using the `pdfplumber` library. It intelligently groups
words based on their spatial relationships on a page to preserve layout
as much as possible when direct text extraction fails.

Features:
    - Handles both text-based and scanned PDFs (fallback to word grouping)
    - Groups words based on horizontal/vertical distances
    - Suppresses pdfplumber warnings for cleaner output
    - Provides detailed error handling and page-wise output
"""


import pdfplumber
import math
import logging
from collections import defaultdict

# Suppress specific pdfplumber CropBox warnings
logging.getLogger("pdfplumber").setLevel(logging.ERROR)

def get_directional_distances(word1, word2):
    """
    Calculate the horizontal and vertical distances between
    the centers of two word bounding boxes.

    Args:
        word1 (dict): Word metadata dictionary returned by pdfplumber.
        word2 (dict): Another word metadata dictionary.

    Returns:
        tuple: (horizontal_distance, vertical_distance)
    """
    
    
    # Calculate horizontal and vertical distances using bounding box centers
    x1, y1 = (word1['x0'] + word1['x1']) / 2, (word1['top'] + word1['bottom']) / 2
    x2, y2 = (word2['x0'] + word2['x1']) / 2, (word2['top'] + word2['bottom']) / 2
    
    # Return absolute horizontal and vertical distance
    horizontal_dist = abs(x2 - x1)
    vertical_dist = abs(y2 - y1)
    return horizontal_dist, vertical_dist

def extract_structured_text(page, threshold=15):
    """
    Extract structured word groups from a given PDF page when
    simple text extraction fails (e.g., scanned, badly formatted, or table PDFs).

    This function:
        - Extracts all words with small positional tolerances
        - Sorts them top-to-bottom, left-to-right
        - Groups them into lines based on spatial proximity

    Args:
        page (pdfplumber.page.Page): The page object to extract text from.
        threshold (int): Distance threshold in pixels for grouping words.

    Returns:
        list[list[dict]]: List of grouped words (each group represents one line).
    """
    
    
    # Extract words with adjusted tolerances to capture more words
    words = page.extract_words(x_tolerance=2, y_tolerance=2, keep_blank_chars=True)
    if not words:
        return []
    
    # Sort words from top to bottom, then left to right
    words = sorted(words, key=lambda w: (w['top'], w['x0']))
    
    groups = []         # List of word groups (lines)
    processed = set()   # Track which words are already used in a group
    
    # Iterate over each word to build groups
    for i, current_word in enumerate(words):
        if i in processed:
            continue
        
        # Start a new group (potential new line)
        current_group = [current_word]
        processed.add(i)
        
        # Try to expand the group by finding neighboring words
        while True:
            closest_word = None
            min_horizontal_dist = float('inf')
            min_vertical_dist = float('inf')
            closest_idx = None
            is_horizontal = True
            
            # Compare with all other unprocessed words
            for j, other_word in enumerate(words):
                if j in processed:
                    continue
                
                # Compute distance between current word and candidate
                h_dist, v_dist = get_directional_distances(current_word, other_word)
                
                # Determine which direction the neighbor likely belongs to
                if h_dist < v_dist and h_dist < min_horizontal_dist:
                    # Likely on the same line (horizontal)
                    min_horizontal_dist = h_dist
                    closest_word = other_word
                    closest_idx = j
                    is_horizontal = True
                elif v_dist < min_vertical_dist:
                    # Likely next line (vertical)
                    min_vertical_dist = v_dist
                    closest_word = other_word
                    closest_idx = j
                    is_horizontal = False
            
            # Stop if no nearby word is within threshold
            if closest_word is None or min(min_horizontal_dist, min_vertical_dist) > threshold:
                break
                
            # Mark this word as processed
            processed.add(closest_idx)
            
            # Add horizontally or vertically, depending on position
            if is_horizontal:
                # Continue adding to same line
                current_group.append(closest_word)
                current_word = closest_word
            else:
                # Finalize current line before starting new one
                current_group = sorted(current_group, key=lambda w: w['x0'])
                groups.append(current_group)
                current_group = [closest_word]
                current_word = closest_word
        
        # After loop ends, finalize the current group (line)
        if current_group:
            current_group = sorted(current_group, key=lambda w: w['x0'])
            groups.append(current_group)
    
    return groups

# Main function for text extraction from pdf
def extract_text_from_pdf(pdf_path):
    """
    Extract readable text from a given PDF file.

    The function automatically detects whether the PDF supports
    direct text extraction. If not, it falls back to structured
    extraction using bounding box grouping.

    Args:
        pdf_path (str): Full path to the PDF file.

    Returns:
        str: Combined extracted text from all pages, separated by headers.
    """
    
    
    print("Starting text extraction")
    full_text = ""
    try:
        # Open PDF using pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                # Try normal text extraction first
                text = page.extract_text(keep_blank_chars=True)
                if text and len(text.strip()) > 0:
                    # Add extracted text with page header
                    full_text += f"\n--- Page {i+1} ---\n{text.strip()}\n"
                else:
                    # Fallback: use structured extraction (grouping method)
                    groups = extract_structured_text(page)
                    if groups:
                        full_text += f"\n--- Page {i+1} ---\n"
                        for idx, group in enumerate(groups):
                            # Join words in each line
                            group_text = " ".join(word['text'] for word in group).strip()
                            if group_text:
                                full_text += f"{group_text}\n"
                    else:
                        # Handle pages with no text at all
                        full_text += f"\n--- Page {i+1} ---\n[No text found]\n"
        return full_text.strip()
    except FileNotFoundError:
        return "Error: The file was not found. Please provide the correct file path."
    except Exception as e:
        return f"Error: An unexpected issue occurred: {str(e)}"