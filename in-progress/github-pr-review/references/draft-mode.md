# Draft Mode

Draft mode analyzes the PR and reports findings to the user only. It never writes to GitHub.

## Hard Boundaries

Never mutate GitHub:

- no `gh pr review`
- no `gh pr comment`
- no `gh pr merge`
- no `gh pr edit`
- no mutating `gh api`
- no approve, request changes, label, assignment, close/reopen, merge, or comment action

Never publish local changes:

- no `git commit`
- no `git push`
- no remote mutation of any kind

Local workspace writes are allowed only for review validation: caches, build outputs, coverage, snapshots, temporary scripts, or local-only experimental edits. Disclose any remaining local modifications in the final answer.

## Workflow

### 1. Confirm Context

Run non-mutating checks:

```sh
pwd
git status --short --branch
git branch --show-current
git remote -v
gh repo view --json nameWithOwner,url
```

Resolve the PR from, in order:

1. explicit PR number from the user
2. explicit branch name from the user
3. current branch with `gh pr list --state open --head <current-branch> --json number,title,state,isDraft,author,baseRefName,headRefName,headRepositoryOwner,headRefOid,url --limit 10`
4. ask only when multiple PRs match or no reliable target exists

If no PR can be resolved, stop and report that clearly.

### 2. Existing PR Context Comes First

Before analyzing the diff, inspect:

- PR title and body
- author, base/head branch, draft state
- existing reviews and review states
- review comments, issue comments, author replies, and discussion context
- CI/check status and merge state
- linked issues, linked PRs, references, and closing keywords
- all existing `PRF-*` IDs
- prior excluded-context details blocks

Preferred read-only commands:

```sh
gh pr view <number> --json number,title,state,isDraft,author,baseRefName,headRefName,headRefOid,url,body,commits,files,changedFiles,additions,deletions,reviewDecision,mergeStateStatus,statusCheckRollup,closingIssuesReferences,comments,reviews,latestReviews
gh pr view <number> --comments
gh issue view <issue-or-url> --comments
gh pr view <pr-or-url> --comments
```

Use GraphQL when `gh pr view --comments` does not expose enough inline review-thread detail:

```sh
gh api graphql \
  -F owner='{owner}' \
  -F repo='{repo}' \
  -F number=<number> \
  -f query='
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100) {
        totalCount
        nodes {
          isResolved
          isOutdated
          path
          line
          startLine
          diffSide
          startDiffSide
          subjectType
          comments(first: 100) {
            totalCount
            nodes {
              author { login }
              body
              url
              createdAt
              outdated
            }
          }
        }
      }
    }
  }
}'
```

If `totalCount` exceeds the returned `nodes`, rerun with pagination before concluding a thread or reply is absent.

If PR context links related issues or PRs, inspect those before reviewing the diff when they may contain requirements, prior decisions, reproduction steps, rollout constraints, or unresolved blockers.

Treat existing comments as review input. Do not duplicate an existing concern unless it remains unresolved or materially incomplete.

### 3. Diff And Validation Inputs

Collect parseable diff, changed-file metadata, and check state:

```sh
gh pr diff <number> --name-only
gh pr diff <number> --patch --color never
gh api "repos/{owner}/{repo}/pulls/<number>/files" --paginate --jq '.[] | {path:.filename,status,additions,deletions,changes,patch}'
gh pr checks <number> --json name,state,bucket,link,workflow,description
```

`gh pr checks` can exit non-zero when no checks exist or checks are pending; treat that as check status to report, not as command invalidity.

Optional local inspection after context is verified:

```sh
git diff <base>...HEAD
git log
git show
```

Optional validation may include focused tests, builds, linters, type checks, or reproduction scripts. These may write local artifacts, but must not publish, commit, push, or mutate GitHub.

### 4. Review Priorities

Prioritize:

1. correctness bugs
2. security risks
3. data loss or migration risks
4. race conditions or concurrency issues
5. error handling gaps
6. API or backward compatibility breaks
7. missing tests for changed behavior
8. meaningful performance regressions
9. maintainability risks with concrete impact

Avoid:

- unsupported findings
- subjective style-only requests
- listing every changed file unless it matters
- duplicate comments already covered by reviewers

## ID Rules

Before assigning new IDs, collect every already-used `PRF-*` ID from:

- PR title/body
- comments and reviews
- linked issues/PRs read for context
- excluded-context details blocks

New IDs start after the highest observed numeric suffix. Preserve prior IDs when referring to the same prior concern. Never reuse an ID for a different concern.

Use IDs only for actionable review points. Do not assign IDs to PR metadata, context summaries, validation observations, or the final assessment.

## Submission Target Rules

Every actionable finding must include exactly one target:

- `inline`: specific GitHub-commentable changed line or range
- `file`: file/module concern without one exact changed line
- `general`: PR-wide, architecture, rollout, compatibility, or process concern

Inline target fields:

- `path`: repository-relative path exactly as it appears in the PR diff
- `line`: final line number for the review comment
- `side: RIGHT | LEFT`
- optional `start_line` and `start_side` for ranges

If no faithful commentable diff line exists, report the finding but write `Inline anchor: unavailable` with the reason.

## Output Format

Answer in Korean.

```md
## PR 확인

- PR: #<number> <title>
- URL: <url>
- 브랜치: <head> → <base>
- 현재 위치 확인: <repo/branch match summary>

## 기존 PR 컨텍스트

- 설명/목표: <PR description/body에서 확인한 핵심 의도>
- 기존 리뷰/코멘트: <미해결 우려, 해결된 논의, 참고 맥락 요약>
- 제외 컨텍스트 발견: <prior PRF IDs and reasons, or 없음>
- 테스트/리스크 메모: <PR에 명시된 test plan, rollout, risk notes>

## 리뷰 결과

### Must Fix

- `PRF-001` [Must Fix] <summary>
  - Submission target: inline
  - Inline anchor: `path/to/file.ts:42` (`side: RIGHT`)
  - Risk: <what can go wrong>
  - Suggested fix: <concrete fix>

### Should Fix

- <findings or 없음>

### Consider

- <findings or 없음>

## 테스트/검증 관찰

- <checks status, missing tests, or validation notes>

## 요약

- <1-3 bullets with final assessment>
```

If there are no meaningful findings, say so directly and do not invent IDs.
