export default {
    props: ['api'],
    
    data() {
        return {
            isOpen: false,
            themePreset: 'light',
            colors: {
                backgroundColor: '#667eea',
                secondaryColor: '#6c757d',
                textColor: '#333333',
                fieldBackground: '#ffffff',
                borderColor: '#dddddd'
            },
            presets: {
                light: {
                    backgroundColor: '#667eea',
                    secondaryColor: '#6c757d',
                    textColor: '#333333',
                    fieldBackground: '#ffffff',
                    borderColor: '#dddddd'
                },
                dark: {
                    backgroundColor: '#1a1a2e',
                    secondaryColor: '#0f3460',
                    textColor: '#eaeaea',
                    fieldBackground: '#16213e',
                    borderColor: '#0f3460'
                }
            },
            loading: false
        };
    },
    
    async mounted() {
        // Пытаемся загрузить настройки, но не падаем если не авторизован
        try {
            await this.loadThemeSettings();
        } catch (error) {
            // Если не авторизован, используем дефолтную тему
            this.applyPreset('light');
            this.applyTheme();
        }
    },
    
    methods: {
        async loadThemeSettings() {
            try {
                const settings = await this.api.getThemeSettings();
                if (settings) {
                    this.themePreset = settings.themePreset || 'light';
                    if (settings.themePreset === 'custom') {
                        this.colors = {
                            backgroundColor: settings.backgroundColor || this.colors.backgroundColor,
                            secondaryColor: settings.secondaryColor || this.colors.secondaryColor,
                            textColor: settings.textColor || this.colors.textColor,
                            fieldBackground: settings.cardBackground || this.colors.fieldBackground,
                            borderColor: settings.borderColor || this.colors.borderColor
                        };
                    } else {
                        this.applyPreset(this.themePreset);
                    }
                    this.applyTheme();
                }
            } catch (error) {
                console.error('Error loading theme settings:', error);
            }
        },
        
        async saveThemeSettings() {
            this.loading = true;
            try {
                const settings = {
                    themePreset: this.themePreset,
                    backgroundColor: this.colors.backgroundColor,
                    primaryColor: this.colors.backgroundColor, // Используем фон как primary для совместимости
                    secondaryColor: this.colors.secondaryColor,
                    textColor: this.colors.textColor,
                    cardBackground: this.colors.fieldBackground,
                    borderColor: this.colors.borderColor
                };
                
                // Пытаемся сохранить на сервере (только если авторизован)
                try {
                    await this.api.saveThemeSettings(settings);
                } catch (error) {
                    // Если не авторизован, просто применяем тему локально
                    console.log('Theme applied locally (not authenticated)');
                }
                
                this.applyTheme();
                this.$emit('theme-changed', settings);
            } catch (error) {
                console.error('Error saving theme settings:', error);
            } finally {
                this.loading = false;
            }
        },
        
        applyPreset(preset) {
            if (this.presets[preset]) {
                this.colors = { ...this.presets[preset] };
                this.themePreset = preset;
            }
        },
        
        handlePresetChange(preset) {
            this.applyPreset(preset);
            this.saveThemeSettings();
        },
        
        handleColorChange() {
            this.themePreset = 'custom';
        },
        
        applyTheme() {
            const root = document.documentElement;
            root.style.setProperty('--bg-gradient-start', this.colors.backgroundColor);
            root.style.setProperty('--bg-gradient-end', this.darkenColor(this.colors.backgroundColor, 15));
            // Primary цвет используем для кнопок и акцентов, но не для текста
            root.style.setProperty('--primary-color', this.colors.backgroundColor);
            root.style.setProperty('--primary-hover', this.darkenColor(this.colors.backgroundColor, 10));
            root.style.setProperty('--secondary-color', this.colors.secondaryColor);
            root.style.setProperty('--secondary-hover', this.darkenColor(this.colors.secondaryColor, 10));
            // Текст меняется только через textColor
            root.style.setProperty('--text-color', this.colors.textColor);
            root.style.setProperty('--text-secondary', this.lightenColor(this.colors.textColor, 20));
            // Поля (input) - только для полей ввода
            root.style.setProperty('--field-bg', this.colors.fieldBackground);
            // Карточки остаются белыми (не меняются)
            root.style.setProperty('--card-bg', '#ffffff');
            root.style.setProperty('--border-color', this.colors.borderColor);
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
        },
        
        toggleSettings() {
            this.isOpen = !this.isOpen;
        },
        
        closeSettings() {
            this.isOpen = false;
        }
    },
    
    watch: {
        colors: {
            handler() {
                if (this.themePreset !== 'custom') {
                    return;
                }
                this.applyTheme();
            },
            deep: true
        },
        themePreset() {
            this.applyTheme();
        }
    },
    
    template: `
        <div class="theme-settings">
            <button 
                @click="toggleSettings" 
                class="btn btn-secondary theme-toggle-btn"
                title="Настройки темы"
            >
                🎨
            </button>
            
            <div v-if="isOpen" class="theme-settings-panel">
                <div class="theme-settings-header">
                    <h3>Настройки темы</h3>
                    <button @click="closeSettings" class="close-btn">&times;</button>
                </div>
                
                <div class="theme-settings-content">
                    <div class="preset-section">
                        <h4>Пресеты</h4>
                        <div class="preset-buttons">
                            <button 
                                @click="handlePresetChange('light')"
                                :class="['preset-btn', { active: themePreset === 'light' }]"
                            >
                                ☀️ Светлая
                            </button>
                            <button 
                                @click="handlePresetChange('dark')"
                                :class="['preset-btn', { active: themePreset === 'dark' }]"
                            >
                                🌙 Темная
                            </button>
                        </div>
                    </div>
                    
                    <div class="custom-colors-section">
                        <h4>Настройка цветов</h4>
                        <div class="color-inputs">
                            <div class="color-input-group">
                                <label>Фон</label>
                                <input 
                                    type="color" 
                                    v-model="colors.backgroundColor"
                                    @change="handleColorChange"
                                />
                            </div>
                            <div class="color-input-group">
                                <label>Вторичный</label>
                                <input 
                                    type="color" 
                                    v-model="colors.secondaryColor"
                                    @change="handleColorChange"
                                />
                            </div>
                            <div class="color-input-group">
                                <label>Текст</label>
                                <input 
                                    type="color" 
                                    v-model="colors.textColor"
                                    @change="handleColorChange"
                                />
                            </div>
                            <div class="color-input-group">
                                <label>Поля</label>
                                <input 
                                    type="color" 
                                    v-model="colors.fieldBackground"
                                    @change="handleColorChange"
                                />
                            </div>
                            <div class="color-input-group">
                                <label>Границы</label>
                                <input 
                                    type="color" 
                                    v-model="colors.borderColor"
                                    @change="handleColorChange"
                                />
                            </div>
                        </div>
                    </div>
                    
                    <div class="theme-settings-actions">
                        <button 
                            @click="saveThemeSettings" 
                            class="btn btn-primary"
                            :disabled="loading"
                        >
                            {{ loading ? 'Сохранение...' : 'Сохранить' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `
};

