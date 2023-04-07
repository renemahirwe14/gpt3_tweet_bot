import openai
import requests
import time
import re
import json

# Set up the OpenAI API key
openai.api_key = "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"

print("Starting Twitter Bot...")

while True:
    try:
        # Generate a motivational quote using GPT-3
        prompt = "Generate a unique short tweet in one paragraph, it can be about an inspirational or motivational or  a thought-provoking question or about spirituality or relationships or sex or the future or  just about a touch of humor related to a popular cultural reference to make the tweet more engaging. Remember to avoid new lines and hashtags."
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=64,
            n=1,
            stop=None,
            temperature=0.5,
        )
        quote = response.choices[0].text.strip()

        # Remove any non-text characters from the quote
        clean_quote = re.sub('[^a-zA-Z0-9\s]+', '', quote).replace('\n\n', ' ')

        # Set up the webhook URL for the IFTTT applet
        ifttt_url = "https://maker.ifttt.com/trigger/post_tweet/json/with/key/c1L5fx6vK0cCR0fcaUtgzRY8LMa_GtJZn9Kk67sGA11"

        # Set up the tweet message with the cleaned quote
        tweet_message = clean_quote
        quote_json = json.dumps(tweet_message)
        quote_text = quote_json.replace('{"-": "', '').replace('"}', '')

        # Trigger the IFTTT applet to post the tweet
        response = requests.post(ifttt_url, json={"-": tweet_message})

        if response.status_code == 200:
            print("Tweet request sent to IFTTT. Tweet successfully posted!")
        else:
            print("Error: Failed to post tweet. Response code: ", response.status_code)

        # Wait for an hour before running the script again
        time.sleep(3600)

    except Exception as e:
        print("Error: ", e)
        time.sleep(60)
