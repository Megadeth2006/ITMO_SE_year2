package programming.lab4_web.services;

import programming.lab4_web.entities.User;

import javax.ejb.EJB;
import javax.ejb.Stateless;

@Stateless
public class AuthService {
    
    @EJB
    private UserService userService;
    

    public User register(String username, String password) throws Exception {
        if (userService.usernameExists(username)) {
            throw new Exception("Пользователь с таким именем уже существует");
        }
        return userService.createUser(username, password);
    }
    

    public User login(String username, String password) throws Exception {
        if (!userService.verifyCredentials(username, password)) {
            throw new Exception("Неверное имя пользователя или пароль");
        }
        return userService.findByUsername(username)
                .orElseThrow(() -> new Exception("Пользователь не найден"));
    }
}
