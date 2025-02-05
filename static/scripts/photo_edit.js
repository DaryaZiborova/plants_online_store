const hiddenInput = document.getElementById('photo_is_deleted');
// Додаємо слухача подій до поля вибору файлів
document.getElementById('photo').addEventListener('change', function(event) {
    const fileInput = event.target;
    // Перевіряємо, чи файл був вибраний
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader(); 
        // Встановлюємо джерело зображення у вибраний файл
        reader.onload = function(e) {
            previewImage.src = e.target.result; // Встановлюємо src для попереднього перегляду
        };
        // Читаємо файл у форматі Data URL
        reader.readAsDataURL(fileInput.files[0]);
        hiddenInput.value = 'false';
    }
});

const deleteButton = document.getElementById('delete');
const previewImage = document.getElementById('preview');
const file = document.getElementById('photo');

deleteButton.addEventListener('click', function () {
    previewImage.src = window.location.origin + "/static/images/placeholder.jpg";
    file.value = null;
    hiddenInput.value = 'true';
});