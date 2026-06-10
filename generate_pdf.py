from fpdf import FPDF
import os, sys

MODE = 'complete' if '--complete' in sys.argv else 'plain'
BASE = os.path.dirname(os.path.abspath(__file__))

class PDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        font_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
        arial = os.path.join(font_dir, 'arial.ttf')
        arialb = os.path.join(font_dir, 'arialbd.ttf')
        ariali = os.path.join(font_dir, 'ariali.ttf')
        if os.path.exists(arial):
            self.add_font('ArialC', '', arial)
            self.add_font('ArialC', 'B', arialb)
            self.add_font('ArialC', 'I', ariali)
            self.F = 'ArialC'
        else:
            self.F = 'Helvetica'

    def header(self):
        if self.page_no() > 1:
            self.set_font(self.F, 'I', 7)
            self.set_text_color(150, 150, 150)
            self.cell(0, 5, 'Esteban Manuel Lopez Rivero - CV Profesional', align='C')
            self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.F, 'I', 7)
        self.set_text_color(180, 180, 180)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', align='C')

    def section_title(self, t):
        self.set_font(self.F, 'B', 13)
        self.set_text_color(25, 35, 60)
        self.cell(0, 7, t, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(56, 189, 248)
        self.set_line_width(0.5)
        y = self.get_y()
        self.line(10, y, 80, y)
        self.ln(4)

    def sub(self, title, content):
        self.set_font(self.F, 'B', 10)
        self.set_text_color(30, 41, 59)
        self.cell(0, 5.5, title, new_x="LMARGIN", new_y="NEXT")
        self.set_font(self.F, '', 9)
        self.set_text_color(80, 90, 110)
        self.multi_cell(0, 4.5, content)
        self.ln(2)

    def bullet(self, text):
        self.set_font(self.F, '', 9)
        self.set_text_color(80, 90, 110)
        self.multi_cell(0, 4.5, f'  - {text}')
        self.ln(1)


pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

# ===== HEADER WITH PHOTO =====
img_path = os.path.join(BASE, 'IMG', 'FOTO 3X4.jpg')
if os.path.exists(img_path):
    pdf.image(img_path, x=12, y=12, w=28, h=36)
    pdf.set_xy(44, 14)
else:
    pdf.set_xy(12, 14)

pdf.set_font(pdf.F, 'B', 22)
pdf.set_text_color(15, 23, 42)
pdf.cell(0, 8, 'ESTEBAN MANUEL LOPEZ RIVERO', new_x="LMARGIN", new_y="NEXT")
pdf.set_x(44)
pdf.set_font(pdf.F, '', 11)
pdf.set_text_color(56, 189, 248)
pdf.cell(0, 6, 'Tecnico en Sistemas | Full-Stack Developer | Infraestructura de Redes | Automatizacion', new_x="LMARGIN", new_y="NEXT")
pdf.set_x(44)
pdf.set_font(pdf.F, '', 8)
pdf.set_text_color(100, 110, 130)
pdf.cell(0, 4, 'CR 11 6A-10, Cerete, Cordoba | love8012e@gmail.com | 3017400553', new_x="LMARGIN", new_y="NEXT")
pdf.set_x(44)
pdf.cell(0, 4, 'linkedin.com/in/esteban-manuel-lopez-rivero-3b5887370 | github.com/studioanime977', new_x="LMARGIN", new_y="NEXT")
pdf.ln(14)

# ===== PERFIL =====
pdf.section_title('PERFIL PROFESIONAL')
pdf.set_font(pdf.F, '', 9)
pdf.set_text_color(80, 90, 110)
pdf.multi_cell(0, 4.5,
    'Profesional hibrido con solida formacion tecnica y profunda experiencia en el sector comercial. '
    'Tecnico en Sistemas (CENSA - Monteria) con formacion en Platzi, complementado por certificacion SENA en '
    'Contabilidad (calificacion 4.5). Experiencia como Asesor de Ventas en Tienda Altos del Noval (2023-2025) '
    'con funciones de caja, inventarios y operacion general. En el ambito tecnologico, administra servidores '
    'Ubuntu en VPS con protocolos Vmess/V2ray y panel VPS TunnelActive, desarrolla bots Python para trading '
    'algoritmico (API Binance) en VPS 24/7, crea plataformas web full-stack indexadas y monetizadas, y dirige '
    '13 proyectos web ademas de las marcas @STUDIOOTAKUFF, MacroViral StudioFF y MoviVIP Network. '
    'Capacidad unica para fusionar tecnologia, gestion comercial y analisis financiero.')
pdf.ln(3)

# ===== EXPERIENCIA =====
pdf.section_title('EXPERIENCIA PROFESIONAL')
pdf.sub('Desarrollador Web & Administrador de Servidores',
    'Ene 2026 - Actualidad\n'
    'Implementacion y hardening de servidores Ubuntu en VPS con protocolos Vmess/V2ray y panel VPS TunnelActive '
    'para balanceo de trafico y control de puertos HTTP/HTTPS. Desarrollo de scripts Python para trading '
    'algoritmico automatizado (API Binance) en VPS 24/7. Creacion de plataformas web full-stack indexadas y monetizadas.')
pdf.sub('Fundador - MoviVIP Network',
    'May 2026 - Actualidad\n'
    'Arquitectura e implementacion de plataforma de aprovisionamiento de servicios de internet movil VIP. '
    'Automatizacion de flujo de ventas y notificaciones mediante bots en Telegram integrados al backend.')
pdf.sub('Practicas - Cabarcas Sarmiento S.A.S',
    'Tecnico en Sistemas Informaticos | Feb - Ago 2025 (+2 meses)\n'
    'Soporte tecnico nivel 1 y 2: mantenimiento preventivo/correctivo de hardware. Diseno e instalacion de '
    'redes estructuradas empresariales. Instalacion y configuracion de sistemas CCTV (DVR/NVR) con monitoreo remoto.')
pdf.sub('Asesor de Ventas y Gestor Operativo',
    'Tienda Altos del Noval (NIT 30688395-6) | Feb 2023 - Sep 2025\n'
    'Coordinacion de apertura/cierre, conciliacion de caja, auditoria de inventarios, fidelizacion de clientes '
    'mediante atencion personalizada basada en datos de consumo.')
pdf.sub('Creador de Contenido - @STUDIOOTAKUFF',
    '2024 - Actualidad\n'
    'Estrategia de engagement y marketing digital en TikTok y YouTube. Creacion de MacroViral StudioFF '
    '(kits virales y generador de sensibilidad para Free Fire) y EMLFLOW (produccion musical con IA).')
pdf.ln(1)

if MODE == 'complete':
    # ===== SKILLS VISUAL =====
    pdf.section_title('COMPETENCIAS TECNICAS')
    skills = [
        ('Infraestructura y Redes', 'Servidores Ubuntu Linux, VPS TunnelActive, Protocolos Vmess y V2ray, enrutamiento avanzado, balanceo de puertos, seguridad perimetral, CCTV DVR/NVR con monitoreo remoto.'),
        ('Desarrollo Full-Stack', 'JavaScript (Node.js), Java (POO), Python, HTML5, CSS3, APIs REST. Plataformas indexadas y monetizadas en Vercel y Firebase.'),
        ('Datos y Seguridad', 'SQL, MySQL, Supabase (Autenticacion, RLS), CORS, Security Headers, Hardening de sistemas operativos.'),
        ('Automatizacion y Negocio', 'Integracion de APIs (Binance API), Bots de Telegram, Auditoria de inventarios, Gestion y conciliacion de caja.'),
        ('Optimizacion de Sistemas', 'Personalizacion extrema de Windows 10/11 via NTLite (reduccion de consumo RAM a 2-3GB). Hardening y eliminacion de bloatware.'),
    ]
    for cat, items in skills:
        pdf.set_fill_color(240, 244, 248)
        pdf.set_font(pdf.F, 'B', 9)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(0, 5.5, f'  {cat}', new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_font(pdf.F, '', 8.5)
        pdf.set_text_color(80, 90, 110)
        pdf.set_x(13)
        pdf.multi_cell(0, 4, f'     {items}')
        pdf.ln(1.5)

    pdf.section_title('HABILIDADES BLANDAS')
    soft = 'Pensamiento Analitico | Liderazgo Tecnico | Adaptabilidad Tecnologica | Atencion al Detalle | Comunicacion Asertiva | Resolucion de Problemas | Gestion del Tiempo | Trabajo en Equipo | Aprendizaje Continuo'
    pdf.set_font(pdf.F, '', 9)
    pdf.set_text_color(80, 90, 110)
    pdf.set_x(13)
    pdf.multi_cell(0, 4.5, f'  {soft}')
    pdf.ln(3)

    # ===== PROJECTS =====
    pdf.section_title('PORTAFOLIO DE PROYECTOS WEB (13)')
    projects = [
        ('Trading Bot Algoritmico', 'Python + Binance API en VPS 24/7. Automatizacion de analisis financiero y ejecucion de ordenes en tiempo real.'),
        ('MoviVIP Network', 'movivip-network.web.app | Plataforma de datos moviles VIP con bots Telegram para ventas y soporte.'),
        ('Inmobiliaria Integrales Cerete', 'inmobiliariaintegarlescerete.vercel.app | Indexado y monetizado en Google.'),
        ('MacroViral StudioFF', 'macroviralstudioff.web.app | Ecosistema de kits virales y calibracion DPI para Free Fire.'),
        ('Mundo Otaku Latino', 'mundootakulatino.vercel.app | Portal anime indexado y monetizado.'),
        ('Edu-Clic', 'edu-clic.vercel.app | Plataforma educativa interactiva.'),
        ('Dinamica Juvenil', 'dinamicajuvenil.vercel.app | Cuestionarios interactivos gamificados.'),
        ('Eliminador de Marcas de Agua', 'eliminador-de-marcas-de-agua.vercel.app | Herramienta IA para fotos.'),
        ('EML Studio', 'eml-studio-yquw.vercel.app | Editor de documentos con PDF.js.'),
        ('Casa de Avivamiento', 'casa-de-avivamiento-y-reino-cerete.vercel.app | Sitio web para iglesia.'),
        ('Generacion Benjamin', 'generacion-benjamin.vercel.app | Portal de grupo juvenil.'),
        ('Servicios (Plantilla)', 'servicios-psi.vercel.app | Template profesional de servicios.'),
        ('Terrenos Prueba', 'terrenosprueba.vercel.app | Gestion y visualizacion de terrenos.'),
    ]
    for name, desc in projects:
        pdf.set_font(pdf.F, 'B', 9)
        pdf.set_text_color(45, 55, 72)
        pdf.set_x(13)
        pdf.cell(0, 5, f'  {name}', new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(pdf.F, '', 8)
        pdf.set_text_color(80, 90, 110)
        pdf.set_x(18)
        pdf.multi_cell(0, 4, desc)
    pdf.ln(3)

else:
    # ===== PLAIN MODE =====
    pdf.section_title('HABILIDADES TECNICAS')
    pdf.bullet('Hardware: Armado 60+ equipos, mantenimiento avanzado, optimizacion extrema Windows con NTLite (RAM 2-3GB)')
    pdf.bullet('Redes: Servidores Ubuntu, VPS TunnelActive, Vmess/V2ray, routers, CCTV, DVR/NVR')
    pdf.bullet('Desarrollo: HTML, CSS, JS, Node.js, Java, SQL/MySQL, Python, APIs REST')
    pdf.bullet('Seguridad: Row Level Security (RLS), Supabase, CORS, Security Headers')
    pdf.bullet('Trading: Bots Python, API Binance, VPS 24/7')
    pdf.bullet('Gaming: @STUDIOOTAKUFF, MacroViral StudioFF, DPI 500-630 Infinix Hot 50 Pro+')
    pdf.bullet('MoviVIP: Datos moviles VIP, aprovisionamiento, soporte, bots Telegram')
    pdf.bullet('Audio: Consolas de sonido, ecualizacion para eventos comunitarios')
    pdf.bullet('Comercial: Atencion al cliente, inventarios, caja, ventas, contabilidad basica SENA')
    pdf.ln(1)

    pdf.section_title('PROYECTOS WEB DESTACADOS')
    for name, url in [
        ('Trading Bot Algoritmico (Python + Binance API)', 'VPS 24/7 - Automatizacion financiera'),
        ('MoviVIP Network (Marca Propia)', 'movivip-network.web.app'),
        ('Inmobiliaria Integrales Cerete (indexado/monetizado)', 'inmobiliariaintegarlescerete.vercel.app'),
        ('MacroViral StudioFF (Marca Propia)', 'macroviralstudioff.web.app'),
        ('Mundo Otaku Latino (indexado/monetizado)', 'mundootakulatino.vercel.app'),
        ('Edu-Clic', 'edu-clic.vercel.app'),
        ('Dinamica Juvenil', 'dinamicajuvenil.vercel.app'),
        ('Eliminador de Marcas de Agua', 'eliminador-de-marcas-de-agua.vercel.app'),
        ('EML Studio', 'eml-studio-yquw.vercel.app'),
        ('Casa de Avivamiento', 'casa-de-avivamiento-y-reino-cerete.vercel.app'),
        ('Generacion Benjamin', 'generacion-benjamin.vercel.app'),
        ('Servicios (Plantilla)', 'servicios-psi.vercel.app'),
        ('Terrenos Prueba', 'terrenosprueba.vercel.app'),
    ]:
        pdf.set_font(pdf.F, '', 9)
        pdf.set_text_color(45, 55, 72)
        pdf.cell(0, 5, f'  - {name}', new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(pdf.F, 'I', 8)
        pdf.set_text_color(56, 189, 248)
        pdf.cell(0, 4, f'    {url}', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

# ===== FORMACION =====
pdf.section_title('FORMACION ACADEMICA')
pdf.sub('Tecnico en Sistemas Informaticos', 'CENSA - Monteria, Colombia | 2024 - Sep 2025')
pdf.sub('Bachiller Academico', 'I.E. Dolores Garrido de Gonzales | Graduado 2023')

pdf.section_title('FORMACION COMPLEMENTARIA')
pdf.sub('Java Programming (POO y Arquitectura)', 'Platzi - Feb 2026')
pdf.sub('Node.js Backend Development y REST APIs', 'Platzi - Feb 2026')
pdf.sub('Administracion de Bases de Datos SQL y MySQL', 'Platzi - Feb 2026')
pdf.sub('Document Object Model (DOM) Avanzado', 'Platzi - Feb 2026')
pdf.sub('Calidad de Desarrollador de Software', 'SENA - 2023')
pdf.sub('Desarrollo de Aplicaciones Moviles', 'SENA - 2024')
pdf.sub('Telematica y Redes de Datos', '2024')
pdf.sub('Contabilidad: Reconocimiento de Recursos Financieros', 'SENA - Dic 2022 | Calificacion 4.5/5.0')
pdf.ln(1)

# ===== REFERENCIAS =====
pdf.section_title('REFERENCIAS')
pdf.set_font(pdf.F, '', 9)
pdf.set_text_color(80, 90, 110)
pdf.multi_cell(0, 4.5,
    'Referencias personales y laborales disponibles bajo solicitud.\n'
    'Contacto: love8012e@gmail.com | Celular/WhatsApp: 3017400553')
pdf.ln(3)

# ===== CERTIFICATES (complete mode only) =====
if MODE == 'complete':
    pdf.add_page()
    pdf.section_title('ANEXO DE CERTIFICACIONES')
    pdf.set_font(pdf.F, '', 8.5)
    pdf.set_text_color(80, 90, 110)
    pdf.multi_cell(0, 4.5, '  A continuacion se presentan los certificados que respaldan la formacion academica, la experiencia laboral y las competencias tecnicas declaradas en este documento. Cada certificado ocupa una pagina completa para su correcta visualizacion.')
    pdf.ln(2)

    certs = [
        ('CERTIFICADO ESTEBAN LOPEZ.jpg', 'Certificado de Practicas - Cabarcas Sarmiento S.A.S (2025)'),
        ('diploma_censa.jpg', 'Diploma - Tecnico en Sistemas Informaticos CENSA (2025)'),
        ('acta_censa.jpg', 'Acta de Grado - CENSA (2025)'),
        ('Certificado-cabarcas.jpg', 'Certificado Laboral - Cabarcas Sarmiento (2025)'),
        ('certificado_tienda.jpg', 'Certificado Laboral - Tienda Altos del Noval (2023-2025)'),
        ('calidad de desarrollador de software.jpg', 'Calidad de Desarrollador de Software - SENA (2023)'),
        ('cartificado calidad desarrollador de software.jpg', 'Certificado Calidad de Software - SENA (2023)'),
        ('aplicaciones moviles.jpg', 'Desarrollo de Aplicaciones Moviles - SENA (2024)'),
        ('telematica_y_redes.jpg', 'Telematica y Redes de Datos (2024)'),
        ('CERTIFICADO CONTABILIDAD RECONOCIMIENTO DE RECURSOS FINANCIEROS.jpg', 'Contabilidad: Reconocimiento de Recursos Financieros - SENA (Dic 2022)'),
        ('ACTA CONTABILIDAD RECONOCIMIENTO DE RECURSOS FINANCIEROS.jpg', 'Acta de Notas - Contabilidad SENA (Calif. 4.5)'),
        ('diploma-java_page-0001.jpg', 'Java Programming (POO) - Platzi (Feb 2026)'),
        ('diploma-nodejs_page-0001.jpg', 'Node.js Development - Platzi (Feb 2026)'),
        ('diploma-sql-mysql_page-0001.jpg', 'SQL y MySQL - Platzi (Feb 2026)'),
        ('diploma-document-object-model_page-0001.jpg', 'Document Object Model (DOM) - Platzi (Feb 2026)'),
        ('medio ambiente.jpg', 'Formacion en Medio Ambiente'),
        ('etica y valores.jpg', 'Formacion en Etica y Valores'),
        ('diploma.jpg', 'Diploma Complementario'),
        ('acta de grado.jpg', 'Acta de Grado Complementaria'),
        ('Certificado4.jpg', 'Certificado Adicional'),
    ]

    for fname, label in certs:
        pdf.add_page()
        cert_path = os.path.join(BASE, 'IMG', fname)
        if os.path.exists(cert_path):
            pdf.set_font(pdf.F, 'B', 11)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 7, label, new_x="LMARGIN", new_y="NEXT", align='C')
            pdf.ln(3)
            pdf.image(cert_path, x=25, y=pdf.get_y(), w=160)

pdf.set_font(pdf.F, 'I', 8)
pdf.set_text_color(150, 150, 150)
ver = 'COMPLETA CON CERTIFICADOS' if MODE == 'complete' else 'PLANA (TEXTO)'
pdf.cell(0, 4, f'CV 2026 - Version {ver} | Generado desde hoja-de-vida-v1.vercel.app', new_x="LMARGIN", new_y="NEXT", align='C')

out_dir = os.path.join(BASE, 'H')
os.makedirs(out_dir, exist_ok=True)
fname = 'ESTEBAN-MANUEL-LOPEZ-RIVERO-COMPLETO.pdf' if MODE == 'complete' else 'ESTEBAN-MANUEL-LOPEZ-RIVERO.pdf'
out_path = os.path.join(out_dir, fname)
pdf.output(out_path)
print(f'PDF: {out_path}')
print(f'Size: {os.path.getsize(out_path)} bytes')
