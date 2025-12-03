const std = @import("std");

const MAX_FILE_SIZE = 1024 * 1024; // 1 MiB
const INPUT_FILENAME = "input.txt";
const STDOUT_BUFFER_SIZE = 1024;

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const input = std.fs.cwd().readFileAlloc(allocator, INPUT_FILENAME, MAX_FILE_SIZE) catch |err| {
        std.debug.print("Could not open {s}: {}\n", .{ INPUT_FILENAME, err });
        return err;
    };

    const part1_result = solve_part_one(input);
    const part2_result = solve_part_two(input);

    var stdout_buffer: [STDOUT_BUFFER_SIZE]u8 = undefined;
    var stdout_writer = std.fs.File.stdout().writer(&stdout_buffer);
    const stdout = &stdout_writer.interface;

    try stdout.print("{d}\n", .{part1_result});
    try stdout.print("{d}\n", .{part2_result});

    try stdout.flush();
}

fn solve_part_one(input: []const u8) i64 {
    _ = input; // autofix
    return 0;
}

fn solve_part_two(input: []const u8) i64 {
    _ = input; // autofix
    return 0;
}

test "test part one" {
    const input = "";
    const expected = 0;

    const actual = solve_part_one(input);

    try std.testing.expectEqual(expected, actual);
}

test "test part two" {
    const input = "";
    const expected = 0;

    const actual = solve_part_two(input);

    try std.testing.expectEqual(expected, actual);
}
