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

fn solvePartOne(input: []const u8) i64 {
    _ = input;
    return 0;
}

fn solvePartTwo(input: []const u8) i64 {
    _ = input;
    return 0;
}

test "part one" {
    const input = "";
    const expected = 0;

    const actual = solvePartOne(input);

    try std.testing.expectEqual(expected, actual);
}

test "part two" {
    const input = "";
    const expected = 0;

    const actual = solvePartTwo(input);

    try std.testing.expectEqual(expected, actual);
}
