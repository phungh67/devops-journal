# Components

## Ollama Connector

The customized connector, accepts arguments from user (the `Ollama` URL, the favorite model). Supports fall back with default values, check the constructor for more detail.

Ollama Connector does several job:

- Provides an interface (or a convenient way) for calling LLM agent, you don't have to worry about writing some complex and easily-to-missing-some-flags `cURL` command in the terminal.

- Frames the payload before sending it to the LLM model. As I said earlier, a structural input is better than "normal input". Moreover, the connector also enforces the output to strictly compile with the model definition inside the [prompts](../prompts/), so that you don't have to worry the agent suddenly becomes dump and returns several pragraphs than a JSON structural repsonse.

- (In development) Function to print, warn and deduce a number of token in the common pool, helps you to better control the in/out rate of token usage, because every good models in the worlds now, they are very expensive, so token is money, and money isn't unlimited.

## Prompt-related classes

I place all the related classes for each role of the AI agent inside this directory as well. As you know, each role requires a dedicated, hightly-customized structural definition. For a log analyzer, the most important criteria is the context. What was that service, which is the main language, 200 was normal, but even 400 was normal because it was a feature that "if it was running, let it be?",... 

### Log

Class for the log analyzer role

- **ErrorPattern**: aggregated result of all errors that were in the log, with evidence (log line), count (how many it appeared).
- **Action**: we know the error, so we must have some action.
- **Triage**: structural output, with root cause, severity, next step, confidence,...