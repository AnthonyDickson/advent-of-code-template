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
    var floor: i64 = 0;

    for (input) |char| {
        switch (char) {
            '(' => floor += 1,
            ')' => floor -= 1,
            else => @panic("Illegal char found, only '(' and ')' are allowed."),
        }
    }

    return floor;
}

fn solve_part_two(input: []const u8) i64 {
    var floor: i64 = 0;

    for (input, 0..) |char, i| {
        switch (char) {
            '(' => floor += 1,
            ')' => floor -= 1,
            else => @panic("Illegal char found, only '(' and ')' are allowed."),
        }

        if (floor == -1) {
            return 1 + @as(i64, @intCast(i));
        }
    }

    return 0;
}

test "test part one" {
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

        const actual = solve_part_one(input);

        std.testing.expectEqual(expected, actual) catch |err| {
            std.debug.print("test failed for input {s}\n", .{input});
            return err;
        };
    }
}

test "test part two" {
    const cases = [_]struct { []const u8, i64 }{
        .{ ")", 1 },
        .{ "()())", 5 },
    };

    for (cases) |case| {
        const input, const expected = case;

        const actual = solve_part_two(input);

        std.testing.expectEqual(expected, actual) catch |err| {
            std.debug.print("test failed for input {s}\n", .{input});
            return err;
        };
    }
}
