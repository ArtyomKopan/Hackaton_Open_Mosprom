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




        let dataSpan = document.querySelector('.image-placeholder span').textContent = "";
        let data1 = {
            periodFrom: this.periodFrom.value,
            periodTo: this.periodTo.value,
        };
		fetch('/graphics3', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data1)
        })
        .then(response => response.blob()) // Получаем blob изображения
        .then(blob => {
           // Из blob создаем URL
            const imgElement = document.createElement('img');
            imgElement.src = "static/plot4.png"; // Кладем src
            imgElement.alt = "static/plot4.png";
            document.body.appendChild(imgElement);
            const imgElement2 = document.createElement('img');
            imgElement2.src = "static/plot5.png"; // Кладем src
            imgElement2.alt = "static/plot5.png";

            document.body.appendChild(imgElement2);// Добавляем на страницу
            console.log("добавил картинку")
	})


        let data5 = {
            periodFrom: this.periodFrom.value,
            periodTo: this.periodTo.value,
            specialization: 'общее',
            value : ''
        };
        console.log("debug")
        fetch('/get_revenue', {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify(data5)
         })
         .then(response => response.json())
         .then(data => {
             console.log('Результаты поиска:', data);
			 document.getElementById('stat-value-salary').textContent = data.sum + ' тыс, руб';
			 document.getElementById('stat-value-earnings').textContent = data.sum2 + ' тыс, руб';
			 document.getElementById('stat-value-work').textContent = data.sum3 + ' человек';

         })
         .catch(error => {
             console.error('Ошибка поиска:', error);
         });


        console.log('Выполняется поиск за период:', searchData);
        let fromDate = '';
        let toDate = '';
         fetch('/search', {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({
            fromDate: searchData.periodFrom,  // дата начала
            toDate: searchData.periodTo
            })
         })
         .then(response => response.json())
         .then(data => {
             console.log('Результаты поиска:', data);
         })
         .catch(error => {
             console.error('Ошибка поиска:', error);
         });

        // Для демонстрации - показываем уведомление
				// для вставки изображения использовать function insertImages(images)
        this.showNotification(`Поиск данных за период ${searchData.periodFrom}-${searchData.periodTo}`);
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