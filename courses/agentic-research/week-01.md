# Week 1: Git, GitHub, and the Command Line

## Overview

This session does double duty: it teaches the foundational tools (git, terminal, GitHub) and sets the stage for the entire course. The core argument is simple: AI coding agents like Claude Code are extraordinarily powerful, and that power is exactly why you need version control, quality assurance (QA), and structured workflows.

!!! abstract "Learning Objectives"
    - Describe the current landscape of AI coding agents and how they fit into research workflows
    - Explain why AI-powered productivity demands stronger quality assurance, not weaker
    - Navigate the filesystem using `cd`, `ls`, `pwd`, `mkdir`
    - Initialize a git repository, stage files, commit, push to GitHub
    - Understand the difference between `git` (version control) and `gh` (GitHub CLI)
    - Create branches, pull requests, and issues on GitHub

<!-- ## Recording

<div class="embed-container">
  <iframe
    src="https://www.youtube.com/embed/VIDEO_ID_HERE"
    title="Week 1: Git, GitHub, and the Command Line"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen>
  </iframe>
</div> -->

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

=== "macOS: Homebrew"

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

    Follow the on-screen instructions, then verify:

    ```bash
    brew --version
    ```

=== "Linux (Debian/Ubuntu) or WSL"

    You already have `apt`. Update it:

    ```bash
    sudo apt update
    ```

### 3. Install Git and the GitHub CLI

You need two command-line tools: `git` for version control and `gh` (the GitHub CLI) for interacting with GitHub.

=== "macOS"

    ```bash
    brew install git gh
    ```

=== "Linux or WSL"

    ```bash
    sudo apt install git gh
    ```

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
    2. Click **Join Global Campus**
    3. Verify your academic status (use your `.edu` email or upload proof of enrollment)
    4. Once approved, you get GitHub Pro for free, plus access to dozens of developer tools

    Benefits include unlimited private repos, GitHub Copilot access, and free domain names.

=== "Faculty and researchers"

    Apply for the [GitHub Teacher Toolbox](https://education.github.com/teachers):

    1. Go to [education.github.com/teachers](https://education.github.com/teachers)
    2. Click **Join Global Campus**
    3. Verify your academic status with your institutional email
    4. Once approved, you get GitHub Pro and can create free GitHub Classroom organizations

=== "Research labs (organizations)"

    If your lab or research group has a GitHub organization, you can upgrade it to GitHub Team for free:

    1. Visit [education.github.com/globalcampus/teacher](https://education.github.com/globalcampus/teacher) (you must be verified as faculty first)
    2. Find the **Upgrade your academic organizations** section
    3. Click **Upgrade to GitHub Team**
    4. Select your organization and click **Upgrade**

    This gives your entire lab access to GitHub Team features for free: protected branches, required reviews, code owners, advanced audit logs, and more. Highly recommended for any research group managing shared code.

#### Set up SSH keys (recommended)

SSH keys let you push to GitHub without typing your password every time.

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

Follow the prompts: select GitHub.com, choose SSH, and authenticate through your browser.

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

View your history:

```bash
git log --oneline
```

### 8. Push to GitHub

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

Refresh the GitHub page. Your files and commits are now online.

### 9. Verify Everything Works

```bash
git --version       # Git is installed
gh --version        # GitHub CLI is installed
pwd                 # You are in your project
git status          # Git is tracking the project
git log --oneline   # You have commits
git remote -v       # Your remote is set
```

If all of these work, you are ready for Week 2.

---

## Before Next Session

!!! note "Install Claude Code"
    Before Week 2, install [Claude Code](https://claude.ai/claude-code):

    === "macOS / Linux"

        ```bash
        brew install claude-code
        ```

    === "Official installer"

        ```bash
        curl -fsSL https://claude.ai/install-cli | sh
        ```

    Verify:

    ```bash
    claude --version
    ```

    We will walk through the full setup together in Week 2.

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
| `git commit -m "msg"` | Save a snapshot |
| `git push` | Send commits to GitHub |
| `git pull` | Get updates from GitHub |
| `git log --oneline` | View commit history |
| `git diff` | Show uncommitted changes |
| `git clone <url>` | Copy a remote repo |

### GitHub CLI (`gh`)

| Command | What it does |
|---------|-------------|
| `gh auth login` | Authenticate with GitHub |
| `gh repo create` | Create a new repository |
| `gh repo clone user/repo` | Clone a GitHub repo |
| `gh issue create` | Open a new issue |
| `gh issue develop <num>` | Create a branch from an issue |
| `gh pr create` | Open a pull request |
| `gh pr view` | View pull request details |

---

## Resources

- [Git documentation](https://git-scm.com/doc)
- [GitHub Skills](https://skills.github.com/) (free interactive courses)
- [Course repository](https://github.com/OpenScience-Collective/agentic-research-course)
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
