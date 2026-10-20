# Effective Context Engineering for AI Agents

> Source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
> Authors: Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, and Jeremy Hadfield (Anthropic Applied AI team)
> Contributors: Rafi Ayub, Hannah Moran, Cal Rueb, Connor Jennings, Molly Vorwerck, Stuart Ritchie, Maggie Vo

---

## Introduction

Context engineering represents a fundamental shift in how developers build with language models. As the field has progressed beyond prompt engineering, teams now focus on "what configuration of context is most likely to generate our model's desired behavior?"

**Context** comprises the set of tokens provided to an LLM during sampling. The **engineering** challenge involves optimizing token utility against LLM constraints to achieve consistent, desired outcomes. This requires "thinking in context" -- understanding the holistic state available to the model and potential behaviors it might produce.

## Context Engineering vs. Prompt Engineering

Anthropic views context engineering as the natural progression of prompt engineering. While prompt engineering focuses on writing and organizing LLM instructions for optimal outcomes, context engineering addresses "the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts."

Early LLM engineering emphasized prompting for one-shot tasks. However, as agents operate over multiple inference turns and longer time horizons, developers need strategies for managing entire context states -- system instructions, tools, Model Context Protocol (MCP), external data, and message history.

Agents running in loops generate increasingly more potentially relevant data. Context engineering is the "art and science" of curating what enters the limited context window from that constantly evolving universe of possible information.

## Why Context Engineering Matters for Capable Agents

LLMs experience performance degradation with increased context, similar to human cognitive limitations. Research on needle-in-a-haystack benchmarking has uncovered "context rot": as tokens in the context window increase, the model's ability to accurately recall information from that context decreases.

Context must be treated as a finite resource with diminishing marginal returns. Like humans with limited working memory, LLMs have an "attention budget" that depletes with each new token introduced.

### Architectural Constraints

This attention scarcity stems from LLM architecture. Transformers enable every token to attend to every other token across the entire context, creating n-squared pairwise relationships for n tokens. As context length increases, the model's ability to capture these relationships becomes stretched thin.

Models develop attention patterns from training data where shorter sequences are more common than longer ones, meaning they have less experience with context-wide dependencies. Position encoding interpolation techniques allow handling longer sequences by adapting to originally trained smaller contexts, though with some degradation in token position understanding.

This creates a performance gradient rather than a hard cliff: models remain capable at longer contexts but may show reduced precision for information retrieval and long-range reasoning compared to shorter contexts.

## The Anatomy of Effective Context

Good context engineering means "finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." Implementing this across context components requires careful consideration.

### System Prompts

System prompts should be extremely clear using simple, direct language that presents ideas at the "right altitude." This represents the optimal balance between two failure modes:

**At one extreme:** Engineers hardcode complex, brittle logic in prompts to elicit exact behavior. This creates fragility and increases maintenance complexity.

**At the other extreme:** Vague, high-level guidance fails to give the LLM concrete signals for desired outputs or falsely assumes shared context.

**Optimal altitude:** Specific enough to guide behavior effectively, yet flexible enough to provide strong heuristics.

Recommended approach: Organize prompts into distinct sections using XML tagging or Markdown headers (e.g., `<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description`).

Strive for minimal information that fully outlines expected behavior. Start by testing a minimal prompt with the best available model, then iteratively add clear instructions and examples based on identified failure modes.

### Tools

Tools allow agents to operate within their environment and pull in new context as they work. Since tools define the contract between agents and their information/action space, they must promote efficiency by returning token-efficient information and encouraging efficient agent behaviors.

Tools should be:
- Self-contained and robust to error
- Extremely clear regarding intended use
- Have descriptive, unambiguous input parameters
- Play to the model's inherent strengths

**Common failure mode:** Bloated tool sets covering too much functionality or creating ambiguous decision points about which tool to use. If human engineers cannot definitively state which tool applies in a given situation, AI agents cannot be expected to perform better.

Curating a minimal viable tool set leads to more reliable maintenance and context pruning over long interactions.

### Examples and Few-Shot Prompting

Providing examples through few-shot prompting remains a well-established best practice. However, avoid stuffing exhaustive edge cases into prompts in attempts to articulate every possible rule.

Instead, curate diverse, canonical examples that effectively portray expected agent behavior. For LLMs, "examples are the 'pictures' worth a thousand words."

### Overall Guidance

Across all context components (system prompts, tools, examples, message history), maintain thoughtful curation: keep context informative, yet tight.

## Context Retrieval and Agentic Search

Modern agent definition: "LLMs autonomously using tools in a loop."

### The Shift to "Just-In-Time" Context

Historically, many AI applications employed embedding-based pre-inference retrieval to surface important context. The field increasingly adopts "just-in-time" context strategies that augment retrieval systems.

Rather than pre-processing all relevant data upfront, agents maintain lightweight identifiers (file paths, stored queries, web links) and dynamically load data into context at runtime using tools.

Anthropic's Claude Code uses this approach for complex data analysis over large databases. The model writes targeted queries, stores results, and leverages Bash commands like `head` and `tail` to analyze data without loading full objects into context. This mirrors human cognition: people don't memorize entire corpuses but introduce external organization systems (file systems, inboxes, bookmarks) to retrieve relevant information on demand.

### Metadata as Guidance

Metadata of references provides mechanisms to efficiently refine behavior. For example, a file named `test_utils.py` in a `tests` folder signals different purpose than the same filename in `src/core_logic/`. Folder hierarchies, naming conventions, and timestamps provide signals helping both humans and agents understand how and when to utilize information.

### Progressive Disclosure

Autonomous agent navigation enables progressive disclosure -- agents incrementally discover relevant context through exploration. Each interaction yields context informing the next decision: file sizes suggest complexity, naming conventions hint at purpose, timestamps proxy relevance. Agents assemble understanding layer by layer, maintaining only necessary working memory while leveraging note-taking for additional persistence. This keeps agents focused on relevant subsets rather than drowning in exhaustive information.

### Trade-offs and Hybrid Strategies

Runtime exploration is slower than retrieving pre-computed data. Agents require proper guidance through appropriate tools and heuristics to navigate information landscapes effectively. Without this, agents waste context through tool misuse, dead-ends, or failing to identify key information.

**Hybrid approach:** Some tasks benefit from retrieving data upfront for speed while pursuing further autonomous exploration at the agent's discretion. The appropriate autonomy level depends on task characteristics.

Claude Code exemplifies hybrid modeling: `CLAUDE.md` files are naively dropped into context upfront, while primitives like glob and grep allow runtime navigation and just-in-time retrieval, bypassing stale indexing and complex syntax trees.

Hybrid strategies suit contexts with less dynamic content (legal, finance work). As model capabilities improve, agentic design trends toward allowing intelligent models to act intelligently with progressively less human curation. For teams building agents, "do the simplest thing that works" remains best advice.

## Context Engineering for Long-Horizon Tasks

Long-horizon tasks requiring agents to maintain coherence, context, and goal-directed behavior over sequences where token count exceeds context window limits need specialized techniques. Tasks spanning tens of minutes to multiple hours (large codebase migrations, comprehensive research projects) require working around context window limitations.

Waiting for larger context windows alone is insufficient -- all context window sizes face context pollution and information relevance concerns. Three key techniques address context pollution constraints:

### Compaction

Compaction takes conversations nearing the context window limit, summarizes contents, and reinitializes new context windows with summaries. It typically serves as the first lever in context engineering for better long-term coherence, distilling context window contents in high-fidelity manner enabling agents to continue with minimal performance degradation.

Claude Code implements this by passing message history to the model for summarization and compression of critical details. The model preserves architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs or messages. Agents continue with compressed context plus five most recently accessed files, providing continuity without context window worries.

**The art of compaction** lies in selecting what to keep versus discard. Overly aggressive compaction risks losing subtle but critical context whose importance only becomes apparent later. Recommendations:
- Carefully tune prompts on complex agent traces
- Maximize recall first to capture all relevant information
- Iterate to improve precision by eliminating superfluous content

Low-hanging superfluous content includes clearing tool calls and results. Once tools are called deep in message history, agents rarely need raw results again. Tool result clearing represents one of the safest, lightest-touch compaction forms, recently launched as a feature on the Claude Developer Platform.

### Structured Note-Taking (Agentic Memory)

Structured note-taking involves agents regularly writing notes persisted to memory outside the context window, which get pulled back into context later.

This strategy provides persistent memory with minimal overhead. Like Claude Code creating to-do lists or custom agents maintaining `NOTES.md` files, this simple pattern lets agents track progress across complex tasks, maintaining critical context and dependencies that would otherwise be lost across dozens of tool calls.

Claude playing Pokemon demonstrates memory transforming agent capabilities in non-coding domains. The agent maintains precise tallies across thousands of game steps -- tracking objectives like "for the last 1,234 steps I've been training my Pokemon in Route 1, Pikachu has gained 8 levels toward the target of 10." Without prompting about memory structure, it develops maps of explored regions, remembers unlocked achievements, and maintains strategic notes about combat effectiveness.

After context resets, agents read their own notes and continue multi-hour sequences. This coherence across summarization steps enables long-horizon strategies impossible when keeping all information in LLM context windows alone.

As part of the Sonnet 4.5 launch, Anthropic released a memory tool in public beta on the Claude Developer Platform, making it easier to store and consult information outside context windows through file-based systems. This allows agents to build knowledge bases over time, maintain project state across sessions, and reference previous work without keeping everything in context.

### Sub-Agent Architectures

Sub-agent architectures provide another way around context limitations. Rather than single agents maintaining state across entire projects, specialized sub-agents handle focused tasks with clean context windows. The main agent coordinates with high-level plans while subagents perform deep technical work or find relevant information. Each subagent might explore extensively using tens of thousands of tokens but returns only condensed, distilled summaries (typically 1,000-2,000 tokens).

This achieves clear separation of concerns -- detailed search context remains isolated within sub-agents while lead agents focus on synthesizing and analyzing results. Research on multi-agent systems showed substantial improvement over single-agent systems on complex research tasks.

### Selecting Appropriate Approaches

The choice between techniques depends on task characteristics:

- **Compaction** maintains conversational flow for tasks requiring extensive back-and-forth
- **Note-taking** excels for iterative development with clear milestones
- **Multi-agent architectures** handle complex research and analysis where parallel exploration pays dividends

Even as models improve, maintaining coherence across extended interactions remains central to building more effective agents.

## Conclusion

Context engineering represents fundamental shifts in how developers build with LLMs. As models become more capable, the challenge extends beyond crafting perfect prompts to thoughtfully curating what information enters the model's limited attention budget at each step.

Whether implementing compaction for long-horizon tasks, designing token-efficient tools, or enabling agents to explore environments just-in-time, the guiding principle remains consistent: "find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."

Techniques outlined continue evolving as models improve. Smarter models already require less prescriptive engineering, allowing agents greater autonomy. However, treating context as a precious, finite resource remains central to building reliable, effective agents.

Developers can get started with context engineering in the Claude Developer Platform today, accessing helpful tips and best practices via the memory and context management cookbook.

---

# Appendix: Claude Code Best Practices (Companion Reference)

> Source: https://code.claude.com/docs/en/best-practices
> Note: The original "Claude Code Best Practices" blog post at anthropic.com/engineering/claude-code-best-practices now redirects to this documentation page.

---

## Core Constraint

Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills.

Claude's context window holds your entire conversation, including every message, every file Claude reads, and every command output. However, this can fill up fast. A single debugging session or codebase exploration might generate and consume tens of thousands of tokens.

This matters since LLM performance degrades as context fills. When the context window is getting full, Claude may start "forgetting" earlier instructions or making more mistakes. The context window is the most important resource to manage.

## Give Claude a Way to Verify Its Work

Include tests, screenshots, or expected outputs so Claude can check itself. This is the single highest-leverage thing you can do.

Claude performs dramatically better when it can verify its own work -- run tests, compare screenshots, and validate outputs.

Without clear success criteria, it might produce something that looks right but actually doesn't work. You become the only feedback loop, and every mistake requires your attention.

| Strategy | Before | After |
|----------|--------|-------|
| **Provide verification criteria** | "implement a function that validates email addresses" | "write a validateEmail function. example test cases: user@example.com is true, invalid is false, user@.com is false. run the tests after implementing" |
| **Verify UI changes visually** | "make the dashboard look better" | "[paste screenshot] implement this design. take a screenshot of the result and compare it to the original. list differences and fix them" |
| **Address root causes, not symptoms** | "the build is failing" | "the build fails with this error: [paste error]. fix it and verify the build succeeds. address the root cause, don't suppress the error" |

## Explore First, Then Plan, Then Code

Separate research and planning from implementation to avoid solving the wrong problem. Use Plan Mode to separate exploration from execution.

The recommended workflow has four phases:

1. **Explore**: Enter Plan Mode. Claude reads files and answers questions without making changes.
2. **Plan**: Ask Claude to create a detailed implementation plan.
3. **Implement**: Switch back to Normal Mode and let Claude code, verifying against its plan.
4. **Commit**: Ask Claude to commit with a descriptive message and create a PR.

Plan Mode is useful, but also adds overhead. For tasks where the scope is clear and the fix is small, ask Claude to do it directly. Planning is most useful when you're uncertain about the approach, when the change modifies multiple files, or when you're unfamiliar with the code being modified.

## Provide Specific Context in Your Prompts

The more precise your instructions, the fewer corrections you'll need.

| Strategy | Before | After |
|----------|--------|-------|
| **Scope the task** | "add tests for foo.py" | "write a test for foo.py covering the edge case where the user is logged out. avoid mocks." |
| **Point to sources** | "why does ExecutionFactory have such a weird api?" | "look through ExecutionFactory's git history and summarize how its api came to be" |
| **Reference existing patterns** | "add a calendar widget" | "look at how existing widgets are implemented on the home page to understand the patterns. HotDogWidget.php is a good example. follow the pattern..." |
| **Describe the symptom** | "fix the login bug" | "users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it" |

### Provide Rich Content

- **Reference files with `@`** instead of describing where code lives
- **Paste images directly** -- copy/paste or drag and drop images into the prompt
- **Give URLs** for documentation and API references
- **Pipe in data** by running `cat error.log | claude`
- **Let Claude fetch what it needs** using Bash commands, MCP tools, or by reading files

## Write an Effective CLAUDE.md

CLAUDE.md is a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules. This gives Claude persistent context it can't infer from code alone.

Keep it concise. For each line, ask: "Would removing this cause Claude to make mistakes?" If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions.

| Include | Exclude |
|---------|---------|
| Bash commands Claude can't guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API documentation (link to docs instead) |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost. If Claude asks you questions that are answered in CLAUDE.md, the phrasing might be ambiguous. Treat CLAUDE.md like code: review it when things go wrong, prune it regularly, and test changes by observing whether Claude's behavior actually shifts.

CLAUDE.md files can import additional files using `@path/to/import` syntax:

```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

CLAUDE.md file locations:
- **Home folder (`~/.claude/CLAUDE.md`)**: applies to all Claude sessions
- **Project root (`./CLAUDE.md`)**: check into git to share with your team
- **Parent directories**: useful for monorepos
- **Child directories**: Claude pulls in child CLAUDE.md files on demand

## Manage Context Aggressively

Run `/clear` between unrelated tasks to reset context.

Claude Code automatically compacts conversation history when you approach context limits, which preserves important code and decisions while freeing space.

During long sessions, Claude's context window can fill with irrelevant conversation, file contents, and commands. This can reduce performance and sometimes distract Claude.

- Use `/clear` frequently between tasks to reset the context window entirely
- When auto compaction triggers, Claude summarizes what matters most, including code patterns, file states, and key decisions
- For more control, run `/compact <instructions>`, like `/compact Focus on the API changes`
- To compact only part of the conversation, use `Esc + Esc` or `/rewind`, select a message checkpoint, and choose **Summarize from here**
- Customize compaction behavior in CLAUDE.md with instructions like `"When compacting, always preserve the full list of modified files and any test commands"`
- For quick questions that don't need to stay in context, use `/btw`

## Use Subagents for Investigation

Delegate research with "use subagents to investigate X". They explore in a separate context, keeping your main conversation clean for implementation.

Since context is your fundamental constraint, subagents are one of the most powerful tools available. When Claude researches a codebase it reads lots of files, all of which consume your context. Subagents run in separate context windows and report back summaries:

```text
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

The subagent explores the codebase, reads relevant files, and reports back with findings, all without cluttering your main conversation.

You can also use subagents for verification after Claude implements something:

```text
use a subagent to review this code for edge cases
```

### Custom Subagent Definition Example

```markdown
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

## Run Multiple Claude Sessions (Writer/Reviewer Pattern)

A fresh context improves code review since Claude won't be biased toward code it just wrote.

| Session A (Writer) | Session B (Reviewer) |
|--------------------|---------------------|
| `Implement a rate limiter for our API endpoints` | |
| | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` | |

## Fan Out Across Files

For large migrations or analyses, distribute work across many parallel Claude invocations:

1. **Generate a task list**: Have Claude list all files that need migrating
2. **Write a script to loop through the list**:
   ```bash
   for file in $(cat files.txt); do
     claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
       --allowedTools "Edit,Bash(git commit *)"
   done
   ```
3. **Test on a few files, then run at scale**: Refine your prompt based on what goes wrong with the first 2-3 files

## Avoid Common Failure Patterns

- **The kitchen sink session.** You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information.
  > **Fix**: `/clear` between unrelated tasks.

- **Correcting over and over.** Claude does something wrong, you correct it, it's still wrong, you correct again. Context is polluted with failed approaches.
  > **Fix**: After two failed corrections, `/clear` and write a better initial prompt incorporating what you learned.

- **The over-specified CLAUDE.md.** If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise.
  > **Fix**: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook.

- **The trust-then-verify gap.** Claude produces a plausible-looking implementation that doesn't handle edge cases.
  > **Fix**: Always provide verification (tests, scripts, screenshots). If you can't verify it, don't ship it.

- **The infinite exploration.** You ask Claude to "investigate" something without scoping it. Claude reads hundreds of files, filling the context.
  > **Fix**: Scope investigations narrowly or use subagents so the exploration doesn't consume your main context.

---

# Appendix: Building Effective Agents (Reference)

> Source: https://www.anthropic.com/research/building-effective-agents
> Published: Dec 19, 2024
> Authors: Erik Schluntz and Barry Zhang

---

## Key Principles

The most successful agent implementations use simple, composable patterns rather than complex frameworks.

### Workflows vs. Agents

- **Workflows**: Systems where LLMs and tools are orchestrated through predefined code paths
- **Agents**: Systems where LLMs dynamically direct their own processes and tool usage

### When to Use Agents

Agentic systems often trade latency and cost for better task performance. For many applications, optimizing single LLM calls with retrieval and in-context examples is usually enough.

### Common Workflow Patterns

1. **Prompt Chaining**: Task decomposed into sequence of steps, each LLM call processes output of previous one. Ideal when task can be cleanly decomposed into fixed subtasks.

2. **Routing**: Classifies input and directs to specialized followup task. Works well for distinct categories handled separately.

3. **Parallelization**: LLMs work simultaneously (sectioning into independent subtasks, or voting with multiple perspectives).

4. **Orchestrator-Workers**: Central LLM dynamically breaks down tasks, delegates to worker LLMs, synthesizes results. Key difference from parallelization: subtasks aren't pre-defined but determined by orchestrator.

5. **Evaluator-Optimizer**: One LLM generates response while another provides evaluation and feedback in a loop. Effective when clear evaluation criteria exist.

### Agent Design Principles

1. Maintain **simplicity** in your agent's design
2. Prioritize **transparency** by explicitly showing planning steps
3. Carefully craft your agent-computer interface (ACI) through thorough tool **documentation and testing**

### Tool Design (ACI)

- Give the model enough tokens to "think" before writing itself into a corner
- Keep format close to what model has seen naturally on the internet
- No formatting "overhead" (accurate line counts, string-escaping)
- Put yourself in the model's shoes -- tool definitions should include example usage, edge cases, input format requirements
- Test how the model uses tools with many example inputs
- Poka-yoke tools: change arguments so mistakes are harder (e.g., require absolute filepaths)
