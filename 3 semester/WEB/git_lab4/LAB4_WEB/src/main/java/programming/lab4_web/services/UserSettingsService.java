package programming.lab4_web.services;

import programming.lab4_web.dto.ThemeSettingsDTO;
import programming.lab4_web.entities.User;
import programming.lab4_web.entities.UserSettings;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.PersistenceContext;

@Stateless
public class UserSettingsService {
    
    @PersistenceContext(unitName = "lab4PU")
    private EntityManager em;
    
    public ThemeSettingsDTO getUserSettings(User user) {
        UserSettings settings = findSettingsByUser(user);
        
        if (settings == null) {
            return getDefaultLightTheme();
        }
        
        return convertToDTO(settings);
    }
    
    public void saveUserSettings(User user, ThemeSettingsDTO dto) {
        UserSettings settings = findSettingsByUser(user);
        
        if (settings == null) {
            settings = new UserSettings(user);
            em.persist(settings);
        }
        
        settings.setThemePreset(dto.getThemePreset());
        settings.setBackgroundColor(dto.getBackgroundColor());
        settings.setPrimaryColor(dto.getPrimaryColor());
        settings.setSecondaryColor(dto.getSecondaryColor());
        settings.setTextColor(dto.getTextColor());
        settings.setCardBackground(dto.getCardBackground());
        settings.setBorderColor(dto.getBorderColor());
    }
    
    private UserSettings findSettingsByUser(User user) {
        try {
            return em.createQuery(
                    "SELECT s FROM UserSettings s WHERE s.user = :user", 
                    UserSettings.class)
                    .setParameter("user", user)
                    .getSingleResult();
        } catch (NoResultException e) {
            return null;
        }
    }
    
    private ThemeSettingsDTO convertToDTO(UserSettings settings) {
        return new ThemeSettingsDTO(
            settings.getThemePreset(),
            settings.getBackgroundColor(),
            settings.getPrimaryColor(),
            settings.getSecondaryColor(),
            settings.getTextColor(),
            settings.getCardBackground(),
            settings.getBorderColor()
        );
    }
    
    private ThemeSettingsDTO getDefaultLightTheme() {
        return new ThemeSettingsDTO(
            "light",
            "#667eea",      // primary gradient start
            "#764ba2",      // primary gradient end
            "#6c757d",      // secondary
            "#333333",      // text
            "#ffffff",      // card background
            "#ddd"          // border
        );
    }
}

