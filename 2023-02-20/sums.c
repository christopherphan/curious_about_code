/* C solution to David Amos's coding challenge "Adding it all up":
 * https://discourse.davidamos.dev/t/adding-it-all-up/139 */

#include<stdio.h>
#include<time.h>

#define REPEATS 1000000

long loop(long n) {
    long ret_val = 0;
    if (n > 0) {
        for (long k = 0; k < n + 1; k++) {
            ret_val += k;
        }
        return ret_val;
    } else if (n == 0) {
        return 0;
    } else {
        return loop(-n);
    }
}

int main() {
    printf("%ld, %d \n", loop(12345), 12345 * 12346 / 2);
    long inputs[] = {14, -15, 120, 0};
    long starts[] = {-3, 0, -20};
    long ends[] = {3, 8, 20};
    clock_t t;
    float comp_time;
    for(int j = 0; j < 4; j++) {
        t = clock();
        for(int w = 0; w < REPEATS; w++) {
            loop(inputs[j]);
        }
        t = clock() - t;
        comp_time = ((float) (1000000000 * t))/(CLOCKS_PER_SEC * REPEATS);
        printf("n = %ld: %0.3f ns\n", inputs[j], comp_time);
    }
    for(int j = 0; j < 3; j++) {
        t = clock();
        for(int w = 0; w < REPEATS; w++) {
            long outval = 0;
            for(long u = starts[j]; u < ends[j]; u++){
                outval += loop(u);
            }
        }
        t = clock() - t;
        comp_time = ((float) (1000000000 * t))/(CLOCKS_PER_SEC * REPEATS);
        printf("range %ld to %ld: %0.3f ns\n", starts[j], ends[j], comp_time);
    }
}
