# What is this?
Well, as its name says all, this is the programmatic prompt engineering for AI assistan. Since the LLM chat bot has limited context window, easily to halluciate itself, we should pay attention to these points.

Since a structural reply is better than a "casual" response, for example, when you put some question: "How to write a Fibonacci function in Python", a good response should look like:
```json
{
    "Answer": "def calc_finn...",
    "Confidence": "high | medium | low",
    "Next step": "advance user's input handling"
}
```

From that response, we can know this answer can be applied right away, or requires some double check, additionally research,... 

Furthermore, to gain a structural answer, it is recommended to feed the agent with a structural question.

# Keep in mind

Good prompt should be kept and applied versioning control - to continuous enhance, improve over time (and to avoid the flaw if we cannot detect it right away).

We should not put something in the LLM, and hope it will answer in a good way. Additionally, the token is expensive, so how to write, how to optimize the token usage is a very critical concern.

# Which included?

## Structural
```plaintext
ai-ops/
├── classes/                     # Connector to LLM client (currently Ollama)
├── prompts/                     # Prompts, structural
└── main.py/                     # Entrypoint
```

[classes](classes/): Customized Ollama Connector, direct API calling, customized

[prompts](prompts/): Prompts with role and their own handlers

## Flavors

Currently, there are 3 types of prompts:
- [log analyzer](./prompts/log_analyzer/): an analyzer for log during incident, error troubleshooting time, currently focusing on first prototype, will try to make a "template/sketch" for log analyzer (based on some famous framework like Fiber, Flask,...)
- runbook planner (unstarted): a planner for documenting the code base.
- terraform reviewer (unstarted): the name says it all

# Usage

Can be freely modified, but remember to not cause circular dependencies. The prompts provides domain (definition, template and functions) while the connector simply provides the methods to pass these payload to the Ollama (or Anthropic, Gemini, they are all the same concept). And the main is only for running (entrypoint, orchestrator)