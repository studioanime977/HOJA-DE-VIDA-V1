const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const imgDir = path.join(__dirname, '..', 'public', 'assets', 'images');
const cvPath = path.join(__dirname, '..', 'src', 'data', 'cv.json');
const cvPubPath = path.join(__dirname, '..', 'public', 'assets', 'data', 'cv.json');

// Read cv.json to get the mapping of expected filenames
let cv = JSON.parse(fs.readFileSync(cvPath, 'utf-8'));

// Build map from original name -> hash
const mapping = {};
cv.certificates.forEach(c => {
  // The file field in cv.json is currently the hash name
  // We need to figure out what original name it maps to
  mapping[c.file] = c.file;
});

// Also check the photo
const photoHash = cv.personal.photo.replace('assets/images/', '');
mapping[photoHash] = photoHash;

// Now rebuild: hash each original name to get the expected hash
// First, let's get the actual files on disk
const files = fs.readdirSync(imgDir).filter(f => {
  const ext = path.extname(f).toLowerCase();
  return ['.jpg','.jpeg','.png','.gif','.webp'].includes(ext);
});

console.log('Files on disk:', files.length);
console.log('Certificates in cv.json:', cv.certificates.filter(c=>!c.hidden).length);

// Let's check: for each cert, does the hash file exist?
let missing = [];
cv.certificates.filter(c=>!c.hidden).forEach(c => {
  const imgFile = c.file;
  if (!files.includes(imgFile)) {
    missing.push(imgFile);
  }
});

// Check photo
if (!files.includes(photoHash)) {
  missing.push('PHOTO: ' + photoHash);
}

if (missing.length > 0) {
  console.log('\nMISSING FILES (' + missing.length + '):');
  missing.forEach(m => console.log('  ' + m));
} else {
  console.log('\nAll files present!');
}

// Solution: rename files back to predictable hashes based on ORIGINAL names
// We need to know the original names. Let's use the file-mapping.json
const mappingPath = path.join(__dirname, 'file-mapping.json');
let fileMapping = {};
try { fileMapping = JSON.parse(fs.readFileSync(mappingPath, 'utf-8')); } catch {}

console.log('\nfile-mapping entries:', Object.keys(fileMapping).length);

// The fileMapping maps originalName -> hash1
// But after the second run, files were renamed hash1 -> hash2
// cv.json points to hash2 names
// We need to go back to hash1 or original names

// Let's just rename ALL files back to their original names
// by computing md5 of original and checking if it matches
const originalNames = Object.keys(fileMapping);
let renamed = 0;
originalNames.forEach(orig => {
  const hash1 = fileMapping[orig]; // First hash
  // Check if hash1 file exists
  if (files.includes(hash1)) {
    // Already has the right name, skip
    return;
  }
  // Check if this file was double-hashed
  // The current files are hash2. We need to find which hash2 matches which hash1
  // Since we can't reverse the hash, let's just rename to original names
  const ext = path.extname(orig);
  // Check if original name already exists
  if (files.includes(orig)) return;
  // The current file was hash1 -> renamed to hash2
  // We need to find it. Let's just use the cert info in cv.json
});

// SIMPLEST APPROACH: Restore from cv.json cert titles to original filenames
// Just map what we know
console.log('\nRestoring original filenames from file-mapping...');

// We'll rename the CURRENT hash back to ORIGINAL name
originalNames.forEach(orig => {
  const hash1 = fileMapping[orig];
  if (files.includes(hash1)) {
    // hash1 file exists on disk, rename to original
    const oldPath = path.join(imgDir, hash1);
    const newPath = path.join(imgDir, orig);
    if (!fs.existsSync(newPath)) {
      fs.renameSync(oldPath, newPath);
      renamed++;
    }
    // Update cv.json mapping
    // Find cert with this hash1 and update to original name
    cv.certificates.forEach(c => {
      if (c.file === hash1) c.file = orig;
    });
    if (cv.personal.photo === 'assets/images/' + hash1) {
      cv.personal.photo = 'assets/images/' + orig;
    }
  } else {
    // Could be double-hashed, check if hash2 exists
    // hash2 = md5(hash1)
    const hash2 = crypto.createHash('md5').update(hash1).digest('hex') + path.extname(orig);
    if (files.includes(hash2)) {
      const oldPath = path.join(imgDir, hash2);
      const newPath = path.join(imgDir, orig);
      if (!fs.existsSync(newPath)) {
        fs.renameSync(oldPath, newPath);
        renamed++;
      }
      cv.certificates.forEach(c => {
        if (c.file === hash2) c.file = orig;
      });
      if (cv.personal.photo === 'assets/images/' + hash2) {
        cv.personal.photo = 'assets/images/' + orig;
      }
    }
  }
});

// Save updated cv.json
fs.writeFileSync(cvPath, JSON.stringify(cv, null, 2));
fs.writeFileSync(cvPubPath, JSON.stringify(cv, null, 2));
console.log('Renamed ' + renamed + ' files back to original names');
console.log('cv.json updated');
