// file: mines/src/main.rs
//
// Solution to David Amos's Weekly Coding Challenge for 2023-02-26
// https://discourse.davidamos.dev/t/disarming-minesweeper/142

use mines::MineBoard;
use std::env;
use std::fs;

fn adjacent_bomb_counts(s: &str) -> Vec<Vec<i8>> {
    let board = MineBoard::try_from(s).unwrap();
    board.adjacent_bomb_counts()
}

fn report_abc(v: Vec<Vec<i8>>) -> String {
    let mut outstr = "[[".to_string();
    for (ridx, row) in v.into_iter().enumerate() {
        if ridx != 0 {
            outstr.push_str("],\n [");
        }
        for (cidx, col) in row.into_iter().enumerate() {
            if cidx != 0 {
                outstr.push_str(", ");
            }
            outstr.push_str(&format!("{}", col));
        }
    }
    outstr.push_str("]]");
    outstr
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() > 1 {
        for (idx, filename) in args.iter().enumerate() {
            if idx > 0 {
                let s =
                    fs::read_to_string(filename).expect(&format!("Cannot read file {}", filename));
                println!("Input {}:\n{}\n", filename, s);
                let a = adjacent_bomb_counts(&s);
                println!("Output:\n{}\n", report_abc(a));
            }
        }
    } else {
        println!("usage: {} file1 [file2 ...]", args[0]);
    }
}
