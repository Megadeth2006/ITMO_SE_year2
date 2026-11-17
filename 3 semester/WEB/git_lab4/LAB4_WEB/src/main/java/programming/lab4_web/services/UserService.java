package programming.lab4_web.services;

import programming.lab4_web.entities.User;
import programming.lab4_web.util.PasswordUtil;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.PersistenceContext;
import java.util.Optional;

@Stateless
public class UserService {
    
    @PersistenceContext(unitName = "lab4PU")
    private EntityManager em;
    

    public Optional<User> findByUsername(String username) {
        try {
            User user = em.createQuery("SELECT u FROM User u WHERE u.username = :username", User.class)
                    .setParameter("username", username)
                    .getSingleResult();
            return Optional.of(user);
        } catch (NoResultException e) {
            return Optional.empty();
        }
    }
    

    public User createUser(String username, String password) {
        String passwordHash = PasswordUtil.hashPassword(password);
        User user = new User(username, passwordHash);
        em.persist(user);
        return user;
    }
    

    public boolean verifyCredentials(String username, String password) {
        Optional<User> userOpt = findByUsername(username);
        if (userOpt.isEmpty()) {
            return false;
        }
        return PasswordUtil.verifyPassword(password, userOpt.get().getPasswordHash());
    }
    

    public boolean usernameExists(String username) {
        return findByUsername(username).isPresent();
    }
}
