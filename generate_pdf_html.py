import os
from PIL import Image, ImageDraw
from fpdf import FPDF
from PyPDF2 import PdfMerger
from playwright.sync_api import sync_playwright

def crop_to_circle(image_path, output_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        min_dim = min(img.size)
        left = (img.size[0] - min_dim) / 2
        top = (img.size[1] - min_dim) / 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, min_dim, min_dim), fill=255)
        img.putalpha(mask)
        img.save(output_path, "PNG")
        return True
    except Exception as e:
        print("Error al recortar la foto circular:", e)
        return False

def generate_html_pdf(html_path, output_pdf_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        file_url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
        page.goto(file_url, wait_until="networkidle")
        page.pdf(path=output_pdf_path, format="A4", print_background=True, margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        browser.close()

def generate_certificates_pdf(images_dir, output_pdf_path, profile_pic_hash):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)
    
    valid_exts = [".jpg", ".jpeg", ".png"]
    images = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in valid_exts]
    
    for img_name in images:
        if img_name == profile_pic_hash or img_name == "profile_circle.png":
            continue
            
        img_path = os.path.join(images_dir, img_name)
        pdf.add_page()
        pdf.set_fill_color(146, 180, 242)
        pdf.rect(0, 0, 210, 20, 'F')
        pdf.set_xy(10, 5)
        pdf.set_font("helvetica", "B", 16)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(0, 10, "ANEXO: CERTIFICADO", align="C")
        
        try:
            img_obj = Image.open(img_path)
            w_px, h_px = img_obj.size
            max_w, max_h = 190, 260
            aspect = w_px / h_px
            if aspect > (max_w / max_h):
                calc_w = max_w
                calc_h = max_w / aspect
            else:
                calc_h = max_h
                calc_w = max_h * aspect
                
            x_pos = (210 - calc_w) / 2
            y_pos = 30 + (260 - calc_h) / 2
            pdf.image(img_path, x=x_pos, y=y_pos, w=calc_w, h=calc_h)
        except Exception as e:
            pdf.set_xy(10, 50)
            pdf.multi_cell(0, 10, f"Error cargando imagen: {e}")
            
    pdf.output(output_pdf_path)

def merge_pdfs(base_pdf, append_pdf, output_pdf):
    merger = PdfMerger()
    merger.append(base_pdf)
    merger.append(append_pdf)
    merger.write(output_pdf)
    merger.close()

if __name__ == "__main__":
    out_dir = r"c:\Users\AYB\Desktop\HOJA-DE-VIDA-V1\public\assets\downloads"
    img_dir = r"c:\Users\AYB\Desktop\HOJA-DE-VIDA-V1\public\assets\images"
    profile_hash = "af05a4d09e806b9ed91636c90bcf70d1.jpg"
    
    # Paths
    pic_path = os.path.join(img_dir, profile_hash)
    circle_pic_path = os.path.join(img_dir, "profile_circle.png")
    html_path = r"c:\Users\AYB\Desktop\HOJA-DE-VIDA-V1\cv_template.html"
    sin_cert_pdf = os.path.join(out_dir, "ESTEBAN-MANUEL-LOPEZ-RIVERO.pdf")
    con_cert_pdf = os.path.join(out_dir, "ESTEBAN-MANUEL-LOPEZ-RIVERO-COMPLETO.pdf")
    temp_cert_pdf = os.path.join(out_dir, "temp_certs.pdf")
    
    # 1. Prepare image and HTML
    if os.path.exists(pic_path):
        crop_to_circle(pic_path, circle_pic_path)
    
    # Read HTML and inject actual image path
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # We must replace {{PROFILE_PIC}} with the actual absolute URL for the image
    img_url = "file:///" + circle_pic_path.replace("\\", "/")
    html_content = html_content.replace("{{PROFILE_PIC}}", img_url)
    
    temp_html = r"c:\Users\AYB\Desktop\HOJA-DE-VIDA-V1\cv_template_filled.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    os.makedirs(out_dir, exist_ok=True)
    
    # 2. Generate Sin Certificados PDF
    generate_html_pdf(temp_html, sin_cert_pdf)
    print(f"Generado exitosamente: {sin_cert_pdf}")
    
    # 3. Generate Certificados temp PDF
    generate_certificates_pdf(img_dir, temp_cert_pdf, profile_hash)
    
    # 4. Merge into Con Certificados PDF
    merge_pdfs(sin_cert_pdf, temp_cert_pdf, con_cert_pdf)
    print(f"Generado exitosamente: {con_cert_pdf}")
    
    # Cleanup
    if os.path.exists(temp_cert_pdf):
        os.remove(temp_cert_pdf)
    if os.path.exists(temp_html):
        os.remove(temp_html)
