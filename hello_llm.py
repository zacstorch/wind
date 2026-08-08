from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
import os
import re


client = OpenAI(
                base_url='https://api.anthropic.com/v1/',
                api_key=os.environ["ANTHROPIC_API_KEY"],
            )

class Attraction(BaseModel):
    name: str = Field(description="Name of the attraction")
    description: str = Field(description="Short description")
    duration_minutes: int = Field(description="Estimated visit duration")
    highlights: List[str] = Field(description="Key things to see")


class Res(BaseModel):
    city: str = Field(description="City or destination")
    summary: str = Field(description="Brief introduction to the destination")
    attractions: List[Attraction]
    local_foods: List[str] = Field(description="Recommended local dishes")
    tips: List[str] = Field(description="Helpful travel tips")


res = client.chat.completions.create(
    model='claude-haiku-4-5',
    temperature=0.9,
    messages=[{
        'role': 'system',
        'content': (
            "You are a JSON API.\n"
            f'Schema: {Res.model_json_schema()}\n'
            'You are a local israely captivating storyteller, obsessed with obscure urban legends and fringe local myths that people dismiss but you do believe. You tell them vividly, mysteriously, and with such conviction that tourists start questioning what’s real.\n'
            "Return ONLY valid JSON. Do not use markdown. Do not add anything. Do not wrap the JSON"
        )},{
        'role': 'user',
        'content': 'where are we now'
    }]
)



txt = res.choices[0].message.content

print("----")
print(txt)
print("----")

match = re.search(r"\{.*\}", txt, re.DOTALL)
if not match:
    raise ValueError("No JSON match")
j = Res.model_validate_json(match.group(0))

print(j.city)
print(j.summary)

for i in j.attractions:
    print(f"{i.name}: {i.duration_minutes} minutes")

