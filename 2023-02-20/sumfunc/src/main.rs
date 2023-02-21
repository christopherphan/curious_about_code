/* Rust solution to David Amos's coding challenge "Adding it all up":
 * https://discourse.davidamos.dev/t/adding-it-all-up/139 */

use std::collections::HashMap;
#[macro_use]
extern crate timeit;

fn _loop(n: i64) -> i64 {
    // "loop" is a keyword
    let mut ret_val: i64 = 0;
    if n > 0 {
        for k in 1..(n + 1) {
            ret_val += k;
        }
        ret_val
    } else if n == 0 {
        0
    } else {
        -_loop(-n)
    }
}

fn reduce(n: i64) -> i64 {
    if n > 0 {
        (1..(n + 1)).reduce(|acc, e| acc + e).unwrap()
        // Literally the example for "reduce" in the documentation:
        // https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.reduce
    } else if n == 0 {
        0
    } else {
        -reduce(-n)
    }
}

fn recursive(n: i64) -> i64 {
    if n > 0 {
        n + recursive(n - 1)
    } else if n == 0 {
        0
    } else {
        -recursive(-n)
    }
}

fn memoized_recursive(n: i64, cache: &mut HashMap<i64, i64>) -> i64 {
    match cache.get(&n) {
        Some(k) => *k,
        None => {
            let mut k: i64 = 0;
            if n > 0 {
                k = n + memoized_recursive(n - 1, cache);
            } else if n < 0 {
                k = -memoized_recursive(-n, cache);
            }
            cache.insert(n, k);
            k
        }
    }
}

fn gauss_sum(n: i64) -> i64 {
    if n > 0 {
        n * (n + 1) / 2
    } else if n == 0 {
        0
    } else {
        -gauss_sum(-n)
    }
}

fn main() {
    let numbers: [i64; 4] = [14, -15, 120, 0];
    let ranges: [(i64, i64); 3] = [(-3, 3), (0, 8), (-20, 20)];
    let mut cache1: HashMap<i64, i64> = HashMap::new();
    for k in numbers {
        assert_eq!(_loop(k), reduce(k));
        assert_eq!(_loop(k), recursive(k));
        assert_eq!(_loop(k), memoized_recursive(k, &mut cache1));
        assert_eq!(_loop(k), gauss_sum(k));
    }
    println!("All functions correct.");
    for n in numbers {
        println!("n = {}:", n);
        print!("  `_loop` with ");
        timeit!({
            _loop(n);
        });
        print!("  `reduce` with ");
        timeit!({
            reduce(n);
        });
        print!("  `recursive` with ");
        timeit!({
            recursive(n);
        });
        print!("  `memoized_recursive` with ");
        timeit!({
            let mut c: HashMap<i64, i64> = HashMap::new();
            memoized_recursive(n, &mut c);
        });
        print!("  `gauss_sum` with ");
        timeit!({
            gauss_sum(n);
        });
    }
    let mut a: Vec<i64> = Vec::new();
    for r in ranges {
        println!(" r = {}..{}", r.0, r.1);
        print!("  `_loop` with ");
        timeit!({
            a.extend((r.0..r.1).map(|k| _loop(k)));
        });
        print!("  `reduce` with ");
        timeit!({
            a.extend((r.0..r.1).map(|k| reduce(k)));
        });
        print!("  `recursive` with ");
        timeit!({
            a.extend((r.0..r.1).map(|k| recursive(k)));
        });
        print!("  `memoized_recursive` with ");
        timeit!({
            let mut c: HashMap<i64, i64> = HashMap::new();
            a.extend((r.0..r.1).map(|k| memoized_recursive(k, &mut c)));
        });
        print!("  `gauss_sum` with ");
        timeit!({
            a.extend((r.0..r.1).map(|k| gauss_sum(k)));
        });
    }
}
