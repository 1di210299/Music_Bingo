#!/usr/bin/env python3
"""
Script para extraer información de los PDFs de Pub Quiz
Utiliza PyPDF2 para leer el contenido de los archivos PDF
"""

import os
import sys

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 no está instalado. Instalando...")
    os.system(f"{sys.executable} -m pip install PyPDF2")
    import PyPDF2


def extract_text_from_pdf(pdf_path):
    """
    Extrae todo el texto de un archivo PDF
    
    Args:
        pdf_path: Ruta al archivo PDF
        
    Returns:
        String con todo el texto extraído
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            print(f"\n{'='*80}")
            print(f"Archivo: {os.path.basename(pdf_path)}")
            print(f"Número de páginas: {len(pdf_reader.pages)}")
            print(f"{'='*80}\n")
            
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                text += f"\n--- Página {page_num} ---\n"
                text += page_text + "\n"
            
            return text
    except Exception as e:
        return f"Error al leer {pdf_path}: {str(e)}"


def main():
    """Función principal"""
    docs_dir = "docs"
    
    # Lista de PDFs a procesar
    pdf_files = [
        "Pub Quiz 1 - Quizz Format.pdf",
        "Pub Quiz 2 - Printed Answer Sheets.pdf",
        "Pub Quiz 3 - using Quiz Buzzers.pdf",
        "Pub Quiz 4 - Gentre Selection.pdf"
    ]
    
    # Archivo de salida
    output_file = os.path.join(docs_dir, "PUB_QUIZ_EXTRACTED_INFO.md")
    
    all_content = "# Información Extraída de PDFs de Pub Quiz\n\n"
    all_content += f"Fecha de extracción: {os.popen('date').read().strip()}\n\n"
    
    # Procesar cada PDF
    for pdf_file in pdf_files:
        pdf_path = os.path.join(docs_dir, pdf_file)
        
        if not os.path.exists(pdf_path):
            print(f"⚠️  Archivo no encontrado: {pdf_path}")
            continue
        
        print(f"📄 Procesando: {pdf_file}")
        extracted_text = extract_text_from_pdf(pdf_path)
        
        # Agregar al contenido total
        all_content += f"\n\n{'#'*80}\n"
        all_content += f"## {pdf_file}\n"
        all_content += f"{'#'*80}\n\n"
        all_content += extracted_text
        
        # También imprimir en consola
        print(extracted_text[:500])  # Mostrar primeros 500 caracteres
        print("...\n")
    
    # Guardar en archivo
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_content)
    
    print(f"\n✅ Extracción completada!")
    print(f"📝 Información guardada en: {output_file}")
    print(f"\n💡 Puedes revisar el archivo con: cat {output_file}")


if __name__ == "__main__":
    main()
