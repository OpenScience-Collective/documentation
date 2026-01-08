# Contributing

Thank you for your interest in contributing to the Open Science Collective! We welcome contributions of all kinds from everyone.

## Development Workflow

All development follows: **Issue -> Feature Branch -> PR -> Review -> Merge**

1. **Pick an issue** from GitHub Issues
2. **Create feature branch**: `git checkout -b feature/issue-N-short-description`
3. **Implement** with atomic commits
4. **Create PR** with `gh pr create`
5. **Address review findings** before merging
6. **Merge with merge commit** (never squash)

```bash
# Example workflow
gh issue list                                    # Find issue to work on
git checkout -b feature/issue-7-description      # Create branch
# ... implement ...
git add -A && git commit -m "feat: add X"        # Atomic commits
gh pr create --title "feat: add X" --body "Closes #7"
git push -u origin feature/issue-7-description
gh pr merge --merge --delete-branch              # Merge commit, never squash
```

## Ways to Contribute

### Code Contributions

- Fix bugs or implement new features
- Improve test coverage (with real tests, no mocks)
- Refactor and optimize existing code

### Documentation

- Fix typos and improve clarity
- Add examples and tutorials
- Improve API documentation

### Community

- Answer questions from other users
- Report bugs and suggest features
- Share your use cases and feedback

## Setting Up Your Environment

```bash
# Clone the repository
git clone https://github.com/OpenScience-Collective/osa
cd osa

# Install dependencies with uv
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest tests/ -v
```

## Code Style

We use [Ruff](https://docs.astral.sh/ruff/) for Python linting and formatting:

```bash
# Check code style
uv run ruff check .

# Format code
uv run ruff format .
```

### Guidelines

- Type hints required for all public APIs
- Docstrings for public functions and classes (Google style)
- Atomic commits with concise messages, no emojis
- Pre-commit hooks for automatic formatting

## Testing

- **NO MOCKS**: Real tests with real data only
- **Dynamic tests**: Query registries/configs, don't hardcode values
- **Coverage**: >70% minimum
- Run `uv run pytest --cov` before committing

## Questions?

If you have questions or need help:

- Open an issue on GitHub
- Start a discussion in the repository
