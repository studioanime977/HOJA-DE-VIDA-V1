const fs = require('fs');

let c = fs.readFileSync('src/data/cv.json', 'utf-8');
const phoneMatch = c.match(/"phone":\s*"([^"]+)"/);
const waMatch = c.match(/"whatsapp":\s*"([^"]+)"/);
console.log('phone:', phoneMatch?.[1]);
console.log('whatsapp:', waMatch?.[1]);

// Fix phone back to original (calls number)
if (phoneMatch && phoneMatch[1] === '573117008185') {
  c = c.replace('"phone": "573117008185"', '"phone": "3017400553"');
  fs.writeFileSync('src/data/cv.json', c);
  console.log('Fixed phone back to 3017400553');
}

// Same for public copy
let c2 = fs.readFileSync('public/assets/data/cv.json', 'utf-8');
const phoneMatch2 = c2.match(/"phone":\s*"([^"]+)"/);
if (phoneMatch2 && phoneMatch2[1] === '573117008185') {
  c2 = c2.replace('"phone": "573117008185"', '"phone": "3017400553"');
  fs.writeFileSync('public/assets/data/cv.json', c2);
  console.log('Fixed public phone back to 3017400553');
}

console.log('Done.');
