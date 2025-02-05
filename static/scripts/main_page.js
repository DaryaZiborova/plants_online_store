document.getElementById('search').addEventListener('input', function (event) {
    const input = event.target;
    input.value = input.value.charAt(0).toUpperCase() + input.value.slice(1);
    });

document.getElementById('search').addEventListener('input', function() {
    const query = this.value;
    console.log("Подія введення спрацювала. Запит:", query);  
    if (query.length > 2) {  
        fetch(`/autocomplete/?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                console.log("Дані автозаповнення:", data);  
                const resultsContainer = document.getElementById('autocomplete-results');
                resultsContainer.innerHTML = '';  // Очищаємо попередні результати
                data.forEach(plant => {
                    const div = document.createElement('div');
                    div.textContent = plant.plant_name;
                    div.addEventListener('click', () => {
                        document.getElementById('search').value = plant.plant_name;
                        resultsContainer.innerHTML = '';  // Очищаємо результати після вибору
                    });
                    resultsContainer.appendChild(div);
                });
            })
            .catch(error => console.error("Помилка отримання даних автозаповнення:", error));  
    } else {
        document.getElementById('autocomplete-results').innerHTML = '';  // Очищаємо результати, якщо запит занадто короткий
    }
});
