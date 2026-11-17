package programming.lab4_web.util;

import java.math.BigDecimal;
import java.math.MathContext;


public class AreaChecker {
    
    private static final BigDecimal ZERO = BigDecimal.ZERO;
    private static final BigDecimal TWO = BigDecimal.valueOf(2);
    
    // чекаем точку
    public static boolean check(BigDecimal x, BigDecimal y, BigDecimal r) {

        BigDecimal effectiveR = r.abs();
        BigDecimal effectiveX = r.compareTo(ZERO) >= 0 ? x : x.negate();
        BigDecimal effectiveY = r.compareTo(ZERO) >= 0 ? y : y.negate();
        
        return checkPositiveR(effectiveX, effectiveY, effectiveR);
    }
    
    private static boolean checkPositiveR(BigDecimal x, BigDecimal y, BigDecimal r) {
        BigDecimal r2 = r.divide(TWO, MathContext.DECIMAL128);
        // четверть круга
        if (x.compareTo(ZERO) >= 0 && y.compareTo(ZERO) >= 0) {

            BigDecimal distanceSquared = x.multiply(x).add(y.multiply(y));
            BigDecimal radiusSquared = r2.multiply(r2);
            return distanceSquared.compareTo(radiusSquared) <= 0;
        }
       // треугольник
        else if (x.compareTo(ZERO) >= 0 && y.compareTo(ZERO) <= 0) {

            BigDecimal lineValue = x.subtract(TWO.multiply(y));
            return lineValue.compareTo(r) <= 0;
        }
        
        // квадрат
        else if (x.compareTo(ZERO) <= 0 && y.compareTo(ZERO) <= 0) {
            BigDecimal negR = r.negate();
            return x.compareTo(negR) >= 0 && y.compareTo(negR) >= 0;
        }
        
        return false;
    }
}

