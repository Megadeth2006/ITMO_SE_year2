export default {
    props: ['api'],
    
    data() {
        return {
            isRegistering: false,
            username: '',
            password: '',
            error: '',
            loading: false
        };
    },
    
    mounted() {
        this.resetToLightTheme(); // сбрасываем на светлую
    },
    
    methods: {
        resetToLightTheme() {
            const root = document.documentElement;
            // Светлая тема по умолчанию
            root.style.setProperty('--bg-gradient-start', '#667eea');
            root.style.setProperty('--bg-gradient-end', '#764ba2');
            root.style.setProperty('--primary-color', '#667eea');
            root.style.setProperty('--primary-hover', '#5568d3');
            root.style.setProperty('--secondary-color', '#6c757d');
            root.style.setProperty('--secondary-hover', '#5a6268');
            root.style.setProperty('--text-color', '#333333');
            root.style.setProperty('--text-secondary', '#666666');
            root.style.setProperty('--card-bg', '#ffffff');
            root.style.setProperty('--field-bg', '#ffffff');
            root.style.setProperty('--area-bg', '#ffffff');
            root.style.setProperty('--border-color', '#dddddd');
        },
        
        toggleMode() {
            this.isRegistering = !this.isRegistering;
            this.error = '';
            this.username = '';
            this.password = '';
        },
        
        async handleSubmit() {
            this.error = '';
            
         
            if (!this.username.trim()) {
                this.error = 'Введите имя пользователя';
                return;
            }
            
            if (this.password.length < 4) {
                this.error = 'Пароль должен содержать минимум 4 символа';
                return;
            }
            
            this.loading = true;
            
            try {
                const response = this.isRegistering 
                    ? await this.api.register(this.username, this.password)
                    : await this.api.login(this.username, this.password);
                
                if (response.success) {
                    this.$emit('login', response.username);
                } else {
                    this.error = response.message || 'Ошибка авторизации';
                }
            } catch (error) {
                this.error = 'Ошибка подключения к серверу';
            } finally {
                this.loading = false;
            }
        }
    },
    
    template: `
        <div class="login-container">
            <div class="login-card">
                <header class="app-header">
                    <h1>Лабораторная работа №4</h1>
                    <div class="student-info">
                        <p><strong>ФИО:</strong> Григорьев Даниил Александрович</p>
                        <p><strong>Группа:</strong> P3216</p>
                        <p><strong>Вариант:</strong> 3216024</p>
                    </div>
                </header>
                
                <div class="login-form-container">
                    <h2>{{ isRegistering ? 'Регистрация' : 'Вход' }}</h2>
                    
                    <form @submit.prevent="handleSubmit" class="login-form">
                        <div class="form-group">
                            <label for="username">Имя пользователя:</label>
                            <input 
                                type="text" 
                                id="username" 
                                v-model="username"
                                :disabled="loading"
                                required
                                maxlength="50"
                            />
                        </div>
                        
                        <div class="form-group">
                            <label for="password">Пароль:</label>
                            <input 
                                type="password" 
                                id="password" 
                                v-model="password"
                                :disabled="loading"
                                required
                                minlength="4"
                            />
                        </div>
                        
                        <div v-if="error" class="error-message">
                            {{ error }}
                        </div>
                        
                        <button 
                            type="submit" 
                            class="btn btn-primary"
                            :disabled="loading"
                        >
                            {{ loading ? 'Загрузка...' : (isRegistering ? 'Зарегистрироваться' : 'Войти') }}
                        </button>
                    </form>
                    
                    <div class="toggle-mode">
                        <button 
                            @click="toggleMode" 
                            class="btn btn-link"
                            :disabled="loading"
                        >
                            {{ isRegistering ? 'Уже есть аккаунт? Войти' : 'Нет аккаунта? Зарегистрироваться' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `
};
