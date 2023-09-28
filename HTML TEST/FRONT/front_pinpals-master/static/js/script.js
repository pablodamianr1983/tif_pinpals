const daySelect = document.querySelector('select[name="day"]');
const monthSelect = document.querySelector('select[name="month"]');
const yearSelect = document.querySelector('select[name="year"]');

for (let day = 1; day <= 31; day++) {
    const option = document.createElement('option');
    option.value = day;
    option.textContent = day;
    daySelect.appendChild(option);
}


for (let month = 1; month <= 12; month++) {
    const option = document.createElement('option');
    option.value = month;
    option.textContent = month;
    monthSelect.appendChild(option);
}


const currentYear = new Date().getFullYear();
for (let year = currentYear; year >= 1960; year--) {
    const option = document.createElement('option');
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
}
