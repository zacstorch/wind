import os

# after the first run, model is local
offline = True

if offline:
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    
import torch
from transformers import pipeline, GenerationConfig


def main():
    model = "Qwen/Qwen2.5-0.5B-Instruct"
    prompt = "tell me a story about Jerusalem"
    messages = [{'role': 'user', 'content': prompt}]

    generator = pipeline(
        "text-generation",
        model=model,
        device_map="auto",
        dtype=torch.float16,
        clean_up_tokenization_spaces=False,
    )

    gen_conf = GenerationConfig.from_pretrained(
        model,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.5,
    )

    res = generator(
        messages,
        generation_config=gen_conf
    )

    txt = res[0]['generated_text'][-1]['content']
    print('\n\n---')
    print(txt)
    print('---\n\n')

if __name__ == '__main__':
    main()
    
