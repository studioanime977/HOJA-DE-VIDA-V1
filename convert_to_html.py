import docx
from bs4 import BeautifulSoup

# Load the document
file_path = 'c:/Users/Admin/Desktop/HOJA-DE-VIDA-/H/Hoja de Vida Administrador Sencillo Blanco y Negro.docx'
doc = docx.Document(file_path)

# Create a new HTML document
html = BeautifulSoup('<html><head><title>Hoja de Vida</title></head><body></body></html>', 'html.parser')
body = html.body

# Iterate through paragraphs in the Word document
for para in doc.paragraphs:
    p = html.new_tag('p')
    p.string = para.text
    body.append(p)

# Output HTML to a file
with open('c:/Users/Admin/Desktop/HOJA-DE-VIDA-/hoja_de_vida.html', 'w', encoding='utf-8') as f:
    f.write(str(html))
