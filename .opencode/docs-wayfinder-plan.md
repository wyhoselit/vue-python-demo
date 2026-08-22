# Documentation Workflow Standardization

## Decisions Needed

### 1. Trigger Definition
**Question**: What constitutes a "documentation change trigger"?
- API endpoint modification
- Python function/class change with docstrings
- Schema/database model change

### 2. OpenAPI Generation Timing
**Options**:
- A: Generate on every push to master
- B: Generate only on PR creation
- C: Generate via CI only, never locally

**Recommendation**: Option B - Generate on PR creation for consistency

### 3. Breaking Change Validation
**Process**:
- Compare against master baseline
- Fail PR if breaking changes detected
- Require approval for breaking changes

### 4. Review Process
- **Primary reviewer**: API owner
- **Secondary reviewer**: Docs maintainer
- **Blocking**: All 162 tests must pass

### 5. Automated vs Manual
**Automation Level**:
- ✅ OpenAPI spec generation: AUTOMATED
- ✅ Docs build: AUTOMATED (CI)
- ✅ Changelog entry: AUTOMATED (script)
- ❌ PR merge: MANUAL (approval)

## Ticket Plan

### Ticket 1: Define documentation trigger rules
**Blocking**: None
**Assignee**: Maintainer
**State**: COMPLETED

### Ticket 2: Implement documentation automation script
**Blocking**: Ticket 1
**Assignee**: Maintainer
**State**: COMPLETED

### Ticket 3: Set up default branch protection
**Blocking**: Ticket 2
**Assignee**: Maintainer
**State**: COMPLETED

### Ticket 4: Create team review guidelines
**Blocking**: Ticket 3
**Assignee**: Maintainer
**State**: COMPLETED

## Execution

Run this plan with:
```bash
# In repo root
# Plan creates tickets in GitHub Issues
wayfinder -p "documentation-workflow-standardization"
```

Then resolve tickets in order.