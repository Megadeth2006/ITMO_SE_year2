package programming.lab4_web.entities;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import java.io.Serializable;

@Entity
@Table(name = "user_settings")
@Getter
@Setter
@NoArgsConstructor
public class UserSettings implements Serializable {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @OneToOne
    @JoinColumn(name = "user_id", nullable = false, unique = true)
    private User user;
    
    @Column(name = "theme_preset", length = 20)
    private String themePreset; // "light", "dark", "custom"
    
    @Column(name = "background_color", length = 7)
    private String backgroundColor;
    
    @Column(name = "primary_color", length = 7)
    private String primaryColor;
    
    @Column(name = "secondary_color", length = 7)
    private String secondaryColor;
    
    @Column(name = "text_color", length = 7)
    private String textColor;
    
    @Column(name = "card_background", length = 7)
    private String cardBackground;
    
    @Column(name = "border_color", length = 7)
    private String borderColor;
    
    public UserSettings(User user) {
        this.user = user;
        this.themePreset = "light";
    }
}






