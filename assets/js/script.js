let handle;
const outDirName = 'out';

async function makeEditable(element) {
    const input = document.createElement('input');
    input.value = element.innerText;
    input.onblur = function () {
        element.innerText = input.value;
        element.classList.remove('editing');
    };
    element.innerHTML = '';
    element.appendChild(input);
    input.focus();
    element.classList.add('editing');
}

async function saveChanges() {
    const products = [];
    document.querySelectorAll('.product').forEach(productElement => {
        const product = {
            urun: productElement.querySelector('.urun').innerText,
            ozellikler: Array.from(productElement.querySelectorAll('.ozellik')).map(e => e.innerText),
            dosya_adi: productElement.querySelector('.dosya_adi').innerText,
            image_path: encodeURIComponent(productElement.querySelector('img').src)
        };
        products.push(product);
    });

    const json = JSON.stringify(products, null, 2);
    const timestamp = new Date().toISOString().replace(/[:.]/g, '_');
    const filename = `product_${timestamp}.json`;

    if (!handle) {
        handle = await window.showDirectoryPicker();
    }

    const outDirHandle = await handle.getDirectoryHandle(outDirName, { create: true });
    const fileHandle = await outDirHandle.getFileHandle(filename, { create: true });
    const writable = await fileHandle.createWritable();
    await writable.write(json);
    await writable.close();

    alert('File saved successfully!');
}

async function loadProductFile() {
    if (!handle) {
        handle = await window.showDirectoryPicker();
    }

    const outDirHandle = await handle.getDirectoryHandle(outDirName);
    const files = [];
    for await (const entry of outDirHandle.values()) {
        if (entry.kind === 'file' && entry.name.endsWith('.json')) {
            files.push(entry.name);
        }
    }

    const fileSelect = document.createElement('select');
    files.forEach(file => {
        const option = document.createElement('option');
        option.value = file;
        option.innerText = file;
        fileSelect.appendChild(option);
    });

    const loadButton = document.createElement('button');
    loadButton.innerText = 'Load';
    loadButton.onclick = async function () {
        const selectedFile = fileSelect.value;
        const fileHandle = await outDirHandle.getFileHandle(selectedFile);
        const file = await fileHandle.getFile();
        const json = await file.text();
        const products = JSON.parse(json);

        document.getElementById('products').innerHTML = '';
        products.forEach(product => {
            const productDiv = document.createElement('div');
            productDiv.classList.add('product');
            productDiv.innerHTML = `
                <img src="${decodeURIComponent(product.image_path)}" alt="${product.urun}">
                <h2 class="urun editable" onclick="makeEditable(this)">${product.urun}</h2>
                <ul>${product.ozellikler.map(feature => `<li class="ozellik editable" onclick="makeEditable(this)">${feature}</li>`).join('')}</ul>
                <p class="dosya_adi editable" onclick="makeEditable(this)" style="display:none">${product.dosya_adi}</p>
            `;
            document.getElementById('products').appendChild(productDiv);
        });
    };

    const container = document.getElementById('loadContainer');
    container.innerHTML = '';
    container.appendChild(fileSelect);
    container.appendChild(loadButton);
}


