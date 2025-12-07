public func solvePartOne(_ input: String) -> Int {
  var floor = 0

  for char in input {
    switch char {
    case "(":
      floor += 1
    case ")":
      floor -= 1
    default:
      fatalError("Invalid char \(char)")
    }
  }

  return floor
}

public func solvePartTwo(_ input: String) -> Int {
  var floor = 0

  for (i, char) in input.enumerated() {
    switch char {
    case "(":
      floor += 1
    case ")":
      floor -= 1
    default:
      fatalError("Invalid char \(char)")
    }

    if floor == -1 {
      return 1 + i
    }
  }

  return 0
}
