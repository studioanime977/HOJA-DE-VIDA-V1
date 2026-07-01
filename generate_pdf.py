import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, text=f"Página {self.page_no()}", align="C")

def create_resume(output_path, include_certificates=False):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title / Name
    pdf.set_font("helvetica", "B", 18)
    pdf.cell(0, 10, text="ESTEBAN MANUEL LÓPEZ RIVERO", new_x="LMARGIN", new_y="NEXT", align="C")
    
    # Subtitle
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 6, text="Técnico en Sistemas | Full-Stack Developer | Infraestructura | Automatización", new_x="LMARGIN", new_y="NEXT", align="C")
    
    # Contact Info
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 5, text="Email: love8012e@gmail.com | Tel: +57 3017400553 | WhatsApp: +57 3117008185", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 5, text="Cereté, Córdoba, Colombia | LinkedIn: linkedin.com/in/esteban-manuel-lópez-rivero-3b5887370", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 5, text="Portfolio: hoja-de-vida-v1.vercel.app | GitHub: github.com/studioanime977", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)
    
    # Resumen Profesional
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, text="PERFIL PROFESIONAL", new_x="LMARGIN", new_y="NEXT", align="L", border="B")
    pdf.ln(2)
    pdf.set_font("helvetica", "", 10)
    resumen = (
        "Técnico en Sistemas Informáticos y Desarrollador Full-Stack con visión integral de negocio. "
        "Enfoque en diseñar, optimizar y automatizar infraestructuras tecnológicas robustas. "
        "Fusión de habilidades técnicas avanzadas (redes, servidores, desarrollo web, cloud computing, IA, "
        "automatización) con sólida base en gestión financiera y operativa (certificación SENA en Contabilidad 4.5/5.0). "
        "Más de 30 certificaciones técnicas en Platzi, SENA y CENSA."
    )
    pdf.multi_cell(0, 5, text=resumen, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Experiencia
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, text="EXPERIENCIA PROFESIONAL", new_x="LMARGIN", new_y="NEXT", align="L", border="B")
    pdf.ln(2)
    
    experiences = [
        {
            "title": "Desarrollador Web & Adm. de Servidores | Freelance",
            "date": "Ene 2026 - Actualidad",
            "bullets": [
                "Configuración y hardening de servidores Ubuntu en VPS con protocolos Vmess/V2ray.",
                "Panel VPS TunnelActive, balanceo de puertos HTTP/HTTPS y monitoreo 24/7.",
                "Desarrollo de bots Python para trading algorítmico integrado con API Binance.",
                "Despliegue de soluciones serverless (GCP, AWS, Firebase) y plataformas full-stack."
            ]
        },
        {
            "title": "Fundador | MoviVIP Network",
            "date": "May 2026 - Actualidad",
            "bullets": [
                "Plataforma de aprovisionamiento de datos móviles VIP.",
                "Automatización de ventas mediante bots en Telegram.",
                "Soporte técnico especializado y gestión de red."
            ]
        },
        {
            "title": "Prácticas Técnico en Sistemas | Cabarcas Sarmiento S.A.S",
            "date": "Feb 2025 - Ago 2025",
            "bullets": [
                "Soporte técnico nivel 1 y 2, mantenimiento preventivo/correctivo.",
                "Redes estructuradas empresariales y sistemas CCTV con monitoreo remoto."
            ]
        },
        {
            "title": "Asesor de Ventas y Gestor Operativo | Tienda Altos del Noval",
            "date": "Feb 2023 - Sep 2025",
            "bullets": [
                "Coordinación de apertura/cierre, conciliación de caja y auditoría de inventarios.",
                "Fidelización de clientes con atención personalizada."
            ]
        }
    ]
    
    for exp in experiences:
        pdf.set_font("helvetica", "B", 10)
        # title
        pdf.cell(130, 6, text=exp["title"], new_x="RIGHT", new_y="TOP")
        pdf.set_font("helvetica", "I", 10)
        # date
        pdf.cell(0, 6, text=exp["date"], align="R", new_x="LMARGIN", new_y="NEXT")
        
        # We must make sure X is at LMARGIN for multi_cell
        pdf.set_x(pdf.l_margin)
        pdf.set_font("helvetica", "", 10)
        for bullet in exp["bullets"]:
            pdf.multi_cell(0, 5, text="- " + bullet, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        
    # Habilidades
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, text="HABILIDADES TÉCNICAS", new_x="LMARGIN", new_y="NEXT", align="L", border="B")
    pdf.ln(2)
    
    skills = [
        ("Desarrollo Web & Cloud", "HTML5, CSS3, JS, Node.js, Python, Java, SQL, Firebase, GCP, AWS, Serverless"),
        ("Redes & Servidores", "Ubuntu Server, Vmess/V2ray, VPN, Balanceo de puertos, Enrutamiento, CCTV"),
        ("Sistemas & Seguridad", "Armado/Mantenimiento PC, Hardening (Win/Linux), RLS, CORS, JWT"),
        ("Automatización & IA", "Trading Bots (Binance), n8n, ChatGPT, Bots Telegram, Generación Audio IA")
    ]
    
    for category, skill_list in skills:
        pdf.set_font("helvetica", "B", 10)
        # Category on its own line to simplify
        pdf.cell(0, 5, text=category + ":", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(0, 5, text=skill_list, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
    
    # Educacion
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 8, text="FORMACIÓN ACADÉMICA", new_x="LMARGIN", new_y="NEXT", align="L", border="B")
    pdf.ln(2)
    
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 5, text="Técnico en Sistemas Informáticos", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 5, text="CENSA - Montería | 2024 - 2025", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    
    pdf.set_font("helvetica", "B", 10)
    pdf.cell(0, 5, text="Bachiller Académico", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("helvetica", "", 10)
    pdf.cell(0, 5, text="I.E. Dolores Garrido de Gonzáles | Graduado en 2023", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    if include_certificates:
        pdf.add_page()
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 8, text="CERTIFICACIONES RELEVANTES", new_x="LMARGIN", new_y="NEXT", align="L", border="B")
        pdf.ln(2)
        
        certs = [
            "Contabilidad: Reconocimiento de Recursos Financieros - SENA (2022) | Calificación 4.5",
            "Calidad de Desarrollador de Software - SENA (2023)",
            "Aplicaciones Móviles - SENA (2024)",
            "Telemática y Redes de Datos - SENA (2024)",
            "Backend con Node.js, Autenticación y JWT - Platzi (2026)",
            "Python Avanzado para Arquitectura de Proyectos - Platzi (2026)",
            "Firebase para Web y Google Serverless - Platzi (2026)",
            "Automatizaciones Low-Code con n8n - Platzi (2026)",
            "Cloud Computing con AWS - Platzi (2026)",
            "Java Programming, SQL y MySQL - Platzi (2026)"
        ]
        pdf.set_font("helvetica", "", 10)
        for cert in certs:
            pdf.multi_cell(0, 5, text="- " + cert, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)
    print(f"Generado: {output_path}")

if __name__ == "__main__":
    out_dir = r"c:\Users\AYB\Desktop\HOJA-DE-VIDA-V1\public\assets\downloads"
    create_resume(os.path.join(out_dir, "Hoja_de_Vida_Sin_Certificados.pdf"), include_certificates=False)
    create_resume(os.path.join(out_dir, "Hoja_de_Vida_Con_Certificados.pdf"), include_certificates=True)
