interface UploadedFile {
    name: string;
    size: number;
    type: string;
}

class FileUploader {
    private fileInput: HTMLInputElement;
    private uploadArea: HTMLDivElement;
    private fileButton: HTMLButtonElement;
    private fileInfo: HTMLDivElement;
    private overlay: HTMLDivElement;
    private container: HTMLDivElement;

    constructor() {
        this.fileInput = document.getElementById('fileInput') as HTMLInputElement;
        this.uploadArea = document.getElementById('uploadArea') as HTMLDivElement;
        this.fileButton = document.getElementById('fileButton') as HTMLButtonElement;
        this.fileInfo = document.getElementById('fileInfo') as HTMLDivElement;
        this.overlay = document.getElementById('overlay') as HTMLDivElement;
        this.container = document.querySelector('.container') as HTMLDivElement;

        this.initializeEventListeners();
    }

    private initializeEventListeners(): void {
        // Клик по кнопке "Выбрать файл"
        this.fileButton.addEventListener('click', (e: Event) => {
            e.stopPropagation();
            this.fileInput.click();
        });

        // Клик по области загрузки
        this.uploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });

        // Изменение выбора файла через input
        this.fileInput.addEventListener('change', (e: Event) => {
            const target = e.target as HTMLInputElement;
            if (target.files && target.files.length > 0) {
                this.handleFileUpload(target.files[0]);
            }
        });

        // Drag and drop события
        this.uploadArea.addEventListener('dragover', (e: DragEvent) => {
            e.preventDefault();
            this.setDragState(true);
        });

        this.uploadArea.addEventListener('dragenter', (e: DragEvent) => {
            e.preventDefault();
            this.setDragState(true);
        });

        this.uploadArea.addEventListener('dragleave', (e: DragEvent) => {
            e.preventDefault();
            // Проверяем, что мы действительно вышли из области загрузки
            if (!this.uploadArea.contains(e.relatedTarget as Node)) {
                this.setDragState(false);
            }
        });

        this.uploadArea.addEventListener('drop', (e: DragEvent) => {
            e.preventDefault();
            this.setDragState(false);
            
            if (e.dataTransfer && e.dataTransfer.files.length > 0) {
                this.handleFileUpload(e.dataTransfer.files[0]);
            }
        });

        // Отслеживаем выход за пределы всей страницы
        document.addEventListener('dragleave', (e: DragEvent) => {
            e.preventDefault();
            if (e.clientX <= 0 || e.clientY <= 0 || 
                e.clientX >= window.innerWidth || 
                e.clientY >= window.innerHeight) {
                this.setDragState(false);
            }
        });

        document.addEventListener('dragend', () => {
            this.setDragState(false);
        });
    }

    private setDragState(isDragging: boolean): void {
        if (isDragging) {
            this.uploadArea.classList.add('drag-over');
            this.overlay.classList.add('active');
            document.body.classList.add('drag-active');
        } else {
            this.uploadArea.classList.remove('drag-over');
            this.overlay.classList.remove('active');
            document.body.classList.remove('drag-active');
        }
    }

    private handleFileUpload(file: File): void {
        // Проверка формата файла
        const allowedExtensions = ['.csv', '.xls', '.xlsx'];
        const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
        
        if (!allowedExtensions.includes(fileExtension)) {
            this.showFileInfo(
                `Ошибка: Неподдерживаемый формат файла. Разрешены: ${allowedExtensions.join(', ')}`,
                false
            );
            return;
        }

        // Проверка размера файла (максимум 50MB)
        const maxSize = 50 * 1024 * 1024; // 50MB в байтах
        if (file.size > maxSize) {
            this.showFileInfo(
                'Ошибка: Файл слишком большой. Максимальный размер: 50MB',
                false
            );
            return;
        }

        // Файл прошел валидацию
        const uploadedFile: UploadedFile = {
            name: file.name,
            size: file.size,
            type: file.type
        };

        this.showFileInfo(uploadedFile, true);
        this.processFile(file);
    }

    private showFileInfo(data: UploadedFile | string, success: boolean): void {
        this.fileInfo.innerHTML = '';

        if (success && typeof data !== 'string') {
            const file = data as UploadedFile;
            this.fileInfo.innerHTML = `
                <div class="file-name">✓ Файл успешно загружен: ${file.name}</div>
                <div class="file-size">Размер: ${this.formatFileSize(file.size)}</div>
            `;
            this.fileInfo.className = 'file-info show success';
        } else {
            this.fileInfo.innerHTML = `
                <div class="file-name">${data}</div>
            `;
            this.fileInfo.className = 'file-info show error';
        }
    }

    private formatFileSize(bytes: number): string {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    private processFile(file: File): void {
        // Здесь можно добавить логику обработки файла
        console.log('Обработка файла:', {
            name: file.name,
            size: this.formatFileSize(file.size),
            type: file.type,
            lastModified: new Date(file.lastModified).toLocaleString('ru-RU')
        });

        // Имитация обработки файла
        setTimeout(() => {
            console.log('Файл обработан:', file.name);
        }, 1000);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new FileUploader();
});