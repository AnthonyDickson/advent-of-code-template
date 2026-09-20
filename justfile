default:
    @just --list

# Move the nixpkgs and rust-overlay pins in flake.lock to their latest revisions.
update-flake:
    nix flake update

# Bump the dprint plugins pinned in dprint.json.
update-dprint:
    dprint config update
