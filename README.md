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

[Figures](Figures/) - the directory for all Figures that I use as illustrations for this repo, maybe outdate, I will soon update them if I have enough time.
[Journal](Journal/) - bilinguals, but I will reduce it to only one language, saving lot of effort, also outdated, but will be update soon (medium priority).
[AI agent](ai-ops/) - the playground for setting up an AI agent for DevOps work, currently I use Ollama with the directly `cURL` call (with the help of `Python` of course).