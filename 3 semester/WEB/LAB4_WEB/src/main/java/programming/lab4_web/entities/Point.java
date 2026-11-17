package programming.lab4_web.entities;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.*;
import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "points")
@Getter
@Setter
@NoArgsConstructor
public class Point implements Serializable {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(precision = 30, scale = 10, nullable = false)
    private BigDecimal x;
    
    @Column(precision = 30, scale = 10, nullable = false)
    private BigDecimal y;
    
    @Column(precision = 30, scale = 10, nullable = false)
    private BigDecimal r;
    
    @Column(name = "in_area", nullable = false)
    private boolean inArea;
    
    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    public Point(BigDecimal x, BigDecimal y, BigDecimal r, boolean inArea, User user) {
        this.x = x;
        this.y = y;
        this.r = r;
        this.inArea = inArea;
        this.user = user;
        this.createdAt = LocalDateTime.now();
    }
}
