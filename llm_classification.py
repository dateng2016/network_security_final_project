import json
import openai
import time

openai.api_key = "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"
CLASS_CHOICES = {'Marketing', 'Personalization', 'Functional', 'Analytics', 'Security'}

def classify_cookie(cookie):
    prompt = (
        f"Given this cookie's metadata, classify it into one of the categories: "
        f"{', '.join(CLASS_CHOICES)}.\n\n"
        f"Cookie:\n{json.dumps(cookie, indent=2)}\n\n"
        f"Respond with just one word from the list."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        classification = response.choices[0].message.content.strip()
        if classification in CLASS_CHOICES:
            return classification
        else:
            print(f"[Warning] Unexpected classification: {classification}")
            return None
    except Exception as e:
        print(f"[Error] API call failed: {e}")
        return None

def process_file(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    for domain, cookies in data.items():
        if not isinstance(cookies, list):
            continue
        for cookie in cookies:
            if cookie.get("classification") is None:
                print(f"[Info] Classifying cookie: {cookie.get('name')}")
                new_class = classify_cookie(cookie)
                if new_class:
                    cookie["classification"] = new_class

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    process_file("website_cookies.json", "website_output.json")
    process_file("mobile_cookies.json", "mobile_output.json")
