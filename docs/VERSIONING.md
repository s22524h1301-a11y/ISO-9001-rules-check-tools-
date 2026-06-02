# Versioning and Commit Rules

This project uses a simple SemVer-based workflow so that progress is easy to follow over time.

## Version Format

- `v0.x.y` means the project is still evolving
- `x` changes when we finish a meaningful feature stage
- `y` changes for small fixes, documentation updates, and minor adjustments

## Version Types

- `patch` for documentation updates, bug fixes, and small improvements
- `minor` for new user-visible features
- `major` for breaking changes to workflow or output format

## Commit Types

- `docs:` documentation changes
- `feat:` new features
- `fix:` bug fixes
- `refactor:` internal code restructuring without behavior change
- `test:` test updates
- `chore:` maintenance or tooling updates

## Release Flow

1. Update the code or documentation
2. Update `pyproject.toml` if the version should change
3. Update `CHANGELOG.md`
4. Commit with a clear message
5. Push to GitHub
6. Add a Git tag when the change marks a meaningful release

## Recommended Convention

Use these as a guide:

- Documentation only: `v0.1.1` -> `v0.1.2`
- Small fix: `v0.1.1` -> `v0.1.2`
- New feature: `v0.1.1` -> `v0.2.0`
- Breaking change: `v0.1.1` -> `v1.0.0`

## Why This Helps

- Visitors can see the project is actively evolving
- Maintainers can keep releases consistent
- GitHub history stays easy to read
- `CHANGELOG.md` becomes a reliable record of progress
