# Introduction

It has been a long time since the last update of this repository. This project is a journal of me, in order to store the knowledge and sandbox practices that I have gathered during my working time in GHTK, Samsung RnD,...

The newest update focuses on applying agentic workflow, since with the help of AI, the productivity can be increased a lot, the only consideration is, it requires the user to have a solid base knowledge about the code produced by the AI and the ability to assert the safety when applying these into the existing infrastructures.

Furthermore, it also contains some knowledge I gained from various hackathon contests, startup projects, course projects during my master's degree perios at Chalmers University of Technology, Sweden.

# This repository is suitable for?

I guess it can be read, forked, and fixed by anyone who has the zeal to contribute and practice new skills. For example, Cloud Provider is essential, but for some cases, in some environments that require more stricly security compliance, using another vendor's products is unavailable, we must rely on "classical" tool, load balancer with Nginx or HA proxy, high availability with keepalive, ...

So in this repository, I will try to focus on these tools. But it is not a "walkthrough" or "how to play" like usual, I want to tell story about the reason why I chose these tools, how I configured them and if it was possible, which tool I would use instead.

# What's new?

Currently, with the rapidly rising of the AI, and the inspiration from [AI for DevOps](https://github.com/VersusControl/devops-ai-guidelines/tree/main). For me, since I already have several years of experience, I will focus on creating my customize tools based on these documents. Since I have my own workstation, and my current situation does not favor the choice of using an expensive solution like provisioned GPU nodes, edge AI machines,... Moreover, since my lastest (and biggest) project is not my sole involvement, I have to keep it as a secret till the day all members decied to publish it.

# Structural
```plaintext
devops-journal/
├── Figures/                     # Lot of illustrations, outdated, maybe never update LOL
├── Journal/                     # Step-by-step a pet project, will be updated soon
└── ai-ops/                      # AI agent setup and practical (will be in product)
```

[Figures](Figures/) - the directory for all Figures that I use as illustrations for this repo, maybe outdate, I will soon update them if I have enough time. Rarely updated

[Journal](Journal/) - bilinguals, but I will reduce it to only one language, saving lot of effort, also outdated, but will be update soon (medium priority). Not been updated for a long time, but will be received a new update soon.

[AI agent](ai-ops/) - the playground for setting up an AI agent for DevOps work, currently I use Ollama with the directly `cURL` call (with the help of `Python` of course). Actively updated on daily basis.

## Figures:

Contains the architecture of my previous probation project at GHTK - a large tech company in Vietnam with nearly 600 personnel for only Innovation Center (only count technical personnel, excluding financial, human resource). This company focuses on developing their own solution, infrastructure for their own software (map, vehicle tracking, parcel classification,...). Nearly 10000 servers was used and could be up to 20000 servers during its peak.

The pet project is simple: a Flask web application, with a full CI CD pipeline, observation stack, high availability,...

Used technology: `HAproxy`, `keepalive`, `sentinel` (for `redis`), `argoCD`, and `ELK` stack (with `filebeat` too).

## Journal:

A walkthrough, step-by-step that guides you through the full deployment of this pet project, but honestly, this was obsoleted shortly after first push. But soon will be another release with new architecture, more public cloud native. Since GTHK favoured the private cloud platform, so they used `Ansible`, but modern used `Terraform` instead because not every companies have the sufficient resources to organize and provision a whole fleet of on-premise infrastructure.

Also, since the `Flask` framework at that point was old up to present, and maybe not support some functions at the moment.

## AI-Ops:

Newest member of this repository, used to orchestrate and optimize the usage of AI agent. Currently supports open-source AI model: `gemma4`, `llama3.1` via `Ollama`. Although `Python` offers a dedicated library for `Ollama`, I chose to self implement the API call and all sort of patterns, constraints,... Since it will help developer to understand the core priciples, how to call, how to put the rate limiter (to not overload the AI agent, use token effectively,...).

I also wrote some specialzied functions, for example (currently) log analyzer with ability to read several log files at a time, extract the content and prepare the data for analysis process. Also implement the model for data in and out during this process. Because the AI easily halluciates itself, so the strutral input and output is a good way to ensure that we can get (almost) what we want. Also the strutural can act as a baseline in case you want to restrict and optimize the budget spent of token for LLM agent.

This work currently supports `llama3.1`a coding agent and very good at producing the structural output. I tried with `gemma4` but because it is a common, multi-purposes AI model, so it is quite bad at structural output.

Inside this directory, you can find:
- [classes](./ai-ops/classes/) the `Connector`- connect to the `Ollama`, frames, prepares data and gives you the output.
- [prompts](./ai-ops/prompts/) the library for different roles, for example: log analyzer, planner and code reviewer. Treat the prompt like code, can be versioned, updated and continuously tweaked for better performance.

The high level architecture should be: main (orchestrator) calls the necessary functions (log - aggregate log files and prepares data for analyze) then calls the connector to pass these fully prepared data to the LLM agent. Along with the connector, the corresponding prompt function (inside the `prompts` directory) will handle the data structural enforcer, output validation - that ensures you get your desried result. Inside the `classes`, I also try to create dedicated data classes for each function (log, code review and playbook planner surely need different constraints and expect different structural outputs).

# Credits

A lot of thanks to this repository: [DevOps AI Guidelines & Learning Path](https://github.com/VersusControl/devops-ai-guidelines/tree/main) since this is my main inspiration source.

Second thank to this project: [LLM prompt-injection defender](https://github.com/phungh67/devops-docs/tree/main/language-based-security/project) in collaboration with Emilia Nicander from my class, as the final project of the **Language-based Security course**. This allowed me to gain knowledge about API calling, LLM protection and foundation knowledge about interacting with a LLM model.