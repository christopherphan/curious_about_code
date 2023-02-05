/* Rust-based solution to solve 15-game puzzles
 * (Solution to puzzle by David Amos:
 * https://discourse.davidamos.dev/t/the-fifteen-puzzle/124 )
 */

use std::collections::HashMap;
use std::env;
use std::fs;

const SOLVED: [usize; 16] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15];

fn parse_input(filename: &String) -> [usize; 16] {
    let raw_text = fs::read_to_string(&filename).expect(&format!("Unable to read file {filename}"));
    let split = raw_text.split_whitespace();
    let mut output: [usize; 16] = [0; 16];
    for (idx, k) in split.enumerate() {
        if k == "E" {
            output[15] = idx;
        } else {
            let place: usize = k.parse().unwrap();
            output[place - 1] = idx;
        }
    }
    output
}

fn is_odd(arrangement: [usize; 16]) -> bool {
    let mut num_even_cycles: usize = 0;
    let mut used_up: [bool; 16] = [false; 16];
    for idx in 0..16 {
        if !used_up[idx] {
            let mut current = idx;
            let mut cycle_len = 0;
            while !used_up[current] {
                cycle_len += 1;
                used_up[current] = true;
                current = arrangement[current];
            }
            if cycle_len % 2 == 0 {
                num_even_cycles += 1
            }
        }
    }
    num_even_cycles % 2 == 1
}

fn manhattan_dist(x: (usize, usize), y: (usize, usize)) -> usize {
    (x.0).abs_diff(y.0) + (x.1).abs_diff(y.1)
}

fn position_to_coord(pos: usize) -> (usize, usize) {
    (pos % 4, pos / 4)
}

fn valid_arrangement(arrangement: [usize; 16]) -> bool {
    (manhattan_dist(position_to_coord(arrangement[15]), (3usize, 3usize)) % 2 == 1)
        == is_odd(arrangement)
}

fn swap(mut arr: [usize; 16], pos: (usize, usize)) -> [usize; 16] {
    let temp = arr[pos.0];
    arr[pos.0] = arr[pos.1];
    arr[pos.1] = temp;
    arr
}

fn score(&arrangement: &[usize; 16]) -> usize {
    let mut ret_val: usize = 0;
    for idx in 0..16 {
        ret_val += manhattan_dist(position_to_coord(arrangement[idx]), position_to_coord(idx))
    }
    ret_val
}

fn find_in(arr: [usize; 16], val: usize) -> Option<usize> {
    for k in 0..15 {
        if arr[k] == val {
            return Some(k);
        }
    }
    None
}

fn print_pos(&arr: &[usize; 16]) -> String {
    let mut output_arr: [usize; 16] = [0; 16];
    for k in 0..16 {
        output_arr[arr[k]] = k;
    }
    let mut outstr = String::new();
    for k in 0..16 {
        if output_arr[k] == 15 {
            outstr.push('E');
        } else {
            outstr.push_str(&format!("{}", output_arr[k] + 1));
        }
        if k % 4 == 3 {
            outstr.push('\n');
        } else {
            outstr.push(' ');
        }
    }
    outstr
}

fn adjacent(arrangement: [usize; 16]) -> Vec<(usize, [usize; 16])> {
    let mut ret_val: Vec<(usize, [usize; 16])> = Vec::new();
    // up
    if arrangement[15] > 4 {
        if let Some(k) = find_in(arrangement, arrangement[15] - 4) {
            ret_val.push((k, swap(arrangement, (15, k))));
        }
    }
    // down
    if arrangement[15] < 11 {
        if let Some(k) = find_in(arrangement, arrangement[15] + 4) {
            ret_val.push((k, swap(arrangement, (15, k))));
        }
    }
    // left
    if arrangement[15] % 4 != 0 {
        if let Some(k) = find_in(arrangement, arrangement[15] - 1) {
            ret_val.push((k, swap(arrangement, (15, k))));
        }
    }
    // right
    if arrangement[15] % 4 != 3 {
        if let Some(k) = find_in(arrangement, arrangement[15] + 1) {
            ret_val.push((k, swap(arrangement, (15, k))));
        }
    }
    ret_val
}

fn get_best(scores: HashMap<[usize; 16], usize>) -> (HashMap<[usize; 16], usize>, [usize; 16]) {
    let mut best: Option<([usize; 16], usize)> = None;
    for (arr, sc) in scores.iter() {
        match best {
            None => {
                best = Some((*arr, *sc));
            }
            Some(k) => {
                if k.1 > *sc {
                    best = Some((*arr, *sc));
                }
            }
        }
    }
    (scores, best.unwrap().0)
}

fn print_status(checked: usize) {
    println!("Examined {} arrangements", checked);
}

fn find_solution(puzzle_start: [usize; 16]) -> Vec<usize> {
    let mut scores: HashMap<[usize; 16], usize> =
        HashMap::from([(puzzle_start, score(&puzzle_start))]);
    let mut shortest_path: HashMap<[usize; 16], Vec<usize>> =
        HashMap::from([(puzzle_start, Vec::new())]);
    let mut best_loc: [usize; 16];
    let mut best_score = score(&puzzle_start);
    let mut exhausted: HashMap<[usize; 16], bool> = HashMap::new();
    let mut checked: usize = 0;
    while best_score != 0 {
        if checked > 0 && checked % 1000 == 0 {
            print_status(checked);
        }
        checked += 1;
        (scores, best_loc) = get_best(scores);
        for (to_move, arr) in adjacent(best_loc).iter() {
            let mut new_path = shortest_path[&best_loc].clone();
            new_path.push(*to_move);
            if let None = scores.get(arr) {
                if let None = exhausted.get(arr) {
                    scores.insert(arr.clone(), score(arr));
                };
            }
            match shortest_path.get(arr) {
                Some(path) => {
                    if path.len() > new_path.len() {
                        shortest_path.remove(arr);
                        shortest_path.insert(*arr, new_path);
                    }
                }
                None => {
                    shortest_path.insert(*arr, new_path);
                }
            }
        }
        if score(&best_loc) < best_score {
            best_score = score(&best_loc);
        }
        scores.remove(&best_loc);
        exhausted.insert(best_loc, true);
    }
    print_status(checked);
    shortest_path[&SOLVED].clone()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() == 1 {
        println!("Usage: {} filename", &args[0]);
    } else {
        let puzzle_start = parse_input(&args[1]);
        println!("Arrangement:\n{}", print_pos(&puzzle_start));
        if !valid_arrangement(puzzle_start) {
            println!("Invalid arrangement.")
        } else {
            let soln = find_solution(puzzle_start);
            let mut output_text = String::from("\nSolution:");
            let mut cols = 9;
            let mut to_add;
            for k in soln {
                if k > 9 {
                    to_add = 4;
                } else {
                    to_add = 3;
                }
                if cols + to_add > 70 {
                    output_text.push_str(",\n");
                    cols = to_add - 1;
                } else {
                    output_text.push_str(", ");
                    cols += to_add;
                }
                output_text.push_str(&format!("{}", k + 1));
            }
            println!("{output_text}");
        }
    }
}
