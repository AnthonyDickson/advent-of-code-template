// swift-tools-version: 6.2
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
  name: "AoC",
  platforms: [
    .macOS(.v14)
  ],
  products: [
    .executable(name: "aoc-cli", targets: ["AoCCLI"])  // Define the final executable product
  ],
  targets: [
    .target(name: "AoC", path: "Sources/AoC"),
    .executableTarget(name: "AoCCLI", dependencies: ["AoC"], path: "Sources/AoCCLI"),
    .testTarget(
      name: "AoCTests",
      dependencies: ["AoC"]
    ),
  ]
)
