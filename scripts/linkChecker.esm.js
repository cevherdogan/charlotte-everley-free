// scripts/linkChecker.esm.js
import fs from 'fs/promises';
import path from 'path';
import fetch from 'node-fetch';

async function readMdFiles(dir) {
  let results = [];
  const files = await fs.readdir(dir, { withFileTypes: true });
  for (let file of files) {
    const full = path.join(dir, file.name);
    if (file.isDirectory()) results.push(...await readMdFiles(full));
    else if (file.name.endsWith('.md')) {
      const text = await fs.readFile(full, 'utf-8');
      const links = [...text.matchAll(/\[.*?\]\((https?:\/\/.*?)\)/g)];
      for (let [, url] of links) results.push({ file: full, url });
    }
  }
  return results;
}

async function checkLinks(entries) {
  const report = [];
  for (let { file, url } of entries) {
    try {
      const res = await fetch(url, { method: 'HEAD', redirect: 'manual', timeout: 5000 });
      if (!res.ok) report.push({ file, url, status: res.status });
    } catch (err) {
      report.push({ file, url, error: err.message });
    }
  }
  return report;
}

(async ()=>{
  // const entries = await readMdFiles('./articles');
  const entries = await readMdFiles('./');
  const bad = await checkLinks(entries);
  if (bad.length === 0) console.log('✅ Tüm bağlantılar çalışıyor.');
  else bad.forEach(b =>
    console.log(`❌ ${b.file} → ${b.url} — ${b.status||b.error}`)
  );
})();
