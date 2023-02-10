/* Solution to puzzle "Fix the Chain!", posted by user miguelraz on
 * David Amos's "Curious About Code" site:
 *
 * https://discourse.davidamos.dev/t/code-challenge-fix-the-chain/132
 */

// Keeps track of where we are in the fixed chain
enum ChainPosition {
    Start(usize), // the next item to be returned is the vector at given position
    End(usize),   // the next item to be returned is the vector containing the 2nd item of
                  // current position, and the 1st item of the next position
}

// An iterator which fixes a chain: given a vector of tuples,
// it produces an interator such that the second element of each
// tuple is the first element of the next tuple
struct ChainFixer<T: Eq + Copy> {
    position: ChainPosition,
    original: Vec<(T, T)>,
}

impl<T: Eq + Copy> ChainFixer<T> {
    // Create a ChainFixer from the vector v
    fn from(v: Vec<(T, T)>) -> ChainFixer<T> {
        ChainFixer {
            position: ChainPosition::Start(0),
            original: v,
        }
    }
}

impl<T: Eq + Copy> Iterator for ChainFixer<T> {
    type Item = (T, T);

    fn next(&mut self) -> Option<Self::Item> {
        match self.position {
            ChainPosition::Start(k) => {
                if k < self.original.len() {
                    self.position = ChainPosition::End(k);
                    Some(self.original[k])
                } else {
                    None
                }
            }
            ChainPosition::End(k) => {
                if k + 1 < self.original.len() {
                    if self.original[k].1 != self.original[k + 1].0 {
                        self.position = ChainPosition::Start(k + 1);
                        Some((self.original[k].1, self.original[k + 1].0))
                    } else {
                        self.position = ChainPosition::End(k + 1);
                        Some(self.original[k + 1])
                    }
                } else {
                    None
                }
            }
        }
    }
}

fn main() {
    let v: Vec<(i32, i32)> = vec![(1, 1), (1, 2), (3, 4)];
    for k in ChainFixer::from(v) {
        println!("({}, {})", k.0, k.1);
    }
}
