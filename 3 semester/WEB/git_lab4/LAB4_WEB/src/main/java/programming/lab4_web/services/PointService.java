package programming.lab4_web.services;

import programming.lab4_web.dto.PointDTO;
import programming.lab4_web.entities.Point;
import programming.lab4_web.entities.User;
import programming.lab4_web.util.AreaChecker;

import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

@Stateless
public class PointService {
    
    @PersistenceContext(unitName = "lab4PU")
    private EntityManager em;
    

    public PointDTO addPoint(BigDecimal x, BigDecimal y, BigDecimal r, User user) {
        boolean inArea = AreaChecker.check(x, y, r);
        Point point = new Point(x, y, r, inArea, user);
        em.persist(point);
        em.flush(); 
        return convertToDTO(point);
    }
    

    public List<PointDTO> getUserPoints(User user) {
        List<Point> points = em.createQuery(
                "SELECT p FROM Point p WHERE p.user = :user ORDER BY p.createdAt DESC", 
                Point.class)
                .setParameter("user", user)
                .getResultList();
        
        return points.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    
    /**
     * Get all points from all users
     */
    public List<PointDTO> getAllPoints() {
        List<Point> points = em.createQuery(
                "SELECT p FROM Point p ORDER BY p.createdAt DESC", 
                Point.class)
                .getResultList();
        
        return points.stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }
    

    public void clearUserPoints(User user) {
        em.createQuery("DELETE FROM Point p WHERE p.user = :user")
                .setParameter("user", user)
                .executeUpdate();
    }
    

    private PointDTO convertToDTO(Point point) {
        return new PointDTO(
                point.getId(),
                point.getX(),
                point.getY(),
                point.getR(),
                point.isInArea(),
                point.getCreatedAt()
        );
    }
}
