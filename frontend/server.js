const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 8080;
const BACKEND_URL = process.env.BACKEND_URL || '';

// Inject BACKEND_URL into HTML
function injectBackendUrl(html) {
  return html.replace(
    '<head>',
    `<head>\n    <script>window.BACKEND_URL = '${BACKEND_URL}';</script>`
  );
}

// Special handling for root - serve game.html
app.get('/', (req, res) => {
  console.log('📄 Request for / - serving game.html');
  const filePath = path.join(__dirname, 'game.html');
  console.log(`📂 Loading file: ${filePath}`);
  
  fs.readFile(filePath, 'utf8', (err, html) => {
    if (err) {
      console.error('❌ Error loading game.html:', err);
      return res.status(500).send('Error loading game');
    }
    
    console.log(`✓ game.html loaded (${html.length} bytes)`);
    console.log(`🔗 Injecting BACKEND_URL: ${BACKEND_URL || '(empty)'}`);
    
    const injectedHtml = injectBackendUrl(html);
    res.setHeader('Content-Type', 'text/html');
    res.send(injectedHtml);
    
    console.log('✓ game.html sent to client');
  });
});

// Serve HTML files with BACKEND_URL injection
app.get('*.html', (req, res) => {
  console.log(`📄 Request for HTML: ${req.path}`);
  const filePath = path.join(__dirname, req.path);
  
  fs.readFile(filePath, 'utf8', (err, html) => {
    if (err) {
      console.error(`❌ Error loading ${req.path}:`, err);
      return res.status(404).send('Not found');
    }
    
    console.log(`✓ ${req.path} loaded (${html.length} bytes)`);
    const injectedHtml = injectBackendUrl(html);
    res.setHeader('Content-Type', 'text/html');
    res.send(injectedHtml);
// Serve static files AFTER HTML routes (CSS, JS, images, etc)
app.use(express.static(__dirname, {
  setHeaders: (res, filepath) => {
    console.log(`📦 Serving static file: ${filepath}`);
    if (filepath.endsWith('.html')) {
      // This shouldn't be reached due to routes above
      res.setHeader('Cache-Control', 'no-cache');
    }
  }
}));  res.setHeader('Cache-Control', 'no-cache');
    }
  }
}));

app.listen(PORT, '0.0.0.0', () => {
  console.log(`✓ Frontend server running on port ${PORT}`);
  console.log(`✓ Backend URL: ${BACKEND_URL || 'Not configured'}`);
  console.log(`✓ Serving game.html on /`);
});
