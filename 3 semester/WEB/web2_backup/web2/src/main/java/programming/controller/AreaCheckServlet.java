package programming.controller;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import programming.model.Point;
import programming.model.ResultBean;
import programming.utils.HitChecker;

@WebServlet("/areaCheck")
public class AreaCheckServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        try {
            // Парсим параметры
            double x = Double.parseDouble(req.getParameter("x").replace(',', '.'));
            double y = Double.parseDouble(req.getParameter("y").replace(',', '.'));
            double r = Double.parseDouble(req.getParameter("r").replace(',', '.'));

            // Проверка попадания
            boolean hit = HitChecker.check(x, y, r);
            Point point = new Point(x, y, r, hit);

            // Получаем Bean из сессии (для сохранения результатов)
            ResultBean bean = (ResultBean) req.getSession().getAttribute("results");
            if (bean == null) {
                bean = new ResultBean();
            }

            bean.add(point);
            req.getSession().setAttribute("results", bean);

            // Возвращаем пользователя обратно на index.jsp
            req.getRequestDispatcher("/index.jsp").forward(req, resp);

        } catch (NumberFormatException e) {
            req.setAttribute("error", "Некорректные данные");
            req.getRequestDispatcher("/index.jsp").forward(req, resp);
        }
    }
}
