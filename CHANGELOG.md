# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD workflows
- Comprehensive .gitignore file
- Issue and PR templates
- Dependabot configuration
- CodeQL security scanning
- Contributing guidelines
- Changelog

## [1.0.0] - 2026-05-05

### Added
- Initial release
- Find Git repositories in directory tree
- Display today's commits by default
- `--list` flag to show project list
- Two command aliases: `git-finder` and `gf`
- Cross-platform support (Windows, Linux, macOS)
- Interactive mode for directory selection
- Skip common non-repository directories for performance
- Timeout protection for Git commands
- Comprehensive documentation:
  - README.md
  - QUICKSTART.md
  - INSTALL.md
  - PROJECT_STRUCTURE.md
  - CODE_GUIDE.md
  - START_HERE.md
- Installation scripts:
  - install.bat (Windows)
  - install.sh (Linux/Mac)
  - test_install.py (verification)
- Well-documented, readable code with:
  - Section headers
  - Comprehensive docstrings
  - Inline comments
  - Type hints
  - Examples in docstrings

### Changed
- Default behavior shows commits instead of project list
- Organized project structure with dedicated folders:
  - `git_finder/` for source code
  - `scripts/` for installation scripts
  - `docs/` for documentation

### Security
- Added timeout to Git subprocess calls
- Input validation for directory paths
- Proper error handling throughout

## Version History

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward compatible manner
- PATCH version for backward compatible bug fixes

### Release Types

- **Major Release (X.0.0)**: Breaking changes, major new features
- **Minor Release (1.X.0)**: New features, backward compatible
- **Patch Release (1.0.X)**: Bug fixes, minor improvements

## Upgrade Guide

### From 0.x to 1.0.0
This is the initial stable release. No upgrade needed.

## Future Plans

### Planned Features
- [ ] Show commits from custom date ranges
- [ ] Filter by author
- [ ] Export results to file (JSON, CSV)
- [ ] Configuration file support
- [ ] Colored output
- [ ] Progress bar for large searches
- [ ] Git statistics (lines changed, files modified)
- [ ] Integration with GitHub/GitLab APIs

### Under Consideration
- [ ] GUI version
- [ ] Web dashboard
- [ ] Team collaboration features
- [ ] Commit analysis and insights

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute to this project.

## Links

- [Repository](https://github.com/yourusername/git-finder)
- [Issue Tracker](https://github.com/yourusername/git-finder/issues)
- [Documentation](README.md)

---

**Note**: This changelog is manually maintained. Please update it when making significant changes.
