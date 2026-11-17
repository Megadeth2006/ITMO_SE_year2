package programming.lab4_web.dto;

import java.io.Serializable;

public class ThemeSettingsDTO implements Serializable {
    private String themePreset;
    private String backgroundColor;
    private String primaryColor;
    private String secondaryColor;
    private String textColor;
    private String cardBackground;
    private String areaBackground;
    private String borderColor;
    
    public ThemeSettingsDTO() {}
    
    public ThemeSettingsDTO(String themePreset, String backgroundColor, String primaryColor, 
                          String secondaryColor, String textColor, String cardBackground, 
                          String areaBackground, String borderColor) {
        this.themePreset = themePreset;
        this.backgroundColor = backgroundColor;
        this.primaryColor = primaryColor;
        this.secondaryColor = secondaryColor;
        this.textColor = textColor;
        this.cardBackground = cardBackground;
        this.areaBackground = areaBackground;
        this.borderColor = borderColor;
    }
    
    public String getThemePreset() {
        return themePreset;
    }
    
    public void setThemePreset(String themePreset) {
        this.themePreset = themePreset;
    }
    
    public String getBackgroundColor() {
        return backgroundColor;
    }
    
    public void setBackgroundColor(String backgroundColor) {
        this.backgroundColor = backgroundColor;
    }
    
    public String getPrimaryColor() {
        return primaryColor;
    }
    
    public void setPrimaryColor(String primaryColor) {
        this.primaryColor = primaryColor;
    }
    
    public String getSecondaryColor() {
        return secondaryColor;
    }
    
    public void setSecondaryColor(String secondaryColor) {
        this.secondaryColor = secondaryColor;
    }
    
    public String getTextColor() {
        return textColor;
    }
    
    public void setTextColor(String textColor) {
        this.textColor = textColor;
    }
    
    public String getCardBackground() {
        return cardBackground;
    }
    
    public void setCardBackground(String cardBackground) {
        this.cardBackground = cardBackground;
    }
    
    public String getAreaBackground() {
        return areaBackground;
    }
    
    public void setAreaBackground(String areaBackground) {
        this.areaBackground = areaBackground;
    }
    
    public String getBorderColor() {
        return borderColor;
    }
    
    public void setBorderColor(String borderColor) {
        this.borderColor = borderColor;
    }
}







