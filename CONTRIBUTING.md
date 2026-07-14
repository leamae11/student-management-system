# Contributing Guidelines

## Welcome!

Thank you for your interest in contributing to the CS Student Dashboard project! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- No harassment or discrimination
- Report violations to maintainers

## How to Contribute

### 1. Fork the Repository

```bash
git clone https://github.com/YOUR_USERNAME/student-management-system.git
cd student-management-system
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes

- Write clean, readable code
- Follow PEP 8 style guide
- Add comments for complex logic
- Write tests for new features

### 4. Test Your Changes

```bash
python manage.py test
```

### 5. Commit Your Changes

```bash
git commit -m "Add feature: Brief description of what was added"
```

### 6. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request

- Go to the original repository
- Click "New Pull Request"
- Provide clear description of changes
- Link related issues

## Coding Standards

- Follow PEP 8
- Classes: PascalCase
- Functions/Methods: snake_case
- Constants: UPPER_SNAKE_CASE

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
```