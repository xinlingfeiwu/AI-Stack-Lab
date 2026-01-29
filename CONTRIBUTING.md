# Contributing to AI Stack Lab 🤝

Thank you for your interest in contributing to AI Stack Lab! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Style Guidelines](#style-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. Please:

- Be respectful and considerate in all interactions
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Accept differing viewpoints gracefully

## How Can I Contribute?

### 🐛 Reporting Bugs

If you find a bug, please create an issue with:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Node.js version, etc.)
- Screenshots if applicable

### 💡 Suggesting Features

We welcome feature suggestions! Please:

- Check existing issues to avoid duplicates
- Provide a clear description of the feature
- Explain the use case and benefits
- Consider implementation details if possible

### 📝 Improving Documentation

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add missing information
- Improve code examples
- Translate content (with maintainer approval)

### 💻 Contributing Code

Code contributions can include:

- Bug fixes
- New features
- Performance improvements
- Test coverage improvements

## Getting Started

### Prerequisites

- **Node.js** >= 18.0.0
- **Python** >= 3.10
- **Git** for version control

### Setup

1. **Fork the repository**
   
   Click the "Fork" button on GitHub to create your own copy.

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/AI-Stack-Lab.git
   cd AI-Stack-Lab
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/xinlingfeiwu/AI-Stack-Lab.git
   ```

4. **Install dependencies** (for example projects)
   ```bash
   cd 01-MCP/01-Foundation/examples/typescript-hello-world
   npm install
   ```

## Development Workflow

1. **Sync with upstream**
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   
   - Write clean, readable code
   - Add comments where necessary
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # For TypeScript examples
   npm run build
   npm start
   
   # For Python examples
   python server.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(scope): add your feature description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**

## Style Guidelines

### Documentation

- Use clear, concise language
- Include code examples where helpful
- Use proper Markdown formatting
- Add diagrams for complex concepts

### TypeScript/JavaScript

- Use TypeScript for type safety
- Follow ES6+ conventions
- Use meaningful variable names
- Add JSDoc comments for functions

```typescript
/**
 * Greets a user with a personalized message
 * @param name - The name of the user to greet
 * @returns A greeting message
 */
function greet(name: string): string {
  return `Hello, ${name}!`;
}
```

### Python

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions

```python
def greet(name: str) -> str:
    """
    Greets a user with a personalized message.
    
    Args:
        name: The name of the user to greet
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}!"
```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Code style changes (formatting, etc.) |
| `refactor` | Code refactoring |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |

### Scopes

- `mcp` - MCP module related
- `skills` - Skills module related
- `examples` - Example code
- `deps` - Dependencies

### Examples

```bash
feat(mcp): add weather data aggregation server
fix(examples): resolve TypeScript compilation error
docs(mcp): update environment setup instructions
chore(deps): upgrade @modelcontextprotocol/sdk to v1.1.0
```

## Pull Request Process

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] Self-reviewed the changes
- [ ] Added/updated documentation if needed
- [ ] Tested the changes locally
- [ ] Commit messages follow conventions

### PR Title Format

Use the same format as commit messages:

```
feat(mcp): add new tool for database queries
```

### PR Description Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Other (please describe)

## Testing
Describe how you tested the changes.

## Checklist
- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have added necessary documentation
- [ ] My changes generate no new warnings
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged

## 🎉 Recognition

Contributors will be recognized in:

- The project README
- Release notes for significant contributions
- GitHub contributors list

## ❓ Questions?

If you have questions:

- Open a [Discussion](https://github.com/xinlingfeiwu/AI-Stack-Lab/discussions)
- Check existing issues and discussions
- Reach out to maintainers

---

Thank you for contributing to AI Stack Lab! Your contributions help make this project better for everyone. 🚀
