const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const imagesDir = path.join(__dirname, '..', 'public', 'assets', 'images');
const cvJsonPath = path.join(__dirname, '..', 'src', 'data', 'cv.json');
const cvPublicPath = path.join(__dirname, '..', 'public', 'assets', 'data', 'cv.json');
const mappingPath = path.join(__dirname, 'file-mapping.json');

let mapping = {};
try { mapping = JSON.parse(fs.readFileSync(mappingPath, 'utf-8')); } catch {}

const files = fs.readdirSync(imagesDir).filter(f => {
  const ext = path.extname(f).toLowerCase();
  return ['.jpg','.jpeg','.png','.gif','.webp'].includes(ext);
});

files.forEach(f => {
  if (mapping[f]) return;
  const ext = path.extname(f);
  const hash = crypto.createHash('md5').update(f).digest('hex');
  const newName = hash + ext;
  fs.renameSync(path.join(imagesDir, f), path.join(imagesDir, newName));
  mapping[f] = newName;
  console.log(f + ' -> ' + newName);
});

fs.writeFileSync(mappingPath, JSON.stringify(mapping, null, 2));

let cv = fs.readFileSync(cvJsonPath, 'utf-8');
for (const [old, hash] of Object.entries(mapping)) {
  const escaped = old.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  cv = cv.replace(new RegExp(escaped, 'g'), hash);
}
fs.writeFileSync(cvJsonPath, cv, 'utf-8');
fs.writeFileSync(cvPublicPath, cv, 'utf-8');

console.log('\nDone. ' + Object.keys(mapping).length + ' files mapped, cv.json updated.');
