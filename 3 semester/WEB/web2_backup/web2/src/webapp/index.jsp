<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html lang="ru">
<%@ page import="programming.model.ResultBean" %>
<%@ page import="programming.model.Point" %>
<html>
<head>
    <meta charset="UTF-8">
    <title>Лабораторная 2</title>
    <link rel="stylesheet" href="css/style.css">
    <script src="js/script.js"></script>
</head>
<body>
<h2>Григорьев Даниил Александрович / Группа P3216 / Вариант </h2>

<link rel="stylesheet" href="css/style.css">
<form method="post" action="controller" onsubmit="return validateForm();">
    X:
    <select name="x">
        <option>-5</option><option>-4</option>...<option>3</option>
    </select>
    Y: <input id="y" name="y" type="text" placeholder="-5...5">
    R: <input id="r" name="r" type="text" placeholder="1...4">
    <button type="submit">Проверить</button>
</form>

<canvas id="graph" width="300" height="300" onclick="handleClick(event)"></canvas>

<% ResultBean bean = (ResultBean) session.getAttribute("results");
    if (bean != null) { %>
<table>
    <tr><th>X</th><th>Y</th><th>R</th><th>Попадание</th></tr>
    <% for (Point p : bean.getResults()) { %>
    <tr>
        <td><%= p.getX() %></td>
        <td><%= p.getY() %></td>
        <td><%= p.getR() %></td>
        <td><%= p.isHit() ? "Да" : "Нет" %></td>
    </tr>
    <% } %>
</table>
<% } %>

<div id="error"><%= request.getAttribute("error") == null ? "" : request.getAttribute("error") %></div>

</body>
</html>
