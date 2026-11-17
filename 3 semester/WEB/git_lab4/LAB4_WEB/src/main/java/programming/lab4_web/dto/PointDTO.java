package programming.lab4_web.dto;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

public class PointDTO implements Serializable {
    public Long id;
    public String x;
    public String y;
    public String r;
    public Boolean inArea;
    public String createdAt;
    
    public PointDTO() {}
    
    public PointDTO(Long id, BigDecimal x, BigDecimal y, BigDecimal r, boolean inArea, LocalDateTime createdAt) {
        this.id = id;
        this.x = x != null ? x.toString() : null;
        this.y = y != null ? y.toString() : null;
        this.r = r != null ? r.toString() : null;
        this.inArea = inArea;
        this.createdAt = createdAt != null ? createdAt.toString() : null;
    }
    
  
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getX() { return x; }
    public void setX(String x) { this.x = x; }
    
    public String getY() { return y; }
    public void setY(String y) { this.y = y; }
    
    public String getR() { return r; }
    public void setR(String r) { this.r = r; }
    
    public Boolean getInArea() { return inArea; }
    public void setInArea(Boolean inArea) { this.inArea = inArea; }
    
    public String getCreatedAt() { return createdAt; }
    public void setCreatedAt(String createdAt) { this.createdAt = createdAt; }
}

