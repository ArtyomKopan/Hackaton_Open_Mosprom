/**
 * Инициализирует выпадающий список отраслей с данными с сервера
 * @param {string} selectId - ID select элемента (по умолчанию 'industry-select')
 * @param {string} apiUrl - URL API для получения отраслей (по умолчанию '/api/industries')
 */
function initIndustrySelect(selectId = 'industry-select', apiUrl = '/api/industries') {
    const selectElement = document.getElementById(selectId);
    
    if (!selectElement) {
        console.error(`Элемент с ID "${selectId}" не найден`);
        return;
    }
    
    // Показываем состояние загрузки
    selectElement.innerHTML = '<option value="">Загрузка...</option>';
    selectElement.disabled = true;
    selectElement.classList.add('loading');
    
    // Загружаем данные с сервера
    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(industries => {
            updateSelectOptions(selectElement, industries);
        })
        .catch(error => {
            console.error('Ошибка загрузки отраслей:', error);
            showError(selectElement, 'Не удалось загрузить отрасли');
        });
}

/**
 * Обновляет опции в select элементе
 * @param {HTMLSelectElement} selectElement - Select элемент
 * @param {Array} industries - Массив отраслей
 */
function updateSelectOptions(selectElement, industries) {
    selectElement.innerHTML = '<option value="">Выберите отрасль</option>';
    
    if (!industries || industries.length === 0) {
        selectElement.innerHTML = '<option value="">Нет доступных отраслей</option>';
        return;
    }
    
    industries.forEach(industry => {
        const option = document.createElement('option');
        option.value = industry.id || industry.value;
        option.textContent = industry.name || industry.label;
        selectElement.appendChild(option);
    });
    
    selectElement.disabled = false;
    selectElement.classList.remove('loading');
}

/**
 * Показывает сообщение об ошибке
 * @param {HTMLSelectElement} selectElement - Select элемент
 * @param {string} message - Сообщение об ошибке
 */
function showError(selectElement, message) {
    selectElement.innerHTML = `<option value="">${message}</option>`;
    selectElement.disabled = false;
    selectElement.classList.remove('loading');
}

/**
 * Получает выбранное значение отрасли
 * @param {string} selectId - ID select элемента
 * @returns {string} Выбранное значение
 */
function getSelectedIndustry(selectId = 'industry-select') {
    const selectElement = document.getElementById(selectId);
    return selectElement ? selectElement.value : '';
}

/**
 * Устанавливает выбранную отрасль
 * @param {string} industryId - ID отрасли
 * @param {string} selectId - ID select элемента
 */
function setSelectedIndustry(industryId, selectId = 'industry-select') {
    const selectElement = document.getElementById(selectId);
    if (selectElement) {
        selectElement.value = industryId;
    }
}

// Автоматическая инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initIndustrySelect();
});