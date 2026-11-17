package programming.lab4_web.util;

import java.math.BigDecimal;


public class ValidationUtil {
    
    private static final BigDecimal X_MIN = BigDecimal.valueOf(-5);
    private static final BigDecimal X_MAX = BigDecimal.valueOf(3);
    private static final BigDecimal Y_MIN = BigDecimal.valueOf(-3);
    private static final BigDecimal Y_MAX = BigDecimal.valueOf(3);
    private static final BigDecimal R_MIN = BigDecimal.valueOf(-5);
    private static final BigDecimal R_MAX = BigDecimal.valueOf(3);
    

    public static boolean isValidX(BigDecimal x) {
        return x != null && x.compareTo(X_MIN) >= 0 && x.compareTo(X_MAX) <= 0;
    }

    public static boolean isValidY(BigDecimal y) {
        return y != null && y.compareTo(Y_MIN) >= 0 && y.compareTo(Y_MAX) <= 0;
    }

    public static boolean isValidR(BigDecimal r) {
        return r != null && r.compareTo(R_MIN) >= 0 && r.compareTo(R_MAX) <= 0;
    }
    

    public static boolean isValidPoint(BigDecimal x, BigDecimal y, BigDecimal r) {
        return isValidX(x) && isValidY(y) && isValidR(r);
    }

    public static boolean isValidUsername(String username) {
        return username != null && !username.trim().isEmpty() && username.length() <= 50;
    }
    

    public static boolean isValidPassword(String password) {
        return password != null && password.length() >= 4;
    }
    

    public static BigDecimal parseBigDecimal(String value) {
        if (value == null || value.trim().isEmpty()) {
            return null;
        }
        try {

            String normalized = value.trim().replace(',', '.');
            return new BigDecimal(normalized);
        } catch (NumberFormatException e) {
            return null;
        }
    }
}

