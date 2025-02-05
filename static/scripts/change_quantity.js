document.addEventListener("DOMContentLoaded", function () {
    const decrementBtn = document.getElementById("decrement");
    const incrementBtn = document.getElementById("increment");
    const quantityInput = document.getElementById("quantity");
    let minQuantity = parseInt(quantityInput.min, 10);
    let maxQuantity = parseInt(quantityInput.max, 10);
    let currentQuantity = parseInt(quantityInput.value, 10);
    const itemPriceElement = document.getElementById("item-price");
    const totalPriceElement = document.getElementById("order-total");
    const originalPrice = parseFloat(itemPriceElement.textContent.replace(" грн", ""));

    function updateButtonsState() {
        decrementBtn.disabled = currentQuantity <= minQuantity;
        incrementBtn.disabled = currentQuantity >= maxQuantity;
    }
    function updatePrice() {
        const newPrice = (currentQuantity * originalPrice).toFixed(2);
        itemPriceElement.textContent = `${newPrice} грн`;
        totalPriceElement.textContent = `Загальна сума: ${newPrice} грн`;
    }

    decrementBtn.addEventListener("click", function () {
        if (currentQuantity > minQuantity) {
            currentQuantity--;
            quantityInput.value = currentQuantity;
            updateButtonsState();
            updatePrice();
        }
    });

    incrementBtn.addEventListener("click", function () {
        if (currentQuantity < maxQuantity) {
            currentQuantity++;
            quantityInput.value = currentQuantity;
            updateButtonsState();
            updatePrice();
        }
    });
});