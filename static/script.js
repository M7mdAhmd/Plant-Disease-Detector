const fileInput = document.getElementById('file-upload');
const preview = document.getElementById('preview');
const errorMsg = document.getElementById('errorMsg');

preview.style.display = 'none';

window.addEventListener('beforeunload', function() {
    if (preview.src && preview.style.display === 'block') {
        sessionStorage.setItem('plantGuardImage', preview.src);
        sessionStorage.setItem('plantGuardFile', preview.src);
    }
});

window.addEventListener('load', function() {
    const savedImage = sessionStorage.getItem('plantGuardImage');
    const savedFile = sessionStorage.getItem('plantGuardFile');
    if (savedImage) {
        preview.src = savedImage;
        preview.style.display = 'block';
        if (savedFile) {
            const blob = dataURLtoBlob(savedFile);
            const file = new File([blob], "uploaded-image.jpg", { type: blob.type });
            const dt = new DataTransfer();
            dt.items.add(file);
            fileInput.files = dt.files;
        }
        sessionStorage.removeItem('plantGuardImage');
        sessionStorage.removeItem('plantGuardFile');
    }
});

function dataURLtoBlob(dataurl) {
    const arr = dataurl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while(n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type:mime});
}

fileInput.addEventListener('change', function() {
    const file = this.files[0];
    if(file) {
        if(file.size > 5 * 1024 * 1024) {
            errorMsg.textContent = 'File is too large!';
            this.value = "";
            preview.style.display = 'none';
            return;
        }
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            errorMsg.textContent = '';
        }
        reader.readAsDataURL(file);
    } else {
        preview.style.display = 'none';
    }
});