# 🤝 Contribution Guidelines

Thank you for your interest in contributing to **Oracle Support AI**! This document provides guidelines for contributing to our project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Types of Contributions](#types-of-contributions)
- [Submission Process](#submission-process)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

### Our Pledge
We are committed to providing a welcoming and inspiring community for all.

### Our Standards
- Use welcoming and inclusive language
- Be respectful of differing opinions and experiences
- Accept constructive criticism gracefully
- Focus on what is best for the community

---

## Getting Started

### 1. Fork the Repository
```bash
gh repo fork Mahendarreddy143/oracle-support-ai --clone
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/issue-xyz
```

### 3. Set Up Development Environment
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 4. Make Your Changes
- Keep commits atomic and focused
- Follow coding standards (see below)
- Add tests for new features
- Update documentation

### 5. Test Locally
```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend && npm test

# Docker
docker-compose up
```

---

## Types of Contributions

### 🐛 Bug Reports
- Create an issue with detailed reproduction steps
- Include error messages and logs
- Specify your environment (OS, Python version, etc.)
- Suggest a fix if you have one

### ✨ Feature Requests
- Describe the use case clearly
- Provide examples or mockups if applicable
- Explain how this benefits users
- Discuss potential implementation approaches

### 📝 Documentation
- Fix typos and clarify instructions
- Add missing documentation
- Create tutorials or guides
- Improve API documentation

### 💻 Code Contributions
- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test additions

### 📚 Knowledge Base
- Add new issues and solutions
- Create code samples
- Share best practices
- Contribute error solutions

---

## Submission Process

### Step 1: Check Existing Issues
Before starting work, check if the issue/feature already exists.

### Step 2: Create an Issue (if needed)
```markdown
## Description
Clear description of the problem or feature.

## Steps to Reproduce
1. Step 1
2. Step 2

## Expected Behavior
What should happen

## Actual Behavior
What currently happens

## Environment
- OS: 
- Python: 
- Version: 
```

### Step 3: Create Feature Branch
```bash
git checkout -b feature/ISSUE-123-brief-description
```

### Step 4: Commit & Push
```bash
git add .
git commit -m "feat(module): description"
git push origin feature/ISSUE-123
```

### Step 5: Create Pull Request
- Link to related issue
- Describe your changes
- Include any breaking changes
- Add screenshots if applicable

---

## Coding Standards

### Python
```python
# Follow PEP 8
# Use type hints
def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate semantic similarity between two texts.
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score (0-1)
    """
    pass

# Use f-strings
message = f"Processing {item_count} items"

# Meaningful variable names
user_email = "user@example.com"  # Good
ue = "user@example.com"  # Bad
```

### JavaScript/TypeScript
```typescript
// Use const by default
const MAX_ITEMS = 100;
let count = 0;

// Use meaningful names
const getUserById = async (id: string): Promise<User> => {
  // implementation
};

// Add JSDoc comments
/**
 * Fetch user data from API
 * @param id - User ID
 * @returns User object or null
 */
```

### SQL
```sql
-- Use uppercase for keywords
-- Use meaningful aliases
SELECT 
    u.user_id,
    u.email,
    COUNT(i.issue_id) as total_issues
FROM users u
LEFT JOIN issues i ON u.user_id = i.created_by
GROUP BY u.user_id, u.email
ORDER BY total_issues DESC;
```

---

## Commit Message Guidelines

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation
- **style**: Code style (formatting)
- **refactor**: Code refactoring
- **perf**: Performance improvement
- **test**: Adding/updating tests
- **chore**: Build, dependencies, etc.

### Examples
```bash
git commit -m "feat(search): add semantic similarity scoring"
git commit -m "fix(api): correct pagination offset calculation"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(backend): add unit tests for embeddings"
```

---

## Pull Request Process

### PR Title Format
```
[TYPE] Description of changes

Examples:
[FEATURE] Add semantic search capability
[FIX] Resolve issue with pagination
[DOCS] Update API documentation
```

### PR Description Template
```markdown
## Description
Brief description of changes

## Related Issue
Closes #123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes
- Change 1
- Change 2

## Testing
How to test these changes:
1. Step 1
2. Step 2

## Screenshots
(if applicable)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] No new warnings generated
```

### Review Process
1. Automated checks must pass
2. At least 1 maintainer review required
3. All conversations resolved
4. Squash and merge

---

## Issue Templates

### Bug Report
- Title: [BUG] Brief description
- Use bug report template
- Add labels: bug, priority level
- Link related issues

### Feature Request
- Title: [FEATURE] Brief description
- Use feature template
- Provide use case & benefits
- Add labels: enhancement, module

### Documentation
- Title: [DOCS] Brief description
- Specify missing or unclear areas
- Provide suggestions
- Add labels: documentation

---

## Resources

- **Documentation**: [docs/](../docs/)
- **Issues**: [GitHub Issues](https://github.com/Mahendarreddy143/oracle-support-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Mahendarreddy143/oracle-support-ai/discussions)
- **License**: [MIT License](../LICENSE)

---

## Questions?

Feel free to open a discussion or reach out to the maintainers.

**Thank you for contributing! 🙏**
