"""Contains all methods concerning interaction with the generative AI"""

from env import api_key
import re
import textwrap
import google.generativeai as genai
import markdown
from bs4 import BeautifulSoup
import json
import time
import ModelQuestions


def to_markdown(text):
    text = text.replace("•", "  *")
    indented_text = textwrap.indent(text, "> ", predicate=lambda _: True)
    return markdown.markdown(indented_text)


def html_to_plain_text(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n")
    formatted_text = textwrap.fill(text, width=80)
    return formatted_text


def extract_title_and_content(response_text):
    # Use regex to extract the title and content
    lines = response_text.split("\n")
    title_match = re.search(r"^##\s*(.+)$", lines[1]) if len(lines) > 1 else None
    title = title_match.group(1) if title_match else "No Title Found"
    content = "\n".join(lines[2:]).strip() if len(lines) > 2 else ""
    return title, content


genai.configure(api_key=api_key)


def generate_content(risk_tolerances, max_retries=3, retry_delay=2):
    categories = ["PersonalFinance", "Budgeting", "Investing"]
    content_types = ["Article"]

    content = {
        risk_tolerance: {
            category: {content_type: [] for content_type in content_types}
            for category in categories
        }
        for risk_tolerance in risk_tolerances
    }
    model = genai.GenerativeModel("gemini-1.5-flash")

    risk_type_mapping = {"Low": 3, "Medium": 2, "High": 1}

    for risk_tolerance in risk_tolerances:
        for category in categories:
            for content_type in content_types:
                for _ in range(1):
                    attempt = 0
                    while attempt < max_retries:
                        try:
                            response = model.generate_content(
                                ModelQuestions.risk_tolerance_req.format(
                                    content_type=content_type.lower(),
                                    category=category.lower(),
                                    risk_tolerance=risk_tolerance.lower(),
                                )
                            )
                            answer = response.text.lstrip().rstrip()

                            # Extract title, content, and hint
                            title = answer[3 : answer.find("\n\n")].strip()
                            content_text = answer[answer.find("\n\n") + 2 :].strip()
                            hint_pattern = re.compile(
                                r"Hint:\s*(.*?)\s*(?=\n|$)", re.DOTALL
                            )
                            hint_match = hint_pattern.search(answer)
                            hint = (
                                hint_match.group(1).strip()
                                if hint_match
                                else "No hint provided."
                            )

                            article = {
                                "Title": title,
                                "ContentType": content_type,
                                "Content": content_text,
                                "Topic": category,
                                "risk_type": risk_type_mapping[risk_tolerance],
                                "Hint": hint,
                            }
                            content[risk_tolerance][category][content_type].append(
                                article
                            )
                            break  # Exit the retry loop if successful
                        except Exception as e:
                            print(f"Attempt {attempt + 1} failed: {e}")
                            attempt += 1
                            time.sleep(retry_delay)

    return content


def risk_assessment_questions(max_retries=3, retry_delay=2):
    attempt = 0
    while attempt < max_retries:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                "Generate a 5-question quiz to assess a person's risk tolerance for investment. Assume the person is financially illiterate and make the questions simple and easy to understand. "
                "Ensure the responses are relevant. Do not include any information apart from what is requested. Write everything in one line. Don't attempt to section the responses into multiple lines. "
                "Start with a brief description of what risk tolerance means. Bear in mind that the reader knows absolutely nothing about finance. Structure it as follows: \n\n Description: [Description of risk tolerance] \n\n Question Number. Question: a) Option 1 b) Option 2 c) Option 3"
            )

            answer = response.text.lstrip().rstrip()

            quizzes = {}
            # Updated regex pattern to match the new format with description and three options
            description_pattern = re.compile(
                r"Description:\s*(.*?)\s*(?=\d+\.)", re.DOTALL
            )
            question_pattern = re.compile(
                r"(\d+)\.\s+(.*?)\s+a\)\s*(.*?)\s+b\)\s*(.*?)\s+c\)\s*(.*?)\s*(?=\d+\.|$)",
                re.DOTALL,
            )

            description_match = description_pattern.search(answer)
            description = (
                description_match.group(1).strip()
                if description_match
                else "No description provided."
            )

            quizzes["Description"] = description

            matches = question_pattern.findall(answer)

            for match in matches:
                try:
                    index, question, option_a, option_b, option_c = match
                    index = int(index)
                    quizzes[index] = {
                        "Question": question.strip(),
                        "Options": {
                            "a": option_a.strip(),
                            "b": option_b.strip(),
                            "c": option_c.strip(),
                        },
                    }
                except ValueError as ve:
                    print(f"ValueError encountered: {ve}")
                except Exception as e:
                    print(f"An error occurred while processing a match: {e}")

            # Return quizzes as a JSON object
            return json.dumps(quizzes, indent=4)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(retry_delay)

    # If all attempts fail, return an error message
    return json.dumps(
        {"error": "Failed to generate content after multiple attempts."}, indent=4
    )


def risk_level_assignment(text, responses, max_retries=3, retry_delay=2):
    attempt = 0
    while attempt < max_retries:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                "Assess the risk level of a person based on their responses to the risk tolerance quiz below: \n\n"
                + text
                + "\n\n"
                + responses
                + ". Return a single digit as your response, 1 for High, 2 for Medium, and 3 for Low. Write no more or no less than the single digit. "
                "Also, provide a brief description of what the person's risk tolerance means."
            )

            answer = response.text.lstrip().rstrip()

            # Extract the risk level and description
            risk_pattern = re.compile(r"(\d)")
            description_pattern = re.compile(r"Description:\s*(.*?)$", re.DOTALL)

            risk_match = risk_pattern.search(answer)
            description_match = description_pattern.search(answer)

            risk = (
                int(risk_match.group(1)) if risk_match else 2
            )  # Default to 'Medium' if no match
            description = (
                description_match.group(1).strip()
                if description_match
                else "No description provided."
            )

            risk_mapping = {1: "High", 2: "Medium", 3: "Low"}

            risk_dict = {
                "RiskLevel": risk_mapping.get(
                    risk, "Medium"
                ),  # Default to 'Medium' if risk_level is invalid
                "RiskNo": risk,
                "Description": description,
            }

            return json.dumps(risk_dict, indent=4)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(retry_delay)

    # If all attempts fail, return an error message
    return json.dumps(
        {"error": "Failed to generate content after multiple attempts."}, indent=4
    )


def investment_option_generation(risk_level, max_retries=3, retry_delay=2):
    tolerance = {1: "High", 2: "Medium", 3: "Low"}
    risk_tolerance = tolerance.get(
        risk_level, "Medium"
    )  # Default to 'Medium' if risk_level is invalid

    attempt = 0
    while attempt < max_retries:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"Generate a list of investment options for users with {risk_tolerance.lower()} investment risk tolerance. "
                f"Include a brief description of each investment option and the risk level associated with it. Return exactly 5. Ensure the responses are relevant."
                f"Start with a brief description of what risk tolerance means. Structure it as follows: \n\n Description: [Description of risk tolerance] \n\n1. Investment Name, Description, Risk Level \n2. Investment Name: Description: Risk Level: \n3. Investment Name: Description: Risk Level: \n4. Investment Name: Description: Risk Level: \n5. Investment Name: Description: Risk Level:"
            )

            answer = response.text.lstrip().rstrip()

            options = {}
            # Updated regex pattern to match the new format with description and investment options
            description_pattern = re.compile(
                r"Description:\s*(.*?)\s*(?=\d+\.)", re.DOTALL
            )
            option_pattern = re.compile(r"(\d+)\.\s*(.*?)\s*(?=\d+\.|$)", re.DOTALL)

            description_match = description_pattern.search(answer)
            description = (
                description_match.group(1).strip()
                if description_match
                else "No description provided."
            )

            options["Description"] = description

            matches = option_pattern.findall(answer)

            for match in matches:
                try:
                    index, investment_option = match
                    index = int(index)
                    investment_option = re.sub(
                        r"[\n\t\r#*]", " ", investment_option
                    ).strip()
                    investment_option_list = {}
                    investment_option_list["InvestmentName"] = investment_option[
                        0 : investment_option.find(":")
                    ].strip()
                    investment_option_list["Description"] = investment_option[
                        investment_option.find(":")
                        + 1 : investment_option.find("Risk Level")
                    ].strip()
                    investment_option_list["Risk Level"] = (
                        investment_option[investment_option.find("Risk Level") :]
                        .strip()
                        .replace("Risk Level:", "")
                        .strip()
                    )
                    options[index] = investment_option_list
                except ValueError as ve:
                    print(f"ValueError encountered: {ve}")
                except Exception as e:
                    print(f"An error occurred while processing a match: {e}")

            # Return options as a JSON object
            return json.dumps(options, indent=4)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(retry_delay)

    # If all attempts fail, return an error message
    return json.dumps(
        {"error": "Failed to generate content after multiple attempts."}, indent=4
    )


def generate_diversified_portfolio(risk_level, max_retries=3, retry_delay=2):
    tolerance = {1: "High", 2: "Medium", 3: "Low"}
    risk_tolerance = tolerance.get(
        risk_level, "Medium"
    )  # Default to 'Medium' if risk_level is invalid

    attempt = 0
    while attempt < max_retries:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"Generate a diversified portfolio for users with {risk_tolerance.lower()} investment risk tolerance. "
                f"Include various asset classes like stocks, bonds, real estate, etc. Provide a brief description and the percentage allocation for each asset class. "
                f"Start with a brief description of what risk tolerance means, what a portfolio is, and why diversification of a portfolio is important and what it means. Structure it as follows: \n\n Description: [Description of risk tolerance] \n\n1. Asset Class: Description: Allocation: \n2. Asset Class: Description: Allocation: \n3. Asset Class: Description: Allocation: \n4. Asset Class: Description: Allocation: \n5. Asset Class: Description: Allocation:"
                f"Ensure the responses are relevant. Do not include any information apart from what is requested."
            )

            answer = response.text.lstrip().rstrip()

            portfolio = {}
            # Updated regex pattern to match the new format with description and asset classes
            description_pattern = re.compile(
                r"Description:\s*(.*?)\s*(?=\d+\.)", re.DOTALL
            )
            asset_pattern = re.compile(r"(\d+)\.\s*(.*?)\s*(?=\d+\.|$)", re.DOTALL)

            description_match = description_pattern.search(answer)
            description = (
                description_match.group(1).strip()
                if description_match
                else "No description provided."
            )

            portfolio["Description"] = description

            matches = asset_pattern.findall(answer)

            for match in matches:
                try:
                    index, asset_class = match
                    index = int(index)
                    asset_class = re.sub(r"[\n\t\r#*]", " ", asset_class).strip()
                    asset_class_list = {}
                    asset_class_list["AssetClass"] = asset_class[
                        0 : asset_class.find(":")
                    ].strip()
                    asset_class_list["Description"] = asset_class[
                        asset_class.find(":") + 1 : asset_class.find("Allocation")
                    ].strip()
                    asset_class_list["Allocation"] = (
                        asset_class[asset_class.find("Allocation") :]
                        .strip()
                        .replace("Allocation:", "")
                        .strip()
                    )
                    portfolio[index] = asset_class_list
                except ValueError as ve:
                    print(f"ValueError encountered: {ve}")
                except Exception as e:
                    print(f"An error occurred while processing a match: {e}")

            # Return portfolio as a JSON object
            return json.dumps(portfolio, indent=4)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(retry_delay)

    # If all attempts fail, return an error message
    return json.dumps(
        {"error": "Failed to generate content after multiple attempts."}, indent=4
    )


def generate_quizzes(risk_level, max_retries=3, retry_delay=2):
    tolerance = {1: "High", 2: "Medium", 3: "Low"}
    risk_tolerance = tolerance.get(
        risk_level, "Medium"
    )  # Default to 'Medium' if risk_level is invalid

    attempt = 0
    while attempt < max_retries:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"Generate a 5-question quiz to assess a person's understanding of financial concepts for users with {risk_tolerance.lower()} investment risk tolerance. "
                f"Each question should have four options (a, b, c, d), indicate the correct option, and provide a hint that is educative and would help the user get the right answer. "
                f"Structure it as follows: \n\n1. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option: \n   Hint: \n2. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option: \n   Hint: \n3. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option: \n   Hint: \n4. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option: \n   Hint: \n5. Question: \n   a) Option 1 \n   b) Option 2 \n   c) Option 3 \n   d) Option 4 \n   Correct Option: \n   Hint:"
                f"Ensure the responses are relevant. Do not include any information apart from what is requested."
                f"Correct Option should be a single letter (a, b, c, or d). Write everything in one line. Don't attempt to section the responses into multiple lines."
            )
            answer = response.text.lstrip().rstrip()

            quizzes = {}
            pattern = re.compile(
                r"(\d+)\.\s+(.*?)\s+a\)\s*(.*?)\s+b\)\s*(.*?)\s+c\)\s*(.*?)\s+d\)\s*(.*?)\s+Correct Option:\s*(\w)\s+Hint:\s*(.*?)\s*(?=\d+\.|$)",
                re.DOTALL,
            )
            matches = pattern.findall(answer)

            for match in matches:
                (
                    index,
                    question,
                    option_a,
                    option_b,
                    option_c,
                    option_d,
                    correct_option,
                    hint,
                ) = match
                index = int(index)
                quizzes[index] = {
                    "Question": question.strip(),
                    "Options": {
                        "a": option_a.strip(),
                        "b": option_b.strip(),
                        "c": option_c.strip(),
                        "d": option_d.strip(),
                    },
                    "Correct Option": correct_option.strip(),
                    "Hint": hint.strip(),
                }

            return json.dumps(quizzes, indent=4)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(retry_delay)

    # If all attempts fail, return an error message
    return json.dumps(
        {"error": "Failed to generate content after multiple attempts."}, indent=4
    )


def get_term_meaning(term, context=None, max_retries=3, retry_delay=2):
    model = genai.GenerativeModel("gemini-1.5-flash")
    attempt = 0
    while attempt < max_retries:
        try:
            prompt = (
                f"Provide a detailed explanation and breakdown of the term '{term}'. Include its definition, usage, and any relevant examples. "
                f"Ensure the explanation is clear and comprehensive, similar to a dictionary entry. Do not use bullets, headings or paragraphs. Just write it as a single block of text. Limit to 200 words."
            )
            if context:
                prompt = f"Consider that you said this to me last: {context}\n\naddressthis prompt{prompt}"

            response = model.generate_content(prompt)
            answer = response.text.lstrip().rstrip()

            # Extract the explanation and breakdown
            explanation = answer.strip()

            return {"Term": term, "Explanation": explanation}
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(retry_delay)

    # If all attempts fail, return an error message
    return {"error": "Failed to generate content after multiple attempts."}


<<<<<<< HEAD
def return_faqs(word_list, max_retries=3, retry_delay=2):
    model = genai.GenerativeModel("gemini-1.5-flash")
    faqs = {}

    for word in word_list:
        attempt = 0
        while attempt < max_retries:
            try:
                response = model.generate_content(
                    f"Provide a detailed explanation and breakdown of the term '{word}'. Include its definition, usage, and any relevant examples. "
                    f"Ensure the explanation is clear and comprehensive, similar to a dictionary entry."
                    f"Limit to 100 words. Do not use bullets, headings or paragraphs. Just write it as a single block of text. Do not repeat the term in the explanation."
                )
                answer = response.text.lstrip().rstrip()

                # Extract the explanation and breakdown
                explanation = answer.strip()

                faqs[word] = explanation
                break  # Exit the retry loop if successful
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for word '{word}': {e}")
                attempt += 1
                time.sleep(retry_delay)

        if word not in faqs:
            faqs[word] = "Failed to generate content after multiple attempts."

    return json.dumps(faqs, indent=4)



=======
>>>>>>> 98289dc (feat: decluter model questions)
def main():
    # Example usage
    # # risk_tolerances = ["Low"]
    # term = "Compound Interest"
    # answer = get_term_meaning(term)
    # follow_up = "What is the formula for calculating compound interest?"
    # print(json.dumps(get_term_meaning(follow_up, answer["Explanation"]), indent=4))
    # content = generate_content(risk_tolerances)
    # print(content)
    word_list = ["Compound Interest", "Inflation", "Diversification"]
    print(return_faqs(word_list))

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

    # a = risk_assessment_questions()
    # print(a)
    # new_arr = ['a', 'b', 'c', 'a', 'a']
    # responses = '\n'.join(new_arr)
    # b = risk_level_assignment(a, responses)
    # # print(b)
    # c = investment_option_generation(b)
    # # print(c)

    # d = generate_diversified_portfolio(1)
    # print(d)

    # e = generate_quizzes(2)
    # print(e)
    # # e = json.loads(e)
    # # print(e)

    # for index, quiz in e.items():
    #     print(f"{index}. Question: {quiz['Question']}")
    #     print(f"   a) {quiz['Options']['a']}")
    #     print(f"   b) {quiz['Options']['b']}")
    #     print(f"   c) {quiz['Options']['c']}")
    #     print(f"   d) {quiz['Options']['d']}")
    #     print(f"   Correct Option: {quiz['Correct Option']}\n")


if __name__ == "__main__":
    main()
