# Contributing to ETF Flash Crash 2015 Educational Project

Thank you for your interest in contributing! This project welcomes contributions from students, educators, researchers, and finance professionals.

---

## 🎯 Project Status

**Core Track**: ✅ Production-ready
- 3 interactive notebooks
- 18 comprehensive guide files
- 4 detailed case studies
- All APIs tested and verified

**Extensions Track**: ⚠️ Work in Progress
- Infrastructure ready
- Notebooks need API corrections
- Research modules planned but not implemented

---

## 🤝 Ways to Contribute

### High Priority

**1. Fix Extensions Track Notebooks**
- **Issue**: API mismatches in `notebooks/extensions/01-market-maker-simulation.ipynb`
- **Details**: See code review comments in git history
- **Skills needed**: Python, Jupyter, market microstructure knowledge
- **Impact**: High - makes advanced content usable

**2. Implement Extension Modules**
- **Adverse Selection** (`src/extensions/adverse_selection.py`)
  - Glosten-Milgrom model
  - Probability of Informed Trading (PIN)
  - Requires: Econometrics background

- **Inventory Optimization** (`src/extensions/inventory_optimization.py`)
  - Avellaneda-Stoikov market making
  - Optimal quoting strategies
  - Requires: Stochastic control, dynamic programming

- **Contagion Analysis** (`src/extensions/contagion_analysis.py`)
  - Network analysis
  - CoVaR, Marginal Expected Shortfall
  - Requires: Network theory, risk management

**3. Additional Case Studies**
- Other ETFs from August 24, 2015 (EFA, EEM, VWO, etc.)
- International flash crashes (European ETFs, Asian markets)
- Other U.S. flash crashes (2010, 2020 COVID)
- **Format**: Follow existing case study structure in `guide/03-deep-dive/`

### Medium Priority

**4. Improve Visualizations**
- Interactive plotly charts for notebooks
- Animated timeline of August 24
- Network diagrams for market structure
- **Tools**: plotly, matplotlib, d3.js

**5. Additional Exercises and Solutions**
- More hands-on practice problems
- Solutions for extensions track exercises
- Graded difficulty levels
- **Format**: Jupyter notebooks

**6. Documentation Improvements**
- Clarify difficult concepts
- Add more worked examples
- Improve docstrings in source code
- Video tutorials or screencasts

### Lower Priority

**7. Testing**
- Increase test coverage (currently 108+ tests)
- Add integration tests
- Performance benchmarks
- **Framework**: pytest

**8. Internationalization**
- Translate guides to other languages
- Adapt case studies for non-US markets
- **Languages welcome**: Spanish, Chinese, French, German

---

## 📋 Before You Start

### Read These First

1. **[LEARNING_PATH.md](LEARNING_PATH.md)** - Understand the educational structure
2. **[README.md](README.md)** - Project overview and current status
3. **Core Track notebooks** - See what production-ready looks like

### Set Up Your Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/etf-flash-crash-2015.git
cd etf-flash-crash-2015

# Install dependencies
pip install -r requirements-full.txt

# Run tests to verify setup
pytest tests/
```

### Check Existing Issues

- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue before starting work
- Avoid duplicate efforts

---

## 🔧 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

**Branch naming**:
- `feature/` - New content or functionality
- `fix/` - Bug fixes or corrections
- `docs/` - Documentation improvements
- `test/` - Additional tests

### 2. Make Your Changes

**For Notebooks**:
- Test all cells execute without errors
- Clear all outputs before committing: `Cell > All Output > Clear`
- Add markdown cells explaining concepts
- Include visualization where helpful
- **Use code-reviewer workflow**: All notebooks should be reviewed

**For Python Code**:
- Follow PEP 8 style guide
- Add docstrings (Google style preferred)
- Include type hints
- Write unit tests for new functions
- Run tests: `pytest tests/`

**For Guide Files**:
- Use markdown format
- Follow existing structure (Prerequisites, Learning Objectives, etc.)
- Include real examples with data
- Add "See also" links to related content
- Keep reading time under 15 minutes

### 3. Test Thoroughly

**Notebooks**:
```bash
# Test that notebook runs without errors
jupyter nbconvert --to notebook --execute your-notebook.ipynb
```

**Python Code**:
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_your_module.py

# Check coverage
pytest --cov=src tests/
```

**Documentation**:
- Check all links work
- Verify markdown renders correctly
- Spellcheck with tool of choice

### 4. Commit Your Changes

**Commit Message Format**:
```
<type>: <short description>

<optional longer description>

<optional footer>
```

**Types**:
- `feat`: New feature or content
- `fix`: Bug fix or correction
- `docs`: Documentation only
- `test`: Adding or updating tests
- `refactor`: Code refactoring

**Examples**:
```bash
git commit -m "feat: Add EEM case study for August 24 crash"
git commit -m "fix: Correct API usage in market maker notebook"
git commit -m "docs: Improve NAV calculation explanation"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- **Clear title** describing the change
- **Description** explaining what and why
- **Link to issue** if applicable
- **Screenshots** for UI/visualization changes
- **Checklist** (see template below)

---

## ✅ Pull Request Checklist

Before submitting, ensure:

**General**:
- [ ] Code follows project style guidelines
- [ ] All tests pass (`pytest tests/`)
- [ ] No new warnings or errors
- [ ] Commit messages are clear and descriptive

**For Notebooks**:
- [ ] All cells execute without errors
- [ ] Outputs are cleared before committing
- [ ] Markdown cells explain concepts clearly
- [ ] APIs match actual module signatures (critical!)
- [ ] Educational value is clear

**For Python Code**:
- [ ] Docstrings added/updated
- [ ] Type hints included
- [ ] Unit tests added for new functions
- [ ] Code is PEP 8 compliant
- [ ] No unused imports or variables

**For Documentation**:
- [ ] Links verified and working
- [ ] Markdown renders correctly
- [ ] No typos or grammatical errors
- [ ] Consistent with existing style

---

## 📝 Style Guidelines

### Python Code

**Follow PEP 8** with these specifics:
- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings, single for characters
- **Imports**: Absolute imports, grouped (standard lib, third-party, local)

**Type Hints**:
```python
def calculate_nav(
    holdings: Dict[str, float],
    prices: Dict[str, float],
    shares_outstanding: int,
    cash: float = 0.0,
    liabilities: float = 0.0
) -> float:
    """
    Calculate Net Asset Value (NAV) for an ETF.

    Args:
        holdings: Dictionary mapping ticker to number of shares
        prices: Dictionary mapping ticker to current price
        shares_outstanding: Number of ETF shares outstanding
        cash: Cash holdings (default 0.0)
        liabilities: Fund liabilities (default 0.0)

    Returns:
        NAV per share

    Example:
        >>> holdings = {'AAPL': 100, 'MSFT': 80}
        >>> prices = {'AAPL': 150.0, 'MSFT': 300.0}
        >>> calculate_nav(holdings, prices, 10000, cash=5000, liabilities=1000)
        3.8
    """
    # Implementation
```

### Jupyter Notebooks

**Structure**:
1. Title cell (markdown, H1)
2. Metadata (Track, Difficulty, Time, Prerequisites)
3. Learning Objectives list
4. Setup cell (imports)
5. Sections with exercises (markdown H2)
6. Summary and Next Steps

**Markdown Style**:
- Use **bold** for emphasis
- Use `code` for technical terms
- Use > blockquotes for important notes
- Include ✅ ⚠️ 🚧 status indicators where relevant

### Guide Files

**Required Sections**:
1. Title
2. Track indicator (if applicable)
3. Difficulty level
4. Reading time estimate
5. Prerequisites
6. What You'll Learn
7. Content (with headings)
8. "See also" links

**Example Header**:
```markdown
# Case Study: XYZ ETF

**Track**: [CORE] | **Difficulty**: ⭐⭐ Intermediate | **Reading Time**: 10-12 minutes

**Prerequisites**:
- Basic understanding of ETFs
- Familiarity with order types

**What You'll Learn**:
- Why XYZ crashed 40% while holdings fell 5%
- How stop-loss orders amplified the decline
- Market maker perspective on the event
```

---

## 🧪 Testing Standards

### For Python Modules

**Test Coverage Target**: >80% for new code

**Test Structure**:
```python
import pytest
from src.your_module import your_function

def test_your_function_normal_case():
    """Test function with typical inputs."""
    result = your_function(10, 20)
    assert result == 30

def test_your_function_edge_case():
    """Test function with edge cases."""
    result = your_function(0, 0)
    assert result == 0

def test_your_function_error():
    """Test function error handling."""
    with pytest.raises(ValueError):
        your_function(-1, 5)
```

### For Notebooks

**Manual Testing Required**:
1. Restart kernel & run all cells
2. Verify all outputs make sense
3. Check visualizations render correctly
4. Confirm educational flow is logical

**Automated Testing**:
```bash
# Convert and execute notebook
jupyter nbconvert --to notebook --execute notebook.ipynb
```

---

## 🎓 Educational Standards

All contributions should maintain high educational value:

### Clarity
- Explain concepts before using them
- Provide intuition, not just formulas
- Use real-world examples
- Define jargon on first use

### Accuracy
- Verify facts against primary sources
- Cite academic papers where applicable
- Use actual August 24, 2015 data
- Distinguish fact from interpretation

### Progression
- Build from simple to complex
- Prerequisites clearly stated
- Exercises match difficulty level
- Solutions provided where appropriate

### Engagement
- Use questions to prompt thinking
- Include "Questions for Reflection"
- Provide hands-on exercises
- Show real-world implications

---

## 🐛 Reporting Issues

### Bug Reports

Include:
- **Description**: What went wrong?
- **Expected behavior**: What should happen?
- **Actual behavior**: What actually happened?
- **Steps to reproduce**: Minimal example to trigger the bug
- **Environment**: Python version, OS, dependencies
- **Screenshots**: If applicable

### Feature Requests

Include:
- **Description**: What feature do you want?
- **Use case**: Why is it needed?
- **Proposed solution**: How would it work?
- **Alternatives considered**: Other approaches?
- **Priority**: High/medium/low?

---

## ❓ Questions?

- **General questions**: [GitHub Discussions](https://github.com/yourusername/etf-flash-crash-2015/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/yourusername/etf-flash-crash-2015/issues)
- **Security issues**: Email [your-email] (do not open public issue)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md (coming soon)
- Acknowledged in release notes
- Credited in academic citations when applicable

Thank you for helping make this educational resource better!

---

**Last Updated**: November 2024
