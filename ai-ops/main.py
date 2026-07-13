from ollama import chat
from ollama import ChatResponse

import time

MODELs = ["gemma4", "llama3.1"]

def run_task(model: str, prompt: str) -> dict:
    start = time.perf_counter()
    resp =  chat(
        model=model,
        messages=[{
            'role': 'user',
            'content': prompt
        }],
    )

    return {
        "model": model,
        "output": resp.message.content,
        "latency_s": round(time.perf_counter() - start, 2),
        "input_token": resp.prompt_eval_count,
        "output_token": resp.eval_count
    }

if __name__ == "__main__":
    prompt = "Why the sky is blue?"
    # print(run_task(MODELs[0], prompt))
    resp = run_task(MODELs[0], prompt)
    print(f'This prompt was produced by model: {resp['model']}\n')
    print(f'Duration for this prompt: {resp['latency_s']}\n')
    print(f'Input token: {resp['input_token']}\n')
    print(f'Output token: {resp['output_token']}\n')