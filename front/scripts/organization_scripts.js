/**
 * Инициализирует выпадающий список организаций с данными с сервера
 * @param {string} selectId - ID select элемента (по умолчанию 'organization-select')
 * @param {string} apiUrl - URL API для получения организаций (по умолчанию '/api/organization')
 */
function initOrganizationSelect(selectId = 'organization-select', apiUrl = '/api/organization') {
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
        .then(organization => {
            updateSelectOptions(selectElement, organization);
        })
        .catch(error => {
            console.error('Ошибка загрузки организациq:', error);
            showError(selectElement, 'Не удалось загрузить организации');
        });
}

/**
 * Обновляет опции в select элементе
 * @param {HTMLSelectElement} selectElement - Select элемент
 * @param {Array} organization - Массив организаций
 */
function updateSelectOptions(selectElement, organization) {
    selectElement.innerHTML = '<option value="">Выберите организацию</option>';
    
    if (!organization || organization.length === 0) {
        selectElement.innerHTML = '<option value="">Нет доступных организаций</option>';
        return;
    }
    
    organization.forEach(organization => {
        const option = document.createElement('option');
        option.value = organization.id || organization.value;
        option.textContent = organization.name || organization.label;
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
 * Получает выбранное значение организации
 * @param {string} selectId - ID select элемента
 * @returns {string} Выбранное значение
 */
function getSelectedOrganization(selectId = 'organization-select') {
    const selectElement = document.getElementById(selectId);
    return selectElement ? selectElement.value : '';
}

/**
 * Устанавливает выбранную организацию
 * @param {string} organizationId - ID организации
 * @param {string} selectId - ID select элемента
 */
function setSelectedOrganization(organizationId, selectId = 'organization-select') {
    const selectElement = document.getElementById(selectId);
    if (selectElement) {
        selectElement.value = organization;
    }
}

// Автоматическая инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initOrganizationSelect();
});