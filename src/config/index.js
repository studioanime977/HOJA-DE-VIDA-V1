const path = require('path');

const config = {
  port: process.env.PORT || 3000,
  root: path.resolve(__dirname, '..', '..'),
  publicDir: path.resolve(__dirname, '..', '..', 'public'),
  dataFile: path.resolve(__dirname, '..', 'data', 'cv.json'),
  imagesDir: '/public/assets/images',
  downloadsDir: '/public/assets/downloads',
  iconsDir: '/public/assets/icons',
};

module.exports = config;
