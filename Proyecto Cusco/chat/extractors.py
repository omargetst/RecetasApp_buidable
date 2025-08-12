import pdfplumber
from PIL import Image
import pytesseract
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdfs(files):
    """
    Extrae texto de una lista de archivos PDF.
    """
    combined_text = ""
    for file in files:
        try:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        combined_text += text + "\n"
        except Exception as e:
            logger.warning(f"Error al procesar PDF {file.name}: {e}")
    return combined_text

def extract_text_from_images(files):
    """
    Extrae texto usando OCR de una lista de imágenes (JPG, PNG, etc.).
    """
    combined_text = ""
    for file in files:
        try:
            image = Image.open(file)
            text = pytesseract.image_to_string(image)
            combined_text += text + "\n"
        except Exception as e:
            logger.warning(f"Error al procesar imagen {file.name}: {e}")
    return combined_text
