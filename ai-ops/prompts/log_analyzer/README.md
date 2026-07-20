# What's this?

This directory contains the definition (or precisely, the constraint for log analyzer role of the LLM agent) in json file [Analyzer](./log_analyzer.json), the original idea [idea](./log.txt) and the function, defined in [Function](./log_analyzer.py)

# How to customize it?

It is very simple, just open the `log_analyzer.py`and modify the `Triage` class with desired property, and also reflect with the JSON file.

# Under the hood

The JSON file acts as a source of truth for reading and templating all the constraints, contexts, roles, ... to feed in the Ollama Connector. So that, if you find another way to better enhance the prompt, remeber to update it, keep it in versioning control to reflext, tweak and finalize into production environment.

Python script only helps to tranform all the properties defined in the JSON file into payload, then send to Ollama. 

It is recommened to use some "coding" model like Qwen or Llama. The test proved that although Gemma could satisfy some "short" and "hard-coded" context, but in the later case with a log file, LLama had a better result (while Gemma had a halluciation)

# Futher tweak

Check the [Connector](../../classes/ollama_agent_connector.py), since it prepares the payload, frames the data and responsible for returning the result, also displaying some metric (like the correlation between input and output tokens,...)