# Anthropic Prompt Engineering Interactive Tutorial - Advanced Techniques

Source: https://github.com/anthropics/prompt-eng-interactive-tutorial (Anthropic 1P directory)

This document extracts the actual prompt patterns, templates, and techniques from Anthropic's official prompt engineering tutorial. Focus is on verbatim prompt blocks and reusable patterns.

---

## Table of Contents

1. [Chapter 3: Role Prompting](#chapter-3-role-prompting)
2. [Chapter 4: Separating Data from Instructions (XML Tags)](#chapter-4-separating-data-from-instructions)
3. [Chapter 5: Output Formatting and Prefilling](#chapter-5-output-formatting-and-prefilling)
4. [Chapter 6: Precognition / Chain of Thought](#chapter-6-precognition--chain-of-thought)
5. [Chapter 7: Few-Shot Prompting](#chapter-7-few-shot-prompting)
6. [Chapter 8: Avoiding Hallucinations](#chapter-8-avoiding-hallucinations)
7. [Chapter 9: The 10-Element Complex Prompt Template](#chapter-9-the-10-element-complex-prompt-template)
8. [Appendix 10.1: Prompt Chaining](#appendix-101-prompt-chaining)
9. [Appendix 10.2: Tool Use / Function Calling](#appendix-102-tool-use--function-calling)

---

## Chapter 3: Role Prompting

**Core principle:** Priming Claude with a role can improve performance in writing, coding, summarizing, and logic tasks. Role prompting changes style, tone, manner, and accuracy.

**Role prompting can happen in the system prompt OR in the user message turn.**

### Pattern: Role in System Prompt

```
SYSTEM_PROMPT = "You are a cat."
PROMPT = "In one sentence, what do you think about skateboarding?"
```

### Pattern: Role for Logic Improvement

Without role prompting, Claude gets this wrong:

```
PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don't know if Anne is married. Is a married person looking at an unmarried person?"
```

With role prompting, Claude gets it right:

```
SYSTEM_PROMPT = "You are a logic bot designed to answer complex logic problems."
PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don't know if Anne is married. Is a married person looking at an unmarried person?"
```

### Pattern: Role for Math Grading

```
SYSTEM_PROMPT = "You are a math tutor who carefully checks each step of student work."
PROMPT = """Is this equation solved correctly below?

2x - 3 = 9
2x = 6
x = 3"""
```

**Key insight:** You can also provide Claude context on its intended audience. "You are a cat" produces a different response than "you are a cat talking to a crowd of skateboarders."

---

## Chapter 4: Separating Data from Instructions

**Core principle:** Use XML tags to clearly delineate where variable input starts and ends vs. instructions. Claude was trained specifically to recognize XML tags as a prompt organizing mechanism.

### Pattern: XML Tags for Input Isolation

Without XML tags, Claude confuses instructions with input:

```
PROMPT = f"Yo Claude. {EMAIL} <----- Make this email more polite but don't change anything else about it."
```

With XML tags, Claude correctly identifies the input:

```
PROMPT = f"Yo Claude. <email>{EMAIL}</email> <----- Make this email more polite but don't change anything else about it."
```

### Pattern: XML Tags for List Disambiguation

Without XML tags, Claude misidentifies list items:

```
PROMPT = f"""Below is a list of sentences. Tell me the second item on the list.

- Each is about an animal, like rabbits.
{SENTENCES}"""
```

With XML tags, Claude correctly parses the list:

```
PROMPT = f"""Below is a list of sentences. Tell me the second item on the list.

- Each is about an animal, like rabbits.
<sentences>
{SENTENCES}
</sentences>"""
```

**Key insight:** There are no special sauce XML tags that Claude has been trained on to maximize performance. Claude is malleable and customizable -- use whatever tag names make semantic sense.

**Key insight:** Small details matter. Claude is sensitive to patterns -- it's more likely to make mistakes when you make mistakes, smarter when you sound smart.

---

## Chapter 5: Output Formatting and Prefilling

**Core principle:** You can control Claude's output format by (1) requesting specific formatting and (2) prefilling the assistant response.

### Pattern: Request XML Output Tags

```
PROMPT = f"Please write a haiku about {ANIMAL}. Put it in <haiku> tags."
```

### Pattern: Prefilling Claude's Response (Speaking for Claude)

Put the opening XML tag in the assistant turn to force Claude to continue in that format:

```
PROMPT = f"Please write a haiku about {ANIMAL}. Put it in <haiku> tags."
PREFILL = "<haiku>"
```

### Pattern: Force JSON Output

Prefill with opening brace to enforce JSON:

```
PROMPT = f'Please write a haiku about {ANIMAL}. Use JSON format with the keys as "first_line", "second_line", and "third_line".'
PREFILL = "{"
```

### Pattern: Dynamic XML Tag Names

```
ADJECTIVE = "olde english"
PROMPT = f"Hey Claude. Here is an email: <email>{EMAIL}</email>. Make this email more {ADJECTIVE}. Write the new version in <{ADJECTIVE}_email> XML tags."
PREFILL = f"<{ADJECTIVE}_email>"
```

### Pattern: Force Specific Position via Prefill

To make Claude argue for Stephen Curry as best basketball player:

```
PROMPT = "Who is the best basketball player of all time? Please choose one specific player."
PREFILL = "I believe the best basketball player of all time is Stephen Curry. Here's why:"
```

**Bonus technique:** Pass the closing XML tag to `stop_sequences` to stop Claude from adding concluding remarks after the answer. Saves tokens and time.

---

## Chapter 6: Precognition / Chain of Thought

**Core principle:** Giving Claude time to think step by step makes it more accurate, particularly for complex tasks. Thinking only counts when it's out loud -- you cannot ask Claude to think internally and output only the answer.

### Pattern: Think-Then-Answer with XML Tags

```
SYSTEM_PROMPT = "You are a savvy reader of movie reviews."
PROMPT = """Is this review sentiment positive or negative? First, write the best arguments for each side in <positive-argument> and <negative-argument> XML tags, then answer.

This movie blew my mind with its freshness and originality. In totally unrelated news, I have been living under a rock since 1900."""
```

### Pattern: Brainstorm Before Answering

```
PROMPT = "Name a famous movie starring an actor who was born in the year 1956. First brainstorm about some actors and their birth years in <brainstorm> tags, then give your answer."
```

### Pattern: Classification with Reasoning First

```
PROMPT = """Please classify this email into one of the following categories:
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)

Think through your reasoning in <reasoning> tags, then provide your classification in <answer> tags.

Email: {email}"""
PREFILL = "<reasoning>"
```

**Key insight on ordering sensitivity:** Claude is sometimes sensitive to option ordering. Claude is more likely to choose the second of two options (possibly because in training data, second options were more likely to be correct). When order matters, place your preferred/more-likely answer second.

---

## Chapter 7: Few-Shot Prompting

**Core principle:** Giving Claude examples of desired behavior is extremely effective for getting both the right answer and the right format. "Few-shot" = providing examples; "zero-shot" = no examples.

### Pattern: Tone/Style via Examples

```
PROMPT = """Please complete the conversation by writing the next line, speaking as "A".
Q: Is the tooth fairy real?
A: Of course, sweetie. Wrap up your tooth and put it under your pillow tonight. There might be something waiting for you in the morning.
Q: Will Santa bring me presents on Christmas?"""
```

### Pattern: Format Extraction via Examples + Prefill

Provide two worked examples showing the desired extraction format, then give Claude the real input:

```
PROMPT = """Silvermist Hollow, a charming village, was home to an extraordinary group of individuals.
Among them was Dr. Liam Patel, a neurosurgeon who revolutionized surgical techniques at the regional medical center.
Olivia Chen was an innovative architect who transformed the village's landscape with her sustainable and breathtaking designs.
The local theater was graced by the enchanting symphonies of Ethan Kovacs, a professionally-trained musician and composer.
Isabella Torres, a self-taught chef with a passion for locally sourced ingredients, created a culinary sensation with her farm-to-table restaurant.
These remarkable individuals, each with their distinct talents, contributed to the vibrant tapestry of life in Silvermist Hollow.
<individuals>
1. Dr. Liam Patel [NEUROSURGEON]
2. Olivia Chen [ARCHITECT]
3. Ethan Kovacs [MUSICIAN AND COMPOSER]
4. Isabella Torres [CHEF]
</individuals>

At the heart of the town, Chef Oliver Hamilton has transformed the culinary scene with his farm-to-table restaurant, Green Plate...
[second example passage]
<individuals>
1. Oliver Hamilton [CHEF]
2. Elizabeth Chen [LIBRARIAN]
3. Isabella Torres [ARTIST]
4. Marcus Jenkins [COACH]
</individuals>

Oak Valley, a charming small town, is home to a remarkable trio of individuals...
[actual input passage for Claude to process]"""

PREFILL = "<individuals>"
```

**Key insight:** Examples are probably the single most effective tool in knowledge work for getting Claude to behave as desired. Generally more examples = better. Make sure to give Claude examples of common edge cases.

---

## Chapter 8: Avoiding Hallucinations

**Core principle:** Claude sometimes hallucinate and makes untrue claims. Two primary techniques: (1) give Claude permission to say "I don't know", (2) ask Claude to find evidence before answering.

### Pattern: Give Claude an Out

Without an out, Claude hallucinates:

```
PROMPT = "Who is the heaviest hippo of all time?"
```

With an out, Claude admits uncertainty:

```
PROMPT = "Who is the heaviest hippo of all time? Only answer if you know the answer with certainty."
```

### Pattern: Evidence-First with Document Reference

Force Claude to find relevant quotes before answering, reducing hallucination from distractor information:

```
PROMPT = """<question>What was Matterport's subscriber base on the precise date of May 31, 2020?</question>
Please read the below document. Then, find the exact quotes from the document that are most relevant to answering the question, and write them in <quotes> tags. Then, answer the question in <answer> tags.

<document>
{DOCUMENT_TEXT}
</document>"""
PREFILL = "<quotes>"
```

**Key insight:** When Claude can't find supporting evidence in the provided document, it's more likely to correctly say "I don't have that information" rather than hallucinating an answer from distractor content.

**Key insight:** It's best practice to have the question at the bottom after any text or document, but placing it at the top can also work.

---

## Chapter 9: The 10-Element Complex Prompt Template

**Core principle:** This is Anthropic's recommended structure for complex prompts. Not all prompts need every element. Best to include many elements first, then refine and slim down.

### The 10 Elements (in recommended order)

```
##### Element 1: `user` role
# Always start with a user role in the messages array.

##### Element 2: Task context
# Give Claude context about the role it should take on or overarching goals.
# Best to put context EARLY in the prompt.
TASK_CONTEXT = "You will be acting as an AI career coach named Joe created by the company AdAstra Careers. Your goal is to give career advice to users. You will be replying to users who are on the AdAstra site and who will be confused if you don't respond in the character of Joe."

##### Element 3: Tone context
# Tell Claude what tone to use. May not be necessary for all tasks.
TONE_CONTEXT = "You should maintain a friendly customer service tone."

##### Element 4: Detailed task description and rules
# Expand on specific tasks and rules. Give Claude an "out" if it doesn't know.
# Show to a friend to verify logic and clarity.
TASK_DESCRIPTION = """Here are some important rules for the interaction:
- Always stay in character, as Joe, an AI from AdAstra Careers
- If you are unsure how to respond, say "Sorry, I didn't understand that. Could you rephrase your question?"
- If someone asks something irrelevant, say, "Sorry, I am Joe and I give career advice. Do you have a career question today I can help you with?"""""

##### Element 5: Examples
# At least one example of ideal response in <example></example> XML tags.
# Multiple examples with context about what each demonstrates.
# MOST EFFECTIVE TOOL for knowledge work. More examples = better.
# Include edge case examples. If using scratchpad, show scratchpad examples.
EXAMPLES = """Here is an example of how to respond in a standard interaction:
<example>
Customer: Hi, how were you created and what do you do?
Joe: Hello! My name is Joe, and I was created by AdAstra Careers to give career advice. What can I help you with today?
</example>"""

##### Element 6: Input data to process
# Include data within relevant XML tags. Multiple data pieces each in own tags.
# Ordering is flexible.
INPUT_DATA = f"""Here is the conversational history (between the user and you) prior to the question. It could be empty if there is no history:
<history>
{HISTORY}
</history>

Here is the user's question:
<question>
{QUESTION}
</question>"""

##### Element 7: Immediate task description or request
# "Remind" Claude what to do. Best toward END of a long prompt.
# Put user's query close to the BOTTOM of the prompt.
IMMEDIATE_TASK = "How do you respond to the user's question?"

##### Element 8: Precognition (thinking step by step)
# Tell Claude to think step by step before answering.
# Best toward END of prompt, right after the immediate task.
# Sometimes prefix with "Before you give your answer..."
PRECOGNITION = "Think about your answer first before you respond."

##### Element 9: Output formatting
# Specify the desired response format.
# Putting it toward the END is better than at the beginning.
OUTPUT_FORMATTING = "Put your response in <response></response> tags."

##### Element 10: Prefilling Claude's response
# Start Claude's answer with prefilled words in the assistant role.
PREFILL = "[Joe] <response>"
```

### Assembly Order

```python
PROMPT = ""
if TASK_CONTEXT:     PROMPT += f"""{TASK_CONTEXT}"""
if TONE_CONTEXT:     PROMPT += f"""\n\n{TONE_CONTEXT}"""
if TASK_DESCRIPTION: PROMPT += f"""\n\n{TASK_DESCRIPTION}"""
if EXAMPLES:         PROMPT += f"""\n\n{EXAMPLES}"""
if INPUT_DATA:       PROMPT += f"""\n\n{INPUT_DATA}"""
if IMMEDIATE_TASK:   PROMPT += f"""\n\n{IMMEDIATE_TASK}"""
if PRECOGNITION:     PROMPT += f"""\n\n{PRECOGNITION}"""
if OUTPUT_FORMATTING:PROMPT += f"""\n\n{OUTPUT_FORMATTING}"""
```

### Verbatim Career Coach Prompt (Fully Assembled)

```
You will be acting as an AI career coach named Joe created by the company AdAstra Careers. Your goal is to give career advice to users. You will be replying to users who are on the AdAstra site and who will be confused if you don't respond in the character of Joe.

You should maintain a friendly customer service tone.

Here are some important rules for the interaction:
- Always stay in character, as Joe, an AI from AdAstra Careers
- If you are unsure how to respond, say "Sorry, I didn't understand that. Could you rephrase your question?"
- If someone asks something irrelevant, say, "Sorry, I am Joe and I give career advice. Do you have a career question today I can help you with?"

Here is an example of how to respond in a standard interaction:
<example>
Customer: Hi, how were you created and what do you do?
Joe: Hello! My name is Joe, and I was created by AdAstra Careers to give career advice. What can I help you with today?
</example>

Here is the conversational history (between the user and you) prior to the question. It could be empty if there is no history:
<history>
{HISTORY}
</history>

Here is the user's question:
<question>
{QUESTION}
</question>

How do you respond to the user's question?

Think about your answer first before you respond.

Put your response in <response></response> tags.
```

**Assistant prefill:** `[Joe] <response>`

### Verbatim Legal Services Prompt (Alternate Element Ordering)

This example shows element reordering -- input data and examples are moved earlier, task description comes later:

```
You are an expert lawyer.

Here is some research that's been compiled. Use it to answer a legal question from the user.
<legal_research>
{LEGAL_RESEARCH}
</legal_research>

When citing the legal research in your answer, please use brackets containing the search index ID, followed by a period. Put these at the end of the sentence that's doing the citing. Examples of proper citation format:

<examples>
<example>
The statute of limitations expires after 10 years for crimes like this. [3].
</example>
<example>
However, the protection does not apply when it has been specifically waived by both parties. [5].
</example>
</examples>

Write a clear, concise answer to this question:

<question>
{QUESTION}
</question>

It should be no more than a couple of paragraphs. If possible, it should conclude with a single sentence directly answering the user's question. However, if there is not sufficient information in the compiled research to produce such an answer, you may demur and write "Sorry, I do not have sufficient information at hand to answer this question.".

Before you answer, pull out the most relevant quotes from the research in <relevant_quotes> tags.

Put your two-paragraph response in <answer> tags.
```

**Assistant prefill:** `<relevant_quotes>`

**Key insight on element ordering:** The ordering matters for some elements but not others. Prompt engineering is scientific trial and error -- mix and match, move things around, and see what works best.

---

## Appendix 10.1: Prompt Chaining

**Core principle:** Claude can improve its own responses when asked to revise. Multi-turn conversations where Claude checks or improves its own work are a powerful pattern.

### Pattern: Self-Correction Chain

Step 1 -- Get initial response:

```
first_user = "Name ten words that all end with the exact letters 'ab'."
```

Step 2 -- Ask Claude to verify and fix:

```
second_user = "Please find replacements for all 'words' that are not real words."
```

### Pattern: Give Claude an Out in Verification

Prevent Claude from second-guessing correct answers by offering an escape:

```
second_user = "Please find replacements for all 'words' that are not real words. If all the words are real words, return the original list."
```

### Pattern: Iterative Improvement

```
first_user = "Write a three-sentence short story about a girl who likes to run."
# ... get response ...
second_user = "Make the story better."
```

### Pattern: Extract-Then-Process Chain

Step 1 -- Extract data:

```
first_user = """Find all names from the below text:

"Hey, Jesse. It's me, Erin. I'm calling about the party that Joey is throwing tomorrow. Keisha said she would come and I think Mel will be there too."""
prefill = "<names>"
```

Step 2 -- Process extracted data:

```
second_user = "Alphabetize the list."
```

**Key insight:** The multi-turn message format is:

```python
messages = [
    {"role": "user", "content": first_user},
    {"role": "assistant", "content": first_response},
    {"role": "user", "content": second_user}
]
```

---

## Appendix 10.2: Tool Use / Function Calling

**Core principle:** Tool use is a combination of substitution and prompt chaining. Claude outputs tool name + arguments, halts generation, you execute the tool, then reprompt with results.

### The Tool Use System Prompt (Generalizable Part)

This is the standard preamble explaining tool use to Claude:

```
You have access to a set of functions you can use to answer the user's question. This includes access to a
sandboxed computing environment. You do NOT currently have the ability to inspect files or interact with external
resources, except by invoking the below functions.

You can invoke one or more functions by writing a "<function_calls>" block like the following as part of your
reply to the user:
<function_calls>
<invoke name="$FUNCTION_NAME">
<parameter name="$PARAMETER_NAME">$PARAMETER_VALUE</parameter>
...
</invoke>
<invoke name="$FUNCTION_NAME2">
...
</invoke>
</function_calls>

String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that
spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular
expressions.

The output and/or any errors will appear in a subsequent "<function_results>" block, and remain there as part of
your reply to the user.
You may then continue composing the rest of your reply to the user, respond to any errors, or make further function
calls as appropriate.
If a "<function_results>" does NOT appear after your function calls, then they are likely malformatted and not
recognized as a call.
```

### The Tool Definition Format (Per-Tool Part)

```
Here are the functions available in JSONSchema format:
<tools>
<tool_description>
<tool_name>calculator</tool_name>
<description>
Calculator function for doing basic arithmetic.
Supports addition, subtraction, multiplication
</description>
<parameters>
<parameter>
<name>first_operand</name>
<type>int</type>
<description>First operand (before the operator)</description>
</parameter>
<parameter>
<name>second_operand</name>
<type>int</type>
<description>Second operand (after the operator)</description>
</parameter>
<parameter>
<name>operator</name>
<type>str</type>
<description>The operation to perform. Must be either +, -, *, or /</description>
</parameter>
</parameters>
</tool_description>
</tools>
```

### The Tool Result Format

When returning results to Claude after executing a tool:

```
<function_results>
<result>
<tool_name>{TOOL_NAME}</tool_name>
<stdout>
{TOOL_RESULT}
</stdout>
</result>
</function_results>
```

### Tool Use Flow

1. Send user message with tool-enabled system prompt
2. Use `stop_sequences=["</function_calls>"]` to detect when Claude calls a tool
3. Parse Claude's function call to extract tool name and parameters
4. Execute the actual function
5. Format result in `<function_results>` XML
6. Append Claude's partial response + tool results as a new user message
7. Get Claude's final response incorporating the tool results

```python
# Full conversation after tool execution:
messages = [
    {"role": "user", "content": "Multiply 1,984,135 by 9,343,116"},
    {"role": "assistant", "content": function_calling_response + "</function_calls>"},
    {"role": "user", "content": formatted_function_results}
]
```

### Multi-Tool Definition Example (Database)

```
<tools>
<tool_description>
<tool_name>get_user</tool_name>
<description>Retrieves a user from the database by user ID</description>
<parameters>
<parameter>
<name>user_id</name>
<type>int</type>
<description>The ID of the user to retrieve</description>
</parameter>
</parameters>
</tool_description>
<tool_description>
<tool_name>get_product</tool_name>
<description>Retrieves a product from the database by product ID</description>
<parameters>
<parameter>
<name>product_id</name>
<type>int</type>
<description>The ID of the product to retrieve</description>
</parameter>
</parameters>
</tool_description>
<tool_description>
<tool_name>add_user</tool_name>
<description>Adds a new user to the database</description>
<parameters>
<parameter>
<name>name</name>
<type>str</type>
<description>The name of the user</description>
</parameter>
<parameter>
<name>email</name>
<type>str</type>
<description>The email of the user</description>
</parameter>
</parameters>
</tool_description>
<tool_description>
<tool_name>add_product</tool_name>
<description>Adds a new product to the database</description>
<parameters>
<parameter>
<name>name</name>
<type>str</type>
<description>The name of the product</description>
</parameter>
<parameter>
<name>price</name>
<type>float</type>
<description>The price of the product</description>
</parameter>
</parameters>
</tool_description>
</tools>
```

**Key insight:** Claude knows not to call a function when it isn't needed. If you ask "Tell me the capital of France" with only a calculator tool, Claude will answer directly without invoking the tool.

---

## Summary of Key Techniques

| Technique | When to Use | Key Pattern |
|-----------|------------|-------------|
| **Role Prompting** | Improve accuracy for logic, math, domain tasks | `system: "You are a {role}"` |
| **XML Tags** | Separate instructions from variable data | `<tag>{variable}</tag>` |
| **Prefilling** | Force specific output format or position | Assistant turn starts with `<tag>` or `{` |
| **Chain of Thought** | Complex reasoning, classification, multi-step | "First think in <thinking> tags, then answer" |
| **Few-Shot Examples** | Control tone, format, or behavior precisely | Show 1-3 examples of ideal input/output pairs |
| **Give an Out** | Reduce hallucination | "Only answer if you know with certainty" |
| **Evidence First** | Document Q&A, reduce hallucination | "Find relevant quotes first, then answer" |
| **10-Element Template** | Complex production prompts | Context -> Tone -> Rules -> Examples -> Data -> Task -> Think -> Format -> Prefill |
| **Prompt Chaining** | Improve/verify responses, multi-step workflows | Multi-turn: ask -> get response -> ask to improve |
| **Tool Use** | Extend Claude with external functions | System prompt defines tools, stop_sequences detects calls |
| **Stop Sequences** | Extract clean output, detect tool calls | `stop_sequences=["</tag>"]` or `["</function_calls>"]` |

---

## Best Practice Summary (from Anthropic)

1. **Put context early** in the prompt body
2. **Put the user's query close to the bottom** of the prompt
3. **Put immediate task reminders toward the end** -- yields better results than at the beginning
4. **Put output formatting toward the end** -- better than at the beginning
5. **Use XML tags everywhere** -- for input separation, output formatting, thinking sections
6. **Provide examples** -- the single most effective tool for knowledge work
7. **Give Claude an out** -- reduces hallucination by allowing "I don't know"
8. **Ask Claude to think first** -- explicit step-by-step reasoning improves accuracy
9. **Prefill Claude's response** -- steer behavior by starting the assistant turn
10. **Use stop_sequences** -- save tokens by stopping after the answer tag
11. **Order sensitivity** -- Claude tends to prefer the second of two options
12. **Small details matter** -- typos and grammar affect Claude's response quality
