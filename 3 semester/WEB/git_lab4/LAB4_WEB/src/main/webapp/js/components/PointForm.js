export default {
    data() {
        return {
            x: '',
            y: '',
            r: '',
            errors: {
                x: '',
                y: '',
                r: ''
            }
        };
    },
    
    methods: {
        normalizeNumber(value) {
            // Replace comma with dot
            return value.replace(',', '.');
        },
        
        validateX(value) {
            const normalized = this.normalizeNumber(value);
            const num = parseFloat(normalized);
            
            if (isNaN(num)) {
                return 'X должен быть числом';
            }
            if (num < -5 || num > 3) {
                return 'X должен быть в диапазоне [-5, 3]';
            }
            return '';
        },
        
        validateY(value) {
            const normalized = this.normalizeNumber(value);
            const num = parseFloat(normalized);
            
            if (isNaN(num)) {
                return 'Y должен быть числом';
            }
            if (num < -3 || num > 3) {
                return 'Y должен быть в диапазоне [-3, 3]';
            }
            return '';
        },
        
        validateR(value) {
            const normalized = this.normalizeNumber(value);
            const num = parseFloat(normalized);
            
            if (isNaN(num)) {
                return 'R должен быть числом';
            }
            if (num < -5 || num > 3) {
                return 'R должен быть в диапазоне [-5, 3]';
            }
            return '';
        },
        
        handleXInput() {
            this.errors.x = this.validateX(this.x);
        },
        
        handleYInput() {
            this.errors.y = this.validateY(this.y);
        },
        
        handleRInput() {
            this.errors.r = this.validateR(this.r);
            
            // Emit R change for canvas update
            if (!this.errors.r && this.r) {
                const normalized = this.normalizeNumber(this.r);
                this.$emit('rChange', parseFloat(normalized));
            }
        },
        
        handleSubmit() {
            // Validate all fields
            this.errors.x = this.validateX(this.x);
            this.errors.y = this.validateY(this.y);
            this.errors.r = this.validateR(this.r);
            
            // Check if there are any errors
            if (this.errors.x || this.errors.y || this.errors.r) {
                return;
            }
            
            // Normalize and parse values
            const xValue = parseFloat(this.normalizeNumber(this.x));
            const yValue = parseFloat(this.normalizeNumber(this.y));
            const rValue = parseFloat(this.normalizeNumber(this.r));
            
            // Emit submit event
            this.$emit('submit', xValue, yValue, rValue);
            
            // Don't clear R to keep it for canvas clicks
            this.x = '';
            this.y = '';
            this.errors.x = '';
            this.errors.y = '';
        }
    },
    
    template: `
        <form @submit.prevent="handleSubmit" class="point-form">
            <div class="form-group">
                <label for="x-input">
                    X <span class="range-hint">[-5, 3]</span>
                </label>
                <input 
                    type="text" 
                    id="x-input"
                    v-model="x"
                    @input="handleXInput"
                    placeholder="Введите X"
                    class="form-control"
                    :class="{ 'error': errors.x }"
                />
                <span v-if="errors.x" class="error-text">{{ errors.x }}</span>
            </div>
            
            <div class="form-group">
                <label for="y-input">
                    Y <span class="range-hint">[-3, 3]</span>
                </label>
                <input 
                    type="text" 
                    id="y-input"
                    v-model="y"
                    @input="handleYInput"
                    placeholder="Введите Y"
                    class="form-control"
                    :class="{ 'error': errors.y }"
                />
                <span v-if="errors.y" class="error-text">{{ errors.y }}</span>
            </div>
            
            <div class="form-group">
                <label for="r-input">
                    R <span class="range-hint">[-5, 3]</span>
                </label>
                <input 
                    type="text" 
                    id="r-input"
                    v-model="r"
                    @input="handleRInput"
                    placeholder="Введите R"
                    class="form-control"
                    :class="{ 'error': errors.r }"
                />
                <span v-if="errors.r" class="error-text">{{ errors.r }}</span>
            </div>
            
            <button 
                type="submit" 
                class="btn btn-secondary"
            >
                Проверить точку
            </button>
            

        </form>
    `
};
