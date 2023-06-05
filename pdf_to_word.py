import tkinter as tk
from tkinter import filedialog
from pdf2docx import Converter

def convert_pdf_to_word(pdf_file, output_file):
    # Crear un objeto de conversión
    cv = Converter(pdf_file)

    # Procesar y convertir el PDF a un archivo de Word (.docx)
    cv.convert(output_file, start=0, end=None)

    # Cerrar el objeto de conversión
    cv.close()

def select_pdf_file():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de tkinter

    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return file_path

if __name__ == '__main__':
    print("Instrucciones:")
    print("1. Ejecuta este script.")
    print("2. Se abrirá una ventana de diálogo para seleccionar el archivo PDF que deseas convertir.")
    print("3. El archivo de Word (.docx) resultante se guardará en la misma ubicación que el archivo PDF de entrada con el mismo nombre, pero con la extensión .docx.\n")

    input_pdf = select_pdf_file()
    if input_pdf:
        output_docx = input_pdf.replace('.pdf', '.docx')
        convert_pdf_to_word(input_pdf, output_docx)
        print(f'Archivo convertido y guardado como: {output_docx}')
    else:
        print("No se seleccionó ningún archivo.")
