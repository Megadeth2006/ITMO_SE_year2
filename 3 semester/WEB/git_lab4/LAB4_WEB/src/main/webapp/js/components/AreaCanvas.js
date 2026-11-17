export default {
    props: ['points', 'currentR'],
    
    data() {
        return {
            canvas: null,
            ctx: null,
            width: 400,
            height: 400,
            centerX: 200,
            centerY: 200,
            scale: 50,
            drawScheduled: false
        };
    },
    
    mounted() {
        this.canvas = this.$refs.canvas;
        this.ctx = this.canvas.getContext('2d');
        this.scheduleDraw();

        window.addEventListener('resize', this.handleResize);
    },
    
    beforeUnmount() {
        window.removeEventListener('resize', this.handleResize);
    },
    
    watch: {
        points: {
            handler() {
                this.scheduleDraw();
            },
            deep: true
        },
        currentR() {
            this.scheduleDraw();
        }
    },
    
    methods: {

        scheduleDraw() {
            if (this.drawScheduled) return;
            
            this.drawScheduled = true;
            requestAnimationFrame(() => {
                this.draw();
                this.drawScheduled = false;
            });
        },
        
        handleResize() {

            const container = this.canvas.parentElement;
            const size = Math.min(container.clientWidth - 20, 500);
            this.width = size;
            this.height = size;
            this.centerX = size / 2;
            this.centerY = size / 2;
            this.scale = size / 8;
            this.scheduleDraw();
        },
        
        draw() {
            if (!this.ctx) return;
            
            const ctx = this.ctx;
            const { width, height, centerX, centerY } = this;
            

            ctx.clearRect(0, 0, width, height);
            

            if (this.currentR && this.currentR !== 0) {
                this.drawArea();
            }

            this.drawAxes();

            this.drawPoints();
        },
        
        drawArea() {
            const ctx = this.ctx;
            const { centerX, centerY, scale } = this;
            const r = Math.abs(this.currentR);
            const rPixels = r * scale;
            const isNegative = this.currentR < 0;
            
            ctx.fillStyle = 'rgba(135, 206, 250, 0.5)';
            ctx.strokeStyle = 'rgba(135, 206, 250, 0.8)';
            ctx.lineWidth = 2;
            
            ctx.beginPath();
            
            if (!isNegative) {
               // круг
                ctx.arc(centerX, centerY, rPixels / 2, -Math.PI / 2, 0, false);
                ctx.lineTo(centerX, centerY);
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
                
                // треугольник
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(centerX + rPixels, centerY);
                ctx.lineTo(centerX, centerY + rPixels / 2);
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
                
               // квадрат
                ctx.fillRect(centerX - rPixels, centerY, rPixels, rPixels);
                ctx.strokeRect(centerX - rPixels, centerY, rPixels, rPixels);
            } else {
                // для отрицательного r делаем поддержку
                ctx.arc(centerX, centerY, rPixels / 2, Math.PI / 2, Math.PI, false);
                ctx.lineTo(centerX, centerY);
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
                
                // треугольник
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(centerX - rPixels, centerY);
                ctx.lineTo(centerX, centerY - rPixels / 2);
                ctx.closePath();
                ctx.fill();
                ctx.stroke();
                
                // квадрат
                ctx.fillRect(centerX, centerY - rPixels, rPixels, rPixels);
                ctx.strokeRect(centerX, centerY - rPixels, rPixels, rPixels);
            }
        },
        
        drawAxes() {
            const ctx = this.ctx;
            const { width, height, centerX, centerY, scale } = this;
            
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 2;
            ctx.fillStyle = '#000';
            ctx.font = '12px Arial';

            // x оси
            ctx.beginPath();
            ctx.moveTo(0, centerY);
            ctx.lineTo(width, centerY);
            ctx.stroke();
            
            // X стрелка
            ctx.beginPath();
            ctx.moveTo(width - 10, centerY - 5);
            ctx.lineTo(width, centerY);
            ctx.lineTo(width - 10, centerY + 5);
            ctx.stroke();
            
            // y оси
            ctx.beginPath();
            ctx.moveTo(centerX, height);
            ctx.lineTo(centerX, 0);
            ctx.stroke();
            
            // Y стрелка
            ctx.beginPath();
            ctx.moveTo(centerX - 5, 10);
            ctx.lineTo(centerX, 0);
            ctx.lineTo(centerX + 5, 10);
            ctx.stroke();

            const tickValues = [-5, -4, -3, -2, -1, 1, 2, 3];
            tickValues.forEach(val => {
                const x = centerX + val * scale;
                const y = centerY - val * scale;
                

                if (val >= -5 && val <= 3) {
                    ctx.beginPath();
                    ctx.moveTo(x, centerY - 5);
                    ctx.lineTo(x, centerY + 5);
                    ctx.stroke();
                }

                if (val >= -3 && val <= 3) {
                    ctx.beginPath();
                    ctx.moveTo(centerX - 5, y);
                    ctx.lineTo(centerX + 5, y);
                    ctx.stroke();
                }
            });
        },
        
        drawPoints() {
            if (!this.points || this.points.length === 0) return;
            
            const ctx = this.ctx;
            const { centerX, centerY, scale } = this;
            
            this.points.forEach(point => {
                const x = centerX + parseFloat(point.x) * scale;
                const y = centerY - parseFloat(point.y) * scale;
                
                ctx.fillStyle = point.inArea ? 'green' : 'red';
                ctx.beginPath();
                ctx.arc(x, y, 4, 0, Math.PI * 2);
                ctx.fill();
            });
        },
        
        handleClick(event) {
            event.preventDefault();
            event.stopPropagation();
            
            const rect = this.canvas.getBoundingClientRect();
            const clickX = event.clientX - rect.left;
            const clickY = event.clientY - rect.top;
            
            // Convert to coordinates
            let x = (clickX - this.centerX) / this.scale;
            let y = (this.centerY - clickY) / this.scale;
            
            // Clamp coordinates to allowed ranges: X: [-5, 3], Y: [-3, 3]
            x = Math.max(-5, Math.min(3, x));
            y = Math.max(-3, Math.min(3, y));
            
            // Round to 10 decimal places to avoid precision issues
            x = Math.round(x * 10000000000) / 10000000000;
            y = Math.round(y * 10000000000) / 10000000000;
            
            this.$emit('click', x, y);
        }
    },
    
    template: `
        <div class="canvas-container">
            <canvas 
                ref="canvas" 
                :width="width" 
                :height="height"
                @click="handleClick"
                class="area-canvas"
            ></canvas>
        </div>
    `
};
