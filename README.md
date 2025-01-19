# Rust-LLDB Integration

This crate allows you to derive the `DebugPrint` trait that adds a single function which returns the type formatted by the debug formatter.

Then `formatters.py` calls that function for every implementing type when you `p` or `po` a pointer to that type in lldb.

## Usage

In lldb, run `command script import <path to formatters.py>` then print a pointer to any type which derives the `DebugPrint` trait.
