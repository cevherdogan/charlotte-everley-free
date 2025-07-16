const fs = require('fs');
const path = require('path');

const articlesDir = path.join(__dirname, '../../articles');
const indexFile = path.join(articlesDir, 'index.md');

function getTitleFromFilename(filename) {
  const base = path.basename(filename, '.html');
  return base
    .replace(/-/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}

function generateMarkdownLinks() {
  const files = fs.readdirSync(articlesDir);
  const htmlFiles = files.filter(file => file.endsWith('.html'));

  const markdown = htmlFiles.map(file => {
    const title = getTitleFromFilename(file);
    return `- [${title}](./${file})`;
  }).join('\n');

  return `# Articles Index\n\n${markdown}\n`;
}

const content = generateMarkdownLinks();
fs.writeFileSync(indexFile, content);

console.log('✅ articles/index.md updated.');
