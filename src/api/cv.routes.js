const express = require('express');
const fs = require('fs');
const path = require('path');
const config = require('../config');

const router = express.Router();
let cvData = null;

function loadData() {
  if (!cvData) {
    const filePath = path.resolve(__dirname, '..', 'data', 'cv.json');
    cvData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  }
  return cvData;
}

router.get('/', (req, res) => res.json(loadData()));
router.get('/personal', (req, res) => res.json(loadData().personal));
router.get('/experience', (req, res) => res.json(loadData().experience));
router.get('/projects', (req, res) => res.json(loadData().projects));
router.get('/skills', (req, res) => res.json(loadData().skills));
router.get('/education', (req, res) => res.json(loadData().education));
router.get('/certificates', (req, res) => res.json(loadData().certificates));
router.get('/stats', (req, res) => res.json(loadData().stats));
router.get('/chatbot', (req, res) => res.json(loadData().chatbot));
router.get('/profile', (req, res) => res.json({ profile: loadData().profile }));

router.post('/chat', (req, res) => {
  const data = loadData();
  const { message } = req.body;
  if (!message) return res.json({ reply: data.chatbot.greeting });
  const msg = message.toLowerCase();
  for (const [key, reply] of Object.entries(data.chatbot.responses)) {
    if (msg.includes(key)) return res.json({ reply });
  }
  res.json({
    reply: `Puedo responder sobre: experiencia, educación, cursos, habilidades, cloud, proyectos, contacto. ${data.chatbot.greeting}`
  });
});

module.exports = router;
