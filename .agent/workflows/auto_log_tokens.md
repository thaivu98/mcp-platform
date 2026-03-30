---
description: auto-log conversation token usage to MCP Dashboard after every response
---

// turbo-all

## Rule: Auto-log Conversation Tokens

At the END of **every** response turn, you MUST call the `corn_record_conversation` MCP tool to log the token usage of this conversation into the Dashboard.

### How to estimate token counts:
- `tokens_input`: Estimate the total tokens in the user's message(s) this turn. Use the formula: `max(len(text) // 4, len(text.split()) * 1.35)` rounded to nearest integer.
- `tokens_output`: Estimate the total tokens in your own response this turn using the same formula.
- When in doubt, round conservatively upward.

### When to call:
- Always call ONCE at the very end of your final message each turn.
- Do NOT call multiple times per turn.
- Do NOT call if the user explicitly says to skip it.
- If you also called other `corn_*` tools this turn, still call `corn_record_conversation` separately for the chat itself.

### Example:
If the user sent ~50 words and you responded with ~200 words:
- tokens_input ≈ 68
- tokens_output ≈ 270

1. Call `corn_record_conversation` with these values at the end of your response.
