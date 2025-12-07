import AoC
import Foundation

func readInput(filename: String) throws -> String {
  let fileURL = URL(fileURLWithPath: filename)
  return try String(contentsOf: fileURL, encoding: .utf8)
}

@main
struct AoC {
  static func main() {
    do {
      let input = try readInput(filename: "input.txt")

      print(solvePartOne(input))
      print(solvePartTwo(input))
    } catch {
      print("Error reading file: \(error)")
    }
  }
}
