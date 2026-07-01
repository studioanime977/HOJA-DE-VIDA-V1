from fpdf import FPDF
import os, sys, json

MODE = 'complete' if '--complete' in sys.argv else 'plain'
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE, 'src', 'data', 'cv.json'), 'r', encoding='utf-8') as f:
    CV = json.load(f)

IMG_DIR = os.path.join(BASE, 'public', 'assets', 'images')

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

    def footer(self):
        self.set_y(-10)
        self.set_font(self.F, 'I', 7)
        self.set_text_color(150,150,150)
        self.cell(0, 6, f'Pag {self.page_no()}', align='C')


pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

P = CV['personal']

# ── HEADER ──
pdf.set_font(pdf.F, 'B', 16)
pdf.cell(0, 7, P['name'].upper())
pdf.ln(6)
pdf.set_font(pdf.F, '', 9)
pdf.set_text_color(80,80,80)
pdf.cell(0, 4.5, P['title'])
pdf.ln(6)

# Contact info
pdf.set_font(pdf.F, '', 8)
pdf.cell(0, 4, f"Email: {P['email']}  |  Tel: {P['phone']}  |  WhatsApp: 3117008185")
pdf.ln(3.5)
pdf.cell(0, 4, f"Ubicacion: {P['location']}")
pdf.ln(3.5)
pdf.cell(0, 4, f"LinkedIn: linkedin.com/in/esteban-manuel-lopez-rivero-3b5887370")
pdf.ln(3.5)
pdf.cell(0, 4, f"GitHub: github.com/studioanime977")
pdf.ln(3.5)
pdf.cell(0, 4, f"YouTube: @STUDIOOTAKUFF / @EMLFLOW / @STUDIOOTAKU1")
pdf.ln(3.5)
pdf.cell(0, 4, f"TikTok: @studiootakuff")
pdf.ln(6)

# ── PERFIL ──
def sec(t):
    pdf.set_font(pdf.F, 'B', 11)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 6, t.upper())
    pdf.set_draw_color(0,0,0)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

sec('Perfil Profesional')
pdf.set_font(pdf.F, '', 8.5)
pdf.set_text_color(60,60,60)
pdf.multi_cell(0, 4.2, CV['profile'])
pdf.ln(3)

# ── EXPERIENCIA ──
sec('Experiencia Profesional')
for e in CV['experience']:
    pdf.set_font(pdf.F, 'B', 9)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 4.5, e['role'])
    pdf.set_font(pdf.F, '', 7.5)
    pdf.set_text_color(100,100,100)
    pdf.cell(0, 3.5, f"{e['company']} | {e['period']}", new_x="LMARGIN", new_y="NEXT")
    for h in e['highlights']:
        pdf.set_font(pdf.F, '', 8)
        pdf.set_text_color(60,60,60)
        pdf.set_x(13)
        pdf.multi_cell(0, 3.8, f"- {h}")
    pdf.ln(2)

# ── HABILIDADES ──
sec('Habilidades Tecnicas')
for cat in CV['skills']['categories']:
    pdf.set_font(pdf.F, 'B', 8)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 4, cat['title'])
    pdf.ln(3.5)
    pdf.set_font(pdf.F, '', 7.5)
    pdf.set_text_color(60,60,60)
    pdf.set_x(13)
    pdf.multi_cell(0, 3.5, ', '.join(cat['tags']))
    pdf.ln(1.5)

pdf.ln(2)

# ── HABILIDADES BLANDAS ──
pdf.set_font(pdf.F, 'B', 8)
pdf.set_text_color(0,0,0)
pdf.cell(0, 4, 'Habilidades Blandas')
pdf.ln(4)
pdf.set_font(pdf.F, '', 7.5)
pdf.set_text_color(60,60,60)
pdf.set_x(13)
pdf.multi_cell(0, 3.5, ' | '.join(CV['skills']['soft']))
pdf.ln(3)

# ── FORMACION ACADEMICA ──
sec('Formacion Academica')
for ac in CV['education']['academic']:
    pdf.set_font(pdf.F, 'B', 8.5)
    pdf.set_text_color(0,0,0)
    pdf.cell(0, 4, ac['title'])
    pdf.set_font(pdf.F, '', 7.5)
    pdf.set_text_color(80,80,80)
    pdf.cell(0, 3.5, f"{ac['institution']} | {ac['period']}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(13)
    pdf.set_font(pdf.F, '', 7.5)
    pdf.set_text_color(60,60,60)
    pdf.multi_cell(0, 3.5, ac['desc'])
    pdf.ln(1.5)

# ── CURSOS ──
new_c = [c for c in CV['education']['courses'] if c.get('new')]
sec(f'Cursos Platzi ({len(CV["education"]["courses"])} total, {len(new_c)} nuevos Jun 2026)')
pdf.set_font(pdf.F, '', 7.5)
pdf.set_text_color(60,60,60)
for c in CV['education']['courses']:
    hours = f" ({c['hours']}h)" if c.get('hours') else ''
    label = ' NUEVO' if c.get('new') else ''
    pdf.set_x(13)
    pdf.multi_cell(0, 3.5, f"- {c['title']}{label} - {c['institution']} ({c['date']}){hours}")
pdf.ln(2)

# ── SENA ──
sec('Formacion SENA')
pdf.set_font(pdf.F, '', 7.5)
pdf.set_text_color(60,60,60)
for s in CV['education']['sena']:
    extra = f" - {s['note']}" if s.get('note') else ''
    pdf.set_x(13)
    pdf.multi_cell(0, 3.5, f"- {s['title']} - {s.get('institution','')} ({s['date']}){extra}")

# ── PROYECTOS ──
sec(f'Proyectos Web ({len(CV["projects"])})')
pdf.set_font(pdf.F, '', 7.5)
pdf.set_text_color(60,60,60)
for p in CV['projects']:
    pdf.set_x(13)
    pdf.multi_cell(0, 3.5, f"- {p['name']}: {p['desc']}")
pdf.ln(2)

# ── ESTADISTICAS ──
sec('Estadisticas')
pdf.set_font(pdf.F, '', 8)
pdf.set_text_color(60,60,60)
for s in CV['stats']:
    pdf.set_x(13)
    pdf.multi_cell(0, 3.8, f"- {s['label']}: {s['value']}")

# ── CERTIFICADOS (complete mode) ──
if MODE == 'complete':
    for cert in CV.get('certificates', []):
        if cert.get('hidden'):
            continue
        pdf.add_page()
        cert_path = os.path.join(IMG_DIR, cert['file'])
        pdf.set_font(pdf.F, 'B', 10)
        pdf.set_text_color(0,0,0)
        pdf.cell(0, 5, cert['title'], new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.set_font(pdf.F, '', 7.5)
        pdf.set_text_color(80,80,80)
        pdf.cell(0, 4, cert['subtitle'], new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(2)
        if os.path.exists(cert_path):
            pdf.image(cert_path, x=15, y=pdf.get_y(), w=180)

# Output
out_dir = os.path.join(BASE, 'public', 'assets', 'downloads')
os.makedirs(out_dir, exist_ok=True)
fname = 'ESTEBAN-MANUEL-LOPEZ-RIVERO-COMPLETO.pdf' if MODE == 'complete' else 'ESTEBAN-MANUEL-LOPEZ-RIVERO.pdf'
out_path = os.path.join(out_dir, fname)
pdf.output(out_path)
print(f'PDF: {out_path}')
print(f'Size: {os.path.getsize(out_path)} bytes')
