# 🧑‍💻 Git Collaboration Guide

This document explains how to collaborate as a professional team using branches, commits, merging, and pull requests.

---

## 🧩 Branching Strategy
- **main** branch is always production-ready (never push directly)
- All changes go through feature branches and pull requests

---

## 📂 Branch Naming Convention
| Branch Type | Pattern         | Example            |
|-------------|----------------|--------------------|
| Feature     | feat/<name>    | feat/rfp-agent     |
| Bugfix      | fix/<name>     | fix/pdf-crash      |
| Docs        | docs/<name>    | docs/setup-guide   |
| Chore       | chore/<name>   | chore/ci-setup     |

---

## 🔁 Workflow Summary

```mermaid
graph TD
    A[Create Issue] --> B[Create Branch]
    B --> C[Work & Commit (Conventional Commits)]
    C --> D[Push Branch]
    D --> E[Open Pull Request]
    E --> F[Code Review (self or team)]
    F --> G[Merge to main]
    G --> H[GitHub Actions runs tests/deploy]
```

---

## 🧠 Step-by-Step Workflow

1. **Create an Issue**
   - Go to GitHub → Issues → create one
   - Example: `#12 Add FastAPI route for document upload`

2. **Create a Branch**
   ```zsh
   git checkout main
   git pull origin main
   git checkout -b feat/upload-endpoint
   ```

3. **Make Changes & Commit Often**
   - Small, meaningful commits (every 30–60 min or logical unit)
   - Follow [Conventional Commits](../conventional-commits.md)
   - Use `npm run commit` (Commitizen) to format properly

4. **Push Your Branch**
   ```zsh
   git push -u origin feat/upload-endpoint
   ```

5. **Open a Pull Request**
   - Go to GitHub → your branch → Compare & pull request
   - **Title:** Same as your commit style (e.g. `feat(upload): implement document upload route`)
   - **Link the issue:** `Closes #12`
   - **Add description:** what you did, screenshots if needed

6. **Code Review & Merge**
   - Review yourself or with your teammate
   - Ensure CI passes (GitHub Actions)
   - Squash & Merge into main via GitHub UI

7. **Delete Merged Branch**
   - GitHub will offer to delete the branch — click it
   - Locally:
     ```zsh
     git checkout main
     git pull origin main
     git branch -d feat/upload-endpoint
     ```

---

## 🔁 How Often to Commit, Push & PR
| Action  | Frequency                  | Tip                        |
|---------|----------------------------|----------------------------|
| Commit  | Every 30–60 minutes        | One logical unit of work   |
| Push    | End of work session/feature| Keep remote up-to-date     |
| PR      | When feature is testable   | Prefer small PRs (<300 LOC)|
| Pull main | Daily                    | Always pull before new branch |

---

## 🚨 Avoid These Mistakes
- ❌ Pushing directly to main
- ❌ Commit messages like `update` or `wip`
- ❌ Large PRs with unrelated features
- ❌ Merging without reviewing

---

For more, see [Conventional Commits Guide](../conventional-commits.md) and [CONTRIBUTING.md](../CONTRIBUTING.md).
