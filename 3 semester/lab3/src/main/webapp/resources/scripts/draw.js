// =====================================================
//                 ГЛОБАЛЬНЫЕ ДАННЫЕ
// =====================================================
window.existingPoints = window.existingPoints || [];

const SCALE = 30;       // 1 единица = 30 пикселей
const CENTER = 150;     // центр графика


// =====================================================
//      1. СИНХРОНИЗАЦИЯ СЕРВЕРНЫХ ДАННЫХ (таблица)
// =====================================================
function handleRemoteCommandComplete(args) {
    if (args && args.pointsJson) {
        try {
            window.existingPoints = JSON.parse(args.pointsJson);
        } catch (e) {
            console.error("parse pointsJson failed", e);
            window.existingPoints = [];
        }
    } else {
        window.existingPoints = [];
    }

    clearPoints();
    drawAllPoints();
}


// =====================================================
//                       2. ЗВУК
// =====================================================
function playShotSound() {
    const sounds = ['shot1', 'shot2', 'shot3', 'shot4'];
    const audio = document.getElementById(sounds[Math.floor(Math.random() * 4)]);
    if (audio) {
        audio.currentTime = 0;
        audio.play().catch(err => console.warn("Не удалось проиграть звук:", err));
    }
}


// =====================================================
//                  3. ОТРИСОВКА ТОЧЕК
// =====================================================
function drawPoint(x, y, hit) {
    const svg = getSVG();
    if (!svg) return;

    const cx = CENTER + x * SCALE;
    const cy = CENTER - y * SCALE;

    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", cx);
    circle.setAttribute("cy", cy);
    circle.setAttribute("r", 4);
    circle.setAttribute("fill", hit ? "#09a53d" : "#a50909");
    circle.setAttribute("stroke", hit ? "#026d24" : "#5c0000");

    svg.appendChild(circle);
}

function drawAllPoints() {
    window.existingPoints.forEach(p =>
        drawPoint(p.x, p.y, p.inArea)
    );
}

function clearPoints() {
    const svg = getSVG();
    if (!svg) return;
    svg.querySelectorAll("circle").forEach(c => c.remove());
}


// =====================================================
//              4. СИНХРОНИЗАЦИЯ INPUT → HIDDEN
// =====================================================
function syncHiddenWithText() {
    const y = document.getElementById("yInput");
    const r = document.getElementById("rInput");

    if (y) document.getElementById("hiddenY").value = y.value.replace(",", ".");
    if (r) document.getElementById("hiddenR").value = r.value.replace(",", ".");
}


// =====================================================
//              5. X = CHECKBOX ONLY ONE
// =====================================================
function handleXCheckboxChange(event) {
    const hiddenX = document.getElementById("hiddenX");
    const all = document.querySelectorAll('input[type="checkbox"][data-x]');

    all.forEach(cb => {
        if (cb !== event.target) cb.checked = false;
    });

    hiddenX.value = event.target.checked
        ? event.target.dataset.x
        : "";
}


// =====================================================
//           6. ОБРАБОТКА КЛИКА ПО SVG (основное)
// =====================================================
function handleGraphClick(event) {
    const R = parseFloat(document.getElementById("rInput").value);
    if (!R || R < 1 || R > 4) {
        showError("Введите корректное R (1–4)");
        return;
    }

    const rect = event.target.closest("svg").getBoundingClientRect();
    const xPix = event.clientX - rect.left;
    const yPix = event.clientY - rect.top;

    const realX = (xPix - CENTER) / SCALE;
    const realY = (CENTER - yPix) / SCALE;

    document.getElementById("hiddenX").value = realX;
    document.getElementById("hiddenY").value = realY;
    document.getElementById("hiddenR").value = R;

    // снимаем все чекбоксы X
    document.querySelectorAll('input[type="checkbox"][data-x]').forEach(cb => cb.checked = false);

    // Отправка в PrimeFaces
    PrimeFaces.ab({
        source: "submitBtn",
        process: "@form",
        update: "input-form @form :responsesForm",
        oncomplete: () => {
            playShotSound();
            drawAllPoints();
        }
    });
}


// =====================================================
//                7. ОТРИСОВКА ОБЛАСТИ ДЛЯ R
// =====================================================
function updateGraph(R) {
    const svg = getSVG();
    if (!svg) return;

    svg.querySelectorAll(".region").forEach(e => e.remove());

    R = parseFloat(R);
    if (!R || isNaN(R)) return;

    const rPix = R * SCALE;
    const half = rPix / 2;

    // === 1. Прямоугольник (1 квадрант)
    const rect = document.createElementNS(svg.namespaceURI, "rect");
    rect.classList.add("region");
    rect.setAttribute("x", CENTER);
    rect.setAttribute("y", CENTER - half);
    rect.setAttribute("width", rPix);
    rect.setAttribute("height", half);
    rect.setAttribute("fill", "#4eaaff");
    rect.setAttribute("opacity", "0.85");
    svg.appendChild(rect);

    // === 2. Четверть окружности (4 квадрант)
    const circle = document.createElementNS(svg.namespaceURI, "path");
    circle.classList.add("region");
    circle.setAttribute("d",
        `M ${CENTER} ${CENTER}
         L ${CENTER + half} ${CENTER}
         A ${half} ${half} 0 0 1 ${CENTER} ${CENTER + half}
         Z`
    );
    circle.setAttribute("fill", "#4eaaff");
    circle.setAttribute("opacity", "0.85");
    svg.appendChild(circle);

    // === 3. Треугольник (2 квадрант)
    const tri = document.createElementNS(svg.namespaceURI, "polygon");
    tri.classList.add("region");
    tri.setAttribute("points",
        `${CENTER},${CENTER}  ${CENTER - rPix},${CENTER}  ${CENTER},${CENTER - rPix}`
    );
    tri.setAttribute("fill", "#4eaaff");
    tri.setAttribute("opacity", "0.85");
    svg.appendChild(tri);

    // перерисовать точки
    clearPoints();
    drawAllPoints();
}


// =====================================================
//                   8. ИНИЦИАЛИЗАЦИЯ
// =====================================================
window.addEventListener("DOMContentLoaded", () => {

    // === навесить обработчики X
    document.querySelectorAll('input[type="checkbox"][data-x]')
        .forEach(cb => cb.addEventListener("change", handleXCheckboxChange));

    // === обработка кликов по SVG
    const svg = getSVG();
    svg.addEventListener("click", handleGraphClick);

    // === первая отрисовка области
    updateGraph(document.getElementById("rInput").value);
});


// =====================================================
//                 ХЕЛПЕРЫ
// =====================================================
function getSVG() {
    return document.querySelector(".graph-panel svg");
}
