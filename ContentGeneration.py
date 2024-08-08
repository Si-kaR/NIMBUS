"""Contains all methods concerning interaction with the generative AI"""

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
import json

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
    response = model.generate_content("Generate a 5-question quiz to assess a person's risk tolerance for investment. Assume the person s financially illiterate and make the questions simple and easy to understand."
                                      f"Ensure the responses are relevant. Do not include any information apart rom what is requested. Write everything in one line. Don't attempt to section the responses into multiple lines."
                                      f"Structure it as follows: \n\n Question Number. Question: a) Option 1 b) Option 2 c) Option C..."

                                      )

    answer = response.text.lstrip().rstrip()

    quizzes = {}
    # Updated regex pattern to match the new format with three options
    pattern = re.compile(r'(\d+)\.\s+(.*?)\s+a\)\s*(.*?)\s+b\)\s*(.*?)\s+c\)\s*(.*?)\s*(?=\d+\.|$)', re.DOTALL)
    matches = pattern.findall(answer)
    
    for match in matches:
        index, question, option_a, option_b, option_c = match
        index = int(index)
        quizzes[index] = {
            "Question": question.strip(),
            "Options": {
                "a": option_a.strip(),
                "b": option_b.strip(),
                "c": option_c.strip()
            }
        }

    # Return quizzes as a JSON object
    return json.dumps(quizzes, indent=4)


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
        investment_option_list["Risk Level"] = risk_level 
        options[index] = investment_option_list


    return json.dumps(options, indent=4)


def generate_diversified_portfolio(risk_level):
    tolerance = {1: 'High', 2: 'Medium', 3: 'Low'}
    risk_tolerance = tolerance.get(risk_level, 'Medium')  # Default to 'Medium' if risk_level is invalid

    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(
            f"Generate a diversified portfolio for users with {risk_tolerance.lower()} investment risk tolerance. "
            f"Include various asset classes like stocks, bonds, real estate, etc. Provide a brief description and the percentage allocation for each asset class. "
            f"Structure it as follows: \n\n1. Asset Class: Description: Allocation: \n2. Asset Class: Description: Allocation: \n3. Asset Class: Description: Allocation: \n4. Asset Class: Description: Allocation: \n5. Asset Class: Description: Allocation:"
            f"Ensure the responses are relevant. Do not include any information apart rom what is requested."
        )
    except Exception as e:
        print(f"Error generating content: {e}")
        return {}

    portfolio = {}
    pattern = re.compile(r'(\d+)\.\s*(.*?)\s*(?=\d+\.|$)', re.DOTALL)
    matches = pattern.findall(response.text)

    for match in matches:
        index, asset_class = match
        index = int(index)
        asset_class = re.sub(r'[\n\t\r#*]', ' ', asset_class).strip()
        asset_class_list = {}
        asset_class_list["AssetClass"] = asset_class[0:asset_class.find(':')].strip()
        asset_class_list["Description"] = asset_class[asset_class.find(':')+1:asset_class.find('Allocation')].strip()
        asset_class_list["Allocation"] = asset_class[asset_class.find('Allocation'):].strip().replace('Allocation:', '').strip()
        portfolio[index] = asset_class_list

    return json.dumps(portfolio, indent=4)


def generate_quizzes(risk_level):
    tolerance = {1: 'High', 2: 'Medium', 3: 'Low'}
    risk_tolerance = tolerance.get(risk_level, 'Medium')  # Default to 'Medium' if risk_level is invalid

    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(
            f"Generate a 5-question quiz to assess a person's understanding of financial concepts for users with {risk_tolerance.lower()} investment risk tolerance. "
            f"Each question should have four options (a, b, c, d) and indicate the correct option. "
            f"Structure it as follows: \n\n1. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option: \n2. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option: \n3. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option: \n4. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option: \n5. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option:"
            f"Ensure the responses are relevant. Do not include any information apart from what is requested."
            f"Correct Option should be a single letter (a, b, c, or d). Write everything in one line. Don't attempt to section the responses into multiple lines."
        )
    except Exception as e:
        print(f"Error generating content: {e}")
        return {}
    answer = response.text
    end_pos = answer.find('\n\n')
    first = answer[0:end_pos].lstrip().rstrip()
    # answer = answer[end_pos + 2:]
    end_pos = answer.find('\n\n')
    # print(answer[0:end_pos].lstrip().rstrip())
    # print(first)

    # answer = answer + first



    quizzes = {}
    pattern = re.compile(r'(\d+)\.\s+(.*?)\s+a\)\s*(.*?)\s+b\)\s*(.*?)\s+c\)\s*(.*?)\s+d\)\s*(.*?)\s+Correct Option:\s*(\w)', re.DOTALL)
    matches = pattern.findall(answer)
    # print(matches)
    for match in matches:
        index, question, option_a, option_b, option_c, option_d, correct_option = match
        index = int(index)
        quizzes[index] = {
            "Question": question.strip(),
            "Options": {
                "a": option_a.strip(),
                "b": option_b.strip(),
                "c": option_c.strip(),
                "d": option_d.strip()
            },
            "Correct Option": correct_option.strip()
        }

    return json.dumps(quizzes, indent=4)


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
    print(a)
    new_arr = ['a', 'b', 'c', 'a', 'a']
    responses = '\n'.join(new_arr)
    b = risk_level_assignment(a, responses)
    print(b)
    c = investment_option_generation(b)
    # print(c)

    d = generate_diversified_portfolio(b)
    # print(d)

    e = generate_quizzes(b)
    # print(e)
    # e = json.loads(e)
    # print(e)

    # for index, quiz in e.items():
    #     print(f"{index}. Question: {quiz['Question']}")
    #     print(f"   a) {quiz['Options']['a']}")
    #     print(f"   b) {quiz['Options']['b']}")
    #     print(f"   c) {quiz['Options']['c']}")
    #     print(f"   d) {quiz['Options']['d']}")
    #     print(f"   Correct Option: {quiz['Correct Option']}\n")



if __name__ == "__main__":
    main()