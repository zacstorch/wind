import os
import sys
from openai import OpenAI

if len(sys.argv) < 3:
    print('Usage: add a file and a question')
    sys.exit(1)

fp = sys.argv[1]
q = sys.argv[2]

try:
    with open(fp,'r',encoding="utf-8") as f:
        f_txt = f.read()
except FileExistsError:
    print(f'Error file not found: {fp}')
    sys.exit(1)
except Exception as e:
    print(f'Error reading file {e}')
    sys.exit(1)

client = OpenAI(
                base_url='https://api.anthropic.com/v1/',
                api_key=os.environ["ANTHROPIC_API_KEY"],
            )

model='claude-haiku-4-5'
temp=0.0

sys_prompt = """You are an answering assistant.

    Rules:
    Answer ONLY using the Provided document. Do not guess.
    Quote exact passage that supports your answer.
    If answer is not found in document, respond: "I Can't find that in the document."
    Do not add explanations or apologies if the answer is missing.
"""
prompt = f"<document>{f_txt}</document>\nQuestion: {q}"

res = client.chat.completions.create(
    model=model,
    temperature=temp,
    messages=[
        {'role': 'system', 'content': sys_prompt},
        {'role': 'user', 'content': prompt},
    ]
)



txt = res.choices[0].message.content

print("----")
print(txt)
print("----")

