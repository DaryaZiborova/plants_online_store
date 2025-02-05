document.addEventListener("DOMContentLoaded", function() {
    const popup = document.getElementById("popup-message");
    const closeBtn = document.querySelector(".close-btn");
    if (popup) {
        closeBtn.addEventListener("click", function () {
            popup.style.display = "none";
        });
        
        setTimeout(function() {
            popup.style.opacity = "0";
            setTimeout(() => popup.remove(), 500); 
        }, 5000); 
    }
});