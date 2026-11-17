package programming.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class ResultBean implements Serializable{
    private final List<Point> results = new ArrayList<>();

    public void add(Point point) {
        results.add(point);
    }
    public List<Point> getResults() {
        return results;
    }
}
