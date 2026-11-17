#include <stdio.h>

typedef struct Point {
    int x;
    int y;
} Point;

typedef int (*FilterFunc)(Point);

__declspec(dllexport) int filter(Point* points, int count, Point* result, FilterFunc filter_func) {
    int result_count = 0;
    
    for (int i = 0; i < count; i++) {
        if (filter_func(points[i])) {
            result[result_count++] = points[i];
        }
    }
    
    return result_count;
}

