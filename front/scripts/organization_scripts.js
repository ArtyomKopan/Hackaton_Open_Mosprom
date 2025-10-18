// 132 строчка финкция для вставки изборажений(диаграм)
// Навигация между разделами
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    const pageSections = document.querySelectorAll('.page-section');
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    // Переключение активной вкладки
    
    // Мобильное меню
    navToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
        this.classList.toggle('active');
    });

    // Закрытие меню при клике outside
    document.addEventListener('click', function(e) {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        }
    });

    // Закрытие меню при ресайзе окна
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        }
    });
});

// Функция для программного переключения вкладок
function switchToTab(tabName) {
    const tabLink = document.querySelector(`.nav-link[href="#${tabName}"]`);
    if (tabLink) {
        tabLink.click();
    }
}

// Пример использования:
// switchToTab('production'); // Переключится на вкладку "Производство"

class PeriodFilter {
    constructor() {
        this.periodFrom = document.getElementById('periodFrom');
        this.periodTo = document.getElementById('periodTo');
        this.searchBtn = document.getElementById('searchBtn');
        this.errorMessage = this.createErrorMessage();
        
        this.init();
    }
    
    init() {
        // Добавляем сообщение об ошибке в DOM
        this.periodFrom.parentNode.appendChild(this.errorMessage);
        
        // Обработчики событий
        this.searchBtn.addEventListener('click', () => this.handleSearch());
        this.periodFrom.addEventListener('change', () => this.validatePeriod());
        this.periodTo.addEventListener('change', () => this.validatePeriod());
        this.periodFrom.addEventListener('input', () => this.validatePeriod());
        this.periodTo.addEventListener('input', () => this.validatePeriod());
        
        // Enter для поиска
        this.periodFrom.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });
        this.periodTo.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });
        
        // Первоначальная валидация
        this.validatePeriod();
    }
    
    createErrorMessage() {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = 'Год "с" не может быть больше года "до"';
        return errorDiv;
    }
    
    validatePeriod() {
        const from = parseInt(this.periodFrom.value);
        const to = parseInt(this.periodTo.value);
        
        if (from > to) {
            this.periodFrom.classList.add('error');
            this.periodTo.classList.add('error');
            this.errorMessage.classList.add('show');
            this.searchBtn.disabled = true;
            return false;
        } else {
            this.periodFrom.classList.remove('error');
            this.periodTo.classList.remove('error');
            this.errorMessage.classList.remove('show');
            this.searchBtn.disabled = false;
            return true;
        }
    }
    
    handleSearch() {
        if (!this.validatePeriod()) {
            return;
        }
        
        const searchData = {
            periodFrom: this.periodFrom.value,
            periodTo: this.periodTo.value
        };
        
        // Анимация кнопки
        this.animateSearchButton();
        
        // Здесь ваш код для выполнения поиска
        this.performSearch(searchData);
    }
    
    animateSearchButton() {
        const originalText = this.searchBtn.innerHTML;
        this.searchBtn.innerHTML = '<span class="search-icon"></span> Поиск...';
        this.searchBtn.disabled = true;
        
        // Через 2 секунды возвращаем исходное состояние
        setTimeout(() => {
            this.searchBtn.innerHTML = originalText;
            this.searchBtn.disabled = false;
        }, 2000);
    }
    
    performSearch(searchData) {
        console.log('Выполняется поиск за период:', searchData);
        
        // Здесь интегрируйте ваш бэкенд вызов
        // Например:
        // fetch('/api/search', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(searchData)
        // })
        // .then(response => response.json())
        // .then(data => {
        //     console.log('Результаты поиска:', data);
        // })
        // .catch(error => {
        //     console.error('Ошибка поиска:', error);
        // });
        
        // Для демонстрации - показываем уведомление
				// для вставки изображения использовать function insertImages(images)
				// для вставки значений в блоки бюджет, экспорт и т.д. используется function updateStats(newStats)
        this.showNotification(`Поиск данных за период ${searchData.periodFrom}-${searchData.periodTo}`);
    }

		updateStats(newStats) {
    // Обновляем бюджет
    if (newStats.budget !== undefined) {
        const budgetElement = document.querySelector('.stat-item:nth-child(1) .stat-value');
        if (budgetElement) budgetElement.textContent = newStats.budget;
    }
    
    // Обновляем прибыль
    if (newStats.profit !== undefined) {
        const profitElement = document.querySelector('.stat-item:nth-child(2) .stat-value');
        if (profitElement) profitElement.textContent = newStats.profit;
    }
    
    // Обновляем занятость
    if (newStats.employment !== undefined) {
        const employmentElement = document.querySelector('.stat-item:nth-child(3) .stat-value');
        if (employmentElement) employmentElement.textContent = newStats.employment;
    }
    
    // Обновляем экспорт
    if (newStats.export !== undefined) {
        const exportElement = document.querySelector('.stat-item:nth-child(4) .stat-value');
        if (exportElement) exportElement.textContent = newStats.export;
    }
}
    
    showNotification(message) {
        // Создаем уведомление
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 50px;
            right: 20px;
            background: #72C2C9;
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Удаляем через 3 секунды
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    // Методы для внешнего использования
    setPeriod(from, to) {
        this.periodFrom.value = from;
        this.periodTo.value = to;
        this.validatePeriod();
    }
    
    getPeriod() {
        return {
            from: this.periodFrom.value,
            to: this.periodTo.value
        };
    }
}

// CSS анимации для уведомлений
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    const periodFilter = new PeriodFilter();
    
    // Делаем доступным глобально для использования в других скриптах
    window.periodFilter = periodFilter;
});

/**
 * Вставляет изображения в контейнер
 * @param {Array} images - Массив изображений или URL строк
 */
function insertImages(images) {
    const container = document.querySelector('#imagesGrid')
    
    if (!container) {
        console.error(`Контейнер ${containerSelector} не найден`);
        return;
    }
    
    if (!images || images.length === 0) {
        console.warn('Нет изображений для вставки');
        return;
    }
    
    // Очищаем контейнер
    container.innerHTML = '';
    
    // Добавляем изображения
    images.forEach(image => {
        const imgElement = document.createElement('div');
        imgElement.className = 'image-item';
        
        // Если передан объект с данными
        if (typeof image === 'object') {
            imgElement.innerHTML = `
                <img src="${image.url}" alt="${image.name || ''}">
                ${image.name ? `<div class="image-name">${image.name}</div>` : ''}
            `;
        } 
        // Если передан просто URL
        else {
            imgElement.innerHTML = `<img src="${image}" alt="Image">`;
        }
        
        container.appendChild(imgElement);
    });
}

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