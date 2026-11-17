package programming.controller;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

@WebServlet("/controller")
public class ControllerServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {

        // Проверяем: если переданы x, y и r, значит нужно проверить попадание
        if (req.getParameter("x") != null &&
                req.getParameter("y") != null &&
                req.getParameter("r") != null) {

            // Перенаправляем в AreaCheckServlet
            req.getRequestDispatcher("/areaCheck").forward(req, resp);
        } else {
            // Если координат нет — просто показываем страницу с формой
            req.getRequestDispatcher("/index.jsp").forward(req, resp);
        }
    }

}
