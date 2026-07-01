const API = '/api/cv';
let cvData = null;

async function fetchData() {
  try {
    const res = await fetch(API);
    if (!res.ok) throw new Error('API unavailable');
    return await res.json();
  } catch {
    return await loadFallbackData();
  }
}

async function loadFallbackData() {
  try {
    const res = await fetch('/assets/data/cv.json');
    return await res.json();
  } catch {
    const res = await fetch('/api/cv');
    return await res.json();
  }
}

function buildNav(data) {
  const links = [
    { label: 'Inicio', href: '#hero' },
    { label: 'Perfil', href: '#about' },
    { label: 'Experiencia', href: '#experience' },
    { label: 'Proyectos', href: '#projects' },
    { label: 'Habilidades', href: '#skills' },
    { label: 'Cursos', href: '#courses' },
    { label: 'Certificaciones', href: '#certificates' },
    { label: 'Formación', href: '#education' },
    { label: 'CV', href: '#', action: 'download' }
  ];
  const ul = document.getElementById('navLinks');
  ul.innerHTML = links.map(l => {
    const click = l.action === 'download'
      ? `onclick="downloadCV();return false"`
      : `onclick="closeNav();scrollToSection('${l.href}')"`;
    return `<li><a href="${l.href}" ${click}>${l.label}</a></li>`;
  }).join('');
}

function scrollToSection(href) {
  const id = href.replace('#', '');
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

function closeNav() {
  document.getElementById('navLinks').classList.remove('open');
}

function buildHero(data) {
  const p = data.personal;
  return `
  <section id="hero" class="hero section-animate">
    <div class="hero-content">
      <img src="${p.photo}" alt="${p.name}" class="hero-img" loading="lazy">
      <h1 class="hero-title">${p.name}</h1>
      <p class="hero-subtitle">${p.title}</p>
      <div class="hero-meta">
        <span>📍 ${p.location}</span>
        <span>📧 ${p.email}</span>
        <span>📱 ${p.phone}</span>
      </div>
      <div class="hero-contact">
        <a href="${p.social.whatsapp}" target="_blank" class="hero-btn whatsapp">WhatsApp</a>
        <a href="${p.social.linkedin}" target="_blank" class="hero-btn linkedin">LinkedIn</a>
        <a href="${p.social.github}" target="_blank" class="hero-btn github">GitHub</a>
        <a href="#" onclick="downloadCV();return false" class="hero-btn cv">📄 Descargar CV</a>
      </div>
      <div class="hero-contact" style="margin-top:6px">
        <a href="${p.social.youtube_gaming}" target="_blank" class="hero-btn" style="background:#ff0033">🎮 Gaming</a>
        <a href="${p.social.tiktok}" target="_blank" class="hero-btn" style="background:#000">🎵 TikTok</a>
        <a href="${p.social.youtube_music}" target="_blank" class="hero-btn" style="background:#1db954">🎤 IA Music</a>
        <a href="${p.social.youtube_anime}" target="_blank" class="hero-btn" style="background:#6441a5">📺 Anime</a>
      </div>
    </div>
  </section>`;
}

function buildAbout(data) {
  const stats = data.stats.map(s =>
    `<div class="stat-item glass">
      <div class="stat-icon">${s.icon}</div>
      <span class="stat-num">${s.value}</span>
      <span class="stat-label">${s.label}</span>
    </div>`
  ).join('');
  return `
  <section id="about" class="section section-animate">
    <div class="container">
      <h2 class="section-title">Perfil Profesional</h2>
      <div class="about-grid">
        <div class="about-card glass">${data.profile.split('\n').map(p => `<p>${p}</p>`).join('')}</div>
        <div class="stats-grid">${stats}</div>
      </div>
    </div>
  </section>`;
}

function buildExperience(data) {
  const items = data.experience.map(exp => `
    <div class="timeline-item glass" style="--accent-color:${exp.accent}">
      <div class="tl-marker" style="background:${exp.accent};box-shadow:0 0 0 2px ${exp.accent}"></div>
      <div class="tl-content">
        <h3>${exp.role}</h3>
        <div class="tl-company">${exp.company}</div>
        <div class="tl-date">${exp.period}</div>
        <ul class="tl-highlights">${exp.highlights.map(h => `<li>${h}</li>`).join('')}</ul>
      </div>
    </div>
  `).join('');
  return `
  <section id="experience" class="section alt section-animate">
    <div class="container">
      <h2 class="section-title">Experiencia Profesional</h2>
      <div class="timeline">${items}</div>
    </div>
  </section>`;
}

function buildProjects(data) {
  const slides = data.projects.map((p, i) => `
    <div class="swiper-slide">
      <div class="carousel-card glass" style="border-top:4px solid ${p.color}">
        ${p.badge ? `<span class="carousel-badge">${p.badge}</span>` : ''}
        <h3>${p.name}</h3>
        <p>${p.desc}</p>
        <div class="carousel-links">
          ${p.links.web ? `<a href="${p.links.web}" target="_blank">🌐 Ver Sitio</a>` : ''}
          ${p.links.github ? `<a href="${p.links.github}" target="_blank">💻 GitHub</a>` : ''}
          ${p.links.info ? `<span class="carousel-info" onclick="${p.links.info}">ℹ️ Más info</span>` : ''}
        </div>
      </div>
    </div>
  `).join('');
  return `
  <section id="projects" class="section section-animate">
    <div class="container">
      <h2 class="section-title">Proyectos Web</h2>
      <div class="swiper projects-swiper">
        <div class="swiper-wrapper">${slides}</div>
        <div class="swiper-pagination projects-pagination"></div>
        <div class="swiper-button-next projects-next"></div>
        <div class="swiper-button-prev projects-prev"></div>
      </div>
    </div>
  </section>`;
}

function buildSkills(data) {
  const cats = data.skills.categories.map(c =>
    `<div class="skill-card glass"><h3>${c.icon} ${c.title}</h3><div class="skill-tags">${c.tags.map(t => `<span>${t}</span>`).join('')}</div></div>`
  ).join('');
  const soft = data.skills.soft.map(s => `<span class="soft-skill glass">${s}</span>`).join('');
  return `
  <section id="skills" class="section section-animate">
    <div class="container">
      <h2 class="section-title">Habilidades Técnicas</h2>
      <div class="skills-grid">${cats}</div>
      <h2 class="section-title" style="margin-top:36px">Habilidades Blandas</h2>
      <div class="soft-skills">${soft}</div>
    </div>
  </section>`;
}

function buildCourses(data) {
  const courses = data.education.courses.map(c =>
    `<div class="course-card glass${c.new ? ' new' : ''}">
      ${c.new ? '<span class="course-new-badge">NUEVO</span>' : ''}
      <div class="course-icon">${c.icon}</div>
      <div class="course-info"><h4>${c.title}</h4><p>${c.institution} · ${c.date}</p>${c.hours ? `<span class="course-hours">${c.hours}h</span>` : ''}</div>
    </div>`
  ).join('');
  const sena = data.education.sena.map(s =>
    `<div class="course-card glass">
      <div class="course-icon">📜</div>
      <div class="course-info"><h4>${s.title}</h4><p>${s.institution || ''} ${s.date}${s.note ? ` · ${s.note}` : ''}</p></div>
    </div>`
  ).join('');
  return `
  <section id="courses" class="section alt section-animate">
    <div class="container">
      <h2 class="section-title">Cursos Platzi · ${data.education.courses.filter(c=>c.new).length} Nuevos</h2>
      <p style="font-size:13px;color:var(--text-muted);margin-bottom:20px">15 cursos completados el 30 de Junio de 2026 · ${data.education.courses.reduce((a,c)=>a+(c.hours||0),0)}+ horas</p>
      <div class="courses-grid">${courses}</div>
      <h2 class="section-title" style="margin-top:36px">Formación SENA</h2>
      <div class="courses-grid">${sena}</div>
    </div>
  </section>`;
}

function buildCertificates(data) {
  const certs = data.certificates.filter(c => !c.hidden);
  const slides = certs.map(c => `
    <div class="swiper-slide cert-swiper-slide">
      <div class="cert-card glass${c.new ? ' is-new' : ''}" onclick="openCertificate('assets/images/${encodeURIComponent(c.file)}','${c.title}')">
        ${c.new ? '<span class="cert-badge-new">🔥 NUEVO</span>' : ''}
        <img src="assets/images/${encodeURIComponent(c.file)}" alt="${c.title}" loading="lazy">
        <h4>${c.title}</h4>
        <p>${c.subtitle}</p>
      </div>
    </div>
  `).join('');
  return `
  <section id="certificates" class="section section-animate">
    <div class="container">
      <h2 class="section-title">Certificaciones · ${certs.length}</h2>
      <div class="swiper certs-swiper">
        <div class="swiper-wrapper">${slides}</div>
        <div class="swiper-pagination certs-pagination"></div>
        <div class="swiper-button-next certs-next"></div>
        <div class="swiper-button-prev certs-prev"></div>
      </div>
    </div>
  </section>`;
}

function buildEducation(data) {
  const academic = data.education.academic.map((e, i) =>
    `<div class="edu-card glass" style="--accent-color:${['#667eea','#48bb78','#ed8936'][i]}">
      <div class="edu-icon">${e.icon}</div>
      <h3>${e.title}</h3>
      <p class="edu-institution">${e.institution}</p>
      <p class="edu-date">${e.period}</p>
      <p class="edu-desc">${e.desc}</p>
    </div>`
  ).join('');
  return `
  <section id="education" class="section alt section-animate">
    <div class="container">
      <h2 class="section-title">Formación Académica</h2>
      <div class="edu-grid">${academic}</div>
    </div>
  </section>`;
}

function buildFooter(data) {
  const p = data.personal;
  return `
  <footer class="footer">
    <div class="container">
      <div class="footer-links">
        <a href="${p.social.whatsapp}" target="_blank">WhatsApp</a>
        <a href="${p.social.linkedin}" target="_blank">LinkedIn</a>
        <a href="${p.social.github}" target="_blank">GitHub</a>
        <a href="#" onclick="downloadCV();return false">📄 Descargar CV</a>
      </div>
      <p class="footer-copy">© 2026 <strong>${p.name}</strong> — CV de Alto Rendimiento</p>
      <p class="footer-tech">Node.js · Express · Three.js · Swiper.js · REST API · Python</p>
    </div>
  </footer>`;
}

async function render() {
  const loader = document.getElementById('app-loader');
  try {
    cvData = await fetchData();
    buildNav(cvData);
    const app = document.getElementById('app');
    app.innerHTML = buildHero(cvData) + buildAbout(cvData) + buildExperience(cvData) +
      buildProjects(cvData) + buildSkills(cvData) + buildCourses(cvData) +
      buildCertificates(cvData) + buildEducation(cvData) + buildFooter(cvData);

    initSwiperProjects();
    initSwiperCerts();
    initScrollAnimations();
    initNavbar();
    loader.classList.add('hidden');
    setTimeout(() => { loader.style.display = 'none'; }, 600);
  } catch (err) {
    loader.innerHTML = `<p style="color:#ef4444">Error: ${err.message}</p>`;
  }
}

function initNavbar() {
  document.getElementById('navToggle').addEventListener('click', () => {
    document.getElementById('navLinks').classList.toggle('open');
  });
  window.addEventListener('scroll', () => {
    document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 50);
    document.getElementById('scrollTop').classList.toggle('visible', window.scrollY > 300);
  });
  document.getElementById('scrollTop').addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

function initSwiperProjects() {
  new Swiper('.projects-swiper', {
    effect: 'coverflow',
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: 'auto',
    spaceBetween: 24,
    speed: 600,
    loop: true,
    coverflowEffect: {
      rotate: 30,
      stretch: 0,
      depth: 200,
      modifier: 1,
      slideShadows: false
    },
    pagination: {
      el: '.projects-pagination',
      dynamicBullets: true,
      clickable: true
    },
    navigation: {
      nextEl: '.projects-next',
      prevEl: '.projects-prev'
    },
    keyboard: { enabled: true },
    breakpoints: {
      320: { slidesPerView: 1, spaceBetween: 16 },
      640: { slidesPerView: 2, spaceBetween: 20 },
      1024: { slidesPerView: 3, spaceBetween: 24 }
    }
  });
}

function initSwiperCerts() {
  new Swiper('.certs-swiper', {
    effect: 'coverflow',
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: 'auto',
    spaceBetween: 16,
    speed: 500,
    loop: true,
    coverflowEffect: {
      rotate: 40,
      stretch: 0,
      depth: 150,
      modifier: 1,
      slideShadows: true
    },
    pagination: {
      el: '.certs-pagination',
      dynamicBullets: true,
      clickable: true
    },
    navigation: {
      nextEl: '.certs-next',
      prevEl: '.certs-prev'
    },
    keyboard: { enabled: true },
    breakpoints: {
      320: { slidesPerView: 1, spaceBetween: 10 },
      640: { slidesPerView: 2, spaceBetween: 16 },
      1024: { slidesPerView: 4, spaceBetween: 16 }
    }
  });
}

function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.section-animate').forEach(el => observer.observe(el));
}

function openCertificate(src, title) {
  const modal = document.getElementById('imageModal');
  document.getElementById('modalImg').src = src;
  window._currentImageSrc = src;
  modal.style.display = 'flex';
}

function closeModal() {
  document.getElementById('imageModal').style.display = 'none';
}

function downloadCurrentImage() {
  if (window._currentImageSrc) {
    const a = document.createElement('a');
    a.href = window._currentImageSrc;
    a.download = 'certificado.jpg';
    a.click();
  }
}

document.getElementById('imageModal').onclick = function (e) {
  if (e.target === this) closeModal();
};

function showTradingInfo() {
  const modal = document.createElement('div'); modal.className = 'modal'; modal.style.display = 'flex';
  modal.innerHTML = `
    <span class="modal-close" onclick="this.parentElement.remove()">&times;</span>
    <div class="modal-box glass">
      <h2>🤖 Trading Bot Algorítmico</h2>
      <p>Bot en Python para trading algorítmico en criptomonedas, integrado con la <strong>API de Binance</strong>. Opera 24/7 en un VPS con análisis técnico automatizado.</p>
      <ul><li>Integración API Binance</li><li>Análisis financiero automatizado</li><li>Estrategias algorítmicas</li><li>VPS 24/7</li></ul>
    </div>`;
  document.body.appendChild(modal);
  modal.onclick = e => { if (e.target === modal) modal.remove(); };
}

function showMoviVIPInfo() {
  const modal = document.createElement('div'); modal.className = 'modal'; modal.style.display = 'flex';
  modal.innerHTML = `
    <span class="modal-close" onclick="this.parentElement.remove()">&times;</span>
    <div class="modal-box glass">
      <h2>📶 MoviVIP Network</h2>
      <p>Marca propia de datos móviles VIP con aprovisionamiento de red, soporte técnico y bots Telegram.</p>
      <ul><li>Paquetes de datos VIP</li><li>Aprovisionamiento de red</li><li>Soporte 24/7</li></ul>
    </div>`;
  document.body.appendChild(modal);
  modal.onclick = e => { if (e.target === modal) modal.remove(); };
}

function printCV(includeCerts) {
  if (!cvData) { alert('Datos no cargados aun.'); return; }
  const d = cvData;
  const p = d.personal;
  const newC = d.education.courses.filter(c => c.new).length;
  const totalH = d.education.courses.reduce((a,c) => a + (c.hours||0), 0);

  let html = `<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  @page { margin: 0; size: A4; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Inter', sans-serif; background: #fff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { width: 210mm; min-height: 297mm; display: flex; }
  .left { width: 35%; background: #1e293b; padding: 32px 24px; color: #e2e8f0; }
  .right { width: 65%; background: #f8fafc; padding: 32px 32px; }
  .photo { width: 120px; height: 120px; border-radius: 50%; margin: 0 auto 20px; border: 3px solid #334155; overflow: hidden; }
  .photo img { width: 100%; height: 100%; object-fit: cover; }
  .lh { font-size: 11px; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 2px; border-bottom: 1px solid #334155; padding-bottom: 6px; margin: 20px 0 12px; }
  .lh:first-of-type { margin-top: 0; }
  .ci { font-size: 11px; color: #cbd5e1; margin: 5px 0; line-height: 1.4; font-weight: 300; }
  .sc { margin: 8px 0; }
  .sc .sct { font-size: 10px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }
  .sc .sctg { font-size: 9px; color: #94a3b8; margin-top: 2px; line-height: 1.4; }
  .bar { background: #334155; height: 5px; border-radius: 10px; margin: 4px 0 8px; }
  .bar-fill { height: 5px; border-radius: 10px; background: #38bdf8; }
  .la { font-size: 10px; color: #cbd5e1; margin: 4px 0; font-weight: 300; line-height: 1.3; }
  .la strong { color: #e2e8f0; font-weight: 600; }
  .st { font-size: 9px; color: #94a3b8; margin: 2px 0; padding-left: 10px; position: relative; font-weight: 300; }
  .st::before { content:'\\2022'; position:absolute; left:0; }
  .n { font-size: 26px; font-weight: 800; color: #0f172a; line-height: 1.1; }
  .n span { color: #0284c7; }
  .tags { display: flex; flex-wrap: wrap; gap: 5px; margin: 8px 0 16px; }
  .tags span { font-size: 8px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: 3px 8px; background: #e2e8f0; color: #475569; border-radius: 3px; }
  .sec { font-size: 11px; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 2px; margin: 18px 0 10px; display: flex; align-items: center; gap: 8px; }
  .sec::before { content:''; width: 8px; height: 8px; border-radius: 50%; background: #0284c7; display: inline-block; flex-shrink: 0; }
  .right p { font-size: 10px; line-height: 1.5; color: #475569; text-align: justify; font-weight: 300; }
  .ei { margin: 10px 0; padding-left: 12px; border-left: 2px solid #e2e8f0; }
  .eh { display: flex; justify-content: space-between; align-items: baseline; }
  .er { font-size: 11px; font-weight: 700; color: #0f172a; }
  .ed { font-size: 9px; color: #94a3b8; font-weight: 500; }
  .ec { font-size: 10px; color: #475569; font-weight: 500; margin: 2px 0 4px; }
  .ei ul { list-style: none; padding: 0; }
  .ei ul li { font-size: 9.5px; color: #475569; line-height: 1.4; margin: 2px 0; padding-left: 12px; position: relative; font-weight: 300; }
  .ei ul li::before { content:'\\2022'; position:absolute; left:0; color: #0284c7; }
  .ed-row { display: flex; justify-content: space-between; margin: 3px 0; }
  .ed-l { font-size: 10.5px; font-weight: 600; color: #0f172a; }
  .ed-r { font-size: 9px; color: #94a3b8; }
  .ed-s { font-size: 9.5px; color: #475569; font-weight: 300; }
  .cb { display: inline-block; font-size: 8px; font-weight: 600; padding: 2px 8px; border-radius: 4px; background: #e0f2fe; color: #0284c7; }
  .cl { font-size: 9px; color: #475569; line-height: 1.4; font-weight: 300; }
  .cpg { page-break-before: always; padding: 20px; text-align: center; }
  .cpg h2 { font-size: 12px; color: #0f172a; margin-bottom: 2px; }
  .cpg .cps { font-size: 9px; color: #94a3b8; margin-bottom: 8px; }
  .cpg img { max-width: 100%; max-height: 250mm; }
  .ft { font-size: 9px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 10px; margin-top: 20px; display: flex; justify-content: space-between; font-weight: 300; }
</style></head><body>
<div class="page">
  <div class="left">
    <div class="photo"><img src="${p.photo}"></div>
    <div class="lh">Contacto</div>
    <div class="ci">${p.phone}</div>
    <div class="ci">${p.email}</div>
    <div class="ci">linkedin.com/in/esteban</div>
    <div class="ci">github.com/studioanime977</div>
    <div class="lh">Habilidades</div>
    ${d.skills.categories.map(c => '<div class="sc"><div class="sct">'+c.title+'</div><div class="bar"><div class="bar-fill" style="width:'+(c.tags.length>4?90:70)+'%"></div></div><div class="sctg">'+c.tags.slice(0,4).join(', ')+'</div></div>').join('')}
    <div class="lh">Logros Clave</div>
    <div class="la"><strong>Monetizacion Web:</strong> Plataformas full-stack indexadas en Google y Vercel.</div>
    <div class="la"><strong>Automatizacion:</strong> Bots Python + API Binance con 99.9% uptime en VPS.</div>
    <div class="la"><strong>Infraestructura:</strong> Servidores Ubuntu con protocolos Vmess/V2ray y panel TunnelActive.</div>
    <div class="la"><strong>Certificaciones:</strong> 30+ certificados tecnicos en Platzi, SENA y CENSA.</div>
    <div class="lh">Competencias</div>
    ${d.skills.soft.map(s => '<div class="st">'+s+'</div>').join('')}
  </div>
  <div class="right">
    <div class="n">${p.name.split(' ')[0]} ${p.name.split(' ')[1]}<br><span>${p.name.split(' ').slice(2).join(' ')}</span></div>
    <div class="tags">${p.title.split(' · ').map(t => '<span>'+t+'</span>').join('')}</div>
    <div class="sec">Perfil Profesional</div>
    <p>${d.profile}</p>
    <div class="sec">Experiencia</div>
    ${d.experience.map(e => '<div class="ei"><div class="eh"><span class="er">'+e.role+'</span><span class="ed">'+e.period+'</span></div><div class="ec">'+e.company+'</div><ul>'+e.highlights.map(h => '<li>'+h+'</li>').join('')+'</ul></div>').join('')}
    <div class="sec">Formacion</div>
    <div class="ed-row"><span class="ed-l">CENSA - Monteria</span><span class="ed-r">2024 - 2025</span></div>
    <div class="ed-s">Tecnico en Sistemas Informaticos</div>
    <div style="margin:8px 0"><span class="cb">${newC} NUEVOS</span> <strong style="font-size:10px">${d.education.courses.length} cursos Platzi</strong> <span style="font-size:9px;color:#94a3b8">${totalH}h</span></div>
    <div class="cl">${d.education.courses.map(c => c.title).join(' \u2022 ')}</div>
    <div class="sec">Proyectos</div>
    <div class="cl">${d.projects.map(p => p.name).join(' \u2022 ')}</div>
    <div class="ft"><span>${new Date().toLocaleDateString('es-CO')}</span><span>CV - Esteban Manuel Lopez Rivero</span></div>
  </div>
</div>`;

  if (includeCerts) {
    d.certificates.filter(c => !c.hidden).forEach(c => {
      html += '<div class="cpg"><h2>'+c.title+'</h2><div class="cps">'+c.subtitle+'</div><img src="assets/images/'+c.file+'"></div>';
    });
  }

  html += '</body></html>';

  const el = document.createElement('div');
  el.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;z-index:99999;background:white;overflow:auto';
  el.innerHTML = '<iframe style="width:100%;height:100%;border:none" id="pdfFrame"></iframe>';
  document.body.appendChild(el);
  const iframe = el.querySelector('iframe');
  iframe.src = 'data:text/html;charset=utf-8,' + encodeURIComponent(html);
  iframe.onload = function() {
    setTimeout(function() {
      try { iframe.contentWindow.focus(); iframe.contentWindow.print(); } catch(e) {}
    }, 1000);
  };
  setTimeout(function() {
    if (document.body.contains(el)) document.body.removeChild(el);
  }, 120000);
}

function downloadCV() {
  const modal = document.createElement('div'); modal.className = 'modal'; modal.style.display = 'flex';
  modal.innerHTML = `
    <span class="modal-close" onclick="this.parentElement.remove()">&times;</span>
    <div class="modal-box glass" style="max-width:380px;text-align:center">
      <h2>📄 Descargar CV</h2>
      <p style="font-size:12px;color:var(--text-muted);margin:8px 0">Elige la versión:</p>
      <a href="assets/downloads/ESTEBAN-MANUEL-LOPEZ-RIVERO.pdf" download="CV_Esteban_Lopez.pdf" class="hero-btn cv" style="margin:4px;width:85%;text-align:center;text-decoration:none" onclick="this.closest('.modal').remove()">📄 CV Plano (PDF)</a>
      <a href="assets/downloads/ESTEBAN-MANUEL-LOPEZ-RIVERO-COMPLETO.pdf" download="CV_Esteban_Lopez_Completo.pdf" class="hero-btn" style="margin:4px;width:85%;background:#0f9b0f;text-align:center;text-decoration:none" onclick="this.closest('.modal').remove()">📚 CV Completo + Certificados</a>
      <p style="font-size:10px;color:var(--text-muted);margin:8px 0 0">¿No descarga? <a href="#" onclick="this.closest('.modal').remove();printCV(false);return false" style="color:var(--accent)">Generar con navegador</a></p>
    </div>`;
  document.body.appendChild(modal);
  modal.onclick = e => { if (e.target === modal) modal.remove(); };
}

document.addEventListener('DOMContentLoaded', render);
