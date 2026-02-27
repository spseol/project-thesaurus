# AGENTS.md — project-thesaurus

> Instructions for agentic coding agents operating in this repository.

---

## Project Overview

**project-thesaurus** is a university thesis management system with a dual-stack architecture:

| Layer     | Location    | Stack                                           |
|-----------|-------------|-------------------------------------------------|
| Backend   | `django/`   | Python 3.9, Django 3.2, Django REST Framework 3.15 |
| Frontend  | `webpack/`  | TypeScript 4.4, Vue 2.7, Vuetify 2, Webpack 4  |
| Database  | —           | PostgreSQL                                      |
| Proxy     | `nginx/`    | Nginx                                           |

The full dev environment runs via Docker Compose. The Django backend serves a REST API; the Vue SPA is served by the webpack-dev-server in development.

---

## Build & Dev Commands

### Frontend (`webpack/`)

```bash
# Install dependencies
cd webpack && npm install

# Development server (hot-reload, port 3000)
cd webpack && npm run dev

# Production build
cd webpack && npm run build

# Check for missing/unused i18n keys
cd webpack && npm run extract-locale

# Merge translation keys exported from Django into the frontend locale JSON files
cd webpack && npm run merge-locale
```

### Backend (`django/`)

```bash
# Run development server (inside Docker or with Pipenv shell active)
cd django && python manage.py runserver

# Apply migrations
cd django && python manage.py migrate

# Create a superuser
cd django && python manage.py createsuperuser

# Install Python dependencies (Pipenv)
cd django && pipenv install --dev
```

### Docker Compose (recommended for full-stack dev)

```bash
# Start everything (Django + webpack-dev-server + nginx)
docker-compose -f docker-compose.base.yml -f docker-compose.dev.yml up

# Production stack
docker-compose -f docker-compose.base.yml -f docker-compose.prod.yml up

# Build and release a Django image
make release-django TAG=x.y.z
```

### Tests & Linting

**⚠️ This project currently has no automated tests and no linter configuration.**

- No `pytest` / `jest` / `vitest` setup exists — do not attempt to run tests.
- No `eslint`, `prettier`, `ruff`, or `mypy` configs exist — do not attempt to run linters.
- When writing new code, follow the manual style conventions documented below.
- If you add tests or linting infrastructure, document the commands here.

---

## Git Workflow

- **Never commit directly to `master` or `develop`.**
- `master` — production branch.
- `develop` — integration branch (target for PRs).
- Feature branches: `feature/<short-name>` (e.g. `feature/audit-log`).
- Fix branches: `fix/<short-name>` (e.g. `fix/thesis-reservable-flag`).

### Commit messages

Single-line only. Format: `type(scope): description`

```
feat(thesis): add PDF export endpoint
fix(review): correct overlapping layout in detail panel
chore(django): bump Python and Django versions
refactor(thesis): simplify reservation state transition logic
```

- **Types:** `feat`, `fix`, `chore`, `refactor`, `docs`, `test`
- **Scopes:** match Django app names — `thesis`, `review`, `accounts`, `api`, `audit`, `attachment`, `emails`, `frontend`, `django`, `js`, `utils`
- **Note:** reservation logic lives inside `apps/thesis/` — use scope `thesis` for reservation-related commits
- **Description:** imperative mood, lowercase, no trailing period
- No body or footer lines

---

## Python / Django Code Style

### Import ordering

```python
# 1. Standard library
from typing import Optional, Tuple

# 2. Django
from django.contrib.auth import get_user_model
from django.db import models

# 3. Third-party
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

# 4. Local apps (absolute, from apps.*)
from apps.accounts.models import User
from apps.api.permissions import CanSubmitThesisPermission
```

Imports are grouped with a single blank line between groups. The ordering and grouping above must be maintained; do not collapse or reorder groups.

### Naming conventions

| Construct            | Convention              | Example                          |
|----------------------|-------------------------|----------------------------------|
| Variables / functions | `snake_case`           | `get_available_theses`           |
| Classes              | `PascalCase`            | `ThesisViewSet`                  |
| Constants            | `SCREAMING_SNAKE_CASE`  | `STATE_HELP_TEXTS`               |
| Django apps          | lowercase, no hyphens   | `apps/thesis/`, `apps/review/`   |
| URL names            | `kebab-case` strings    | `thesis-list`, `review-detail`   |

### Models

- Inherit from `BaseTimestampedModel` (provides UUID primary key, `created`, `modified` fields, and `django-lifecycle` hooks). Defined in `apps/utils/models/base.py`.
- `related_name` follows the pattern `{model}_{field}` — e.g. `related_name='thesis_supervisor'`.
- Split large model files into a `models/` package; re-export from `models/__init__.py`.
- Nested classes: `class Meta`, `class State(models.TextChoices)`.
- Custom managers are named descriptively: `objects`, `api_objects`, `import_objects`.

### Error handling

```python
# Standard DRF pattern — let the framework handle the response
serializer.is_valid(raise_exception=True)

# Business rule violations
from rest_framework.exceptions import ValidationError
raise ValidationError('Thesis is already reserved.')

# The custom exception handler shapes all error responses:
# apps.api.utils.exceptions.exception_handler
```

- Don't use `try/except` in views solely to shape HTTP responses; let DRF and the custom exception handler handle error responses.
- Prefer `raise_exception=True` and DRF exceptions for validation/business-rule errors; avoid hand-crafting 400 responses unless a view has a specific, documented reason.

### Type annotations

- Add type hints to function signatures; return types where non-obvious.
- Use string forward references for models not yet defined: `def foo(self: 'ThesisViewSet')`.
- Inline `# type: QuerySet` comments are acceptable for local variables.
- `from __future__ import annotations` is not currently used — keep it that way.

---

## TypeScript / Vue Code Style

### Import ordering

```ts
// 1. Third-party packages (alphabetical)
import * as Sentry from '@sentry/browser';
import Vue from 'vue';

// 2. Side-effect imports
import '../scss/index.scss';

// 3. Local source files
import App from './App.vue';
import { DjangoPermsPlugin, I18nRoutePlugin } from './plugins';
```

Imports run together without blank lines between groups — do not add separators.

### Naming conventions

| Construct               | Convention              | Example                         |
|-------------------------|-------------------------|---------------------------------|
| Variables / functions   | `camelCase`             | `loadThesisList`                |
| Classes / components    | `PascalCase`            | `ThesisDetailPanel`             |
| Enums                   | `SCREAMING_SNAKE_CASE`  | `THESIS_ACTIONS`, `PERMS`       |
| Enum values             | Descriptive strings     | `LOAD_THESES = 'Load theses'`   |
| Vue files               | `PascalCase.vue`        | `ThesisDetail.vue`              |
| TS utility files        | `camelCase.ts`          | `axios.ts`, `router.ts`         |

### Vue component structure

- Use **Options API** with `Vue.extend({})`. Do not use `defineComponent` or class-based components.
- Script tag: `<script type="text/tsx">` (not `<script lang="ts">`).
- File order: `<template>` → `<script>` → `<style scoped>`.
- Page-level components live in their own subdirectory with a thin `Page.vue` wrapper:
  ```
  pages/ThesisList/Page.vue          ← route target, thin wrapper
  pages/ThesisList/ThesisList.vue    ← feature component with logic
  ```

### Vuex store modules

```ts
export enum MODULE_MUTATIONS { SET_DATA = 'Set data' }
export enum MODULE_ACTIONS   { LOAD_DATA = 'Load data' }

const state = { data: null as Data | null };
type State = typeof state;

export default {
  namespaced: true,
  state,
  mutations: { [MODULE_MUTATIONS.SET_DATA](state: State, payload: Data) { ... } },
  actions:   { async [MODULE_ACTIONS.LOAD_DATA]({ commit }) { ... } },
  getters:   { ... },
};
```

- All modules are namespaced.
- Use `Vue.set` / `Vue.delete` for reactive object mutations.

### TypeScript strictness

- `strict: false` in `tsconfig.json` — implicit `any` is tolerated for existing code.
- Add explicit types to new public class properties and function signatures.
- Domain types are declared as `declare class X extends Object {}` in `webpack/src/js/types.d.ts`.

### Error handling

- All HTTP errors are handled centrally in `webpack/src/js/axios.ts` interceptors:
  - `401` → force page reload (re-auth)
  - `403` → treated as a **success** by default `validateStatus` (resolves, never reaches the error interceptor); only callers that override `validateStatus` to treat 403 as an error will trigger a toast warning (suppress with `config.allow403 = true`, in which case the error interceptor **handles and swallows** the 403 instead of propagating it)
  - `5xx` → flash error banner
- Use optional chaining (`?.`) throughout; never assume response shape.
- Error interceptors must `return Promise.reject(error)` to propagate errors to callers, **except** in explicitly documented cases where an error is intentionally handled and swallowed (e.g. `403` with `config.allow403 = true`).
- Validation errors (`400`) are treated as successful responses and handled per-form.

---

## Directory Reference

```
django/
  apps/              # Django applications (one per domain)
    utils/           # Shared utilities: BaseTimestampedModel and helpers
  thesaurus/         # Django project config (settings, urls, wsgi/asgi)
  templates/         # Django HTML templates
  locale/            # .po/.mo translation files
  fixtures/          # Initial data
  Pipfile            # Python dependencies

webpack/
  src/js/
    app.ts           # Vue app factory / bootstrap
    axios.ts         # Configured Axios instance + interceptors
    router.ts        # Vue Router with guards
    plugins.ts       # Vue plugins (DjangoPermsPlugin, I18nRoutePlugin)
    utils.ts         # Shared utilities: notificationBus, pageContext
    user.ts          # Permission helpers: hasPerm, hasGroup
    cache.ts         # localforage-backed request cache helpers
    types.d.ts       # Global TypeScript type declarations
    vue-shim.d.ts    # Module declaration shim for .vue files
    store/           # Vuex modules (one file per domain)
    pages/           # Page-level Vue components
    components/      # Shared reusable components
    locale/          # i18n JSON files (cs.json, en.json)
  src/scss/          # Global SCSS
  tsconfig.json
  webpack.*.config.js
```
