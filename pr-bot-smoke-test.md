# PR link-audit bot — smoke test (throwaway, do NOT merge)

This file exists only to trigger `.github/workflows/pr-link-audit.yml` on a real
PR, so we can confirm the Action fires and comments correctly. The PR will be
closed and this branch deleted right after.

Test links (a healthy repo + an archived one, to exercise both paths):

- Active, permissive license: [pallets/flask](https://github.com/pallets/flask)
- Archived, should be flagged: [langchain-ai/langserve](https://github.com/langchain-ai/langserve)
