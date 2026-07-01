const express = require('express');
const path = require('path');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const config = require('./config');
const cvRoutes = require('./api/cv.routes');
const { notFound, errorHandler } = require('./middleware');

const app = express();

// ══════════════════════════════════════════════
// SECURITY: Helmet - HTTP headers hardening
// ══════════════════════════════════════════════
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "'unsafe-eval'",
        "cdnjs.cloudflare.com", "cdn.jsdelivr.net"],
      styleSrc: ["'self'", "'unsafe-inline'",
        "cdn.jsdelivr.net", "fonts.googleapis.com"],
      imgSrc: ["'self'", "data:", "blob:",
        "*.vercel.app", "*.web.app", "*.firebasestorage.app"],
      fontSrc: ["'self'", "data:", "fonts.gstatic.com"],
      connectSrc: ["'self'", "https://hoja-de-vida-esteban.web.app"],
      frameAncestors: ["'none'"],
      upgradeInsecureRequests: []
    }
  },
  crossOriginEmbedderPolicy: false,
  crossOriginResourcePolicy: { policy: "same-origin" }
}));

app.disable('x-powered-by');

// ══════════════════════════════════════════════
// SECURITY: Rate limiting - prevent DoS/brute force
// ══════════════════════════════════════════════
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 150,
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: 'Too many requests, please try again later.' }
});

const chatLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 20,
  message: { error: 'Chat rate limit exceeded.' }
});

app.use('/api/', apiLimiter);
app.use('/api/cv/chat', chatLimiter);

// ══════════════════════════════════════════════
// CORS - locked to specific origins
// ══════════════════════════════════════════════
const allowedOrigins = [
  'http://localhost:3000',
  'https://hoja-de-vida-esteban.web.app',
  'https://hoja-de-vida-esteban.firebaseapp.com',
  'https://hoja-de-vida-v1.vercel.app'
];

app.use(cors({
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('CORS not allowed'));
    }
  },
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type'],
  maxAge: 86400
}));

app.use(express.json({ limit: '100kb' }));

// ══════════════════════════════════════════════
// STATIC FILES - with security headers
// ══════════════════════════════════════════════
const staticOptions = {
  maxAge: '7d',
  etag: true,
  lastModified: true,
  setHeaders: (res, fpath) => {
    if (fpath.endsWith('.pdf')) {
      res.setHeader('Content-Disposition', 'inline');
    }
    if (fpath.match(/\.(png|jpg|jpeg|gif|ico|webp)$/)) {
      res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
    }
  }
};

app.use('/assets/images', express.static(
  path.join(config.publicDir, 'assets', 'images'), staticOptions));
app.use('/assets/icons', express.static(
  path.join(config.publicDir, 'assets', 'icons'), staticOptions));
app.use('/assets/downloads', express.static(
  path.join(config.publicDir, 'assets', 'downloads'), staticOptions));
app.use('/assets/data', express.static(
  path.join(config.publicDir, 'assets', 'data'), staticOptions));
app.use(express.static(config.publicDir, staticOptions));

// ══════════════════════════════════════════════
// API ROUTES
// ══════════════════════════════════════════════
app.use('/api/cv', cvRoutes);

// ══════════════════════════════════════════════
// PDF GENERATION ENDPOINT
// ══════════════════════════════════════════════
app.post('/api/cv/pdf', async (req, res) => {
  try {
    let puppeteer;
    try { puppeteer = require('puppeteer'); } catch {
      try { puppeteer = require('puppeteer-core'); } catch {
        return res.status(503).json({ error: 'PDF generation unavailable' });
      }
    }
    const { mode = 'plain', html } = req.body;
    if (html) {
      const browser = await puppeteer.launch({
        headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox']
      });
      const page = await browser.newPage();
      await page.setContent(html, { waitUntil: 'networkidle0' });
      const pdf = await page.pdf({
        format: 'A4', printBackground: true,
        margin: { top: '15mm', bottom: '15mm', left: '10mm', right: '10mm' }
      });
      await browser.close();
      res.setHeader('Content-Type', 'application/pdf');
      res.setHeader('Content-Disposition', 'attachment; filename=CV_Esteban_Lopez.pdf');
      return res.send(pdf);
    }
    const fullUrl = `${req.protocol}://${req.get('host')}/pdf-template.html?mode=${mode}`;
    const browser = await puppeteer.launch({
      headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.goto(fullUrl, { waitUntil: 'networkidle0', timeout: 30000 });
    await page.waitForTimeout(2000);
    const pdf = await page.pdf({
      format: 'A4', printBackground: true,
      margin: { top: '15mm', bottom: '15mm', left: '10mm', right: '10mm' }
    });
    await browser.close();
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', 'attachment; filename=CV_Esteban_Lopez.pdf');
    res.send(pdf);
  } catch (err) {
    console.error('PDF Error:', err);
    res.status(500).json({ error: 'PDF generation failed' });
  }
});

// ══════════════════════════════════════════════
// ERROR HANDLING
// ══════════════════════════════════════════════
app.use(notFound);
app.use(errorHandler);

app.get('*', (req, res) => {
  res.sendFile(path.join(config.publicDir, 'index.html'));
});

module.exports = app;
