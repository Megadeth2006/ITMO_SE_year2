export default {
    props: ['message', 'type'], // type: 'error', 'success', 'warning', 'info'
    
    data() {
        return {
            visible: false
        };
    },
    
    watch: {
        message(newVal) {
            if (newVal) {
                this.visible = true;
            }
        }
    },
    
    mounted() {
        if (this.message) {
            this.visible = true;
        }
    },
    
    methods: {
        close() {
            this.visible = false;
            this.$emit('close');
        },
        
        getIcon() {
            switch(this.type) {
                case 'success': return '✓';
                case 'error': return '✕';
                case 'warning': return '⚠';
                case 'info': return 'ℹ';
                default: return '';
            }
        },
        
        getClass() {
            return `toast toast-${this.type || 'info'}`;
        }
    },
    
    template: `
        <transition name="toast-fade">
            <div v-if="visible && message" :class="getClass()">
                <span class="toast-icon">{{ getIcon() }}</span>
                <span class="toast-message">{{ message }}</span>
                <button @click="close" class="toast-close">&times;</button>
            </div>
        </transition>
    `
};

