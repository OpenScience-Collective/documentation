# Merging Community Changes

Community maintainers can merge a pull request (PR) that changes **only their own
community's directory** into `develop` themselves, by leaving an explicit
comment. No platform admin is needed for routine community changes.

This only removes the human-approval step; the normal CI checks (ruff + tests)
still gate the merge. Releases to production (`develop` to `main`) are still done
by an OSA admin, so `main` never diverges from the integrated `develop` branch.

## Who can do this

Anyone listed in the `maintainers:` field of your community's
`src/assistants/<your-id>/config.yaml`. The list is read from the **base branch**
(the already-merged code), so it cannot be changed by the PR itself.

```yaml
# src/assistants/hed/config.yaml
maintainers:
  - VisLab
  - yarikoptic
```

## How to merge

1. Open a PR against **`develop`** that changes only files inside your community
   directory, `src/assistants/<your-id>/` (`config.yaml`, `tools.py`, prompts,
   `logo.svg`, etc.). The PR does not have to be authored by you; it can be from
   any contributor.
2. Review it. When you (a listed maintainer) are ready to merge, post a PR
   **comment** containing both keywords **`LGTM`** and **`merge`**, for example:

   > LGTM, please merge

   Casing does not matter, and any phrasing works as long as both words appear.
   To explicitly hold off, include "do not merge" / "don't merge" and it will not
   fire.
3. The bot approves the PR and queues a **squash auto-merge**. The PR merges
   automatically once ruff and the tests pass, and a confirmation comment is
   posted.

That is the whole flow. Nothing merges when the PR is opened; the comment is the
deliberate signal, so a PR can sit in review for as long as you like.

## What is eligible

A comment merges the PR only when **all** of these hold:

- The comment is from a listed maintainer of the target community.
- Every changed file is under a single `src/assistants/<id>/` directory (one
  community, nothing outside it, including a rename's original path).
- The PR does **not** change the `maintainers:` field. Adding or removing a
  maintainer always needs human review by a platform admin.
- The PR targets `develop` (not `main`).
- All required status checks pass (the bot waits for them; it never bypasses CI).

If any condition is not met, the comment simply does nothing and the PR follows
the normal review process.

## Safety notes

- **Pinned to the reviewed commit.** The merge is tied to the exact commit the
  `LGTM ... merge` comment was made on. If new commits are pushed afterward, the
  queued merge is cancelled and a fresh `LGTM ... merge` comment is required. This
  prevents getting an approval on a clean diff and then slipping in changes.
- **Maintainers list is the source of truth.** It is hand-maintained in each
  community's `config.yaml` and is not synced to GitHub Teams. Whoever is listed
  there is trusted to merge changes to that community's directory.
- **Develop only.** Community changes never reach `main` automatically; an OSA
  admin merges `develop` to `main` as part of a release.

## For platform admins

The mechanism is a GitHub Actions workflow
(`.github/workflows/community-admin-pr-merge.yml`) plus a dedicated GitHub App
that performs the approve and merge with a short-lived token. The one-time App
setup and the full trust model are documented in the OSA repository at
`.context/community-admin-merge.md`.
