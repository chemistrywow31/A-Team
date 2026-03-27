# Claude 4.6 Best Practices - Complete Anthropic Documentation

> Fetched 2026-03-27 from Anthropic official docs (platform.claude.com).
> Sources:
> - https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
> - https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6
> - https://platform.claude.com/docs/en/about-claude/models/migration-guide
> - https://platform.claude.com/docs/en/build-with-claude/adaptive-thinking
> - https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/overview

---

# PART 1: Prompting Best Practices

Comprehensive guide to prompt engineering techniques for Claude's latest models, covering clarity, examples, XML structuring, thinking, and agentic systems.

This is the single reference for prompt engineering with Claude's latest models, including Claude Opus 4.6, Claude Sonnet 4.6, and Claude Haiku 4.5. It covers foundational techniques, output control, tool use, thinking, and agentic systems. Jump to the section that matches your situation.

> For an overview of model capabilities, see the models overview. For details on what's new in Claude 4.6, see "What's new in Claude 4.6". For migration guidance, see the Migration guide.

## General principles

### Be clear and direct

Claude responds well to clear, explicit instructions. Being specific about your desired output can help enhance results. If you want "above and beyond" behavior, explicitly request it rather than relying on the model to infer this from vague prompts.

Think of Claude as a brilliant but new employee who lacks context on your norms and workflows. The more precisely you explain what you want, the better the result.

**Golden rule:** Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too.

- Be specific about the desired output format and constraints.
- Provide instructions as sequential steps using numbered lists or bullet points when the order or completeness of steps matters.

**Example: Creating an analytics dashboard**

Less effective:
```text
Create an analytics dashboard
```

More effective:
```text
Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.
```

### Add context to improve performance

Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can help Claude better understand your goals and deliver more targeted responses.

**Example: Formatting preferences**

Less effective:
```text
NEVER use ellipses
```

More effective:
```text
Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.
```

Claude is smart enough to generalize from the explanation.

### Use examples effectively

Examples are one of the most reliable ways to steer Claude's output format, tone, and structure. A few well-crafted examples (known as few-shot or multishot prompting) can dramatically improve accuracy and consistency.

When adding examples, make them:
- **Relevant:** Mirror your actual use case closely.
- **Diverse:** Cover edge cases and vary enough that Claude doesn't pick up unintended patterns.
- **Structured:** Wrap examples in `<example>` tags (multiple examples in `<examples>` tags) so Claude can distinguish them from instructions.

> Include 3-5 examples for best results. You can also ask Claude to evaluate your examples for relevance and diversity, or to generate additional ones based on your initial set.

### Structure prompts with XML tags

XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs. Wrapping each type of content in its own tag (e.g. `<instructions>`, `<context>`, `<input>`) reduces misinterpretation.

Best practices:
- Use consistent, descriptive tag names across your prompts.
- Nest tags when content has a natural hierarchy (documents inside `<documents>`, each inside `<document index="n">`).

### Give Claude a role

Setting a role in the system prompt focuses Claude's behavior and tone for your use case. Even a single sentence makes a difference:

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    system="You are a helpful coding assistant specializing in Python.",
    messages=[
        {"role": "user", "content": "How do I sort a list of dictionaries by key?"}
    ],
)
print(message.content)
```

### Long context prompting

When working with large documents or data-rich inputs (20k+ tokens), structure your prompt carefully to get the best results:

- **Put longform data at the top**: Place your long documents and inputs near the top of your prompt, above your query, instructions, and examples. This can significantly improve performance across all models.

  > Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs.

- **Structure document content and metadata with XML tags**: When using multiple documents, wrap each document in `<document>` tags with `<document_content>` and `<source>` (and other metadata) subtags for clarity.

  Example multi-document structure:
  ```xml
  <documents>
    <document index="1">
      <source>annual_report_2023.pdf</source>
      <document_content>
        {{ANNUAL_REPORT}}
      </document_content>
    </document>
    <document index="2">
      <source>competitor_analysis_q2.xlsx</source>
      <document_content>
        {{COMPETITOR_ANALYSIS}}
      </document_content>
    </document>
  </documents>

  Analyze the annual report and competitor analysis. Identify strategic advantages and recommend Q3 focus areas.
  ```

- **Ground responses in quotes**: For long document tasks, ask Claude to quote relevant parts of the documents first before carrying out its task. This helps Claude cut through the noise of the rest of the document's contents.

  Example quote extraction:
  ```xml
  You are an AI physician's assistant. Your task is to help doctors diagnose possible patient illnesses.

  <documents>
    <document index="1">
      <source>patient_symptoms.txt</source>
      <document_content>
        {{PATIENT_SYMPTOMS}}
      </document_content>
    </document>
    <document index="2">
      <source>patient_records.txt</source>
      <document_content>
        {{PATIENT_RECORDS}}
      </document_content>
    </document>
    <document index="3">
      <source>patient01_appt_history.txt</source>
      <document_content>
        {{PATIENT01_APPOINTMENT_HISTORY}}
      </document_content>
    </document>
  </documents>

  Find quotes from the patient records and appointment history that are relevant to diagnosing the patient's reported symptoms. Place these in <quotes> tags. Then, based on these quotes, list all information that would help the doctor diagnose the patient's symptoms. Place your diagnostic information in <info> tags.
  ```

### Model self-knowledge

If you would like Claude to identify itself correctly in your application or use specific API strings:

```text
The assistant is Claude, created by Anthropic. The current model is Claude Opus 4.6.
```

For LLM-powered apps that need to specify model strings:

```text
When an LLM is needed, please default to Claude Opus 4.6 unless the user requests otherwise. The exact model string for Claude Opus 4.6 is claude-opus-4-6.
```

## Output and formatting

### Communication style and verbosity

Claude's latest models have a more concise and natural communication style compared to previous models:

- **More direct and grounded:** Provides fact-based progress reports rather than self-celebratory updates
- **More conversational:** Slightly more fluent and colloquial, less machine-like
- **Less verbose:** May skip detailed summaries for efficiency unless prompted otherwise

This means Claude may skip verbal summaries after tool calls, jumping directly to the next action. If you prefer more visibility into its reasoning:

```text
After completing a task that involves tool use, provide a quick summary of the work you've done.
```

### Control the format of responses

There are a few particularly effective ways to steer output formatting:

1. **Tell Claude what to do instead of what not to do**

   - Instead of: "Do not use markdown in your response"
   - Try: "Your response should be composed of smoothly flowing prose paragraphs."

2. **Use XML format indicators**

   - Try: "Write the prose sections of your response in \<smoothly_flowing_prose_paragraphs\> tags."

3. **Match your prompt style to the desired output**

   The formatting style used in your prompt may influence Claude's response style. If you are still experiencing steerability issues with output formatting, try matching your prompt style to your desired output style as closely as possible. For example, removing markdown from your prompt can reduce the volume of markdown in the output.

4. **Use detailed prompts for specific formatting preferences**

   For more control over markdown and formatting usage, provide explicit guidance:

```text
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form content, write in clear, flowing prose using complete paragraphs and sentences. Use standard paragraph breaks for organization and reserve markdown primarily for `inline code`, code blocks (```...```), and simple headings (###, and ###). Avoid using **bold** and *italics*.

DO NOT use ordered lists (1. ...) or unordered lists (*) unless : a) you're presenting truly discrete items where a list format is the best option, or b) the user explicitly requests a list or ranking

Instead of listing items with bullets or numbers, incorporate them naturally into sentences. This guidance applies especially to technical writing. Using prose instead of excessive formatting will improve user satisfaction. NEVER output a series of overly short bullet points.

Your goal is readable, flowing text that guides the reader naturally through ideas rather than fragmenting information into isolated points.
</avoid_excessive_markdown_and_bullet_points>
```

### LaTeX output

Claude Opus 4.6 defaults to LaTeX for mathematical expressions, equations, and technical explanations. If you prefer plain text, add the following instructions to your prompt:

```text
Format your response in plain text only. Do not use LaTeX, MathJax, or any markup notation such as \( \), $, or \frac{}{}. Write all math expressions using standard text characters (e.g., "/" for division, "*" for multiplication, and "^" for exponents).
```

### Document creation

Claude's latest models excel at creating presentations, animations, and visual documents with impressive creative flair and strong instruction following. The models produce polished, usable output on the first try in most cases.

For best results with document creation:

```text
Create a professional presentation on [topic]. Include thoughtful design elements, visual hierarchy, and engaging animations where appropriate.
```

### Migrating away from prefilled responses

Starting with Claude 4.6 models, prefilled responses on the last assistant turn are no longer supported. Model intelligence and instruction following has advanced such that most use cases of prefill no longer require it. Existing models will continue to support prefills, and adding assistant messages elsewhere in the conversation is not affected.

Here are common prefill scenarios and how to migrate away from them:

**Controlling output formatting:**
Prefills have been used to force specific output formats like JSON/YAML, classification, and similar patterns where the prefill constrains Claude to a particular structure.

Migration: The Structured Outputs feature is designed specifically to constrain Claude's responses to follow a given schema. Try simply asking the model to conform to your output structure first, as newer models can reliably match complex schemas when told to, especially if implemented with retries. For classification tasks, use either tools with an enum field containing your valid labels or structured outputs.

**Eliminating preambles:**
Prefills like `Here is the requested summary:\n` were used to skip introductory text.

Migration: Use direct instructions in the system prompt: "Respond directly without preamble. Do not start with phrases like 'Here is...', 'Based on...', etc." Alternatively, direct the model to output within XML tags, use structured outputs, or use tool calling. If the occasional preamble slips through, strip it in post-processing.

**Avoiding bad refusals:**
Prefills were used to steer around unnecessary refusals.

Migration: Claude is much better at appropriate refusals now. Clear prompting within the `user` message without prefill should be sufficient.

**Continuations:**
Prefills were used to continue partial completions, resume interrupted responses, or pick up where a previous generation left off.

Migration: Move the continuation to the user message, and include the final text from the interrupted response: "Your previous response was interrupted and ended with \`[previous_response]\`. Continue from where you left off." If this is part of error-handling or incomplete-response-handling and there is no UX penalty, retry the request.

**Context hydration and role consistency:**
Prefills were used to periodically ensure refreshed or injected context.

Migration: For very long conversations, inject what were previously prefilled-assistant reminders into the user turn. If context hydration is part of a more complex agentic system, consider hydrating via tools (expose or encourage use of tools containing context based on heuristics such as number of turns) or during context compaction.

## Tool use

### Tool usage

Claude's latest models are trained for precise instruction following and benefit from explicit direction to use specific tools. If you say "can you suggest some changes," Claude will sometimes provide suggestions rather than implementing them, even if making changes might be what you intended.

For Claude to take action, be more explicit:

**Example: Explicit instructions**

Less effective (Claude will only suggest):
```text
Can you suggest some changes to improve this function?
```

More effective (Claude will make the changes):
```text
Change this function to improve its performance.
```

Or:
```text
Make these edits to the authentication flow.
```

To make Claude more proactive about taking action by default, you can add this to your system prompt:

```text
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is unclear, infer the most useful likely action and proceed, using tools to discover any missing details instead of guessing. Try to infer the user's intent about whether a tool call (e.g., file edit or read) is intended or not, and act accordingly.
</default_to_action>
```

On the other hand, if you want the model to be more hesitant by default, less prone to jumping straight into implementations, and only take action if requested, you can steer this behavior with a prompt like the below:

```text
<do_not_act_before_instructions>
Do not jump into implementatation or changes files unless clearly instructed to make changes. When the user's intent is ambiguous, default to providing information, doing research, and providing recommendations rather than taking action. Only proceed with edits, modifications, or implementations when the user explicitly requests them.
</do_not_act_before_instructions>
```

Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt than previous models. If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said "CRITICAL: You MUST use this tool when...", you can use more normal prompting like "Use this tool when...".

### Optimize parallel tool calling

Claude's latest models excel at parallel tool execution. These models will:

- Run multiple speculative searches during research
- Read several files at once to build context faster
- Execute bash commands in parallel (which can even bottleneck system performance)

This behavior is easily steerable. While the model has a high success rate in parallel tool calling without prompting, you can boost this to ~100% or adjust the aggression level:

```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>
```

To reduce parallel execution:
```text
Execute operations sequentially with brief pauses between each step to ensure stability.
```

## Thinking and reasoning

### Overthinking and excessive thoroughness

Claude Opus 4.6 does significantly more upfront exploration than previous models, especially at higher `effort` settings. This initial work often helps to optimize the final results, but the model may gather extensive context or pursue multiple threads of research without being prompted. If your prompts previously encouraged the model to be more thorough, you should tune that guidance for Claude Opus 4.6:

- **Replace blanket defaults with more targeted instructions.** Instead of "Default to using \[tool\]," add guidance like "Use \[tool\] when it would enhance your understanding of the problem."
- **Remove over-prompting.** Tools that undertriggered in previous models are likely to trigger appropriately now. Instructions like "If in doubt, use \[tool\]" will cause overtriggering.
- **Use effort as a fallback.** If Claude continues to be overly aggressive, use a lower setting for `effort`.

In some cases, Claude Opus 4.6 may think extensively, which can inflate thinking tokens and slow down responses. If this behavior is undesirable, you can add explicit instructions to constrain its reasoning, or you can lower the `effort` setting to reduce overall thinking and token usage.

```text
When you're deciding how to approach a problem, choose an approach and commit to it. Avoid revisiting decisions unless you encounter new information that directly contradicts your reasoning. If you're weighing two approaches, pick one and see it through. You can always course-correct later if the chosen approach fails.
```

If you need a hard ceiling on thinking costs, extended thinking with a `budget_tokens` cap is still functional on Opus 4.6 and Sonnet 4.6 but is deprecated. Prefer lowering the effort setting or using `max_tokens` as a hard limit with adaptive thinking.

### Leverage thinking & interleaved thinking capabilities

Claude's latest models offer thinking capabilities that can be especially helpful for tasks involving reflection after tool use or complex multi-step reasoning. You can guide its initial or interleaved thinking for better results.

Claude Opus 4.6 and Claude Sonnet 4.6 use adaptive thinking (`thinking: {type: "adaptive"}`), where Claude dynamically decides when and how much to think. Claude calibrates its thinking based on two factors: the `effort` parameter and query complexity. Higher effort elicits more thinking, and more complex queries do the same. On easier queries that don't require thinking, the model responds directly. In internal evaluations, adaptive thinking reliably drives better performance than extended thinking. Consider moving to adaptive thinking to get the most intelligent responses.

Use adaptive thinking for workloads that require agentic behavior such as multi-step tool use, complex coding tasks, and long-horizon agent loops. Older models use manual thinking mode with `budget_tokens`.

You can guide Claude's thinking behavior:

```text
After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
```

The triggering behavior for adaptive thinking is promptable. If you find the model thinking more often than you'd like, which can happen with large or complex system prompts, add guidance to steer it:

```text
Extended thinking adds latency and should only be used when it will meaningfully improve answer quality - typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

If you are migrating from extended thinking with `budget_tokens`, replace your thinking configuration and move budget control to `effort`:

```python
# Before (extended thinking, older models)
client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=64000,
    thinking={"type": "enabled", "budget_tokens": 32000},
    messages=[{"role": "user", "content": "..."}],
)

# After (adaptive thinking)
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # or max, medium, low
    messages=[{"role": "user", "content": "..."}],
)
```

If you are not using extended thinking, no changes are required. Thinking is off by default when you omit the `thinking` parameter.

- **Prefer general instructions over prescriptive steps.** A prompt like "think thoroughly" often produces better reasoning than a hand-written step-by-step plan. Claude's reasoning frequently exceeds what a human would prescribe.
- **Multishot examples work with thinking.** Use `<thinking>` tags inside your few-shot examples to show Claude the reasoning pattern. It will generalize that style to its own extended thinking blocks.
- **Manual CoT as a fallback.** When thinking is off, you can still encourage step-by-step reasoning by asking Claude to think through the problem. Use structured tags like `<thinking>` and `<answer>` to cleanly separate reasoning from the final output.
- **Ask Claude to self-check.** Append something like "Before you finish, verify your answer against [test criteria]." This catches errors reliably, especially for coding and math.

> Note: When extended thinking is disabled, Claude Opus 4.5 is particularly sensitive to the word "think" and its variants. Consider using alternatives like "consider," "evaluate," or "reason through" in those cases.

## Agentic systems

### Long-horizon reasoning and state tracking

Claude's latest models excel at long-horizon reasoning tasks with exceptional state tracking capabilities. Claude maintains orientation across extended sessions by focusing on incremental progress, making steady advances on a few things at a time rather than attempting everything at once. This capability especially emerges over multiple context windows or task iterations, where Claude can work on a complex task, save the state, and continue with a fresh context window.

#### Context awareness and multi-window workflows

Claude 4.6 and Claude 4.5 models feature context awareness, enabling the model to track its remaining context window (i.e. "token budget") throughout a conversation. This enables Claude to execute tasks and manage context more effectively by understanding how much space it has to work.

**Managing context limits:**

If you are using Claude in an agent harness that compacts context or allows saving context to external files (like in Claude Code), consider adding this information to your prompt so Claude can behave accordingly. Otherwise, Claude may sometimes naturally try to wrap up work as it approaches the context limit. Below is an example prompt:

```text
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to memory before the context window refreshes. Always be as persistent and autonomous as possible and complete tasks fully, even if the end of your budget is approaching. Never artificially stop any task early regardless of the context remaining.
```

The memory tool pairs naturally with context awareness for seamless context transitions.

#### Multi-context window workflows

For tasks spanning multiple context windows:

1. **Use a different prompt for the very first context window**: Use the first context window to set up a framework (write tests, create setup scripts), then use future context windows to iterate on a todo-list.

2. **Have the model write tests in a structured format**: Ask Claude to create tests before starting work and keep track of them in a structured format (e.g., `tests.json`). This leads to better long-term ability to iterate. Remind Claude of the importance of tests: "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

3. **Set up quality of life tools**: Encourage Claude to create setup scripts (e.g., `init.sh`) to gracefully start servers, run test suites, and linters. This prevents repeated work when continuing from a fresh context window.

4. **Starting fresh vs compacting**: When a context window is cleared, consider starting with a brand new context window rather than using compaction. Claude's latest models are extremely effective at discovering state from the local filesystem. In some cases, you may want to take advantage of this over compaction. Be prescriptive about how it should start:
   - "Call pwd; you can only read and write files in this directory."
   - "Review progress.txt, tests.json, and the git logs."
   - "Manually run through a fundamental integration test before moving on to implementing new features."

5. **Provide verification tools**: As the length of autonomous tasks grows, Claude needs to verify correctness without continuous human feedback. Tools like Playwright MCP server or computer use capabilities for testing UIs are helpful.

6. **Encourage complete usage of context**: Prompt Claude to efficiently complete components before moving on:

```text
This is a very long task, so it may be beneficial to plan out your work clearly. It's encouraged to spend your entire output context working on the task - just make sure you don't run out of context with significant uncommitted work. Continue working systematically until you have completed this task.
```

#### State management best practices

- **Use structured formats for state data**: When tracking structured information (like test results or task status), use JSON or other structured formats to help Claude understand schema requirements
- **Use unstructured text for progress notes**: Freeform progress notes work well for tracking general progress and context
- **Use git for state tracking**: Git provides a log of what's been done and checkpoints that can be restored. Claude's latest models perform especially well in using git to track state across multiple sessions.
- **Emphasize incremental progress**: Explicitly ask Claude to keep track of its progress and focus on incremental work

Example: State tracking:

```json
// Structured state file (tests.json)
{
  "tests": [
    { "id": 1, "name": "authentication_flow", "status": "passing" },
    { "id": 2, "name": "user_management", "status": "failing" },
    { "id": 3, "name": "api_endpoints", "status": "not_started" }
  ],
  "total": 200,
  "passing": 150,
  "failing": 25,
  "not_started": 25
}
```

```text
// Progress notes (progress.txt)
Session 3 progress:
- Fixed authentication token validation
- Updated user model to handle edge cases
- Next: investigate user_management test failures (test #2)
- Note: Do not remove tests as this could lead to missing functionality
```

### Balancing autonomy and safety

Without guidance, Claude Opus 4.6 may take actions that are difficult to reverse or affect shared systems, such as deleting files, force-pushing, or posting to external services. If you want Claude Opus 4.6 to confirm before taking potentially risky actions, add guidance to your prompt:

```text
Consider the reversibility and potential impact of your actions. You are encouraged to take local, reversible actions like editing files or running tests, but for actions that are hard to reverse, affect shared systems, or could be destructive, ask the user before proceeding.

Examples of actions that warrant confirmation:
- Destructive operations: deleting files or branches, dropping database tables, rm -rf
- Hard to reverse operations: git push --force, git reset --hard, amending published commits
- Operations visible to others: pushing code, commenting on PRs/issues, sending messages, modifying shared infrastructure

When encountering obstacles, do not use destructive actions as a shortcut. For example, don't bypass safety checks (e.g. --no-verify) or discard unfamiliar files that may be in-progress work.
```

### Research and information gathering

Claude's latest models demonstrate exceptional agentic search capabilities and can find and synthesize information from multiple sources effectively. For optimal research results:

1. **Provide clear success criteria**: Define what constitutes a successful answer to your research question

2. **Encourage source verification**: Ask Claude to verify information across multiple sources

3. **For complex research tasks, use a structured approach**:

```text
Search for this information in a structured way. As you gather data, develop several competing hypotheses. Track your confidence levels in your progress notes to improve calibration. Regularly self-critique your approach and plan. Update a hypothesis tree or research notes file to persist information and provide transparency. Break down this complex research task systematically.
```

This structured approach allows Claude to find and synthesize virtually any piece of information and iteratively critique its findings, no matter the size of the corpus.

### Subagent orchestration

Claude's latest models demonstrate significantly improved native subagent orchestration capabilities. These models can recognize when tasks would benefit from delegating work to specialized subagents and do so proactively without requiring explicit instruction.

To take advantage of this behavior:

1. **Ensure well-defined subagent tools**: Have subagent tools available and described in tool definitions
2. **Let Claude orchestrate naturally**: Claude will delegate appropriately without explicit instruction
3. **Watch for overuse**: Claude Opus 4.6 has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice. For example, the model may spawn subagents for code exploration when a direct grep call is faster and sufficient.

If you're seeing excessive subagent use, add explicit guidance about when subagents are and aren't warranted:

```text
Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that don't need to share state. For simple tasks, sequential operations, single-file edits, or tasks where you need to maintain context across steps, work directly rather than delegating.
```

### Chain complex prompts

With adaptive thinking and subagent orchestration, Claude handles most multi-step reasoning internally. Explicit prompt chaining (breaking a task into sequential API calls) is still useful when you need to inspect intermediate outputs or enforce a specific pipeline structure.

The most common chaining pattern is **self-correction**: generate a draft -> have Claude review it against criteria -> have Claude refine based on the review. Each step is a separate API call so you can log, evaluate, or branch at any point.

### Reduce file creation in agentic coding

Claude's latest models may sometimes create new files for testing and iteration purposes, particularly when working with code. This approach allows Claude to use files, especially python scripts, as a 'temporary scratchpad' before saving its final output. Using temporary files can improve outcomes particularly for agentic coding use cases.

If you'd prefer to minimize net new file creation, you can instruct Claude to clean up after itself:

```text
If you create any temporary new files, scripts, or helper files for iteration, clean up these files by removing them at the end of the task.
```

### Overeagerness

Claude Opus 4.5 and Claude Opus 4.6 have a tendency to overengineer by creating extra files, adding unnecessary abstractions, or building in flexibility that wasn't requested. If you're seeing this undesired behavior, add specific guidance to keep solutions minimal.

For example:

```text
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused:

- Scope: Don't add features, refactor code, or make "improvements" beyond what was asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need extra configurability.

- Documentation: Don't add docstrings, comments, or type annotations to code you didn't change. Only add comments where the logic isn't self-evident.

- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).

- Abstractions: Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. The right amount of complexity is the minimum needed for the current task.
```

### Avoid focusing on passing tests and hard-coding

Claude can sometimes focus too heavily on making tests pass at the expense of more general solutions, or may use workarounds like helper scripts for complex refactoring instead of using standard tools directly. To prevent this behavior and ensure robust, generalizable solutions:

```text
Please write a high-quality, general-purpose solution using the standard tools available. Do not create helper scripts or workarounds to accomplish the task more efficiently. Implement a solution that works correctly for all valid inputs, not just the test cases. Do not hard-code values or create solutions that only work for specific test inputs. Instead, implement the actual logic that solves the problem generally.

Focus on understanding the problem requirements and implementing the correct algorithm. Tests are there to verify correctness, not to define the solution. Provide a principled implementation that follows best practices and software design principles.

If the task is unreasonable or infeasible, or if any of the tests are incorrect, please inform me rather than working around them. The solution should be robust, maintainable, and extendable.
```

### Minimizing hallucinations in agentic coding

Claude's latest models are less prone to hallucinations and give more accurate, grounded, intelligent answers based on the code. To encourage this behavior even more and minimize hallucinations:

```text
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating unless you are certain of the correct answer - give grounded and hallucination-free answers.
</investigate_before_answering>
```

## Capability-specific tips

### Improved vision capabilities

Claude Opus 4.5 and Claude Opus 4.6 have improved vision capabilities compared to previous Claude models. They perform better on image processing and data extraction tasks, particularly when there are multiple images present in context. These improvements carry over to computer use, where the models can more reliably interpret screenshots and UI elements. You can also use these models to analyze videos by breaking them up into frames.

One technique that has proven effective to further boost performance is to give Claude a crop tool or skill. Testing has shown consistent uplift on image evaluations when Claude is able to "zoom" in on relevant regions of an image.

### Frontend design

Claude Opus 4.5 and Claude Opus 4.6 excel at building complex, real-world web applications with strong frontend design. However, without guidance, models can default to generic patterns that create what users call the "AI slop" aesthetic. To create distinctive, creative frontends that surprise and delight:

Here's a system prompt snippet you can use to encourage better frontend design:

```text
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliche color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

## Migration considerations

When migrating to Claude 4.6 models from earlier generations:

1. **Be specific about desired behavior**: Consider describing exactly what you'd like to see in the output.

2. **Frame your instructions with modifiers**: Adding modifiers that encourage Claude to increase the quality and detail of its output can help better shape Claude's performance. For example, instead of "Create an analytics dashboard", use "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation."

3. **Request specific features explicitly**: Animations and interactive elements should be requested explicitly when desired.

4. **Update thinking configuration**: Claude 4.6 models use adaptive thinking (`thinking: {type: "adaptive"}`) instead of manual thinking with `budget_tokens`. Use the effort parameter to control thinking depth.

5. **Migrate away from prefilled responses**: Prefilled responses on the last assistant turn are deprecated starting with Claude 4.6 models. See "Migrating away from prefilled responses" above for detailed guidance on alternatives.

6. **Tune anti-laziness prompting**: If your prompts previously encouraged the model to be more thorough or use tools more aggressively, dial back that guidance. Claude 4.6 models are significantly more proactive and may overtrigger on instructions that were needed for previous models.

### Migrating from Claude Sonnet 4.5 to Claude Sonnet 4.6

Claude Sonnet 4.6 defaults to an effort level of `high`, in contrast to Claude Sonnet 4.5 which had no effort parameter. Consider adjusting the effort parameter as you migrate from Claude Sonnet 4.5 to Claude Sonnet 4.6. If not explicitly set, you may experience higher latency with the default effort level.

**Recommended effort settings:**
- **Medium** for most applications
- **Low** for high-volume or latency-sensitive workloads
- Set a large max output token budget (64k tokens recommended) at medium or high effort to give the model room to think and act

**When to use Opus 4.6 instead:** For the hardest, longest-horizon problems (large-scale code migrations, deep research, extended autonomous work), Opus 4.6 remains the right choice. Sonnet 4.6 is optimized for workloads where fast turnaround and cost efficiency matter most.

#### If you're not using extended thinking

If you're not using extended thinking on Claude Sonnet 4.5, you can continue without it on Claude Sonnet 4.6. You should explicitly set effort to the level appropriate for your use case. At `low` effort with thinking disabled, you can expect similar or better performance relative to Claude Sonnet 4.5 with no extended thinking.

```python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    thinking={"type": "disabled"},
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "..."}],
)
```

#### If you're using extended thinking

If you're using extended thinking with `budget_tokens` on Claude Sonnet 4.5, it is still functional on Claude Sonnet 4.6 but is deprecated. Migrate to adaptive thinking with the effort parameter.

##### Migrating to adaptive thinking

Adaptive thinking is particularly well suited to the following workload patterns:

- **Autonomous multi-step agents:** coding agents that turn requirements into working software, data analysis pipelines, and bug finding where the model runs independently across many steps. Adaptive thinking lets the model calibrate its reasoning per step, staying on path over longer trajectories. For these workloads, start at `high` effort. If latency or token usage is a concern, scale down to `medium`.
- **Computer use agents:** Claude Sonnet 4.6 achieved best-in-class accuracy on computer use evaluations using adaptive mode.
- **Bimodal workloads:** a mix of easy and hard tasks where adaptive skips thinking on simple queries and reasons deeply on complex ones.

When using adaptive thinking, evaluate `medium` and `high` effort on your tasks. The right level depends on your workload's tradeoff between quality, latency, and token usage.

```python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": "..."}],
)
```

##### Keeping budget_tokens during migration

If you need to keep `budget_tokens` temporarily while migrating, a budget around 16k tokens provides headroom for harder problems without risk of runaway token usage. This configuration is deprecated and will be removed in a future model release.

**For coding use cases** (agentic coding, tool-heavy workflows, code generation), start with `medium` effort:

```python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16384,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "..."}],
)
```

**For chat and non-coding use cases** (chat, content generation, search, classification), start with `low` effort:

```python
client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    thinking={"type": "enabled", "budget_tokens": 16384},
    output_config={"effort": "low"},
    messages=[{"role": "user", "content": "..."}],
)
```

---

# PART 2: What's New in Claude 4.6

Overview of new features and capabilities in Claude Opus 4.6 and Sonnet 4.6.

Claude 4.6 represents the next generation of Claude models, bringing significant new capabilities and API improvements. This page summarizes all new features available at launch.

## New models

| Model | API model ID | Description |
|:------|:-------------|:------------|
| Claude Opus 4.6 | `claude-opus-4-6` | The most intelligent model for building agents and coding |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | The best combination of speed and intelligence |

Claude Opus 4.6 and Sonnet 4.6 both support a 1M token context window, extended thinking, and all existing Claude API features. Opus 4.6 offers 128k max output tokens; Sonnet 4.6 offers 64k max output tokens.

## New features

### Adaptive thinking mode

Adaptive thinking (`thinking: {type: "adaptive"}`) is the recommended thinking mode for Opus 4.6 and Sonnet 4.6. Claude dynamically decides when and how much to think. At the default effort level (`high`), Claude almost always thinks. At lower effort levels, it may skip thinking for simpler problems.

`thinking: {type: "enabled"}` and `budget_tokens` are **deprecated** on Opus 4.6 and Sonnet 4.6. They remain functional but will be removed in a future model release. Use adaptive thinking and the effort parameter to control thinking depth instead. Adaptive thinking also automatically enables interleaved thinking.

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[{"role": "user", "content": "Solve this complex problem..."}],
)
```

### Effort parameter GA

The effort parameter is now generally available (no beta header required). A new `max` effort level provides the absolute highest capability on Opus 4.6. Combine effort with adaptive thinking for optimal cost-quality tradeoffs.

Sonnet 4.6 introduces the effort parameter to the Sonnet family. Consider setting effort to `medium` for most Sonnet 4.6 use cases to balance speed, cost, and performance.

### Code execution is now free with web tools

Code execution is now free when used with web search or web fetch. When either tool is included in your API request, there are no additional charges for code execution beyond standard input and output token costs.

### Improved web search and web fetch with dynamic filtering

Web search and web fetch tools now support dynamic filtering with Opus 4.6 and Sonnet 4.6. Claude can write and execute code to filter results before they reach the context window, keeping only relevant information and improving accuracy while reducing token consumption. To enable dynamic filtering, use the `web_search_20260209` or `web_fetch_20260209` tool versions.

### Tools graduating to general availability

The following tools are now generally available:
- Code execution (free with web tools)
- Web fetch
- Programmatic tool calling
- Tool search tool
- Tool use examples
- Memory tool

### Compaction API (beta)

Compaction provides automatic, server-side context summarization, enabling effectively infinite conversations. When context approaches the window limit, the API automatically summarizes earlier parts of the conversation.

### Fast mode (beta: research preview)

Fast mode (`speed: "fast"`) delivers significantly faster output token generation for Opus models. Fast mode is up to 2.5x as fast at premium pricing ($30/$150 per MTok). This is the same model running with faster inference (no change to intelligence or capabilities).

```python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    speed="fast",
    betas=["fast-mode-2026-02-01"],
    messages=[{"role": "user", "content": "Refactor this module..."}],
)
```

### Fine-grained tool streaming (GA)

Fine-grained tool streaming is now generally available on all models and platforms. No beta header is required.

### 128k output tokens

Opus 4.6 supports up to 128k output tokens, doubling the previous 64k limit. This enables longer thinking budgets and more comprehensive responses.

### Data residency controls

Data residency controls allow you to specify where model inference runs using the `inference_geo` parameter. You can choose `"global"` (default) or `"us"` routing per request. US-only inference is priced at 1.1x on Claude Opus 4.6 and newer models.

## Deprecations

### `type: "enabled"` and `budget_tokens`

`thinking: {type: "enabled", budget_tokens: N}` is **deprecated** on Opus 4.6 and Sonnet 4.6. It is still functional but no longer recommended and will be removed in a future model release. Migrate to `thinking: {type: "adaptive"}` with the effort parameter.

### `interleaved-thinking-2025-05-14` beta header

The `interleaved-thinking-2025-05-14` beta header is **deprecated** on Opus 4.6. It is safely ignored if included, but is no longer required. Adaptive thinking automatically enables interleaved thinking. Remove `betas=["interleaved-thinking-2025-05-14"]` from your requests when using Opus 4.6.

On **Sonnet 4.6**, the `interleaved-thinking-2025-05-14` beta header is still functional for use with manual extended thinking (`thinking: {type: "enabled"}`), but manual mode is deprecated. Adaptive thinking is the recommended path and automatically enables interleaved thinking.

### `output_format`

The `output_format` parameter for structured outputs has been moved to `output_config.format`. The old parameter remains functional but is deprecated and will be removed in a future model release.

```python
# Before
response = client.messages.create(
    output_format={"type": "json_schema", "schema": {...}},
    # ...
)

# After
response = client.messages.create(
    output_config={"format": {"type": "json_schema", "schema": {...}}},
    # ...
)
```

## Breaking changes

### Prefill removal

Prefilling assistant messages (last-assistant-turn prefills) is **not supported** on Opus 4.6. Requests with prefilled assistant messages return a 400 error.

**Alternatives:**
- Structured outputs for controlling response format
- System prompt instructions for guiding response style
- `output_config.format` for JSON output

### Tool parameter quoting

Opus 4.6 may produce slightly different JSON string escaping in tool call arguments (e.g., different handling of Unicode escapes or forward slash escaping). Standard JSON parsers handle these differences automatically. If you parse tool call `input` as a raw string rather than using `json.loads()` or `JSON.parse()`, verify your parsing logic still works.

---

# PART 3: Migration Guide

Guide for migrating to Claude 4.6 models from previous Claude versions.

## Migrating to Claude 4.6

Claude Opus 4.6 is a near drop-in replacement for Claude 4.5, with a few breaking changes to be aware of.

### Update your model name

```python
# Opus migration
model = "claude-opus-4-5"  # Before
model = "claude-opus-4-6"  # After
```

### Breaking changes

1. **Prefill removal:** Prefilling assistant messages returns a 400 error on Claude 4.6 models. Use structured outputs, system prompt instructions, or `output_config.format` instead.

2. **Tool parameter quoting:** Claude 4.6 models may produce slightly different JSON string escaping in tool call arguments (e.g., different handling of Unicode escapes or forward slash escaping). If you parse tool call `input` as a raw string rather than using a JSON parser, verify your parsing logic. Standard JSON parsers (like `json.loads()` or `JSON.parse()`) handle these differences automatically.

### Recommended changes

These are not required but will improve your experience:

1. **Migrate to adaptive thinking:** `thinking: {type: "enabled", budget_tokens: N}` is deprecated on Claude 4.6 models and will be removed in a future model release. Switch to `thinking: {type: "adaptive"}` and use the effort parameter to control thinking depth.

   ```python
   # Before
   response = client.beta.messages.create(
       model="claude-opus-4-5",
       max_tokens=16000,
       thinking={"type": "enabled", "budget_tokens": 32000},
       betas=["interleaved-thinking-2025-05-14"],
       messages=[...],
   )

   # After
   response = client.messages.create(
       model="claude-opus-4-6",
       max_tokens=16000,
       thinking={"type": "adaptive"},
       output_config={"effort": "high"},
       messages=[{"role": "user", "content": "Your prompt here"}],
   )
   ```

   Note that the migration also moves from `client.beta.messages.create` to `client.messages.create`. Adaptive thinking and effort are GA features and do not require the beta SDK namespace or any beta headers.

2. **Remove effort beta header:** The effort parameter is now GA. Remove `betas=["effort-2025-11-24"]` from your requests.

3. **Remove fine-grained tool streaming beta header:** Fine-grained tool streaming is now GA. Remove `betas=["fine-grained-tool-streaming-2025-05-14"]` from your requests.

4. **Remove interleaved thinking beta header:** Adaptive thinking automatically enables interleaved thinking on both Opus 4.6 and Sonnet 4.6. Remove `betas=["interleaved-thinking-2025-05-14"]` from your requests.

5. **Migrate to output_config.format:** If using structured outputs, update `output_format={...}` to `output_config={"format": {...}}`. The old parameter remains functional but is deprecated.

### Migrating from Claude 4.1 or earlier to Claude 4.6

If you're migrating from Opus 4.1, Sonnet 4, or earlier models directly to Claude 4.6, apply the Claude 4.6 breaking changes above plus these additional changes:

#### Additional breaking changes

1. **Update sampling parameters**: Use only `temperature` OR `top_p`, not both (breaking change from Claude 3.x models).

2. **Update tool versions**: Update to the latest tool versions. Remove any code using the `undo_edit` command.
   - **Text editor:** Use `text_editor_20250728` and `str_replace_based_edit_tool`
   - **Code execution:** Upgrade to `code_execution_20250825`

3. **Handle the `refusal` stop reason**: Update your application to handle `refusal` stop reasons.

4. **Handle the `model_context_window_exceeded` stop reason**: Claude 4.5+ models return a `model_context_window_exceeded` stop reason when generation stops due to hitting the context window limit.

5. **Verify tool parameter handling (trailing newlines)**: Claude 4.5+ models preserve trailing newlines in tool call string parameters that were previously stripped.

6. **Update your prompts for behavioral changes**: Claude 4+ models have a more concise, direct communication style and require explicit direction.

#### Additional recommended changes

- **Remove legacy beta headers:** Remove `token-efficient-tools-2025-02-19` and `output-128k-2025-02-19`. All Claude 4+ models have built-in token-efficient tool use and these headers have no effect.

### Claude 4.6 migration checklist

- [ ] Update model ID to `claude-opus-4-6`
- [ ] **BREAKING:** Remove assistant message prefills (returns 400 error); use structured outputs or `output_config.format` instead
- [ ] **Recommended:** Migrate from `thinking: {type: "enabled", budget_tokens: N}` to `thinking: {type: "adaptive"}` with the effort parameter (`budget_tokens` is deprecated)
- [ ] Verify tool call JSON parsing uses a standard JSON parser
- [ ] Remove `effort-2025-11-24` beta header (effort is now GA)
- [ ] Remove `fine-grained-tool-streaming-2025-05-14` beta header
- [ ] Remove `interleaved-thinking-2025-05-14` beta header (adaptive thinking enables interleaved thinking automatically)
- [ ] Migrate `output_format` to `output_config.format` (if applicable)
- [ ] If migrating from Claude 4.1 or earlier: update sampling parameters to use only `temperature` OR `top_p`
- [ ] If migrating from Claude 4.1 or earlier: update tool versions (`text_editor_20250728`, `code_execution_20250825`)
- [ ] If migrating from Claude 4.1 or earlier: handle `refusal` stop reason
- [ ] If migrating from Claude 4.1 or earlier: handle `model_context_window_exceeded` stop reason
- [ ] If migrating from Claude 4.1 or earlier: verify tool string parameter handling for trailing newlines
- [ ] If migrating from Claude 4.1 or earlier: remove legacy beta headers (`token-efficient-tools-2025-02-19`, `output-128k-2025-02-19`)
- [ ] Review and update prompts following prompting best practices
- [ ] Test in development environment before production deployment

---

# PART 4: Adaptive Thinking

Let Claude dynamically determine when and how much to use extended thinking with adaptive thinking mode.

Adaptive thinking is the recommended way to use extended thinking with Claude Opus 4.6 and Sonnet 4.6. Instead of manually setting a thinking token budget, adaptive thinking lets Claude dynamically determine when and how much to use extended thinking based on the complexity of each request.

> Adaptive thinking can drive better performance than extended thinking with a fixed `budget_tokens` for many workloads, especially bimodal tasks and long-horizon agentic workflows. No beta header is required.

## Supported models

Adaptive thinking is supported on:
- Claude Opus 4.6 (`claude-opus-4-6`)
- Claude Sonnet 4.6 (`claude-sonnet-4-6`)

> WARNING: `thinking.type: "enabled"` and `budget_tokens` are deprecated on Opus 4.6 and Sonnet 4.6 and will be removed in a future model release. Use `thinking.type: "adaptive"` with the `effort` parameter instead. Older models (Sonnet 4.5, Opus 4.5, etc.) do not support adaptive thinking and require `thinking.type: "enabled"` with `budget_tokens`.

## How adaptive thinking works

In adaptive mode, thinking is optional for the model. Claude evaluates the complexity of each request and determines whether and how much to use extended thinking. At the default effort level (`high`), Claude almost always thinks. At lower effort levels, Claude may skip thinking for simpler problems.

Adaptive thinking also automatically enables interleaved thinking. This means Claude can think between tool calls, making it especially effective for agentic workflows.

## How to use adaptive thinking

Set `thinking.type` to `"adaptive"` in your API request:

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[
        {
            "role": "user",
            "content": "Explain why the sum of two even numbers is always even.",
        }
    ],
)

for block in response.content:
    if block.type == "thinking":
        print(f"\nThinking: {block.thinking}")
    elif block.type == "text":
        print(f"\nResponse: {block.text}")
```

## Adaptive thinking with the effort parameter

You can combine adaptive thinking with the effort parameter to guide how much thinking Claude does. The effort level acts as soft guidance for Claude's thinking allocation:

| Effort level | Thinking behavior |
|:-------------|:------------------|
| `max` | Claude always thinks with no constraints on thinking depth. Opus 4.6 only. Requests using `max` on other models return an error. |
| `high` (default) | Claude always thinks. Provides deep reasoning on complex tasks. |
| `medium` | Claude uses moderate thinking. May skip thinking for very simple queries. |
| `low` | Claude minimizes thinking. Skips thinking for simple tasks where speed matters most. |

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)
```

## Adaptive vs manual vs disabled thinking

| Mode | Config | Availability | When to use |
|:-----|:-------|:-------------|:------------|
| **Adaptive** | `thinking: {type: "adaptive"}` | Opus 4.6, Sonnet 4.6 | Claude determines when and how much to use extended thinking. Use `effort` to guide. |
| **Manual** | `thinking: {type: "enabled", budget_tokens: N}` | All models. Deprecated on Opus 4.6 and Sonnet 4.6. | When you need precise control over thinking token spend. |
| **Disabled** | Omit `thinking` parameter or pass `{type: "disabled"}` | All models | When you don't need extended thinking and want the lowest latency. |

**Interleaved thinking availability by mode:**
- **Adaptive mode:** Interleaved thinking is automatically enabled on both Opus 4.6 and Sonnet 4.6.
- **Manual mode on Sonnet 4.6:** Interleaved thinking works via the `interleaved-thinking-2025-05-14` beta header.
- **Manual mode on Opus 4.6:** Interleaved thinking is not available. If your agentic workflow requires thinking between tool calls on Opus 4.6, use adaptive mode.

## Important considerations

### Validation changes

When using adaptive thinking, previous assistant turns don't need to start with thinking blocks. This is more flexible than manual mode, where the API enforces that thinking-enabled turns begin with a thinking block.

### Prompt caching

Consecutive requests using `adaptive` thinking preserve prompt cache breakpoints. However, switching between `adaptive` and `enabled`/`disabled` thinking modes breaks cache breakpoints for messages. System prompts and tool definitions remain cached regardless of mode changes.

### Tuning thinking behavior

Adaptive thinking's triggering behavior is promptable. If Claude is thinking more or less often than you'd like, you can add guidance to your system prompt:

```text
Extended thinking adds latency and should only be used when it
will meaningfully improve answer quality -- typically for problems
that require multi-step reasoning. When in doubt, respond directly.
```

> WARNING: Steering Claude to think less often may reduce quality on tasks that benefit from reasoning. Measure the impact on your specific workloads before deploying prompt-based tuning to production. Consider testing with lower effort levels first.

### Cost control

Use `max_tokens` as a hard limit on total output (thinking + response text). The `effort` parameter provides additional soft guidance on how much thinking Claude allocates. Together, these give you effective control over cost.

At `high` and `max` effort levels, Claude may think more extensively and can be more likely to exhaust the `max_tokens` budget. If you observe `stop_reason: "max_tokens"` in responses, consider increasing `max_tokens` to give the model more room, or lowering the effort level.

## Summarized thinking

With extended thinking enabled, the Messages API for Claude 4 models returns a summary of Claude's full thinking process. Summarized thinking provides the full intelligence benefits of extended thinking, while preventing misuse. This is the default behavior when the `display` field on the thinking configuration is unset or set to `"summarized"`.

Important considerations for summarized thinking:
- You're charged for the full thinking tokens generated by the original request, not the summary tokens.
- The billed output token count will **not match** the count of tokens you see in the response.
- The first few lines of thinking output are more verbose, providing detailed reasoning that's particularly helpful for prompt engineering purposes.
- As Anthropic seeks to improve the extended thinking feature, summarization behavior is subject to change.
- Summarization preserves the key ideas of Claude's thinking process with minimal added latency, enabling a streamable user experience.
- Summarization is processed by a different model than the one you target in your requests. The thinking model does not see the summarized output.

### Controlling thinking display

The `display` field on the thinking configuration controls how thinking content is returned in API responses:

- `"summarized"` (default): Thinking blocks contain summarized thinking text.
- `"omitted"`: Thinking blocks are returned with an empty `thinking` field. The `signature` field still carries the encrypted full thinking for multi-turn continuity.

Setting `display: "omitted"` is useful when your application doesn't surface thinking content to users. The primary benefit is **faster time-to-first-text-token when streaming.**

```python
thinking = {"type": "adaptive", "display": "omitted"}
```

Important considerations for omitted thinking:
- You're still charged for the full thinking tokens. Omitting reduces latency, not cost.
- If you pass thinking blocks back in multi-turn conversations, pass them unchanged.
- `display` is invalid with `thinking.type: "disabled"`.
- When using `thinking.type: "adaptive"` and the model skips thinking for a simple request, no thinking block is produced regardless of `display`.

### Thinking encryption

Full thinking content is encrypted and returned in the `signature` field. This field is used to verify that thinking blocks were generated by Claude when passed back to the API.

- It is only strictly necessary to send back thinking blocks when using tools with extended thinking. Otherwise you can omit thinking blocks from previous turns.
- `signature` values are significantly longer in Claude 4 models than in previous models.
- `signature` values are compatible across platforms (Claude APIs, Amazon Bedrock, and Vertex AI).

### Pricing

The thinking process incurs charges for:
- Tokens used during thinking (output tokens)
- Thinking blocks from the last assistant turn included in subsequent requests (input tokens)
- Standard text output tokens

When using summarized thinking:
- **Input tokens:** Tokens in your original request (excludes thinking tokens from previous turns)
- **Output tokens (billed):** The original thinking tokens that Claude generated internally
- **Output tokens (visible):** The summarized thinking tokens you see in the response
- **No charge:** Tokens used to generate the summary

> WARNING: The billed output token count will **not** match the visible token count in the response. You are billed for the full thinking process, not the thinking content visible in the response.

---

# PART 5: Prompt Engineering Overview

## Before prompt engineering

This guide assumes that you have:
1. A clear definition of the success criteria for your use case
2. Some ways to empirically test against those criteria
3. A first draft prompt you want to improve

## When to prompt engineer

This guide focuses on success criteria that are controllable through prompt engineering. Not every success criteria or failing eval is best solved by prompt engineering. For example, latency and cost can be sometimes more easily improved by selecting a different model.

## How to prompt engineer

All prompting techniques -- from clarity and examples to XML structuring, role prompting, thinking, and prompt chaining -- are covered in the Prompting best practices page (Part 1 of this document). That's the living reference; start there.

---

# APPENDIX: Quick Reference -- All Verbatim Prompt Blocks from Anthropic

Below is a consolidated index of every ready-to-use prompt block/template provided by Anthropic in the documentation above. These can be dropped directly into system prompts.

## 1. `<default_to_action>` -- Make Claude proactively implement changes

```text
<default_to_action>
By default, implement changes rather than only suggesting them. If the user's intent is unclear, infer the most useful likely action and proceed, using tools to discover any missing details instead of guessing. Try to infer the user's intent about whether a tool call (e.g., file edit or read) is intended or not, and act accordingly.
</default_to_action>
```

## 2. `<do_not_act_before_instructions>` -- Make Claude wait for explicit instructions

```text
<do_not_act_before_instructions>
Do not jump into implementatation or changes files unless clearly instructed to make changes. When the user's intent is ambiguous, default to providing information, doing research, and providing recommendations rather than taking action. Only proceed with edits, modifications, or implementations when the user explicitly requests them.
</do_not_act_before_instructions>
```

## 3. `<use_parallel_tool_calls>` -- Maximize parallel tool execution

```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>
```

## 4. `<investigate_before_answering>` -- Minimize hallucinations in agentic coding

```text
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating unless you are certain of the correct answer - give grounded and hallucination-free answers.
</investigate_before_answering>
```

## 5. `<avoid_excessive_markdown_and_bullet_points>` -- Control formatting

```text
<avoid_excessive_markdown_and_bullet_points>
When writing reports, documents, technical explanations, analyses, or any long-form content, write in clear, flowing prose using complete paragraphs and sentences. Use standard paragraph breaks for organization and reserve markdown primarily for `inline code`, code blocks (```...```), and simple headings (###, and ###). Avoid using **bold** and *italics*.

DO NOT use ordered lists (1. ...) or unordered lists (*) unless : a) you're presenting truly discrete items where a list format is the best option, or b) the user explicitly requests a list or ranking

Instead of listing items with bullets or numbers, incorporate them naturally into sentences. This guidance applies especially to technical writing. Using prose instead of excessive formatting will improve user satisfaction. NEVER output a series of overly short bullet points.

Your goal is readable, flowing text that guides the reader naturally through ideas rather than fragmenting information into isolated points.
</avoid_excessive_markdown_and_bullet_points>
```

## 6. `<frontend_aesthetics>` -- Better frontend design, avoid "AI slop"

```text
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliche color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

## 7. Anti-over-engineering prompt

```text
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused:

- Scope: Don't add features, refactor code, or make "improvements" beyond what was asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need extra configurability.

- Documentation: Don't add docstrings, comments, or type annotations to code you didn't change. Only add comments where the logic isn't self-evident.

- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).

- Abstractions: Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. The right amount of complexity is the minimum needed for the current task.
```

## 8. Anti-test-gaming / anti-hard-coding prompt

```text
Please write a high-quality, general-purpose solution using the standard tools available. Do not create helper scripts or workarounds to accomplish the task more efficiently. Implement a solution that works correctly for all valid inputs, not just the test cases. Do not hard-code values or create solutions that only work for specific test inputs. Instead, implement the actual logic that solves the problem generally.

Focus on understanding the problem requirements and implementing the correct algorithm. Tests are there to verify correctness, not to define the solution. Provide a principled implementation that follows best practices and software design principles.

If the task is unreasonable or infeasible, or if any of the tests are incorrect, please inform me rather than working around them. The solution should be robust, maintainable, and extendable.
```

## 9. Autonomy and safety guardrails

```text
Consider the reversibility and potential impact of your actions. You are encouraged to take local, reversible actions like editing files or running tests, but for actions that are hard to reverse, affect shared systems, or could be destructive, ask the user before proceeding.

Examples of actions that warrant confirmation:
- Destructive operations: deleting files or branches, dropping database tables, rm -rf
- Hard to reverse operations: git push --force, git reset --hard, amending published commits
- Operations visible to others: pushing code, commenting on PRs/issues, sending messages, modifying shared infrastructure

When encountering obstacles, do not use destructive actions as a shortcut. For example, don't bypass safety checks (e.g. --no-verify) or discard unfamiliar files that may be in-progress work.
```

## 10. Context window management for agent harnesses

```text
Your context window will be automatically compacted as it approaches its limit, allowing you to continue working indefinitely from where you left off. Therefore, do not stop tasks early due to token budget concerns. As you approach your token budget limit, save your current progress and state to memory before the context window refreshes. Always be as persistent and autonomous as possible and complete tasks fully, even if the end of your budget is approaching. Never artificially stop any task early regardless of the context remaining.
```

## 11. Encourage complete context usage for long tasks

```text
This is a very long task, so it may be beneficial to plan out your work clearly. It's encouraged to spend your entire output context working on the task - just make sure you don't run out of context with significant uncommitted work. Continue working systematically until you have completed this task.
```

## 12. Structured research approach

```text
Search for this information in a structured way. As you gather data, develop several competing hypotheses. Track your confidence levels in your progress notes to improve calibration. Regularly self-critique your approach and plan. Update a hypothesis tree or research notes file to persist information and provide transparency. Break down this complex research task systematically.
```

## 13. Subagent usage guidance

```text
Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that don't need to share state. For simple tasks, sequential operations, single-file edits, or tasks where you need to maintain context across steps, work directly rather than delegating.
```

## 14. Constrain overthinking / commit to approaches

```text
When you're deciding how to approach a problem, choose an approach and commit to it. Avoid revisiting decisions unless you encounter new information that directly contradicts your reasoning. If you're weighing two approaches, pick one and see it through. You can always course-correct later if the chosen approach fails.
```

## 15. Reduce adaptive thinking frequency

```text
Extended thinking adds latency and should only be used when it will meaningfully improve answer quality - typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

## 16. Guide interleaved thinking after tool results

```text
After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
```

## 17. Temporary file cleanup

```text
If you create any temporary new files, scripts, or helper files for iteration, clean up these files by removing them at the end of the task.
```

## 18. Post-tool-use summaries

```text
After completing a task that involves tool use, provide a quick summary of the work you've done.
```

## 19. LaTeX suppression (plain text math)

```text
Format your response in plain text only. Do not use LaTeX, MathJax, or any markup notation such as \( \), $, or \frac{}{}. Write all math expressions using standard text characters (e.g., "/" for division, "*" for multiplication, and "^" for exponents).
```
