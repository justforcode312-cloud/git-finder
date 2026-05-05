# Quick Start Guide

## Installation (30 seconds)

### Windows
1. Open terminal in the project directory
2. Run: `install.bat`
3. Done! ✅

### Linux/Mac
1. Open terminal in the project directory
2. Run: `chmod +x install.sh && ./install.sh`
3. Done! ✅

## Usage

### See today's commits from all your projects
```bash
# Interactive - will prompt for directory
gf

# Or specify a directory
gf ~/projects
gf C:\Users\YourName\Documents
```

### List all Git projects (without commits)
```bash
gf --list
gf ~/projects --list
```

## Examples

### Example 1: Check what you worked on today
```bash
$ gf ~/work

================================================================================
TODAY'S COMMITS (2026-05-05)
================================================================================

website - Fix responsive layout on mobile
website - Update homepage content
api-server - Add authentication middleware
api-server - Fix database connection pool
mobile-app - No commits

================================================================================
Total: 4 commit(s) across 3 project(s)
================================================================================
```

### Example 2: Find all your Git projects
```bash
$ gf ~/projects --list

Found 5 Git project(s) under: /home/user/projects

#     Project Name                   Path
--------------------------------------------------------------------------------
1     api-server                     /home/user/projects/api-server
2     mobile-app                     /home/user/projects/mobile-app
3     website                        /home/user/projects/website
4     scripts                        /home/user/projects/scripts
5     tools                          /home/user/projects/tools
```

## Tips

- Use `gf` instead of `git-finder` for faster typing
- Run `gf` without arguments for interactive mode
- Use `gf .` to search from current directory
- Add to your daily routine to track your work

## Common Use Cases

### Daily standup preparation
```bash
gf ~/work
```
Quickly see what you committed yesterday/today for standup meetings.

### Project discovery
```bash
gf ~ --list
```
Find all Git repositories on your system.

### Weekly review
```bash
gf ~/projects
```
Review your commits across all projects.

## Need Help?

```bash
gf --help
```

For detailed documentation, see [README.md](README.md)
