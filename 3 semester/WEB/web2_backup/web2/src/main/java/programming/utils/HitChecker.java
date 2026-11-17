package programming.utils;

public class HitChecker {
    public static boolean check(double x, double y, double r) {
        // Левая верхняя часть — прямоугольник
        if (x <= 0 && y >= 0 && x >= -r && y <= r) return true;
        // Правая верхняя — треугольник
        if (x >= 0 && y >= 0 && y <= (-0.5 * x + r / 2)) return true;
        // Левая нижняя — четверть круга
        if (x <= 0 && y <= 0 && (x * x + y * y <= r * r)) return true;

        return false;
    }
}
