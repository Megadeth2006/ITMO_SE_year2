export default {
    props: ['points'],
    
    methods: {
        formatNumber(value) {
            return parseFloat(value).toFixed(4);
        },
        
        formatDate(dateString) {
            const date = new Date(dateString);
        },
        
        getResultText(inArea) {
            return inArea ? 'Попадание' : 'Промах';
        },
        
        getResultClass(inArea) {
            return inArea ? 'result-hit' : 'result-miss';
        }
    },
    
    template: `
        <div class="points-table-container">
            <div v-if="!points || points.length === 0" class="empty-table">
                <p>Нет результатов проверки. Добавьте точку через форму или кликните по графику.</p>
            </div>
            
            <table v-else class="points-table">
                <thead>
                    <tr>
                        <th>№</th>
                        <th>X</th>
                        <th>Y</th>
                        <th>R</th>
                        <th>Результат</th>
                        <th>Время</th>
                    </tr>
                </thead>
                <tbody>
                    <tr 
                        v-for="(point, index) in points" 
                        :key="point.id"
                        :class="getResultClass(point.inArea)"
                    >
                        <td>{{ index + 1 }}</td>
                        <td>{{ formatNumber(point.x) }}</td>
                        <td>{{ formatNumber(point.y) }}</td>
                        <td>{{ formatNumber(point.r) }}</td>
                        <td class="result-cell">
                            <span :class="'badge ' + (point.inArea ? 'badge-success' : 'badge-danger')">
                                {{ getResultText(point.inArea) }}
                            </span>
                        </td>
                        <td>{{ formatDate(point.createdAt) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    `
};
