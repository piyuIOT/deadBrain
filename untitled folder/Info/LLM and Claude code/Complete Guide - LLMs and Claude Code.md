# The Complete Guide to LLMs and Claude Code

## Part 1: Understanding Large Language Models (LLMs)

### What is an LLM?

Think of a Large Language Model as an extremely well-read assistant that has consumed millions of books, articles, and code repositories. But here's the twist: it doesn't remember specific facts like a database. Instead, it has learned **patterns** in how language works.

When you ask it a question, it's not looking up an answer. It's generating text, one word (or "token") at a time, based on patterns it learned during training. It's like how you can finish the sentence "Once upon a..." without ever memorizing that specific phrase—you just know how stories typically start.

### Key Concepts You Need to Know

#### Tokens: The Currency of LLMs

LLMs don't see words the way you do. They break text into **tokens**:
- A token might be a word, part of a word, or even punctuation
- "hello" = 1 token
- "understanding" might be 2 tokens: "under" + "standing"
- Code is also tokenized: `function()` might be 3-4 tokens

**Why this matters:** Every interaction has a cost measured in tokens, and every LLM has limits on how many tokens it can process.

#### Context Window: The Working Memory

Imagine having a conversation with someone who can only remember the last 5 minutes. That's essentially what a context window is—the amount of text an LLM can "see" at once.

- **Older models:** 4,000-8,000 tokens (~3-6 pages of text)
- **Modern models:** 100,000-200,000+ tokens (~75-150 pages)

Everything counts toward this limit: your messages, the LLM's responses, system instructions, and any documents you provide.

**Why this matters:**
- Long codebases might exceed the context window
- Better tools use smart strategies to work within these limits
- The context window is like RAM—it's temporary working memory, not long-term storage

#### Prompts: How to Talk to an LLM

A **prompt** is your instruction to the LLM. Good prompts are specific, clear, and provide context:

**Bad prompt:**
```
Fix the bug
```

**Good prompt:**
```
There's a bug in the login function where users with special characters
in their email addresses can't log in. The error happens in
src/auth/login.js around line 42. Please investigate and fix it.
```

**Pro tips:**
- Be specific about what you want
- Provide relevant context
- Break complex tasks into steps
- Use examples when possible

### Function Calling: Giving LLMs Superpowers

Here's where things get interesting. LLMs are great at understanding and generating text, but they can't directly:
- Read files on your computer
- Run commands
- Search the web
- Access databases

**Function calling** (also called "tool use") bridges this gap. Here's how it works:

1. You give the LLM access to "tools" (functions it can call)
2. The LLM decides when to use a tool based on your request
3. The tool executes and returns results
4. The LLM uses those results to continue the conversation

**Example:**
```
You: "What's the weather in New York?"
LLM: [Thinks: I need weather data, I'll use the weather_api tool]
LLM: [Calls: weather_api("New York")]
Tool: [Returns: "72°F, sunny"]
LLM: "The weather in New York is 72°F and sunny!"
```

Without function calling, the LLM would just make up an answer (called "hallucinating").

### Agents: LLMs That Take Action

An **agent** is an LLM that can:
1. Plan a sequence of actions
2. Use tools to gather information or make changes
3. Observe the results
4. Adjust its plan accordingly

**Simple LLM interaction:**
```
You: "Analyze this code"
LLM: "I can't see your code, please paste it"
```

**Agent-based interaction:**
```
You: "Analyze the authentication code"
Agent: [Uses file search tool to find auth files]
Agent: [Reads the relevant files]
Agent: [Analyzes the code]
Agent: "I found your authentication code in src/auth/.
       Here's my analysis: ..."
```

Agents are proactive and autonomous. They figure out what tools to use and when to use them.

### Agentic Orchestration: Multiple Agents Working Together

Sometimes one agent isn't enough. **Agentic orchestration** means coordinating multiple specialized agents:

- **Explore Agent:** Searches and understands the codebase
- **Plan Agent:** Designs implementation strategies
- **Code Agent:** Writes the actual code
- **Test Agent:** Runs tests and validates changes
- **Review Agent:** Checks code quality

Each agent is optimized for its specific task, making the overall system more efficient and capable.

### Model Context Protocol (MCP): The Universal Connector

**MCP** is like a USB port for LLMs—a standard way to connect them to external tools and data sources.

**Without MCP:** Every tool integration is custom-built and fragile.
**With MCP:** Tools expose their capabilities through a standard protocol, and any MCP-compatible LLM can use them.

**MCP servers you can use:**
- **GitHub:** Access repositories, issues, PRs
- **Google Drive:** Read and write documents
- **Filesystem:** Navigate your local files
- **Browser:** Interact with web pages
- **Databases:** Query SQL databases
- **Slack:** Send messages, read channels

Think of MCP as the app store for LLM capabilities.

---

## Part 2: Claude Code - Your AI Coding Partner

### What is Claude Code?

Claude Code is Anthropic's official AI coding tool. It's not just a chatbot that knows programming—it's an **agentic system** that can:

- Edit files directly in your codebase
- Run terminal commands
- Search and understand your project structure
- Create git commits and pull requests
- Integrate with external tools via MCP
- Execute multi-step workflows autonomously

**Key difference from other tools:**
- **Not a chat window:** Works directly in your terminal
- **Not an autocomplete:** Makes architectural decisions and implements features
- **Not passive:** Takes direct action on your codebase

### Installation

Choose your preferred method:

**Quick install (macOS/Linux/WSL):**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Homebrew:**
```bash
brew install --cask claude-code
```

**NPM (requires Node.js 18+):**
```bash
npm install -g @anthropic-ai/claude-code
```

First-time use requires authentication with your Claude.ai account. Claude Code auto-updates, so you're always on the latest version.

### Getting Started: Your First Session

Navigate to your project and start Claude:

```bash
cd my-project
claude
```

**Try these starter prompts:**
```
"Explain what this project does"
"Where is the user authentication handled?"
"Add error handling to the login function"
"Run the tests and fix any failures"
```

Claude will read files, search the codebase, and take action based on your instructions.

### Interactive Mode: The Command Center

Interactive mode is where you'll spend most of your time. It's a rich terminal interface with powerful shortcuts and features.

#### Essential Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit Claude Code |
| `Ctrl+L` | Clear screen (keeps conversation) |
| `Esc` `Esc` | Rewind to previous state |
| `Shift+Tab` | Toggle permission modes |
| `Ctrl+B` | Background current command |

#### Multiline Input

When writing longer prompts or pasting code:
- `\` + `Enter` — Continue on next line (all platforms)
- `Shift+Enter` — Alternative multiline (after setup)

#### Special Input Modes

**Bash Mode** (prefix with `!`):
Run commands directly without Claude's interpretation:
```
! git status
! npm test
! ls -la
```

**Memory Mode** (prefix with `#`):
Add important context to CLAUDE.md file:
```
#Remember: We use tabs, not spaces
#Database password is in .env.local
```

**Vim Mode**:
Enable with `/vim` for full vim keybindings in the input area. Perfect if you're a vim user.

### CLAUDE.md: Your Project's Brain

**CLAUDE.md** is a special file that Claude automatically reads. Use it to document:

- **Code style:** "We use 2-space indentation, single quotes"
- **Architecture:** "Auth is handled by Firebase, payments by Stripe"
- **Testing:** "Run `npm test` before committing"
- **Quirks:** "The production API uses different endpoints"
- **Commands:** "Deploy with `./deploy.sh staging`"

**Where to place it:**
- Project root: `my-project/CLAUDE.md`
- Monorepo parent: `monorepo/CLAUDE.md`
- Global: `~/.claude/CLAUDE.md`

**Example CLAUDE.md:**
```markdown
# Project Context

## Tech Stack
- React 18 with TypeScript
- Node.js backend with Express
- PostgreSQL database
- Jest for testing

## Code Style
- Use functional components with hooks
- Prefer async/await over promises
- All new features need tests

## Commands
- Start dev: `npm run dev`
- Run tests: `npm test`
- Build: `npm run build`

## Important Notes
- API keys are in .env.local (not committed)
- Database migrations run automatically on start
- Don't modify files in /generated folder
```

### Permission Modes: Control What Claude Can Do

Claude Code has three permission modes:

**Normal Mode** (default):
- Claude asks before editing files, running commands, or committing
- Safest option when starting out

**Auto-Accept Mode** (`Shift+Tab`):
- Claude takes action without asking
- Faster workflow once you're comfortable
- Great for trusted operations like testing and linting

**Plan Mode**:
- Claude explores and plans without making changes
- Reviews the plan with you before implementing
- Best for complex features or unfamiliar codebases

**Customize permissions:**
```bash
/permissions
```

Set allowlists for operations you trust (e.g., `git status`, `npm test`).

### Workflows That Work

#### 1. Explore, Plan, Code, Commit

**The deliberate approach for new features:**

```
You: "I need to add user profile editing functionality"

[Explore Phase]
Claude: [Reads existing user management code]
Claude: [Understands current database schema]
Claude: [Identifies relevant API endpoints]

You: "Think through how to implement this"

[Plan Phase - Extended Thinking]
Claude: "Here's my plan:
1. Add PUT endpoint to /api/user/profile
2. Create ProfileEdit component
3. Add validation for email/username
4. Update database schema if needed
5. Write tests for new functionality"

You: "Looks good, implement it"

[Code Phase]
Claude: [Creates files, edits code, implements feature]

You: "Run the tests"

Claude: [Runs test suite, fixes any failures]

You: "Commit this work"

Claude: [Creates git commit with descriptive message]
```

#### 2. Test-Driven Development (TDD)

**Write tests first, then implement:**

```
You: "Write tests for a password validation function that requires:
- At least 8 characters
- One uppercase letter
- One number
- One special character"

Claude: [Writes comprehensive test suite]

You: "Run the tests"

Claude: [Runs tests - they all fail as expected]

You: "Now implement the validation function"

Claude: [Implements function to pass all tests]

You: "Run tests again"

Claude: [All tests pass ✓]
```

#### 3. Visual Iteration

**Perfect for UI work:**

```
You: "Here's a mockup of the login page I want"
[Paste screenshot or drag-and-drop image]

Claude: [Implements the UI]

You: "Take a screenshot of how it looks now"

Claude: [Runs app, captures screenshot]

You: "The spacing is too tight, and make the button blue"

Claude: [Adjusts styling]

[Repeat until perfect]
```

#### 4. Debug and Fix

**Let Claude investigate issues:**

```
You: "Users are reporting login failures. Investigate."

Claude: [Reads auth code]
Claude: [Checks error logs]
Claude: [Identifies issue with token validation]
Claude: "Found the problem - tokens are expiring too quickly
        due to a timezone issue in tokenValidation.js:45"

You: "Fix it and add tests to prevent this"

Claude: [Fixes bug, adds regression tests]
```

#### 5. Git and GitHub Operations

**Leverage Claude for version control:**

```
"Search git history for when the API endpoint changed"
"Create a new branch called feature/user-export"
"Write a commit message for these changes"
"Create a PR comparing this branch to main"
"What caused the CI failure in the latest PR?"
```

Install `gh` CLI for full GitHub integration.

### Background Commands: Multitask Like a Pro

Long-running processes don't block Claude:

```
You: "Run the build in the background"

Claude: [Starts build process in background]
Claude: "Build running in background (task id: bg_123)"

[You can continue working while build runs]

You: "Check on the build"

Claude: [Shows build output]
Claude: "Build completed successfully ✓"
```

**Press `Ctrl+B` during any command to background it.**

Common background tasks:
- Test suites
- Development servers
- Build processes
- Long-running scripts

### Slash Commands: Quick Actions

Access built-in commands with `/`:

| Command | Purpose |
|---------|---------|
| `/help` | Show help documentation |
| `/clear` | Clear conversation (fresh start) |
| `/permissions` | Configure tool permissions |
| `/vim` | Enable vim keybindings |
| `/config` | Open configuration file |
| `/tasks` | List background tasks |

### Best Practices: Work Smarter

#### Be Specific

**Vague:**
```
"Fix the performance issue"
```

**Specific:**
```
"The user list page loads slowly when there are >1000 users.
Profile the code, identify bottlenecks, and optimize the query
in src/api/users.js"
```

#### Provide Context

Include relevant information upfront:
- Files that are related
- Error messages
- Expected vs actual behavior
- Constraints (backwards compatibility, performance targets)

#### Use Visual Input

Claude can see images! Use them:
- Design mockups
- Error screenshots
- Architecture diagrams
- Example outputs

**How to provide images:**
- Paste from clipboard: `Ctrl+V` (Mac/Linux) or `Alt+V` (Windows)
- Drag and drop into terminal
- Provide file path: `screenshot.png`

#### Break Down Large Tasks

**Instead of:**
```
"Build a complete e-commerce checkout flow"
```

**Try:**
```
1. "Add shopping cart functionality"
2. "Implement checkout form with validation"
3. "Integrate payment processing"
4. "Add order confirmation page"
```

#### Use /clear Between Unrelated Tasks

Context accumulates during long sessions. Reset when switching focus:

```
[Just finished work on authentication]

/clear

"Now I need to work on the email notification system"
```

#### Let Claude Explore First

Before jumping to code:

```
You: "Read the payment processing code and understand how it works"

Claude: [Explores, reads files, understands architecture]

You: "Now add support for refunds"

Claude: [Implements following existing patterns]
```

### Model Context Protocol (MCP): Extend Claude's Capabilities

MCP servers give Claude access to external tools and data.

#### Installing MCP Servers

**Add a server:**
```bash
claude mcp add server-name npx package-name
```

**Example - GitHub integration:**
```bash
claude mcp add github npx @modelcontextprotocol/server-github
```

**Example - Browser control:**
```bash
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest
```

#### Popular MCP Servers

**Filesystem Access:**
```bash
claude mcp add filesystem npx @modelcontextprotocol/server-filesystem
```
Gives Claude safe access to specific directories.

**PostgreSQL:**
```bash
claude mcp add postgres npx @modelcontextprotocol/server-postgres
```
Query and manage databases.

**Brave Search:**
```bash
claude mcp add brave-search npx @modelcontextprotocol/server-brave-search
```
Search the web for information.

**Slack:**
```bash
claude mcp add slack npx @modelcontextprotocol/server-slack
```
Send messages and read channels.

#### Configuration

MCP servers can be configured in:
1. Project config: `.mcp.json` in your project
2. Global config: `~/.claude/config.json`

**Example .mcp.json:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Advanced Features

#### Subagents: Specialized Workers

Claude Code can spawn specialized agents for specific tasks:

- **Explore Agent:** Fast codebase exploration and search
- **Plan Agent:** Design implementation strategies
- **General Agent:** Complex multi-step research tasks

You don't usually invoke these manually—Claude automatically uses them when appropriate. But you can be explicit:

```
"Use the explore agent to find all API endpoints"
"Create a plan for refactoring the auth system"
```

#### Checkpointing: Time Travel for Code

Made a mistake? Rewind:

**Undo last change:**
- Press `Esc` `Esc` to rewind conversation and code

**Explore alternatives:**
- Rewind to a previous state
- Edit your prompt
- See how different instructions lead to different implementations

#### Parallel Work: Multiple Claude Instances

Run separate Claude sessions for independent work:

**Terminal 1:**
```bash
cd my-project/frontend
claude
"Refactor the user components"
```

**Terminal 2:**
```bash
cd my-project/backend
claude
"Add caching to the API"
```

**Use git worktrees for true isolation:**
```bash
git worktree add ../feature-branch feature-branch
cd ../feature-branch
claude
```

#### Headless Mode: Automate Everything

Use Claude in scripts and CI/CD:

```bash
claude -p "Run the test suite and fix any failures" \
  --output-format stream-json
```

**CI/CD Integration:**
```yaml
# .github/workflows/claude-fix-tests.yml
name: Auto-fix Tests
on: [push]
jobs:
  fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: claude -p "Fix failing tests" --auto-approve
```

### Common Pitfalls to Avoid

**1. Jumping straight to code**
- Let Claude explore and understand first
- Ask for a plan before implementation

**2. Overloading CLAUDE.md**
- Keep it concise and relevant
- Test what actually helps vs adds noise

**3. Vague instructions**
- Be specific about requirements
- Provide examples and constraints

**4. Ignoring early course-correction**
- If Claude starts down the wrong path, interrupt early
- Press `Ctrl+C` and clarify

**5. Letting context bloat**
- Use `/clear` between unrelated tasks
- Start fresh sessions for new features

**6. Not using permissions wisely**
- Start conservative, then add trusted operations
- Use auto-approve for safe, repetitive tasks

### Where Claude Code Extends

Claude Code isn't just a CLI. It's available across your entire workflow:

**Web Interface:** [claude.ai/code](https://claude.ai/code)
- Asynchronous cloud execution
- Access from any device
- Great for planning and exploration

**Desktop App:** Claude desktop
- Integrated experience
- System-wide access

**IDE Extensions:**
- VS Code
- JetBrains (IntelliJ, PyCharm, etc.)
- Visual Studio

**CI/CD Platforms:**
- GitHub Actions
- GitLab CI/CD
- Jenkins

**Collaboration Tools:**
- Slack integration
- Team workflows

**Browser:** Chrome extension (beta)
- Interact with web apps
- Test and debug web interfaces

### Resources and Next Steps

**Official Documentation:**
- [Claude Code Docs](https://code.claude.com/docs/en/overview)
- [Best Practices Guide](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)

**Community:**
- [GitHub Issues](https://github.com/anthropics/claude-code/issues)
- Discord community
- Example projects and templates

**Build Custom Extensions:**
- Create custom slash commands in `.claude/commands/`
- Build MCP servers for your tools
- Use Claude Agent SDK (Python/TypeScript)

### Final Thoughts

Claude Code is most powerful when you think of it as a **collaborator**, not just a tool:

- **Explain your goals**, not just the implementation
- **Iterate together** through exploration, planning, and coding
- **Use its strengths**: reading large codebases, following patterns, handling repetitive tasks
- **Apply your judgment**: review changes, make architectural decisions, ensure correctness

The developers who thrive with AI are those who master the symbiosis—using Claude Code to amplify their capabilities while maintaining deep understanding of their codebase.

You're not replacing your skills. You're multiplying them.

---

**Happy coding!**
