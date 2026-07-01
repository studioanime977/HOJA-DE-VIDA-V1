const app = require('./src/server');
const config = require('./src/config');

app.listen(config.port, () => {
  console.log(`\x1b[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`  CV API Server`);
  console.log(`  http://localhost:${config.port}`);
  console.log(`  API: http://localhost:${config.port}/api/cv`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m`);
});
