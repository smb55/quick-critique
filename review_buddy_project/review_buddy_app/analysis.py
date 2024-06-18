from openai import OpenAI
from .creds import openai_api_key

client = OpenAI(api_key=openai_api_key)


def initialise_context():
    return [
        {
            "role": "system",
            "content": "You are an assistant that analyses restaurant reviews and replies concisely and \
            accurately. The text you will be given along with this context is made up of multiple reviews in the \
            form of a Python dictionary that includes various information about the review. Note that the 'reviews' \
            item is the number of reviews the reviewer has made - you might use this to lower the weight of the \
            review in the case of very few reviews (if it appears like it might be either fake or malicious). Focus on \
            identifying common themes in the reviews, both negative and positive, and for the type of meal or type of group \
            and anything else that may be important to someone trying to decide whether to visit the restaurant. Your \
            response should be a concise but detailed summary of the sentiment and common themes in the reviews.",
        }
    ]


def add_user_message(context, message):
    context.append({"role": "user", "content": message})


def get_gpt4_response(context):
    response = client.chat.completions.create(model="gpt-4", messages=context)
    return response.choices[0].message.content


def summarise_reviews(reviews):
    context = initialise_context()
    reviews_text = str(reviews)
    add_user_message(
        context, f"Summarise the following restaurant reviews: {reviews_text}"
    )
    summary = get_gpt4_response(context)
    return summary
