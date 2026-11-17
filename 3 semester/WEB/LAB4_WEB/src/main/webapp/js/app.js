const { createApp } = Vue;


import LoginPage from './components/LoginPage.js';
import MainPage from './components/MainPage.js';

const api = {
    baseURL: '/LAB4_WEB/api',
    
    request: async function(url, options = {}) {
        const response = await fetch(`${api.baseURL}${url}`, {
            ...options,
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        const data = await response.json();
        

        if (response.status === 401 && !url.startsWith('/auth/')) {
            throw new Error('UNAUTHORIZED');
        }

        return data;
    },
    
    checkAuth: async function() {
        try {
            return await api.request('/auth/check');
        } catch (error) {
            return { success: false };
        }
    },
    
    login: async function(username, password) {
        return api.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    },
    
    register: async function(username, password) {
        return api.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
    },
    
    logout: async function() {
        return api.request('/auth/logout', { method: 'POST' });
    },
    
    getPoints: async function() {
        return api.request('/points');
    },
    
    addPoint: async function(x, y, r) {
        return api.request('/points', {
            method: 'POST',
            body: JSON.stringify({ 
                x: String(x), 
                y: String(y), 
                r: String(r) 
            })
        });
    },
    
    clearPoints: async function() {
        return api.request('/points', { method: 'DELETE' });
    },
    
    getThemeSettings: async function() {
        return api.request('/theme');
    },
    
    saveThemeSettings: async function(settings) {
        return api.request('/theme', {
            method: 'POST',
            body: JSON.stringify(settings)
        });
    }
};


const app = createApp({
    data() {
        return {
            currentPage: 'login',
            isAuthenticated: false,
            username: null,
            checkingAuth: true
        };
    },
    
    async mounted() {

        this.resetToLightTheme();
        
        await this.checkAuth();
        this.checkingAuth = false;
        

        window.addEventListener('storage', this.handleStorageChange);
        

        setInterval(() => this.checkAuth(), 5000);
    },
    
    computed: {
        api() {
            return api;
        }
    },
    
    methods: {
        async checkAuth() {
            try {
                const response = await api.checkAuth();
                if (response.success) {
                    this.isAuthenticated = true;
                    this.username = response.username;
                    if (this.currentPage === 'login') {
                        this.currentPage = 'main';
                    }
                    localStorage.setItem('authenticated', 'true');
                } else {
                    this.handleLogout(false);
                }
            } catch (error) {
                this.handleLogout(false);
            }
        },
        
        handleLogin(username) {
            this.isAuthenticated = true;
            this.username = username;
            this.currentPage = 'main';
            localStorage.setItem('authenticated', 'true');
            

            localStorage.setItem('authEvent', Date.now().toString());
        },
        
        async handleLogout(manual = true) {
            if (manual) {
                try {
                    await api.logout();
                } catch (error) {
                    console.error('Logout error:', error);
                }
            }
            
            this.isAuthenticated = false;
            this.username = null;
            this.currentPage = 'login';
            localStorage.removeItem('authenticated');
            

            this.resetToLightTheme();
            
            if (manual) {
                localStorage.setItem('logoutEvent', Date.now().toString());
            }
        },
        
        resetToLightTheme() {
            const root = document.documentElement;

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
        
        handleStorageChange(event) {
            if (event.key === 'logoutEvent') {
                this.handleLogout(false);
            } else if (event.key === 'authEvent') {
                this.checkAuth();
            }
        }
    },
    
    watch: {
        currentPage(newPage) {

            if (newPage === 'login') {
                this.resetToLightTheme();
            }
        }
    },
    
    components: {
        LoginPage,
        MainPage
    },
    
    template: `
        <div v-if="checkingAuth" class="loading">
            <p>Загрузка...</p>
        </div>
        <LoginPage 
            v-else-if="currentPage === 'login'" 
            @login="handleLogin"
            :api="api"
        />
        <MainPage 
            v-else-if="currentPage === 'main'" 
            :username="username"
            @logout="handleLogout"
            :api="api"
        />
    `
});

app.mount('#app');

