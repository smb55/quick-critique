from openai import OpenAI
from .creds import openai_api_key
from .ai import ai_context, reminder

client = OpenAI(api_key=openai_api_key)


def initialise_context():
    return [
        {
            "role": "system",
            "content": ai_context,
        }
    ]


def add_user_message(context, message):
    context.append({"role": "user", "content": message})
    context.append({"role": "system", "content": reminder})


def get_gpt4_response(context):
    response = client.chat.completions.create(model="gpt-4o", messages=context)
    return response.choices[0].message.content


def summarise_reviews(reviews):
    print("Sending reviews to AI API.")
    context = initialise_context()
    reviews_text = str(reviews)
    add_user_message(
        context, f"Summarise the following restaurant reviews: {reviews_text}"
    )
    summary = get_gpt4_response(context)
    # Split the response into sections based on the * delimiter in the AI response
    sections = ["Food", "Service", "Atmosphere", "Price", "Trend", "Summary"]
    response_sections = {section: "" for section in sections}

    parts = summary.split("*")
    del parts[0]
    for part in parts:
        for section in sections:
            if part.startswith(f"{section}:"):
                # Need to strip out the heading text here
                response_sections[section] = part[len(section) + 1 :].strip()
                break
    return response_sections
