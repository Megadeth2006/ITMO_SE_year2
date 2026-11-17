package programming.lab4_web.rest;

import programming.lab4_web.dto.AuthRequestDTO;
import programming.lab4_web.dto.AuthResponseDTO;
import programming.lab4_web.entities.User;
import programming.lab4_web.exceptions.AuthenticationException;
import programming.lab4_web.exceptions.DatabaseException;
import programming.lab4_web.exceptions.ValidationException;
import programming.lab4_web.services.AuthService;
import programming.lab4_web.util.ValidationUtil;

import javax.ejb.EJB;
import javax.persistence.PersistenceException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import javax.ws.rs.*;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/auth")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AuthResource {
    
    @EJB
    private AuthService authService;
    
    @Context
    private HttpServletRequest request;
    
    
    @POST
    @Path("/register")
    public Response register(AuthRequestDTO authRequest) throws ValidationException, DatabaseException {
        if (!ValidationUtil.isValidUsername(authRequest.getUsername())) {
            throw new ValidationException("Некорректное имя пользователя");
        }
        
        if (!ValidationUtil.isValidPassword(authRequest.getPassword())) {
            throw new ValidationException("Пароль должен содержать минимум 4 символа");
        }
        
        try {
            User user = authService.register(authRequest.getUsername(), authRequest.getPassword());
            
            HttpSession session = request.getSession(true);
            session.setAttribute("userId", user.getId());
            session.setAttribute("username", user.getUsername());
            
            return Response.ok(new AuthResponseDTO(true, "Регистрация успешна", user.getUsername())).build();
        } catch (Exception e) {
            if (e instanceof PersistenceException) {
                throw new DatabaseException("Ошибка при регистрации пользователя в базе данных", e);
            }
            // Если это исключение от AuthService (например, пользователь уже существует)
            throw new ValidationException(e.getMessage());
        }
    }
    
   
    @POST
    @Path("/login")
    public Response login(AuthRequestDTO authRequest) throws ValidationException, AuthenticationException, DatabaseException {
        if (!ValidationUtil.isValidUsername(authRequest.getUsername()) || 
            !ValidationUtil.isValidPassword(authRequest.getPassword())) {
            throw new ValidationException("Некорректные данные");
        }
        
        try {
            User user = authService.login(authRequest.getUsername(), authRequest.getPassword());
            
            HttpSession session = request.getSession(true);
            session.setAttribute("userId", user.getId());
            session.setAttribute("username", user.getUsername());
            
            return Response.ok(new AuthResponseDTO(true, "Вход выполнен успешно", user.getUsername())).build();
        } catch (Exception e) {
            if (e instanceof PersistenceException) {
                throw new DatabaseException("Ошибка при входе в систему", e);
            }
            // Если это исключение от AuthService (неверный логин/пароль)
            throw new AuthenticationException(e.getMessage());
        }
    }
    
    
    @POST
    @Path("/logout")
    public Response logout() {
        HttpSession session = request.getSession(false);
        if (session != null) {
            session.invalidate();
        }
        return Response.ok(new AuthResponseDTO(true, "Выход выполнен успешно", null)).build();
    }
    
    
    @GET
    @Path("/check")
    public Response check() {
        HttpSession session = request.getSession(false);
        if (session != null && session.getAttribute("userId") != null) {
            String username = (String) session.getAttribute("username");
            return Response.ok(new AuthResponseDTO(true, "Авторизован", username)).build();
        }
        return Response.status(Response.Status.UNAUTHORIZED)
                .entity(new AuthResponseDTO(false, "Не авторизован", null))
                .build();
    }
}
