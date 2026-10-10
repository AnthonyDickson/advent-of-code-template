const std = @import("std");

const max_file_size = 1024 * 1024; // 1 MiB
const input_filename = "input.txt";
const stdout_buffer_size = 1024;

pub fn main(init: std.process.Init) !void {
    const io = init.io;
    const allocator = init.arena.allocator();

    const input = std.Io.Dir.cwd().readFileAlloc(io, input_filename, allocator, .limited(max_file_size)) catch |err| {
        std.log.err("Could not open {s}: {}", .{ input_filename, err });
        return err;
    };

    const part_one = solvePartOne(input);
    const part_two = solvePartTwo(input);

    var stdout_buffer: [stdout_buffer_size]u8 = undefined;
    var stdout_writer = std.Io.File.stdout().writer(io, &stdout_buffer);
    const stdout = &stdout_writer.interface;

    try stdout.print("{d}\n", .{part_one});
    try stdout.print("{d}\n", .{part_two});

    try stdout.flush();
}

fn step(char: u8) i64 {
    return switch (char) {
        '(' => 1,
        ')' => -1,
        else => 0,
    };
}

fn solvePartOne(input: []const u8) i64 {
    var floor: i64 = 0;

    for (input) |char| {
        floor += step(char);
    }

    return floor;
}

fn solvePartTwo(input: []const u8) i64 {
    var floor: i64 = 0;

    for (input, 0..) |char, i| {
        floor += step(char);

        if (floor == -1) {
            return @intCast(i + 1);
        }
    }

    return 0;
}

test "part one" {
    const cases = [_]struct { []const u8, i64 }{
        .{ "(())", 0 },
        .{ "()()", 0 },
        .{ "(((", 3 },
        .{ "(()(()(", 3 },
        .{ "))(((((", 3 },
        .{ "())", -1 },
        .{ "))(", -1 },
        .{ ")))", -3 },
        .{ ")())())", -3 },
    };

    for (cases) |case| {
        const input, const expected = case;

        const actual = solvePartOne(input);

        try std.testing.expectEqual(expected, actual);
    }
}

test "part two" {
    const cases = [_]struct { []const u8, i64 }{
        .{ ")", 1 },
        .{ "()())", 5 },
    };

    for (cases) |case| {
        const input, const expected = case;

        const actual = solvePartTwo(input);

        try std.testing.expectEqual(expected, actual);
    }
}
