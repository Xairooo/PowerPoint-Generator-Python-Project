import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_development(user_message):
    conversation = build_conversation(user_message)
    try:
        assistant_message = generate_assistant_message(conversation)
    except openai.error.RateLimitError as e:
        assistant_message = "Rate limit exceeded. Sleeping for a bit..."

    return assistant_message


def build_conversation(user_message):
    return [
        {"role": "system",
         "content": """
I am creating a slide presentation on 'Lionel Messi'. Here is the content for each slide:

[ {"title": "[Basic Information of Message]", "content": "[Date of birth, where he was born]"}, {"title": "[Football career]", "content": "[Brief description, bullet points, or detailed text]"}, ... ]

Can you suggest suitable slide layouts for each slide in JSON format?

Automatically identify content structures such as lists, comparisons, timelines, summaries, etc.
Use only these layout types:
TITLE
TITLE_AND_CONTENT
SECTION_HEADER
TWO_CONTENT
COMPARISON
TITLE_ONLY
BLANK
CONTENT_WITH_CAPTION
PICTURE_WITH_CAPTION
TITLE_AND_VERTICAL_TEXT
VERTICAL_TITLE_AND_TEXT

Return the entire response as a well-structured JSON object following this concise pattern:
{
  "slides": [
    {
      "title": "Slide title",
      "layout": {
        "type": "TITLE | TITLE_AND_CONTENT | SECTION_HEADER | TWO_CONTENT | TITLE_ONLY | BLANK | CONTENT_WITH_CAPTION | PICTURE_WITH_CAPTION | TITLE_AND_VERTICAL_TEXT | VERTICAL_TITLE_AND_TEXT",
        "sections": [
          { "type": "title", "content": "..." },
          { "type": "text/bullets/image", "content": "string | array | nested object" }
        ]
      },
      "layout": {
        "type": "COMPARISON",
        "sections": [
          { "position": "left", "title": "...", "content": ["..."] },
          { "position": "right", "title": "...", "content": ["..."] }
        ]
      }
    },
    ...
  ]
}

Make the layout visually appropriate, clear, and engaging for the content type.
"""},
        {"role": "user", "content": user_message}
    ]


def generate_assistant_message(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    return response['choices'][0]['message']['content']
