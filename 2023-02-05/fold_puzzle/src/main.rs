/* Solves David Amos's folding puzzle:
 * https://discourse.davidamos.dev/t/a-puzzle-above-the-fold/125 */

use itertools::Itertools;
use std::env;
use std::fs;
use std::io;

const EMPTY_STACK: Vec<Square> = Vec::<Square>::new();
const ALL_CREASES: [Crease; 4] = [
    Crease::Lengthwise,
    Crease::VerticalLeft,
    Crease::VerticalCenter,
    Crease::VerticalRight,
];

const ALL_CREASE_TYPES: [CreaseType; 2] = [CreaseType::Inward, CreaseType::Outward];

fn make_arr(vals: [[usize; 4]; 2]) -> [[Vec<Square>; 4]; 2] {
    let ret_val: [[Vec<Square>; 4]; 2] = (0..2)
        .map(|row| {
            (0..4)
                .map(|col| {
                    vec![Square {
                        label: vals[row][col],
                        facing: Facing::Up,
                    }]
                })
                .collect::<Vec<Vec<Square>>>()
                .try_into()
                .unwrap()
        })
        .collect::<Vec<[Vec<Square>; 4]>>()
        .try_into()
        .unwrap();
    ret_val
}

#[derive(Clone, Debug, Copy)]
enum CreaseType {
    Inward,  // Pointing AWAY from player
    Outward, // Pointing TOWARD player
}

impl CreaseType {
    fn describe(&self) -> &str {
        match self {
            CreaseType::Inward => "with crease pointing away from you",
            CreaseType::Outward => "with crease pointing toward you",
        }
    }

    fn fold_over(&self, v1: &Vec<Square>, v2: &Vec<Square>) -> Vec<Square> {
        let mut v3 = Square::reverse(&v1);
        let mut v4 = v2.clone();
        match &self {
            CreaseType::Inward => {
                v3.extend(v4);
                v3
            }
            CreaseType::Outward => {
                v4.extend(v3);
                v4
            }
        }
    }

    fn num_to_crease_types(num: usize) -> [CreaseType; 4] {
        (0..4)
            .map(|k| ALL_CREASE_TYPES[(num >> k) % 2])
            .collect::<Vec<CreaseType>>()
            .try_into()
            .unwrap()
    }
}

#[derive(Clone, Debug, Copy)]
enum Crease {
    Lengthwise,
    VerticalLeft,
    VerticalCenter,
    VerticalRight,
}

impl Crease {
    fn to_fold(self, ct: CreaseType) -> Fold {
        match self {
            Crease::Lengthwise => Fold::Lengthwise(ct),
            Crease::VerticalLeft => Fold::VerticalLeft(ct),
            Crease::VerticalCenter => Fold::VerticalCenter(ct),
            Crease::VerticalRight => Fold::VerticalRight(ct),
        }
    }

    fn with_types(cr: Vec<&Crease>, ct: [CreaseType; 4]) -> Vec<Fold> {
        (0..4)
            .map(|k| cr[k].clone().to_fold(ct[k]))
            .collect::<Vec<Fold>>()
    }

    fn describe(&self) -> &str {
        match self {
            Crease::Lengthwise => "lengthwise",
            Crease::VerticalLeft => "along left vertical crease",
            Crease::VerticalCenter => "along center vertical crease",
            Crease::VerticalRight => "along right vertical crease",
        }
    }
}

#[derive(Clone, Debug, Copy)]
enum Fold {
    Lengthwise(CreaseType),
    VerticalLeft(CreaseType),
    VerticalCenter(CreaseType),
    VerticalRight(CreaseType),
}

impl Fold {
    fn decompose(&self) -> (Crease, CreaseType) {
        match self {
            Fold::Lengthwise(t) => (Crease::Lengthwise, t.clone()),
            Fold::VerticalLeft(t) => (Crease::VerticalLeft, t.clone()),
            Fold::VerticalCenter(t) => (Crease::VerticalCenter, t.clone()),
            Fold::VerticalRight(t) => (Crease::VerticalRight, t.clone()),
        }
    }

    fn describe(&self) -> String {
        let (crease, crease_type) = self.decompose();
        format!("fold {} {}", crease.describe(), crease_type.describe())
    }

    fn on(&self, arr: [[Vec<Square>; 4]; 2]) -> [[Vec<Square>; 4]; 2] {
        match self {
            Fold::Lengthwise(ct) => [
                (0..4)
                    .map(|k| ct.fold_over(&arr[0][k], &arr[1][k]))
                    .collect::<Vec<Vec<Square>>>()
                    .try_into()
                    .unwrap(),
                [EMPTY_STACK; 4],
            ],
            Fold::VerticalLeft(ct) => (0..2)
                .map(|k| {
                    [
                        EMPTY_STACK,
                        ct.fold_over(&arr[k][0], &arr[k][1]),
                        arr[k][2].clone(),
                        arr[k][3].clone(),
                    ]
                })
                .collect::<Vec<[Vec<Square>; 4]>>()
                .try_into()
                .unwrap(),
            Fold::VerticalCenter(ct) => (0..2)
                .map(|k| {
                    [
                        EMPTY_STACK,
                        EMPTY_STACK,
                        ct.fold_over(&arr[k][1], &arr[k][2]),
                        ct.fold_over(&arr[k][0], &arr[k][3]),
                    ]
                })
                .collect::<Vec<[Vec<Square>; 4]>>()
                .try_into()
                .unwrap(),
            Fold::VerticalRight(ct) => (0..2)
                .map(|k| {
                    [
                        arr[k][0].clone(),
                        arr[k][1].clone(),
                        ct.fold_over(&arr[k][3], &arr[k][2]),
                        EMPTY_STACK,
                    ]
                })
                .collect::<Vec<[Vec<Square>; 4]>>()
                .try_into()
                .unwrap(),
        }
    }

    fn verify_sequence(
        sequence: Vec<Fold>,
        arr: [[Vec<Square>; 4]; 2],
    ) -> (bool, [[Vec<Square>; 4]; 2]) {
        let mut new_arr = arr.clone();
        for fold in sequence {
            new_arr = fold.on(new_arr);
        }
        let new_arr2 = new_arr.clone();
        (Square::verify_arrangement(new_arr), new_arr2)
    }
}

#[derive(Clone, Debug, Copy)]
enum Facing {
    Up,
    Down,
}

impl Facing {
    fn opposite(&self) -> Facing {
        match self {
            Facing::Up => Facing::Down,
            Facing::Down => Facing::Up,
        }
    }

    fn describe(&self) -> &str {
        match self {
            Facing::Up => "facing up",
            Facing::Down => "facing down",
        }
    }
}

#[derive(Clone, Debug, Copy)]
struct Square {
    label: usize,
    facing: Facing,
}

impl Square {
    fn swap_facing(&self) -> Square {
        Square {
            label: self.label,
            facing: self.facing.opposite(),
        }
    }

    fn reverse(stack: &Vec<Square>) -> Vec<Square> {
        let s = stack.len();
        (0..s)
            .map(|k| stack[s - k - 1].swap_facing())
            .collect::<Vec<Square>>()
    }

    fn verify_arrangement(arr: [[Vec<Square>; 4]; 2]) -> bool {
        // Collect all the non-empty stacks
        let mut non_empty_stacks = Vec::<Vec<Square>>::new();
        for row in 0..1 {
            for col in 0..4 {
                if arr[row][col].len() > 0 {
                    non_empty_stacks.push(arr[row][col].clone());
                }
            }
        }
        // Verify
        if non_empty_stacks.len() == 1 {
            (0..8).all(|k| non_empty_stacks[0][k].label == k + 1)
                || (0..8).all(|k| non_empty_stacks[0][k].label == 8 - k)
        } else {
            false
        }
    }

    fn brief_arrangement(arr: [[Vec<Square>; 4]; 2]) -> String {
        let mut out_string = String::new();
        // Collect all the non-empty stacks
        let mut non_empty_stacks = Vec::<Vec<Square>>::new();
        for row in 0..1 {
            for col in 0..4 {
                if arr[row][col].len() > 0 {
                    non_empty_stacks.push(arr[row][col].clone());
                }
            }
        }
        // Verify
        let stack = non_empty_stacks.pop();
        match stack {
            Some(s) => {
                for k in s {
                    out_string.push_str(&format!("{}", k.label));
                }
            }
            None => {}
        }
        out_string
    }

    fn describe(&self) -> String {
        format!("({}, {})", &self.label, &self.facing.describe())
    }

    fn describe_stack(stack: Vec<Square>) -> String {
        let mut out_string = String::new();
        let mut first: bool = true;
        let mut first_on_line: bool = true;
        let mut col = 14;
        for &sq in &stack {
            if !first {
                out_string.push(',');
                col += 1;
            } else {
                first = false;
            }
            let to_add = &sq.describe();
            if col + to_add.len() + 2 > 60 {
                out_string.push('\n');
                for _ in 0..14 {
                    out_string.push(' ');
                }
                col = to_add.len() + 14;
                first_on_line = true;
            } else {
                col += to_add.len();
            }
            if !first_on_line {
                out_string.push(' ');
                col += 1;
            } else {
                first_on_line = false;
            }
            out_string.push_str(&to_add);
        }
        out_string
    }

    fn describe_arrangement(arr: [[Vec<Square>; 4]; 2]) -> String {
        let mut out_string = String::new();
        for row in 0..2 {
            for col in 0..4 {
                out_string.push_str(&format!(
                    "row {}, col {}: {}\n",
                    row + 1,
                    col + 1,
                    Square::describe_stack(arr[row][col].clone())
                ))
            }
        }
        out_string
    }

    fn draw_arrangement(arr: [[Vec<Square>; 4]; 2]) -> String {
        let mut out_string = String::from("       col\n   ");
        for k in 1..5 {
            out_string.push_str(&format!("     {}", k));
        }
        for row in 0..2 {
            for subrow in 0..5 {
                if subrow == 2 {
                    out_string.push_str(&format!("\nrow {}", row + 1));
                } else if subrow != 4 || row == 1 {
                    out_string.push_str("\n     ");
                }
                for col in 0..4 {
                    // Top border
                    if subrow == 0 || (row == 1 && subrow == 4) {
                        out_string.push('+');
                        if ((row == 0 || subrow == 4) && arr[row][col].len() > 0)
                            || (row == 1
                                && subrow == 0
                                && (arr[0][col].len() + arr[1][col].len() > 1))
                        {
                            out_string.push_str("-----");
                        } else {
                            out_string.push_str(". . .");
                        }
                        if col == 3 {
                            out_string.push('+');
                            if row == 1 && subrow == 0 {
                                out_string.push_str("<--lengthwise");
                            }
                        }
                    }
                    // middle of cell
                    else if row != 0 || subrow != 4 {
                        // non-empty cell
                        if (col == 0 && arr[row][0].len() > 0)
                            || (col > 0 && arr[row][col - 1].len() + arr[row][col].len() > 0)
                        {
                            if subrow != 2 || arr[row][col].len() == 0 {
                                out_string.push_str("|     ");
                            } else {
                                let sq = arr[row][col][0];
                                let (format_left, format_right) = match sq.facing {
                                    Facing::Up => (" ", " "),
                                    Facing::Down => ("[", "]"),
                                };
                                out_string.push_str(&format!(
                                    "| {}{}{} ",
                                    format_left, sq.label, format_right,
                                ));
                            }
                            if col == 3 {
                                if arr[row][3].len() > 0 {
                                    out_string.push('|');
                                } else {
                                    out_string.push('.');
                                }
                            }
                        }
                        // empty cell
                        else {
                            out_string.push_str(".     ");
                            if col == 3 {
                                out_string.push('.');
                            }
                        }
                    }
                }
            }
        }
        out_string.push_str("\n           ^     ^     ^");
        out_string.push_str("\n           |     |     |");
        out_string.push_str("\n           |     |     +--right vertical");
        out_string.push_str("\n           |     +--center vertical");
        out_string.push_str("\n           +---left vertical");
        out_string
    }
}

fn find_solution(arr: [[Vec<Square>; 4]; 2], verbose: bool, num_only: bool) -> Option<Vec<Fold>> {
    for (idx, (crease_perm, num)) in ALL_CREASES
        .iter()
        .permutations(4)
        .cartesian_product(0..16)
        .enumerate()
    {
        let temp_arr = arr.clone();
        let pattern = Crease::with_types(crease_perm, CreaseType::num_to_crease_types(num));
        if verbose {
            let p2 = pattern.clone();
            println!("trying #{}/384, {})", idx + 1, describe_pattern(p2));
        }
        let p3 = pattern.clone();
        let (outcome, outcome_arr) = Fold::verify_sequence(p3, temp_arr);
        if verbose {
            let temp_arr2 = outcome_arr.clone();
            println!("outcome:\n{}", Square::describe_arrangement(temp_arr2));
        }
        if num_only {
            println!("{}", Square::brief_arrangement(outcome_arr));
        }
        if verbose {
            println!("---");
        }
        if outcome {
            return Some(pattern);
        }
    }
    None
}

fn describe_pattern(p: Vec<Fold>) -> String {
    let mut out_str = String::new();
    let mut first = true;
    for k in p {
        if !first {
            out_str.push_str(", ");
        } else {
            first = false;
        }
        out_str.push_str(&k.describe());
    }
    out_str
}

fn creases_left(arr: [[Vec<Square>; 4]; 2]) -> Vec<Crease> {
    let mut to_return = Vec::<Crease>::new();
    let row_sum = (0..2)
        .map(|r| {
            (0..4)
                .map(|c| arr[r][c].len())
                .collect::<Vec<usize>>()
                .into_iter()
                .sum()
        })
        .collect::<Vec<usize>>();
    let col_sum = (0..4)
        .map(|c| {
            (0..2)
                .map(|r| arr[r][c].len())
                .collect::<Vec<usize>>()
                .into_iter()
                .sum()
        })
        .collect::<Vec<usize>>();
    if row_sum[0] != 0 && row_sum[1] != 0 {
        to_return.push(Crease::Lengthwise);
    }
    if col_sum[0] != 0 && col_sum[1] != 0 {
        to_return.push(Crease::VerticalLeft)
    }
    if col_sum[1] != 0 && col_sum[2] != 0 {
        to_return.push(Crease::VerticalCenter)
    }
    if col_sum[2] != 0 && col_sum[3] != 0 {
        to_return.push(Crease::VerticalRight)
    }
    to_return
}

fn interactive(mut arr: [[Vec<Square>; 4]; 2]) {
    loop {
        let arr_to_show = arr.clone();
        let arr_to_show2 = arr.clone();
        println!("---\n{}\n", &Square::draw_arrangement(arr_to_show2));
        println!("---\n{}\n", Square::describe_arrangement(arr_to_show));
        let cl = creases_left(arr.clone());
        if cl.len() == 0 {
            break;
        }
        println!("Which crease?");
        for (idx, crease) in cl.iter().enumerate() {
            println!("{}: fold {}", idx + 1, crease.describe());
        }
        println!("0: Quit");
        let mut crease_choice = String::new();
        io::stdin()
            .read_line(&mut crease_choice)
            .expect("Failed to read line");

        let crease_choice = match crease_choice.trim().parse::<usize>() {
            Ok(num) => {
                if num > 0 && num < cl.len() + 1 {
                    cl[num - 1]
                } else if num == 0 {
                    break;
                } else {
                    println!("Invalid input.");
                    continue;
                }
            }
            Err(_) => {
                println!("Invalid input.");
                continue;
            }
        };

        println!("How?");
        for (idx, ct) in ALL_CREASE_TYPES.iter().enumerate() {
            println!(
                "{}: fold {} {}",
                idx + 1,
                crease_choice.describe(),
                ct.describe()
            );
        }
        let mut ct_choice = String::new();
        io::stdin()
            .read_line(&mut ct_choice)
            .expect("Failed to read line");

        let ct_choice = match ct_choice.trim().parse::<usize>() {
            Ok(num) => {
                if num > 0 && num < 3 {
                    ALL_CREASE_TYPES[num - 1]
                } else {
                    println!("Invalid input.");
                    continue;
                }
            }
            Err(_) => {
                println!("Invalid input.");
                continue;
            }
        };
        let fold = crease_choice.to_fold(ct_choice);
        println!("Chosen move: {}", fold.describe());
        arr = fold.on(arr);
    }
    if Square::verify_arrangement(arr) {
        println!("You won! Good job!");
    } else {
        println!("Sorry, try again.");
    }
}

fn parse_arguments(args: Vec<String>) -> (Option<String>, bool, bool, bool, bool) {
    let mut interactive_mode = false;
    let mut verbose = false;
    let mut brief = false;
    let mut find_all = false;
    let mut filename: Option<String> = None;
    for k in 1..args.len() {
        if args[k] == "--interactive" {
            interactive_mode = true;
        } else if args[k] == "--verbose" {
            verbose = true;
        } else if args[k] == "--brief" {
            brief = true;
        } else if args[k] == "--find-all" {
            find_all = true;
        } else {
            filename = Some(args[k].clone());
        }
    }
    (filename, interactive_mode, verbose, brief, find_all)
}

fn read_file(filename: String) -> Option<[[Vec<Square>; 4]; 2]> {
    let initial_text = fs::read_to_string(&filename).expect(&format!("Unable to read file"));
    let raw_text = initial_text.trim();
    let raw_rows = raw_text.split("\n").collect::<Vec<&str>>();
    if raw_rows.len() != 2 {
        return None;
    }
    let mut arr: [[usize; 4]; 2] = [[0; 4]; 2];
    for (row_num, row_text) in raw_rows.into_iter().enumerate() {
        let row = row_text.split(",").map(|x| x.trim()).collect::<Vec<&str>>();
        if row.len() != 4 {
            return None;
        }
        for (col_num, col_text) in row.into_iter().enumerate() {
            let col_opt = col_text.trim().parse::<usize>();
            let col_val = match col_opt {
                Ok(num) => num,
                Err(_) => {
                    return None;
                }
            };
            arr[row_num][col_num] = col_val;
        }
    }
    Some(make_arr(arr))
}

fn find_all_solvable() {
    let perms = (1..9).permutations(8);
    for k in perms {
        let mut arr_raw = [[0; 4]; 2];
        for (idx, val) in k.into_iter().enumerate() {
            let row = idx / 4;
            let col = idx % 4;
            arr_raw[row][col] = val;
        }
        let arr = make_arr(arr_raw.clone());
        match find_solution(arr, false, false) {
            Some(_) => {
                println!("---");
                for row in arr_raw {
                    println!("{} {} {} {}", row[0], row[1], row[2], row[3]);
                }
            }
            _ => {}
        }
    }
}

fn main() {
    let mut arr = make_arr([[3, 4, 5, 6], [2, 1, 8, 7]]);
    let mut file_error = false;
    let args: Vec<String> = env::args().collect();
    let (filename, interactive_mode, verbose, brief, find_all) = parse_arguments(args);
    if find_all {
        find_all_solvable();
    } else {
        match filename {
            Some(f) => match read_file(f) {
                Some(new_arr) => {
                    arr = new_arr;
                }
                None => {
                    file_error = true;
                }
            },
            None => {}
        }
        if file_error {
            println!("Could not read file.");
        } else if interactive_mode {
            interactive(arr);
        } else {
            let soln = find_solution(arr, verbose, brief);
            match soln {
                Some(pattern) => {
                    for k in pattern {
                        println!("{}", k.describe());
                    }
                }
                None => {
                    println!("No solution found.")
                }
            }
        }
    }
}
