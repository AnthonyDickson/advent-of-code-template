# The entry point: it reads `input.txt` and prints both answers, one per line.

use src/aoc.nu [solve-part-one, solve-part-two]

def main [] {
    let input = open --raw input.txt
    print (solve-part-one $input)
    print (solve-part-two $input)
}
