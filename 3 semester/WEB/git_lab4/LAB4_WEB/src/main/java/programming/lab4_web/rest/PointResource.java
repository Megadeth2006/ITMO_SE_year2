package programming.lab4_web.rest;

import programming.lab4_web.dto.PointDTO;
import programming.lab4_web.dto.PointRequestDTO;
import programming.lab4_web.entities.User;
import programming.lab4_web.exceptions.AuthenticationException;
import programming.lab4_web.exceptions.DatabaseException;
import programming.lab4_web.exceptions.ValidationException;
import programming.lab4_web.services.PointService;
import programming.lab4_web.services.UserService;
import programming.lab4_web.util.ValidationUtil;

import javax.ejb.EJB;
import javax.persistence.PersistenceException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import javax.ws.rs.*;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Path("/points")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class PointResource {
    
    @EJB
    private PointService pointService;
    
    @EJB
    private UserService userService;
    
    @Context
    private HttpServletRequest request;
    
    
    @POST
    public Response addPoint(PointRequestDTO pointRequest) throws AuthenticationException, ValidationException, DatabaseException {
        User user = getCurrentUser();
        if (user == null) {
            throw new AuthenticationException("Не авторизован");
        }
        
        BigDecimal x = ValidationUtil.parseBigDecimal(pointRequest.getX());
        BigDecimal y = ValidationUtil.parseBigDecimal(pointRequest.getY());
        BigDecimal r = ValidationUtil.parseBigDecimal(pointRequest.getR());
        
        if (x == null || y == null || r == null) {
            throw new ValidationException("Некорректный формат координат");
        }
        
        if (!ValidationUtil.isValidPoint(x, y, r)) {
            throw new ValidationException("Координаты вне допустимого диапазона. X: [-5, 3], Y: [-3, 3], R: [-5, 3]");
        }
        
        try {
            PointDTO point = pointService.addPoint(x, y, r, user);
            return Response.ok(point).build();
        } catch (PersistenceException e) {
            throw new DatabaseException("Ошибка при сохранении точки в базу данных", e);
        }
    }
    
   
    @GET
    public Response getPoints() throws AuthenticationException, DatabaseException {
        User user = getCurrentUser();
        if (user == null) {
            throw new AuthenticationException("Не авторизован");
        }
        
        try {

            List<PointDTO> points = pointService.getAllPoints();
            return Response.ok(points).build();
        } catch (PersistenceException e) {
            throw new DatabaseException("Ошибка при получении точек из базы данных", e);
        }
    }
    
   
    @DELETE
    public Response clearPoints() throws AuthenticationException, DatabaseException {
        User user = getCurrentUser();
        if (user == null) {
            throw new AuthenticationException("Не авторизован");
        }
        
        try {

            pointService.clearUserPoints(user);
            
            Map<String, Object> response = new HashMap<>();
            response.put("success", true);
            response.put("message", "Все точки удалены");
            
            return Response.ok(response).build();
        } catch (PersistenceException e) {
            throw new DatabaseException("Ошибка при удалении точек из базы данных", e);
        }
    }
    
    
    private User getCurrentUser() {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("username") == null) {
            return null;
        }
        
        String username = (String) session.getAttribute("username");
        return userService.findByUsername(username).orElse(null);
    }
}
