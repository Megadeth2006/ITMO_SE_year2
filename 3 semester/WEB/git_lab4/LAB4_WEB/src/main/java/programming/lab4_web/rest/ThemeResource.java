package programming.lab4_web.rest;

import programming.lab4_web.dto.ThemeSettingsDTO;
import programming.lab4_web.entities.User;
import programming.lab4_web.exceptions.AuthenticationException;
import programming.lab4_web.exceptions.DatabaseException;
import programming.lab4_web.services.UserService;
import programming.lab4_web.services.UserSettingsService;

import javax.ejb.EJB;
import javax.persistence.PersistenceException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import javax.ws.rs.*;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

@Path("/theme")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ThemeResource {
    
    @EJB
    private UserSettingsService userSettingsService;
    
    @EJB
    private UserService userService;
    
    @Context
    private HttpServletRequest request;
    
    @GET
    public Response getThemeSettings() throws AuthenticationException, DatabaseException {
        User user = getCurrentUser();
        if (user == null) {
            throw new AuthenticationException("Не авторизован");
        }
        
        try {
            ThemeSettingsDTO settings = userSettingsService.getUserSettings(user);
            return Response.ok(settings).build();
        } catch (PersistenceException e) {
            throw new DatabaseException("Ошибка при получении настроек темы", e);
        }
    }
    
    @POST
    public Response saveThemeSettings(ThemeSettingsDTO settings) throws AuthenticationException, DatabaseException {
        User user = getCurrentUser();
        if (user == null) {
            throw new AuthenticationException("Не авторизован");
        }
        
        try {
            userSettingsService.saveUserSettings(user, settings);
            return Response.ok(settings).build();
        } catch (PersistenceException e) {
            throw new DatabaseException("Ошибка при сохранении настроек темы", e);
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






