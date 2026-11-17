import AreaCanvas from './AreaCanvas.js';
import PointForm from './PointForm.js';
import PointsTable from './PointsTable.js';
import Toast from './Toast.js';
import ThemeSettings from './ThemeSettings.js';

export default {
    props: ['username', 'api'],
    
    components: {
        AreaCanvas,
        PointForm,
        PointsTable,
        Toast,
        ThemeSettings
    },
    
    data() {
        return {
            points: [],
            currentR: null,
            loading: false,
            toastMessage: '',
            toastType: 'info'
        };
    },
    
    computed: {
        // Пересчитываем попадание точек для текущего радиуса
        recalculatedPoints() {
            if (!this.currentR) {
                return this.points;
            }
            
            return this.points.map(point => ({
                ...point,
                inArea: this.checkArea(
                    parseFloat(point.x),
                    parseFloat(point.y),
                    this.currentR
                )
            }));
        }
    },
    
    async mounted() {
        await this.loadPoints();
        // Загружаем настройки темы при монтировании
        await this.loadThemeSettings();
    },
    
    methods: {
        showToast(message, type = 'info') {
            this.toastMessage = message;
            this.toastType = type;
            
            // Автоматически скрыть через 3 секунды
            setTimeout(() => {
                this.toastMessage = '';
            }, 3000);
        },
        
        closeToast() {
            this.toastMessage = '';
        },
        
        // Проверка попадания точки в область (та же логика что на сервере)
        checkArea(x, y, r) {
            // Обработка отрицательного радиуса (зеркальное отражение)
            const effectiveR = Math.abs(r);
            const effectiveX = r >= 0 ? x : -x;
            const effectiveY = r >= 0 ? y : -y;
            
            const r2 = effectiveR / 2;
            
            // Четверть круга в I четверти (x >= 0, y >= 0) с радиусом R/2
            if (effectiveX >= 0 && effectiveY >= 0) {
                const distanceSquared = effectiveX * effectiveX + effectiveY * effectiveY;
                return distanceSquared <= r2 * r2;
            }
            
            // Треугольник в IV четверти (x >= 0, y <= 0)
            // Вершины: (0,0), (R,0), (0,-R/2)
            // Линия: x - 2y <= R
            if (effectiveX >= 0 && effectiveY <= 0) {
                return effectiveX - 2 * effectiveY <= effectiveR;
            }
            
            // Квадрат в III четверти (x <= 0, y <= 0)
            // -R <= x <= 0 and -R <= y <= 0
            if (effectiveX <= 0 && effectiveY <= 0) {
                return effectiveX >= -effectiveR && effectiveY >= -effectiveR;
            }
            
            return false;
        },
        
        async loadPoints() {
            this.loading = true;
            try {
                const response = await this.api.getPoints();
                this.points = Array.isArray(response) ? response : [];
            } catch (error) {
                if (error.message === 'UNAUTHORIZED') {
                    this.$emit('logout');
                } else {
                    this.showToast('Ошибка загрузки точек', 'error');
                }
            } finally {
                this.loading = false;
            }
        },
        
        async handleAddPoint(x, y, r) {
            // Защита от случайного вызова с SubmitEvent вместо координат
            if (typeof x !== 'number' || typeof y !== 'number' || typeof r !== 'number') {
                console.warn('handleAddPoint called with invalid arguments:', x, y, r);
                return;
            }
            
            try {
                const response = await this.api.addPoint(x, y, r);
                
                // Проверяем что это ошибка
                if (response.success === false) {
                    this.showToast(response.message || 'Ошибка добавления точки', 'error');
                    return;
                }
                
                // Успешный ответ - добавляем точку в список
                this.points.unshift(response);
            } catch (error) {
                if (error.message === 'UNAUTHORIZED') {
                    this.$emit('logout');
                } else {
                    this.showToast('Ошибка добавления точки', 'error');
                }
            }
        },
        
        async handleCanvasClick(x, y) {
            if (!this.currentR) {
                this.showToast('Ошибка: необходимо выбрать радиус R', 'error');
                return;
            }
            await this.handleAddPoint(x, y, this.currentR);
        },
        
        async handleClearPoints() {
            if (!confirm('Вы уверены, что хотите удалить все свои точки?')) {
                return;
            }
            
            try {
                await this.api.clearPoints();
                // Перезагружаем все точки, чтобы показать точки других пользователей
                await this.loadPoints();
                this.showToast('Ваши точки удалены', 'success');
            } catch (error) {
                if (error.message === 'UNAUTHORIZED') {
                    this.$emit('logout');
                } else {
                    this.showToast('Ошибка удаления точек', 'error');
                }
            }
        },
        
        handleRChange(r) {
            this.currentR = r;
        },
        
        handleLogout() {
            this.$emit('logout', true);
        },
        
        async loadThemeSettings() {
            try {
                const settings = await this.api.getThemeSettings();
                if (settings) {
                    this.applyThemeFromSettings(settings);
                }
            } catch (error) {
                // Игнорируем ошибки при загрузке темы
            }
        },
        
        applyThemeFromSettings(settings) {
            const root = document.documentElement;
            root.style.setProperty('--bg-gradient-start', settings.backgroundColor);
            root.style.setProperty('--bg-gradient-end', this.darkenColor(settings.backgroundColor, 15));
            // Primary цвет для кнопок и акцентов, не для текста
            root.style.setProperty('--primary-color', settings.backgroundColor);
            root.style.setProperty('--primary-hover', this.darkenColor(settings.backgroundColor, 10));
            root.style.setProperty('--secondary-color', settings.secondaryColor);
            root.style.setProperty('--secondary-hover', this.darkenColor(settings.secondaryColor, 10));
            // Текст меняется только через textColor
            root.style.setProperty('--text-color', settings.textColor);
            root.style.setProperty('--text-secondary', this.lightenColor(settings.textColor, 20));
            // Поля (input) - только для полей ввода
            root.style.setProperty('--field-bg', settings.cardBackground);
            // Карточки остаются белыми (не меняются)
            root.style.setProperty('--card-bg', '#ffffff');
            root.style.setProperty('--border-color', settings.borderColor);
        },
        
        handleThemeChanged(settings) {
            this.applyThemeFromSettings(settings);
        },
        
        darkenColor(color, percent) {
            const num = parseInt(color.replace("#", ""), 16);
            const amt = Math.round(2.55 * percent);
            const R = Math.max(0, Math.min(255, (num >> 16) - amt));
            const G = Math.max(0, Math.min(255, (num >> 8 & 0x00FF) - amt));
            const B = Math.max(0, Math.min(255, (num & 0x0000FF) - amt));
            return "#" + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1);
        },
        
        lightenColor(color, percent) {
            const num = parseInt(color.replace("#", ""), 16);
            const amt = Math.round(2.55 * percent);
            const R = Math.max(0, Math.min(255, (num >> 16) + amt));
            const G = Math.max(0, Math.min(255, (num >> 8 & 0x00FF) + amt));
            const B = Math.max(0, Math.min(255, (num & 0x0000FF) + amt));
            return "#" + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1);
        }
    },
    
    template: `
        <div class="main-container">
            <ThemeSettings :api="api" @theme-changed="handleThemeChanged" />
            
            <Toast 
                :message="toastMessage" 
                :type="toastType"
                @close="closeToast"
            />
            
            <header class="app-header">
                <div>
                    <h1>Проверка попадания точки в область</h1>
                    <div class="student-info">
                        <p><strong>ФИО:</strong> Григорьев Даниил Александрович | <strong>Группа:</strong> P3216 | <strong>Вариант:</strong> 3216024</p>
                        <p><strong>Пользователь:</strong> {{ username }}</p>
                    </div>
                </div>
                <button @click="handleLogout" class="btn btn-secondary">Выйти</button>
            </header>
            
            <div class="content-grid">
                <div class="canvas-section">
                    <h2>График</h2>
                    <AreaCanvas 
                        :points="recalculatedPoints"
                        :currentR="currentR"
                        @click="handleCanvasClick"
                    />
                </div>
                
                <div class="form-section">
                    <h2>Координаты точки</h2>
                    <PointForm 
                        @submit="handleAddPoint"
                        @rChange="handleRChange"
                    />
                </div>
            </div>
            
            <div class="table-section">
                <div class="table-header">
                    <h2>Результаты проверок</h2>
                    <button 
                        @click="handleClearPoints" 
                        class="btn btn-danger"
                        :disabled="points.length === 0"
                    >
                        Очистить таблицу
                    </button>
                </div>
                <PointsTable :points="points" />
            </div>
        </div>
    `
};
