function validateForm() {
    const y = document.getElementById("y").value.replace(",", ".");
    const r = document.getElementById("r").value.replace(",", ".");
    if (isNaN(y) || y < -5 || y > 5) {
        showError("Y должен быть числом от -5 до 5");
        return false;
    }
    if (isNaN(r) || r <= 0 || r > 4) {
        showError("R должен быть в диапазоне (0;4]");
        return false;
    }
    return true;
}

function showError(msg) {
    document.getElementById("error").textContent = msg;
}

function handleClick(event) {
    const r = parseFloat(document.getElementById("r").value);
    if (isNaN(r)) {
        showError("Сначала установите радиус R");
        return;
    }

    const canvas = event.target;
    const rect = canvas.getBoundingClientRect();
    const x = ((event.clientX - rect.left) - 150) / (100 / r);
    const y = ((150 - (event.clientY - rect.top)) / (100 / r));

    const form = document.createElement("form");
    form.method = "post";
    form.action = "controller";
    form.innerHTML = `<input name="x" value="${x}"><input name="y" value="${y}"><input name="r" value="${r}">`;
    document.body.appendChild(form);
    form.submit();
}
