# Week 1: Git, GitHub, and the Command Line

## Overview

This session does double duty: it teaches the foundational tools (git, terminal, GitHub) and sets the stage for the entire course. The core argument is simple: AI coding agents like Claude Code are extraordinarily powerful, and that power is exactly why you need version control, quality assurance (QA), and structured workflows.

!!! abstract "Learning Objectives"
    - Describe the current landscape of AI coding agents and how they fit into research workflows
    - Explain why AI-powered productivity demands stronger quality assurance, not weaker
    - Navigate the filesystem using `cd`, `ls`, `pwd`, `mkdir`
    - Initialize a git repository, stage files, commit, push to GitHub
    - Understand the three states (working directory, staging area, repository) and the commands that move files between them
    - Understand the difference between `git` (version control) and `gh` (GitHub CLI)
    - Create branches, pull requests, and issues on GitHub
    - Run a full Issue -> Branch -> Commits -> Pull Request -> Review -> Merge loop end to end

<div class="embed-container">
  <iframe
    src="https://www.youtube.com/embed/t7x8dU8_V3U"
    title="Week 1: Git, GitHub, and the Command Line"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
</div>

## Slides

<div class="embed-container">
  <iframe
    src="../../slides/agentic-research/week-01/presentation.html?presentation=./week-01.json"
    title="Week 1 Slides"
    frameborder="0"
    allowfullscreen>
  </iframe>
</div>

<p class="slide-hint">Use arrow keys to navigate. Press <kbd>F</kbd> for fullscreen, <kbd>?</kbd> for shortcuts.</p>

---

## Setup Guide

A step-by-step walkthrough for getting your research computing environment ready. No prior coding experience is assumed.

### Why This Course Starts Here

The rest of this course is about artificial intelligence (AI) coding agents: tools like Claude Code, GitHub Copilot, and Cursor that do not just autocomplete your code, but plan work, write code across many files, run commands, and open pull requests on their own. They are legitimately useful for research. They also change the risk profile of your work.

**What changed.** Five years ago, "AI in coding" meant a chat window next to your editor that could draft a function if you asked nicely. Today, an AI coding agent reads your entire repository, runs your build, reads the error output, and keeps iterating until tests pass. A typical 30-minute Claude Code task might produce a commit across six files, a new pull request, and a passing test run, without your involvement beyond the first prompt. Different category of tool. Different category of risk.

**The power problem.** AI generates code an order of magnitude faster than a human does. Without discipline, it produces bugs an order of magnitude faster too. In research this matters more than in most contexts, because a silent bug in a preprocessing pipeline can be three years of results before anyone notices.

**Git as a safety net.** Everything later in this course (agents, plugins, continuous integration, automated review) is built on top of git. Git gives you an undo button (`git revert`), an audit trail (`git log`, `git blame`), a review checkpoint (pull requests), and reproducibility (tag a commit; reproduce the state three years from now). None of those benefits are new with AI. They became load-bearing with AI.

Week 1 installs the safety net. Week 2 brings in Claude Code on top of it. The workflow you learn here is what you will use for the next ten weeks and for every research project after that:

```
Issue  ->  Branch  ->  Commits  ->  Pull Request  ->  Review  ->  Merge  ->  Pull main
```

You will run this loop end to end before the session ends.

### 1. Open Your Terminal

Every operating system has a built-in terminal. This is where you type commands instead of clicking buttons.

=== "macOS"

    - Open Spotlight (++cmd+space++), type `Terminal`, press Enter
    - Or find it in Applications > Utilities > Terminal

=== "Linux"

    - Press ++ctrl+alt+t++ (most distributions)
    - Or search for "Terminal" in your application launcher

=== "Windows"

    Install [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install). Open PowerShell as Administrator and run:

    ```powershell
    wsl --install
    ```

    Restart your computer, then open "Ubuntu" from the Start menu. WSL gives you a full Linux terminal inside Windows.

Once your terminal is open, verify it works:

```bash
pwd    # Where am I?
ls     # What files are here?
ls -la # List with details
```

### 2. Install a Package Manager

Package managers let you install software from the command line. Think of them as an app store for developer tools.

=== "macOS"

    Install [Homebrew](https://brew.sh), the standard macOS package manager:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

    The installer prints a "Next steps" section at the end. On Apple Silicon Macs, that includes adding Homebrew to your shell's `PATH`. Run exactly what the installer prints, which usually looks like:

    ```bash
    # Apple Silicon
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"

    # Intel
    echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/usr/local/bin/brew shellenv)"
    ```

    Verify:

    ```bash
    brew --version
    ```

=== "Linux"

    You already have `apt`. Update it:

    ```bash
    sudo apt update
    ```

=== "Windows"

    Your WSL Ubuntu terminal already has `apt` (see Step 1). Update it:

    ```bash
    sudo apt update
    ```

### 3. Install Git and the GitHub CLI

You need two command-line tools: `git` for version control and `gh`, GitHub's command-line interface (CLI), for interacting with GitHub.

=== "macOS"

    ```bash
    brew install git gh
    ```

=== "Linux"

    `git` is in the default apt repos. `gh` is not, so add GitHub's apt repo first (the block below is the official install from [cli.github.com](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)):

    ```bash
    sudo apt install git

    (type -p wget >/dev/null || (sudo apt update && sudo apt install wget -y)) \
      && sudo mkdir -p -m 755 /etc/apt/keyrings \
      && out=$(mktemp) && wget -nv -O$out https://cli.github.com/packages/githubcli-archive-keyring.gpg \
      && cat $out | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
      && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
      && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
      && sudo apt update \
      && sudo apt install gh -y
    ```

    Homebrew also runs on Linux and installs `gh` with a single command (`brew install gh`). See [brew.sh](https://brew.sh).

=== "Windows"

    In your WSL Ubuntu terminal, follow the Linux instructions above. `gh` is not in default Ubuntu repos, so the official apt setup is needed.

Verify both:

```bash
git --version
gh --version
```

Configure your git identity (use the same email you will use for GitHub):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. Understanding `git` vs `gh`

These two tools work together but handle different things:

| | `git` | `gh` |
|---|---|---|
| **What it is** | Version control system | GitHub CLI |
| **What it does** | Tracks file changes, manages history | Manages GitHub features (issues, PRs, repos) |
| **Works without GitHub?** | Yes | No |
| **Installed by default?** | Sometimes (macOS ships a version) | No |

**`git` commands you will use daily:**

```bash
git init           # Start tracking a folder
git add file.md    # Stage a file
git commit -m ""   # Save a snapshot
git push           # Send to remote
git pull           # Get updates
git log --oneline  # View history
git diff           # See what changed
git clone <url>    # Copy a remote repo locally
```

**`gh` commands for GitHub operations:**

```bash
gh repo create     # Create a new GitHub repo
gh repo clone      # Clone a GitHub repo (shorthand)
gh issue create    # Open an issue
gh issue develop   # Create a branch from an issue
gh pr create       # Open a pull request
gh pr view         # View PR details
```

!!! info "Where they overlap"
    Both can clone a repository (`git clone <url>` vs `gh repo clone user/repo`). That is essentially the only overlap. In practice, you use `git` for all version control and `gh` for all GitHub operations.

### 5. Create a GitHub Account

If you do not already have one:

1. Go to [github.com](https://github.com)
2. Click **Sign up**
3. Choose a username, enter your email, create a password
4. Verify your email address

#### GitHub Education (free upgrades for researchers)

GitHub offers free benefits for students, faculty, and research labs. These are worth setting up before you go further.

=== "Students"

    Apply for the [GitHub Student Developer Pack](https://education.github.com/pack):

    1. Go to [education.github.com/students](https://education.github.com/students)
    2. Click **Apply**
    3. Verify your academic status (use your `.edu` email or upload proof of enrollment)
    4. Once approved, you get GitHub Pro for free, plus access to dozens of developer tools

    Benefits include unlimited private repos, GitHub Copilot access, and free domain names.

=== "Faculty and researchers"

    Apply for the [GitHub Teacher Toolbox](https://education.github.com/teachers):

    1. Go to [education.github.com/teachers](https://education.github.com/teachers)
    2. Click **Apply**
    3. Verify your academic status with your institutional email
    4. Once approved, you get a free **GitHub Team** subscription (unlimited collaborators and private repositories), free **GitHub Copilot Pro**, and the ability to create free GitHub Classroom organizations

=== "Research labs (organizations)"

    If your lab or research group has a GitHub organization, you can upgrade it to GitHub Team for free:

    1. Visit [education.github.com/globalcampus/teacher](https://education.github.com/globalcampus/teacher) (you must be verified as faculty first)
    2. Find the **Upgrade your academic organizations** section
    3. Click **Upgrade to GitHub Team**
    4. Select your organization and click **Upgrade**

    This gives your entire lab access to GitHub Team features for free: protected branches, required reviews, code owners, advanced audit logs, and more. Highly recommended for any research group managing shared code.

#### Set up SSH keys (recommended)

Secure Shell (SSH) keys let you push to GitHub without typing your password every time.

```bash
# Generate a new SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"
```

Press Enter to accept the default file location. You can set a passphrase or press Enter for none.

```bash
# Start the SSH agent
eval "$(ssh-agent -s)"

# Add your key
ssh-add ~/.ssh/id_ed25519
```

=== "macOS"

    ```bash
    cat ~/.ssh/id_ed25519.pub | pbcopy
    ```

=== "Linux"

    ```bash
    cat ~/.ssh/id_ed25519.pub
    # Select and copy the output manually
    ```

=== "Windows"

    In your WSL Ubuntu terminal:

    ```bash
    cat ~/.ssh/id_ed25519.pub
    # Select and copy the output manually
    ```

    Or in PowerShell:

    ```powershell
    Get-Content ~\.ssh\id_ed25519.pub | Set-Clipboard
    ```

Then add it to GitHub:

1. Go to [github.com/settings/keys](https://github.com/settings/keys)
2. Click **New SSH key**
3. Paste your key and give it a title (e.g., "My Laptop")
4. Click **Add SSH key**

Test the connection:

```bash
ssh -T git@github.com
```

You should see: `Hi username! You've successfully authenticated...`

#### Authenticate the GitHub CLI

```bash
gh auth login
```

Follow the prompts: pick **GitHub.com**, pick **SSH** as the authentication protocol (matches the key you just added), then authenticate through your browser.

### 6. Terminal Navigation Basics

```bash
pwd              # Print working directory (where you are)
ls               # List files and folders
cd Documents     # Change directory
cd ..            # Go back up one level
mkdir my-project # Create a new folder
cd my-project    # Move into it
```

!!! tip "Key concepts"
    - **Absolute path**: starts from the root, e.g., `/Users/jane/Documents`
    - **Relative path**: starts from where you are, e.g., `Documents/projects`
    - `..` means "one directory up"
    - `.` means "this directory"
    - `~` means your home directory

### 7. Create Your First Repository

```bash
# Create a project folder and move into it
mkdir my-research-project
cd my-research-project

# Initialize git tracking
git init
```

Create a file and make your first commit:

```bash
# Create a README
echo "# My Research Project" > README.md
echo "" >> README.md
echo "This is my first git repository." >> README.md

# Stage and commit
git add README.md
git commit -m "Add README with project description"
```

Make a few more commits to practice:

```bash
# Add a notes file
echo "## Research Notes" > notes.md
echo "" >> notes.md
echo "- Started project setup" >> notes.md
git add notes.md
git commit -m "Add initial research notes"

# Update the README
echo "" >> README.md
echo "## Goals" >> README.md
echo "- Learn git and GitHub" >> README.md
echo "- Set up a reproducible workflow" >> README.md
git add README.md
git commit -m "Add project goals to README"
```

!!! tip "Commit message style"
    Subjects should be atomic (one logical change) and under 50 characters. "Add README with project description" is 35 characters; "Add project goals to README" is 27; both are fine. Anti-pattern: `"updated some stuff and fixed the license thing"`. More on why in Week 3.

View your history:

```bash
git log --oneline
```

You should see something like this (hashes will differ):

```
7f3e1c2 Add project goals to README
b04a2d7 Add initial research notes
a9e5f01 Add README with project description
```

### 8. How Git Thinks: The Three States

You just used `git add` and `git commit` without much explanation. Now that the commands have worked once, the mental model is easier to absorb. Make sure `git status` shows a clean working tree before you start; commit or discard pending changes first.

Every file in a git repository is in one of three places:

```
Working directory  ->  Staging area  ->  Repository
     (edit)             (git add)        (git commit)
```

- **Working directory** is what you see in your file explorer.
- **Staging area** is a holding pen for the next snapshot. `git add README.md` does not save anything permanent; it just says "include this version in the next commit."
- **Repository** is the permanent history. `git commit` takes whatever is in the staging area and writes it as a new snapshot.

#### Why three states instead of two?

The staging area exists so you can commit logically, not chronologically. If you are mid-edit on three files and realize two are a bug fix and the third is an unrelated cleanup, you can:

```bash
git add file1.md file2.md
git commit -m "Fix the citation formatter"

git add file3.md
git commit -m "Clean up leftover debug prints"
```

Two small, focused commits instead of one sprawling "stuff I did today" commit. Your future self (and collaborators, human or AI) can understand each change on its own.

#### See it with your own files

```bash
# Make two unrelated changes
echo "" >> README.md
echo "## Status" >> README.md
echo "- In progress" >> README.md

echo "## Ideas" >> notes.md
echo "- Look into citation managers" >> notes.md

git status
```

Both files show as "modified" in the working directory, nothing staged.

```bash
git add README.md
git status
```

Now `README.md` is in "Changes to be committed" (staging area), while `notes.md` is still "Changes not staged for commit" (working directory only).

```bash
git commit -m "Add status section to README"
git add notes.md
git commit -m "Add ideas for citation managers"
git log --oneline
```

Two commits, not one. That is the whole point of the staging area.

#### Seeing what changed

```bash
git diff          # Changes you have not staged yet
git diff --staged # Changes you have staged but not committed
git show          # What the last commit changed
```

#### The undo button

The opener promised that git gives you an undo button. Here is how to press it:

```bash
git restore README.md            # Discard working-directory changes
git restore --staged README.md   # Unstage, keep the edits
git revert <commit-hash>         # Safely undo a committed change with a new commit
```

`git revert` is the right tool for "this commit broke things, back it out." It creates a new commit, so history stays honest even on commits that have already been pushed.

### 9. Push to GitHub

Create a remote repository:

1. Go to [github.com/new](https://github.com/new)
2. Name it `my-research-project`
3. Leave it **public** (or private, your choice)
4. Do **not** check "Add a README" (you already have one)
5. Click **Create repository**

Connect and push:

```bash
git remote add origin git@github.com:YOUR-USERNAME/my-research-project.git
git branch -M main
git push -u origin main
```

`-u origin main` sets the default remote and branch so future pushes and pulls can be shortened to `git push` and `git pull`. Refresh the GitHub page; your files are now online.

### 10. The GitHub Workflow: Issues, Branches, Pull Requests

You now have a repo on GitHub. The rest of this course assumes you work in a specific loop whenever you change anything non-trivial:

```
Issue  ->  Branch  ->  Commits  ->  Pull Request  ->  Review  ->  Merge
```

That loop looks bureaucratic for a solo project at first. It becomes essential the moment you add an AI agent, a collaborator, or any future self who will forget why you made a change. Practicing it now, on a tiny project where nothing is at stake, means it will be automatic by Week 3 when it actually matters.

#### Open an issue

```bash
gh issue create --title "Add a LICENSE file" --body "The repo should have a license so collaborators know the terms of use. Let's add CC-BY-4.0."
```

`gh` prints the issue number (assume 1 for this walkthrough) and a URL.

#### Create a branch from the issue

Never edit directly on `main`. Always branch, and name the branch after the issue it addresses:

```bash
gh issue develop 1 --checkout
```

This creates a branch linked to issue 1 on GitHub (auto-named something like `1-add-a-license-file`) and checks it out locally.

```bash
git branch --show-current
```

#### Make the change and commit

For the walkthrough, write a placeholder `LICENSE`. For a real repo, replace this with the canonical text from [creativecommons.org/licenses/by/4.0/legalcode.txt](https://creativecommons.org/licenses/by/4.0/legalcode.txt).

```bash
cat > LICENSE <<'EOF'
CC-BY-4.0 License (placeholder)

This project will be licensed under Creative Commons Attribution 4.0
International (CC-BY-4.0). Replace this file with the full legal text
from https://creativecommons.org/licenses/by/4.0/legalcode.txt before
publishing.

Copyright (c) 2026 Your Name
EOF

git add LICENSE
git commit -m "Add CC-BY-4.0 license placeholder"
```

#### Push the branch

```bash
git push -u origin "$(git branch --show-current)"
```

Using `$(git branch --show-current)` avoids hard-coding the auto-generated branch name.

#### Open a pull request

A pull request (PR) is a proposal: "merge these commits into `main`." Even on a solo project, the PR forces you to look at the diff as an outsider before it lands.

```bash
gh pr create --title "Add CC-BY-4.0 license" --body "Closes #1"
```

`Closes #1` tells GitHub to close issue 1 automatically when the PR merges. `Fixes #N` and `Resolves #N` are equivalent.

Open the PR in a browser:

```bash
gh pr view --web
```

Click **Files changed** and read the diff as if someone else wrote it. This is where you catch debug prints, accidentally committed data, copy-paste typos.

#### Merge

On the PR page, click **Merge pull request**, pick **Create a merge commit**, confirm. (We will compare the three merge styles in Week 3; merge commit is the most faithful for now.)

After merging, click **Delete branch** (GitHub offers the button right there).

#### Pull the merged change back to local `main`

```bash
git checkout main
git pull
git log --oneline
```

You should see something like (hashes differ):

```
d5c9af3 Merge pull request #2 from user/1-add-a-license-file
e8b1a02 Add CC-BY-4.0 license placeholder
7f3e1c2 Add project goals to README
b04a2d7 Add initial research notes
a9e5f01 Add README with project description
```

Issue 1 is closed automatically. The loop is complete.

#### Do it once more for practice

Try another round with a slightly bigger change:

```bash
gh issue create --title "Add a CONTRIBUTING.md" --body "Document how collaborators (human or AI) should open PRs."

gh issue develop <issue-number> --checkout

cat > CONTRIBUTING.md <<'EOF'
# Contributing

Open an issue before starting work. Branch from `main` using
`gh issue develop <N>`. Keep commits atomic and under 50 characters.
Open a PR when the branch is ready; link the issue with `Closes #N`.
EOF

git add CONTRIBUTING.md
git commit -m "Add CONTRIBUTING guide"
git push -u origin "$(git branch --show-current)"
gh pr create --title "Add CONTRIBUTING guide" --body "Closes #<issue-number>"
gh pr view --web
```

Merge, delete branch, `git pull`. You have now run the loop twice. By Week 3 it will be automatic.

### 11. Verify Everything Works

```bash
git --version       # Git is installed
gh --version        # GitHub CLI is installed
pwd                 # You are in your project
git status          # Git is tracking the project
git log --oneline   # You have commits
git remote -v       # Your remote is set
gh issue list       # You can list issues from the terminal
gh pr list --state all
```

If all of these work, you are ready for Week 2.

---

## Before Next Session

!!! note "Install Claude Code"
    Before Week 2, install [Claude Code](https://claude.ai/claude-code):

    === "macOS"

        ```bash
        brew install claude-code
        ```

        Or via the installer:

        ```bash
        curl -fsSL https://claude.ai/install.sh | bash
        ```

    === "Linux"

        ```bash
        curl -fsSL https://claude.ai/install.sh | bash
        ```

    === "Windows"

        In PowerShell:

        ```powershell
        irm https://claude.ai/install.ps1 | iex
        ```

        Or in your WSL Ubuntu terminal, follow the Linux instructions above.

    Verify:

    ```bash
    claude --version
    ```

    We will walk through the full setup together in Week 2. If you want to read ahead, the [Week 2 setup guide](./week-02.md) has the same material in written form.

---

## Quick Reference

### Terminal

| Command | What it does |
|---------|-------------|
| `pwd` | Print current directory |
| `ls` | List files |
| `cd <dir>` | Change directory |
| `mkdir <name>` | Create a directory |

### Git (version control)

| Command | What it does |
|---------|-------------|
| `git init` | Start tracking a folder |
| `git status` | See what changed |
| `git add <file>` | Stage a file for commit |
| `git diff` | Show unstaged changes |
| `git diff --staged` | Show staged changes |
| `git commit -m "msg"` | Save a snapshot |
| `git push` | Send commits to GitHub |
| `git pull` | Get updates from GitHub |
| `git log --oneline` | View commit history |
| `git show` | Show the last commit |
| `git restore <file>` | Discard working-directory changes (the undo button) |
| `git restore --staged <file>` | Unstage a file, keep the edits |
| `git revert <hash>` | Safely undo a committed change with a new commit |
| `git clone <url>` | Copy a remote repo |
| `git branch --show-current` | Print the current branch name |
| `git checkout <branch>` | Switch to a branch |

### GitHub CLI (`gh`)

| Command | What it does |
|---------|-------------|
| `gh auth login` | Authenticate with GitHub |
| `gh repo create` | Create a new repository |
| `gh repo clone user/repo` | Clone a GitHub repo |
| `gh issue create` | Open a new issue |
| `gh issue list` | List open issues |
| `gh issue develop <n> --checkout` | Create a branch from an issue and check it out |
| `gh pr create` | Open a pull request |
| `gh pr view` | View pull request details |
| `gh pr view --web` | Open the PR page in your browser |
| `gh pr list` | List open pull requests |

### The GitHub workflow loop

```
Issue  ->  Branch  ->  Commits  ->  Pull Request  ->  Review  ->  Merge  ->  Pull main
```

---

## Resources

- [Git documentation](https://git-scm.com/doc)
- [Pro Git book](https://git-scm.com/book/en/v2) (free, covers the three states in depth)
- [GitHub Skills](https://skills.github.com/) (free interactive courses)
- [Course repository](https://github.com/OpenScience-Collective/agentic-research-course)
- [Week 1 blog (plain markdown source)](https://github.com/OpenScience-Collective/agentic-research-course/blob/main/blog/week-01-setup-guide.md)
- [Week 2 setup guide](./week-02.md) (Claude Code, CLAUDE.md, prompting)
- [Open Science Collective Discord](https://discord.gg/5dWJCUmUww)
- [research-skills plugin](https://github.com/neuromechanist/research-skills)

<style>
.embed-container {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 8px;
  margin-bottom: 1.5rem;
}
.embed-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}
.slide-hint {
  margin: -0.5rem 0 1.5rem 0;
  font-size: 0.75rem;
  color: var(--md-default-fg-color--lighter);
}
.slide-hint kbd {
  font-size: 0.7rem;
  padding: 0.1rem 0.3rem;
  border: 1px solid var(--md-default-fg-color--lightest);
  border-radius: 3px;
  background: var(--md-code-bg-color);
}
</style>
