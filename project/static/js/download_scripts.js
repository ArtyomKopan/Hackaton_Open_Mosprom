class FileUploader {
    constructor() {
        this.fileInput = document.getElementById('fileInput');
        this.button1 = document.getElementById('button1');
        this.uploadContent = document.querySelector('.upload-content');
        this.fileInfo = document.getElementById('fileInfo');
				this.button2 = document.getElementById('button2')
        // новая часть
        this.button3 = document.getElementById('button3')
        this.apiInput = document.getElementById('apiInput')
    // новая часть
            this.initEventListeners();
    }

    initEventListeners() {
        // Клик по кнопке
        		// новая часть
            this.button3.addEventListener('click', () => {
        this.fileInput.click();
    });

		// новая часть
        this.button1.addEventListener('click', () => {
            this.fileInput.click();
        });

        // Выбор файла через input
        this.fileInput.addEventListener('change', (e) => {
            this.handleFileSelection(e);
        });

        // Drag and drop события
        this.uploadContent.addEventListener('dragover', (e) => {
            this.handleDragOver(e);
        });

        this.uploadContent.addEventListener('dragleave', (e) => {
            this.handleDragLeave(e);
        });

        this.uploadContent.addEventListener('drop', (e) => {
            this.handleDrop(e);
        });

				this.button2.addEventListener('click', () => {
					window.location.href = "/general"
				})
    }

    handleFileSelection(event) {
        const target = event.target;
        if (target.files && target.files.length > 0) {
            this.processFile(target.files[0]);
        }
    }
        getFileFromButton() {
        const fileInput = document.getElementById('fileInput2');

        if (fileInput && fileInput.files && fileInput.files.length > 0) {
              let file = fileInput.files[0];
               // Возвращает первый выбранный файл
        } else {
        return null; // Возвращает null если файл не выбран
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        this.uploadContent.classList.add('drag-over');
    }

    handleDragLeave(event) {
        event.preventDefault();
        this.uploadContent.classList.remove('drag-over');
    }

    handleDrop(event) {
        event.preventDefault();
        this.uploadContent.classList.remove('drag-over');

        if (event.dataTransfer && event.dataTransfer.files.length > 0) {
            const file = event.dataTransfer.files[0];
            if (this.isValidFileType(file)) {
                this.processFile(file);
            } else {
                alert('Пожалуйста, выберите файл с расширением .csv, .xls или .xlsx');
            }
        }
    }

    isValidFileType(file) {
        const allowedTypes = ['.csv', '.xls', '.xlsx'];
        const fileName = file.name.toLowerCase();
        
        return allowedTypes.some(ext => fileName.endsWith(ext));
    }

    processFile(file) {
        if (!this.isValidFileType(file)) {
            alert('Недопустимый тип файла. Разрешены только .csv, .xls, .xlsx');
            return;
        }

        // Обновляем информацию о файле
        this.displayFileInfo(file);

        // Здесь можно добавить логику для обработки файла
        this.uploadFile(file);
    }

    displayFileInfo(file) {
        const fileSize = this.formatFileSize(file.size);
        
        this.fileInfo.innerHTML = `
            <div class="file-name">📄 ${file.name}</div>
            <div class="file-size">Размер: ${fileSize}</div>
        `;
        this.fileInfo.style.display = 'block';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    uploadFile(file) {
        // Здесь реализуйте логику загрузки файла на сервер
        console.log('Загружаем файл:', file.name);
        getFileFromButton()
			if ( innFile != null) {
					const api = getApiKey
					// дальше можно работать с api и инн
			}
        // Пример использования FormData для отправки на сервер
        const formData = new FormData();
        formData.append('file', file);
        fetch('/upload', {
         method: 'POST',
         body: formData
          })
          .then(response => response.json())
          .then(data => {
            alert('Результат обработки: ' + data.message);
          })
          .catch(error => {
            alert('Ошибка при загрузке файла');
          });
        }




	getApiKey() {
 			const apiInput = this.apiInput

   		if (apiInput && apiInput.value.trim() !== '') {
     		return apiInput.value.trim(); // Возвращает введенный API ключ
   		} else {
     		return null; // Возвращает null если поле пустое
 			}
	}
    }


// Инициализация после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    new FileUploader();
});