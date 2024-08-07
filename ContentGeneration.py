import pathlib
from env import api_key
import re
import textwrap
import os
import google.generativeai as genai
from markdown import Markdown
import markdown
from typing import Dict
from bs4 import BeautifulSoup


def to_markdown(text):
    text = text.replace('•', '  *')
    indented_text = textwrap.indent(text, '> ', predicate=lambda _: True)
    return markdown.markdown(indented_text)

def html_to_plain_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator='\n')
    formatted_text = textwrap.fill(text, width=80)
    return formatted_text

def extract_title_and_content(response_text):
    # Use regex to extract the title and content
    lines = response_text.split('\n')
    title_match = re.search(r'^##\s*(.+)$', lines[1]) if len(lines) > 1 else None
    title = title_match.group(1) if title_match else "No Title Found"
    content = '\n'.join(lines[2:]).strip() if len(lines) > 2 else ""
    return title, content


genai.configure(api_key=api_key)

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

def risk_assessment_questions():
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Generate a 5-question quiz to assess a person's risk tolerance for investment. Assume the person s financially illiterate and make the questions simple and easy to understand.")
    return response.text.lstrip().rstrip()

def risk_level_assignment(text, responses):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Assess the risk level of a person based on their responses to the risk tolerance quiz below: \n\n" + text + "\n\n" + responses + ". Return a single digit as your response, 1 for High, 2 for Medium, and 3 for Low. Write no more or no less than the single digit.")
    
    if len(response.text) != 1:
        risk = int(re.sub(r'\D', '', response.text))
    else:
        risk = int(response.text)

    return risk

def investment_option_generation(risk_level):
    tolerance = {1: 'High', 2: 'Medium', 3: 'Low'}
    risk_tolerance = tolerance.get(risk_level, 'Medium')  # Default to 'Medium' if risk_level is invalid

    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(
            f"Generate a list of investment options for users with {risk_tolerance.lower()} investment risk tolerance. "
            f"Include a brief description of each investment option and the risk level associated with it. Return exactly 5. Ensure the responses are relevant."
            f"Structure it as follows: \n\n1. Investment Name: Description: Risk Level: \n2. Investment Name: Description: Risk Level: \n3. Investment Name: Description: Risk Level: \n4. Investment Name: Description: Risk Level: \n5. Investment Name: Description: Risk Level:"
        )
    except Exception as e:
        print(f"Error generating content: {e}")
        return {}

    options = {}
    pattern = re.compile(r'(\d+)\.\s*(.*?)\s*(?=\d+\.|$)', re.DOTALL)
    matches = pattern.findall(response.text)

    for match in matches:
        index, investment_option = match
        index = int(index)
        investment_option = re.sub(r'[\n\t\r#*]', ' ', investment_option).strip()
        investment_option_list = {}
        investment_option_list["InvestmentName"] = investment_option[0:investment_option.find(':')].strip()
        investment_option_list["Description"] = investment_option[investment_option.find(':')+1:investment_option.find('Risk Level')].strip()
        investment_option_list["Risk Level"] = investment_option[investment_option.find('Risk Level'):].strip().replace('Risk Level:', '').strip()
        options[index] = investment_option_list


    return options


def main():
    # Example usage
    risk_tolerances = ["Low", "Medium", "High"]
    # content = generate_content(risk_tolerances)

    # # Print the generated content
    # for risk_tolerance, categories in content.items():
    #     print(f"Risk Tolerance: {risk_tolerance}")
    #     for category, types in categories.items():
    #         for content_type, items in types.items():
    #             print(f"{category} - {content_type}")
    #             for item in items:
    #                 print(f"- Title: {item['Title']}")
    #                 print(f"  ContentType: {item['ContentType']}")
    #                 print(f"  Content: {item['Content']}")
    #                 print(f"  Topic: {item['Topic']}")
    #                 print(f"  risk_type: {item['risk_type']}\n")

    a = risk_assessment_questions()
    # print(a)
    new_arr = ['a', 'b', 'c', 'a', 'a']
    responses = '\n'.join(new_arr)
    b = risk_level_assignment(a, responses)
    print(b)
    c = investment_option_generation(b)
    print(c)



if __name__ == "__main__":
    main()