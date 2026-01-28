/**
 * FlipBook - Upload Handler
 */
(function() {
    'use strict';
    
    const MAX_SIZE = 30 * 1024 * 1024; // 30 MB
    
    const $ = id => document.getElementById(id);
    const dropzone = $('dropzone');
    const fileInput = $('fileInput');
    const content = $('dropzoneContent');
    const loading = $('dropzoneLoading');
    const loadingText = $('loadingText');
    const progressFill = $('progressFill');
    
    let uploading = false;
    
    // Event listeners
    dropzone.addEventListener('click', () => !uploading && fileInput.click());
    dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', e => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });
    fileInput.addEventListener('change', e => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });
    
    function handleFile(file) {
        // Validation
        if (file.type !== 'application/pdf') {
            showToast('Seuls les fichiers PDF sont acceptés', 'error');
            return;
        }
        if (file.size > MAX_SIZE) {
            showToast('Fichier trop volumineux (max 30 MB)', 'error');
            return;
        }
        
        upload(file);
    }
    
    function upload(file) {
        if (uploading) return;
        uploading = true;
        
        // UI loading
        content.hidden = true;
        loading.hidden = false;
        progressFill.style.width = '0%';
        loadingText.textContent = 'Upload en cours...';
        
        const formData = new FormData();
        formData.append('file', file);
        
        const xhr = new XMLHttpRequest();
        
        xhr.upload.onprogress = e => {
            if (e.lengthComputable) {
                const pct = Math.round((e.loaded / e.total) * 50);
                progressFill.style.width = pct + '%';
            }
        };
        
        xhr.onload = () => {
            if (xhr.status === 200) {
                const res = JSON.parse(xhr.responseText);
                if (res.success) {
                    loadingText.textContent = 'Conversion...';
                    progressFill.style.width = '75%';
                    setTimeout(() => {
                        progressFill.style.width = '100%';
                        loadingText.textContent = 'Redirection...';
                        setTimeout(() => {
                            window.location.href = res.url;
                        }, 500);
                    }, 500);
                } else {
                    handleError(res.error);
                }
            } else {
                try {
                    const res = JSON.parse(xhr.responseText);
                    handleError(res.error || 'Erreur serveur');
                } catch {
                    handleError('Erreur serveur');
                }
            }
        };
        
        xhr.onerror = () => handleError('Erreur réseau');
        
        xhr.open('POST', '/upload');
        xhr.send(formData);
    }
    
    function handleError(msg) {
        uploading = false;
        content.hidden = false;
        loading.hidden = true;
        fileInput.value = '';
        showToast(msg, 'error');
    }
    
    function showToast(msg, type = 'info') {
        const toast = document.createElement('div');
        toast.className = 'toast ' + type;
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 200);
        }, 4000);
    }
})();
