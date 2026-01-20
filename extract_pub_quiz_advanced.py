#!/usr/bin/env python3
"""
Script avanzado para extraer información de PDFs de Pub Quiz
Intenta múltiples métodos: pdfplumber, PyPDF2, y OCR con pytesseract
"""

import os
import sys

def install_package(package):
    """Instala un paquete si no está disponible"""
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando {package}...")
        os.system(f"{sys.executable} -m pip install {package}")

def extract_with_pdfplumber(pdf_path):
    """Intenta extraer con pdfplumber"""
    try:
        install_package('pdfplumber')
        import pdfplumber
        
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            print(f"  📖 Páginas: {len(pdf.pages)}")
            for i, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n{'='*60}\n"
                    text += f"Página {i}\n"
                    text += f"{'='*60}\n"
                    text += page_text + "\n"
                
                # También intentar extraer tablas
                tables = page.extract_tables()
                if tables:
                    text += f"\n[Tablas encontradas en página {i}]\n"
                    for table_num, table in enumerate(tables, 1):
                        text += f"\nTabla {table_num}:\n"
                        for row in table:
                            text += " | ".join([str(cell) if cell else "" for cell in row]) + "\n"
        
        return text if text.strip() else None
    except Exception as e:
        print(f"  ❌ Error con pdfplumber: {e}")
        return None

def extract_with_pypdf2(pdf_path):
    """Intenta extraer con PyPDF2"""
    try:
        install_package('PyPDF2')
        import PyPDF2
        
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"  📖 Páginas: {len(pdf_reader.pages)}")
            for i, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n{'='*60}\n"
                    text += f"Página {i}\n"
                    text += f"{'='*60}\n"
                    text += page_text + "\n"
        
        return text if text.strip() else None
    except Exception as e:
        print(f"  ❌ Error con PyPDF2: {e}")
        return None

def extract_with_ocr(pdf_path):
    """Intenta OCR si el PDF es una imagen"""
    try:
        print("  🔍 Intentando OCR (esto puede tardar)...")
        install_package('pdf2image')
        install_package('pytesseract')
        
        from pdf2image import convert_from_path
        import pytesseract
        
        # Convertir PDF a imágenes
        images = convert_from_path(pdf_path)
        print(f"  📖 Páginas (imágenes): {len(images)}")
        
        text = ""
        for i, image in enumerate(images, 1):
            print(f"    Procesando página {i} con OCR...")
            page_text = pytesseract.image_to_string(image, lang='eng')
            if page_text:
                text += f"\n{'='*60}\n"
                text += f"Página {i} (OCR)\n"
                text += f"{'='*60}\n"
                text += page_text + "\n"
        
        return text if text.strip() else None
    except Exception as e:
        print(f"  ❌ OCR no disponible: {e}")
        print("  💡 Para usar OCR, instala: brew install poppler tesseract")
        return None

def get_pdf_info(pdf_path):
    """Obtiene información básica del PDF"""
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            info = pdf_reader.metadata
            return {
                'pages': len(pdf_reader.pages),
                'title': info.get('/Title', 'N/A') if info else 'N/A',
                'author': info.get('/Author', 'N/A') if info else 'N/A',
                'subject': info.get('/Subject', 'N/A') if info else 'N/A',
            }
    except:
        return {}

def main():
    """Función principal"""
    docs_dir = "docs"
    
    pdf_files = [
        "Pub Quiz 1 - Quizz Format.pdf",
        "Pub Quiz 2 - Printed Answer Sheets.pdf",
        "Pub Quiz 3 - using Quiz Buzzers.pdf",
        "Pub Quiz 4 - Gentre Selection.pdf"
    ]
    
    output_file = os.path.join(docs_dir, "PUB_QUIZ_EXTRACTED_INFO.md")
    
    all_content = "# Información Extraída de PDFs de Pub Quiz\n\n"
    all_content += f"Fecha de extracción: {os.popen('date').read().strip()}\n\n"
    all_content += "---\n\n"
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(docs_dir, pdf_file)
        
        if not os.path.exists(pdf_path):
            print(f"⚠️  No encontrado: {pdf_file}")
            continue
        
        print(f"\n{'='*80}")
        print(f"📄 Procesando: {pdf_file}")
        print(f"{'='*80}")
        
        # Información básica
        info = get_pdf_info(pdf_path)
        
        all_content += f"\n## {pdf_file}\n\n"
        if info:
            all_content += f"**Páginas:** {info.get('pages', 'N/A')}\n\n"
        
        # Intentar diferentes métodos de extracción
        extracted_text = None
        
        # Método 1: pdfplumber
        print("  🔧 Intentando con pdfplumber...")
        extracted_text = extract_with_pdfplumber(pdf_path)
        
        # Método 2: PyPDF2
        if not extracted_text:
            print("  🔧 Intentando con PyPDF2...")
            extracted_text = extract_with_pypdf2(pdf_path)
        
        # Método 3: OCR
        if not extracted_text:
            extracted_text = extract_with_ocr(pdf_path)
        
        if extracted_text:
            all_content += extracted_text + "\n\n"
            print(f"  ✅ Texto extraído ({len(extracted_text)} caracteres)")
            # Mostrar preview
            preview = extracted_text[:300].replace('\n', ' ')
            print(f"  Preview: {preview}...")
        else:
            warning = "⚠️ No se pudo extraer texto. El PDF puede contener solo imágenes."
            all_content += f"_{warning}_\n\n"
            print(f"  {warning}")
        
        all_content += "\n---\n\n"
    
    # Guardar resultado
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_content)
    
    print(f"\n{'='*80}")
    print(f"✅ COMPLETADO")
    print(f"{'='*80}")
    print(f"📝 Archivo guardado en: {output_file}")
    print(f"📊 Tamaño: {len(all_content)} caracteres")
    print(f"\n💡 Ver resultado: cat '{output_file}'")
    print(f"💡 Abrir en VS Code: code '{output_file}'")

if __name__ == "__main__":
    main()
