import google.generativeai as genai
import json

def init_client():
    genai.configure(api_key="AIzaSyDK4RnkupX3VOUSXZOJDVZw1IQyTZHgCNw")
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model


def parse_genai_response(response):
    # Assuming response is a GenerateContentResponse object
    if response.done:
        # Access the result field
        result = response.result

        # Access the 'candidates' list inside the result
        candidates = result.candidates

        for candidate in candidates:
            # Access the text content within parts
            content = candidate.content.parts[0].text
            print("Raw Content from AI:\n", content)

            try:
                # Extract JSON data within markdown block
                json_start = content.find("```json") + len("```json")
                json_end = content.find("```", json_start)
                json_data = content[json_start:json_end].strip()

                # Parse the JSON data
                reviews = json.loads(json_data)

                print("\nParsed Reviews:")
                for review in reviews:
                    print(f"Title: {review['title']}")
                    print(f"Body: {review['body']}")
                    print(f"Rating: {review['rating']}")
                    print(f"Reviewer: {review['reviewer']}")
                    print()

                # Extract the next page URL
                next_page_marker = "**Next Page URL:**"
                if next_page_marker in content:
                    next_page_url = content.split(next_page_marker)[-1].strip()
                    print(f"Next Page URL: {next_page_url}")

            except (json.JSONDecodeError, IndexError) as e:
                print(f"Error parsing JSON data: {e}")


def process(page_source : str):
    model = init_client()

    content = f"""
        You are a web scraper tasked with extracting product reviews from the given page source.
        Return the reviews in the following format:
        - title
        - body
        - rating
        - reviewer
        Output should be a JSON array of objects with these keys. If there is pagination (e.g., "see more reviews" or "next page"), or there could be href assosiated with the 
        button to view next or more reviews
        also return the next page URL along with the reviews.
        The page source is provided below:
        {page_source}

    """
    response = model.generate_content(contents=content)

    print(response.text)
    return response.text
