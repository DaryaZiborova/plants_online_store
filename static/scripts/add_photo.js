const fileInput = document.getElementById('photo');
const deleteButton = document.getElementById('delete');
const previewImage = document.getElementById('preview');

// Слухач для завантаження фото
fileInput.addEventListener('change', function(event) {
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
        };
        reader.readAsDataURL(fileInput.files[0]);
    }
});

// Слухач для видалення фото
deleteButton.addEventListener('click', function() {
    previewImage.src = window.location.origin + "/static/images/placeholder.jpg";
    fileInput.value = null;
});