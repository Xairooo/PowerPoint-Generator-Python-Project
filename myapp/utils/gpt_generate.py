import os
import openai
from json import loads
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_development(user_message):
    conversation = build_conversation(user_message)
    try:
        assistant_message = generate_assistant_message(conversation)
    except openai.error.RateLimitError as e:
        assistant_message = "Rate limit exceeded. Sleeping for a bit..."

    return loads(assistant_message)


def build_conversation(user_message):
    return [
        {
            "role": "developer",
            "content": f"""
Imagine you are an AI Slides generating tool. Based on the input of the user, generate additional relevant content and create the structure of the slides presentation as a JSON object.
Return the entire response as a well-structured JSON object following this concise pattern:
{{
  "slides": [
    {{
      "title": "Slide title",
      "layout": {{
        "type": "TITLE",
        "sections": [
          {{ "type": "subtitle", "content": "<insert-subtitle>" }}
        ]
      }}
    }},
    {{
      "title": "Slide title",
      "layout": {{
        "type": "TITLE_AND_CONTENT",
        "sections": [
          {{ "type": "bullets", "content": [] }},
          {{ "type": "text", "content": "" }}
        ]
      }}
    }},
    {{
      "title": "Slide title",
      "layout": {{
        "type": "TWO_CONTENT",
        "sections": [
          {{ "type": "bullets", "content": [] }},
          {{ "type": "image", "content": "" }}
        ]
      }}
    }},
     {{
      "title": "Slide title",
      "layout": {{
        "type": "COMPARISON",
        "sections": [
          {{ "position": "left", "title": "<insert-title>", "content": <insert-content>  }},
          {{ "position": "right", "title": "<insert-title>", "content": <insert-content> }}
        ]
      }}
    }},
    {{
      "title": "Slide title",
      "layout": {{
        "type": "PICTURE_WITH_CAPTION",
        "sections": [
          {{ "type": "image", "content": <insert-content>  }},
          {{ "type": "caption", "content": <insert-content> }}
        ]
      }}
    }}
  ]
}}
Create (the number of the slide) slides with at least 50 words for each slide. For each section of type bullets, provide at least 5 points. For each section of type text or title, provide content with at least 40 words.
RESPOND WITH JSON ONLY
"""
        },
        {
            "role": "user",
            "content":  user_message
        }
    ]


def generate_assistant_message(conversation):
    print("start chatting with AI")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    return response['choices'][0]['message']['content']
