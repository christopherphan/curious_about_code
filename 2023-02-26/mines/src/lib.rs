// file: mines/src/lib.rs

pub struct MineBoard {
    num_rows: u16,
    num_cols: u16,
    mine_loc: Vec<(u16, u16)>,
}

impl TryFrom<&str> for MineBoard {
    type Error = &'static str;

    fn try_from(s: &str) -> Result<Self, Self::Error> {
        let s_string = s.to_string();
        let row_strings = s_string.split_whitespace().collect::<Vec<&str>>();
        let num_rows = u16::try_from(row_strings.len());
        let num_cols = u16::try_from(row_strings[0].len());
        let num_rows = match num_rows {
            Ok(k) => k,
            Err(_) => {
                return Err("too many rows");
            }
        };
        let num_cols = match num_cols {
            Ok(k) => k,
            Err(_) => {
                return Err("too many columns");
            }
        };
        for k in &row_strings {
            let k_cols = u16::try_from(k.len());
            match k_cols {
                Ok(u) => {
                    if u != num_cols {
                        return Err("incompatible row lengths");
                    }
                }
                Err(_) => {
                    return Err("incompaible row lengths");
                }
            }
        }
        let mut mine_loc: Vec<(u16, u16)> = Vec::new();
        for (ridx, row) in row_strings.into_iter().enumerate() {
            for (cidx, col) in row.chars().enumerate() {
                if col == '*' {
                    mine_loc.push((ridx.try_into().unwrap(), cidx.try_into().unwrap()));
                }
            }
        }
        Ok(MineBoard {
            num_rows,
            num_cols,
            mine_loc,
        })
    }
}

impl MineBoard {
    pub fn mine_at(&self, row: i32, col: i32) -> bool {
        if row >= 0 && col >= 0 && row < (self.num_rows as i32) && col < (self.num_cols as i32) {
            for k in &self.mine_loc {
                if (k.0 as i32) == row && (k.1 as i32) == col {
                    return true;
                }
            }
        }
        false
    }

    pub fn mines_around(&self, row: u16, col: u16) -> i8 {
        let mut ret_val: i8 = 0;
        let srow = row as i32;
        let scol = col as i32;
        let to_test: Vec<(i32, i32)> = vec![
            (srow - 1, scol - 1),
            (srow - 1, scol),
            (srow - 1, scol + 1),
            (srow, scol - 1),
            (srow, scol + 1),
            (srow + 1, scol - 1),
            (srow + 1, scol),
            (srow + 1, scol + 1),
        ];
        for k in to_test {
            if self.mine_at(k.0, k.1) {
                ret_val += 1;
            }
        }
        ret_val
    }

    fn bomb_counts(&self, row: u16, col: u16) -> i8 {
        if self.mine_at(row as i32, col as i32) {
            -1
        } else {
            self.mines_around(row, col)
        }
    }

    pub fn adjacent_bomb_counts(&self) -> Vec<Vec<i8>> {
        (0..self.num_rows)
            .map(|row| {
                (0..self.num_cols)
                    .map(|col| self.bomb_counts(row, col))
                    .collect()
            })
            .collect()
    }
}

