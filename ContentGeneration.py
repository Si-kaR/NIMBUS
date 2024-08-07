import pathlib
import re
import textwrap

import google.generativeai as genai
from markdown import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def extract_title_and_content(response_text):
    # Use regex to extract the title and content
    lines = response_text.split('\n')
    title_match = re.search(r'^##\s*(.+)$', lines[1]) if len(lines) > 1 else None
    title = title_match.group(1) if title_match else "No Title Found"
    content = '\n'.join(lines[2:]).strip() if len(lines) > 2 else ""
    return title, content

genai.configure(api_key='AIzaSyDqUzqUQV-LEl9kIcX9OhFp6j4jeHug_Ow')

def generate_content(risk_tolerances):
    categories = ['PersonalFinance', 'Budgeting', 'Investing']
    content_types = ['Article']
    
    content = {risk_tolerance: {category: {content_type: [] for content_type in content_types} for category in categories} for risk_tolerance in risk_tolerances}
    model = genai.GenerativeModel("gemini-1.5-flash")

    risk_type_mapping = {'Low': 3, 'Medium': 2, 'High': 1}

    for risk_tolerance in risk_tolerances:
        for category in categories:
            for content_type in content_types:
                for _ in range(1):
                    response = model.generate_content(f"Generate a {content_type.lower()} related to {category.lower()} for users with {risk_tolerance.lower()} investment risk tolerance. Make articles conversation-like and educative.")
                    title = response.text[3:response.text.find('\n\n')].strip()
                    content_text = response.text[response.text.find('\n\n')+2:].strip()
                    article = {
                        'Title': title,
                        'ContentType': content_type,
                        'Content': content_text,
                        'Topic': category,
                        'risk_type': risk_type_mapping[risk_tolerance]
                    }
                    content[risk_tolerance][category][content_type].append(article)
    
    return content

def main():
    # Example usage
    risk_tolerances = ["Low", "Medium", "High"]
    content = generate_content(risk_tolerances)

    # Print the generated content
    for risk_tolerance, categories in content.items():
        print(f"Risk Tolerance: {risk_tolerance}")
        for category, types in categories.items():
            for content_type, items in types.items():
                print(f"{category} - {content_type}")
                for item in items:
                    print(f"- Title: {item['Title']}")
                    print(f"  ContentType: {item['ContentType']}")
                    print(f"  Content: {item['Content']}")
                    print(f"  Topic: {item['Topic']}")
                    print(f"  risk_type: {item['risk_type']}\n")

if __name__ == "__main__":
    main()