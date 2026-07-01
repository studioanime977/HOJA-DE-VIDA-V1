import os
from fpdf import FPDF
from PIL import Image, ImageDraw

# Colors
LEFT_BG = (210, 224, 251)      # #D2E0FB
HEADER_BG = (146, 180, 242)    # #92B4F2
TEXT_DARK = (44, 62, 80)       # Dark slate
TEXT_WHITE = (255, 255, 255)

class ResumePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=False)
        
    def add_modern_page(self):
        self.add_page()
        # Draw left column background
        self.set_fill_color(*LEFT_BG)
        self.rect(0, 0, 75, 297, 'F')
        
        # Draw right top background
        self.set_fill_color(*HEADER_BG)
        self.rect(75, 0, 135, 55, 'F')
        
    def left_section_header(self, y, title):
        self.set_fill_color(*HEADER_BG)
        self.rect(0, y, 75, 10, 'F')
        self.set_xy(10, y + 2)
        self.set_font("helvetica", "B", 12)
        self.set_text_color(*TEXT_DARK)
        self.cell(0, 6, title, border=0)

def crop_to_circle(image_path, output_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        
        # Make square
        min_dim = min(img.size)
        left = (img.size[0] - min_dim) / 2
        top = (img.size[1] - min_dim) / 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        
        # Create mask
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, min_dim, min_dim), fill=255)
        
        img.putalpha(mask)
        img.save(output_path, "PNG")
        return True
    except Exception as e:
        print("Error al recortar la foto circular:", e)
        return False

def create_modern_resume(output_path, include_certificates=False, images_dir="", profile_pic_hash="af05a4d09e806b9ed91636c90bcf70d1.jpg"):
    pdf = ResumePDF()
    pdf.add_modern_page()
    
    # --- LEFT COLUMN ---
    # Profile Picture
    pic_path = os.path.join(images_dir, profile_pic_hash)
    circle_pic_path = os.path.join(images_dir, "profile_circle.png")
    
    if os.path.exists(pic_path):
        if crop_to_circle(pic_path, circle_pic_path):
            pdf.image(circle_pic_path, x=12.5, y=10, w=50, h=50)
        else:
            pdf.image(pic_path, x=12.5, y=10, w=50, h=50)
    else:
        pdf.set_fill_color(255, 255, 255)
        pdf.ellipse(12.5, 10, 50, 50, 'F')
        pdf.set_xy(12.5, 30)
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(50, 10, "[FOTO]", align="C")
    
    # Name
    pdf.set_xy(5, 70)
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(*TEXT_DARK)
    pdf.multi_cell(65, 8, "ESTEBAN MANUEL LÓPEZ RIVERO", align="L")
    
    # Profession
    pdf.set_xy(5, 95)
    pdf.set_font("helvetica", "", 11)
    pdf.multi_cell(65, 5, "TÉCNICO EN SISTEMAS\nFULL-STACK DEVELOPER", align="L")
    
    # CONTACTO
    pdf.left_section_header(115, "CONTACTO")
    pdf.set_xy(10, 130)
    pdf.set_font("helvetica", "", 10)
    contacts = [
        "love8012e@gmail.com",
        "(+57) 3017400553",
        "hoja-de-vida-v1.vercel.app",
        "Cereté, Córdoba, Colombia"
    ]
    y_contact = 130
    for c in contacts:
        pdf.set_xy(10, y_contact)
        pdf.multi_cell(60, 5, c)
        y_contact += 10
        
    # HABILIDADES
    pdf.left_section_header(175, "HABILIDADES")
    pdf.set_xy(10, 190)
    skills = [
        "Desarrollo Web (Full-Stack)",
        "Servidores y Redes (Ubuntu)",
        "Hardening & Seguridad",
        "Automatización (Python/Bots)",
        "Trading Algorítmico",
        "Mantenimiento PC (Hardware)"
    ]
    y_skill = 190
    pdf.set_font("helvetica", "", 10)
    for s in skills:
        pdf.set_xy(10, y_skill)
        pdf.multi_cell(60, 5, "- " + s)
        y_skill += 10
        
    # IDIOMAS
    pdf.left_section_header(255, "IDIOMAS")
    pdf.set_xy(10, 270)
    pdf.cell(30, 5, "Español")
    pdf.cell(30, 5, "Nativo")
    pdf.set_xy(10, 278)
    pdf.cell(30, 5, "Inglés")
    pdf.cell(30, 5, "Técnico")

    # --- RIGHT COLUMN ---
    # PERFIL PROFESIONAL
    pdf.set_xy(80, 10)
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(*TEXT_DARK)
    pdf.cell(0, 8, "PERFIL PROFESIONAL")
    
    pdf.set_xy(80, 20)
    pdf.set_font("helvetica", "", 10)
    resumen = (
        "Técnico en Sistemas Informáticos y Desarrollador Full-Stack con visión integral de negocio. "
        "Enfoque en diseñar, optimizar y automatizar infraestructuras tecnológicas robustas. "
        "Fusión de habilidades técnicas avanzadas (redes, servidores, desarrollo web, cloud computing, IA, "
        "automatización) con sólida base en gestión financiera y operativa (certificación SENA en Contabilidad 4.5/5.0). "
        "Más de 30 certificaciones técnicas en Platzi, SENA y CENSA."
    )
    pdf.multi_cell(120, 5, resumen)
    
    # EXPERIENCIA LABORAL
    pdf.set_xy(80, 65)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "EXPERIENCIA LABORAL")
    
    experiences = [
        {
            "date": "2026 - Actual",
            "title": "Desarrollador Web & Adm. Servidores",
            "company": "Freelance",
            "bullets": [
                "Configuración y hardening de servidores Ubuntu en VPS (Vmess/V2ray).",
                "Desarrollo de bots Python para trading algorítmico integrado con API Binance.",
                "Despliegue de plataformas full-stack serverless en GCP, AWS y Firebase."
            ]
        },
        {
            "date": "2026 - Actual",
            "title": "Fundador",
            "company": "MoviVIP Network",
            "bullets": [
                "Plataforma de aprovisionamiento de datos móviles VIP."
            ]
        },
        {
            "date": "2025 - 2025",
            "title": "Técnico en Sistemas (Prácticas)",
            "company": "Cabarcas Sarmiento S.A.S",
            "bullets": [
                "Soporte técnico y mantenimiento preventivo/correctivo.",
                "Sistemas CCTV (DVR/NVR) con monitoreo remoto."
            ]
        },
        {
            "date": "2023 - 2025",
            "title": "Asesor de Ventas y Gestor Operativo",
            "company": "Tienda Altos del Noval",
            "bullets": [
                "Apertura/cierre, conciliación de caja y auditoría de inventarios."
            ]
        }
    ]
    
    y_exp = 75
    for exp in experiences:
        pdf.set_xy(80, y_exp)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(25, 5, exp["date"])
        
        pdf.set_xy(105, y_exp)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(100, 5, exp["title"])
        
        y_exp += 5
        pdf.set_xy(105, y_exp)
        pdf.set_font("helvetica", "I", 10)
        pdf.cell(100, 5, exp["company"])
        
        y_exp += 6
        pdf.set_font("helvetica", "", 10)
        for bullet in exp["bullets"]:
            pdf.set_xy(105, y_exp)
            pdf.multi_cell(95, 5, "- " + bullet)
            y_exp = pdf.get_y()
        y_exp += 3

    # PROYECTOS WEB RELEVANTES
    pdf.set_xy(80, y_exp)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "PROYECTOS WEB")
    y_proj = y_exp + 10
    
    projects = [
        {"name": "Trading Bot Algorítmico", "desc": "Bot en Python con API Binance y VPS 24/7."},
        {"name": "MoviVIP Network", "desc": "Sitio: movivip-network.web.app - Servicios VIP."},
        {"name": "Inmobiliaria Integrales", "desc": "Indexado/monetizado. Gestión inmobiliaria."},
        {"name": "MacroViral StudioFF", "desc": "Kits y scripts. macroviralstudioff.web.app."}
    ]
    for proj in projects:
        pdf.set_xy(80, y_proj)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(45, 5, proj["name"])
        pdf.set_xy(125, y_proj)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(80, 5, proj["desc"])
        y_proj = pdf.get_y()

    # ESTUDIOS SUPERIORES
    pdf.set_xy(80, y_proj + 3)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, "ESTUDIOS SUPERIORES")
    y_edu = y_proj + 13
    
    education = [
        {"date": "2024 - 2025", "title": "Técnico en Sistemas Informáticos", "inst": "CENSA - Montería"},
        {"date": "2023", "title": "Bachiller Académico", "inst": "I.E. Dolores Garrido de Gonzáles"},
        {"date": "2022 - 2026", "title": "Múltiples Certificaciones TI y Desarrollo", "inst": "SENA y Platzi"}
    ]
    
    for edu in education:
        pdf.set_xy(80, y_edu)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(25, 5, edu["date"])
        
        pdf.set_xy(105, y_edu)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(100, 5, edu["title"])
        
        y_edu += 5
        pdf.set_xy(105, y_edu)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(100, 5, edu["inst"])
        y_edu += 8

    if include_certificates and os.path.exists(images_dir):
        # Find all images in the directory
        valid_exts = [".jpg", ".jpeg", ".png"]
        images = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in valid_exts]
        
        for img_name in images:
            # Exclude profile picture and temp circle pic
            if img_name == profile_pic_hash or img_name == "profile_circle.png":
                continue
                
            img_path = os.path.join(images_dir, img_name)
            
            pdf.add_page()
            pdf.set_fill_color(*HEADER_BG)
            pdf.rect(0, 0, 210, 20, 'F')
            pdf.set_xy(10, 5)
            pdf.set_font("helvetica", "B", 16)
            pdf.set_text_color(*TEXT_DARK)
            pdf.cell(0, 10, "ANEXO: CERTIFICADO", align="C")
            
            # Use PIL to get dimensions to prevent overflow or stretching
            try:
                img_obj = Image.open(img_path)
                w_px, h_px = img_obj.size
                
                # A4 is 210 x 297 mm
                # We have width up to 190mm, height up to 260mm
                max_w = 190
                max_h = 260
                
                aspect = w_px / h_px
                
                if aspect > (max_w / max_h):
                    # Width bounded
                    calc_w = max_w
                    calc_h = max_w / aspect
                else:
                    # Height bounded
                    calc_h = max_h
                    calc_w = max_h * aspect
                    
                x_pos = (210 - calc_w) / 2
                y_pos = 30 + (260 - calc_h) / 2
                
                pdf.image(img_path, x=x_pos, y=y_pos, w=calc_w, h=calc_h)
            except Exception as e:
                pdf.set_xy(10, 50)
                pdf.multi_cell(0, 10, f"Error cargando imagen: {e}")
                
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"Generado exitosamente: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\AYB\Desktop\HOJA-DE-VIDA-V1\public\assets\downloads"
    img_dir = r"c:\Users\AYB\Desktop\HOJA-DE-VIDA-V1\public\assets\images"
    create_modern_resume(os.path.join(out_dir, "Hoja_de_Vida_Sin_Certificados.pdf"), include_certificates=False, images_dir=img_dir)
    create_modern_resume(os.path.join(out_dir, "Hoja_de_Vida_Con_Certificados.pdf"), include_certificates=True, images_dir=img_dir)
