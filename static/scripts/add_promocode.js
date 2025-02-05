document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("popup");
    const addButton = document.getElementById("add-promocode");
    const closeButton = document.querySelector(".close-btn-promocode");

    addButton.addEventListener("click", function () {
        popup.style.display = "flex";
    });

    closeButton.addEventListener("click", function () {
        popup.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target === popup) {
            popup.style.display = "none";
        }
    });
});
