package programming.itmo.beans;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import javax.annotation.PostConstruct;
import javax.faces.bean.ManagedProperty;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.ApplicationScoped;
import lombok.Getter;
import lombok.Setter;
import org.primefaces.PrimeFaces;
import programming.itmo.model.PointDTO;
import programming.itmo.util.CheckAreaUtil;

@ManagedBean(name="pointsBean")
@ApplicationScoped
@Setter
@Getter
public class PointsBean implements Serializable {

    @ManagedProperty("#{checkAreaUtil}")
    private CheckAreaUtil checkAreaUtil;

    private BigDecimal x;
    private BigDecimal y;
    private Map<String, Boolean> xList;
    private BigDecimal r;
    private BigDecimal hiddenR;
    private boolean inArea;

    @PostConstruct
    public void init() {
        xList = new LinkedHashMap<>();
        for (int i = -5; i <= 2; i++) {
            xList.put(String.valueOf(i), false);
        }
    }

    public void check() {
        boolean bulletHit = false;
        
        BigDecimal currentX = x;
        BigDecimal currentR = r;
        
        // Если x не установлен напрямую, пытаемся получить из xList
        if (currentX == null && xList != null) {
            for (Map.Entry<String, Boolean> entry : xList.entrySet()) {
                if (entry.getValue()) {
                    currentX = new BigDecimal(entry.getKey());
                    break;
                }
            }
        }
        
        // Синхронизируем r с hiddenR, если hiddenR установлен
        if (currentR == null && hiddenR != null && !Objects.equals(hiddenR, BigDecimal.ZERO)) {
            currentR = hiddenR;
        }

        if (currentX != null && y != null && currentR != null) {
            inArea = checkAreaUtil.process(currentX, y, currentR);
            if (inArea) bulletHit = true;
        }

        PrimeFaces.current().ajax().addCallbackParam("bulletHit", bulletHit);
    }

    public void resetHiddenR() {
        hiddenR = BigDecimal.ZERO;
    }

    public List<PointDTO> getAllPoints() {
        return checkAreaUtil.getPointRepository().getAllPoints();
    }

    public List<PointDTO> getReversedPoints() {
        List<PointDTO> points = getAllPoints();
        java.util.Collections.reverse(points);
        return points;
    }

    public Map<String, Boolean> getXList() {
        return xList;
    }

    public void setXList(Map<String, Boolean> xList) {
        this.xList = xList;
    }
}
