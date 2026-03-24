---
name: coding-standards
description: Universal coding standards, best practices, and patterns for TypeScript, JavaScript, React, and Node.js development.
weight: passive
origin: ECC
---

# Coding Standards & Best Practices

## When to Activate

- Starting a new project or module
- Reviewing or refactoring code for quality, consistency, or maintainability
- Enforcing naming, formatting, or structural conventions

## Code Quality Principles

- **Readability First** — Clear names, self-documenting code, consistent formatting. Code is read more than written.
- **KISS** — Simplest working solution. No over-engineering or premature optimization.
- **DRY** — Extract common logic into reusable functions/components. No copy-paste.
- **YAGNI** — Don't build it until you need it. Start simple, refactor when required.

## TypeScript/JavaScript Standards

### Variable Naming

```typescript
// Descriptive names (avoid: q, flag, x, temp)
const marketSearchQuery = 'election'
const isUserAuthenticated = true
const totalRevenue = 1000
```

### Function Naming

```typescript
// Verb-noun pattern (avoid: noun-only like market(), email())
async function fetchMarketData(marketId: string) { }
function calculateSimilarity(a: number[], b: number[]) { }
function isValidEmail(email: string): boolean { }
```

### Immutability

```typescript
// Always use spread operator (avoid: direct mutation like obj.x = y, arr.push())
const updatedUser = { ...user, name: 'New Name' }
const updatedArray = [...items, newItem]
```

### Error Handling

```typescript
// Wrap async calls with try/catch, check response status (avoid: bare unhandled awaits)
async function fetchData(url: string) {
  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    return await response.json()
  } catch (error) {
    console.error('Fetch failed:', error)
    throw new Error('Failed to fetch data')
  }
}
```

### Async/Await

```typescript
// Parallelize independent calls (avoid: sequential awaits for unrelated fetches)
const [users, markets, stats] = await Promise.all([
  fetchUsers(), fetchMarkets(), fetchStats()
])
```

### Type Safety

```typescript
// Use specific types and union literals (avoid: 'any')
interface Market {
  id: string
  name: string
  status: 'active' | 'resolved' | 'closed'
  created_at: Date
}
```

## React Best Practices

### Component Structure

```typescript
// Typed props with defaults, destructured params (avoid: untyped props objects)
interface ButtonProps {
  children: React.ReactNode
  onClick: () => void
  disabled?: boolean
  variant?: 'primary' | 'secondary'
}

export function Button({
  children, onClick, disabled = false, variant = 'primary'
}: ButtonProps) {
  return (
    <button onClick={onClick} disabled={disabled} className={`btn btn-${variant}`}>
      {children}
    </button>
  )
}
```

### State Management

```typescript
// Use functional updates for state derived from previous state (avoid: stale closure refs)
const [count, setCount] = useState(0)
setCount(prev => prev + 1)  // NOT: setCount(count + 1)
```

## API Design Standards

### REST Conventions

- `GET /api/resources` — List (supports `?status=active&limit=10&offset=0`)
- `GET /api/resources/:id` — Get one
- `POST /api/resources` — Create
- `PUT /api/resources/:id` — Full update
- `PATCH /api/resources/:id` — Partial update
- `DELETE /api/resources/:id` — Delete

### Response Format

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  meta?: { total: number; page: number; limit: number }
}
```

## Python Standards

### Style & Structure
- Follow PEP 8 (snake_case functions/variables, PascalCase classes)
- Use type hints: `def process(data: list[dict]) -> bool:`
- Prefer f-strings over .format() or %
- Use pathlib over os.path
- Use dataclasses or Pydantic over raw dicts for structured data

### Error Handling
- Catch specific exceptions, never bare `except:`
- Use `logging` module over print() for production code
- Return early on validation failures

### Project Structure
- Use virtual environments (venv/conda)
- Requirements in requirements.txt or pyproject.toml
- Entry points via `if __name__ == "__main__":` or CLI frameworks (click, argparse)

### Testing
- pytest over unittest
- Fixtures for shared setup
- Parametrize for multiple test cases
