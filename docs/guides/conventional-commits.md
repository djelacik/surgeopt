# 🧾 Conventional Commits Guide for doc-agent-pro

This guide ensures that all commit messages in the project follow a clean, consistent, and professional format — used in real-world teams and enabling automated changelogs, semantic versioning, and better collaboration.

---

## ✅ Why Use Conventional Commits?
- Enables automated changelogs
- Helps team members understand code changes quickly
- Integrates with CI/CD workflows (e.g. GitHub Actions, release tagging)
- Makes your repo look professional for reviewers and hiring managers

---

## 🧩 Commit Format

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### 🎯 Example

```
feat(agent): implement base RFP summarizer logic

Includes LangChain agent to handle RFP document parsing and checklist generation.
```

---

## 📚 Commit Types
| Type     | Description                                 |
|----------|---------------------------------------------|
| feat     | A new feature                               |
| fix      | A bug fix                                   |
| docs     | Documentation change                        |
| style    | Code style fix (formatting, semicolons, etc.)|
| refactor | Code change that neither fixes a bug nor adds a feature |
| test     | Adding or refactoring tests                 |
| chore    | Maintenance tasks (build, deps, config)     |
| ci       | CI/CD configuration changes                 |

---

## 🧠 Scope Examples
| Scope    | Description                  |
|----------|------------------------------|
| agent    | LangChain agent logic        |
| parser   | PDF/DOCX text extraction     |
| ui       | Streamlit frontend           |
| backend  | FastAPI core                 |
| ci       | GitHub Actions / pipelines   |
| docs     | Markdown or doc updates      |

---

## 🚀 Using npm run commit

This project is set up with [Commitizen](https://github.com/commitizen/cz-cli) to help you write Conventional Commits easily.

- Instead of using `git commit -m "your message"`, run:

```
npm run commit
```

- This will launch an interactive prompt that guides you through the commit process:
  - **Type**: feat, fix, chore, etc.
  - **Scope**: What part of the code? (e.g. agent, ui)
  - **Description**: What you did

- The tool will generate a properly formatted commit message for you, such as:

```
feat(parser): add PDF parsing with PyMuPDF
```

**Benefits:**
- Ensures all commits follow the Conventional Commits standard
- Reduces mistakes and saves time
- Integrates with tools like Commitlint and semantic-release

---

## ✍️ How to Make a Commit

Instead of:
```
git commit -m "added rfp parser"
```

Use:
```
npm run commit
```

This will prompt you:
- Type: feat, fix, chore, etc.
- Scope: What part of the code? (e.g. agent, ui)
- Description: What you did

It will generate something like:

```
feat(parser): add PDF parsing with PyMuPDF
```
