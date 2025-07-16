// scripts/updateIndex.esmodule.js
import { readFile, writeFile } from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const [,, newPath, title, targetFile = 'index.md'] = process.argv;

if (!newPath || !title) {
  console.error('❌ Usage: node updateIndex.esmodule.js <path> <title> [targetFile]');
  process.exit(1);
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const indexPath = path.resolve(__dirname, '..', targetFile);

const newEntry = `- [${title}](${newPath})\n`;

try {
  const content = await readFile(indexPath, 'utf-8');

  if (content.includes(newPath)) {
    console.log('⚠️ Entry already exists in index.md');
  } else {
    await writeFile(indexPath, content + '\n' + newEntry);
    console.log('✅ Entry added to', targetFile, ':', newEntry);
  }
} catch (err) {
  console.error('❌ Error updating', targetFile, ':', err);
}

