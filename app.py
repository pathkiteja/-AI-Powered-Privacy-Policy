import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
import re

# Ensure the folder for saved policies exists
if not os.path.exists("saved_policies"):
    os.makedirs("saved_policies")

# Custom headers to avoid bot detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Load AI NLP model (optimized for GPU if available)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2", device=0 if torch.cuda.is_available() else -1)

# Load Sentence-BERT model for better question matching
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

# Privacy Risk Score Algorithm
PRIVACY_SCORE_RULES = {
    "data encryption": 10,
    "GDPR compliance": 10,
    "allows data deletion": 10,
    "no third-party sharing": 15,
    "clear opt-out option": 10,
    "sells data to third parties": -15,
    "collects location": -10,
    "tracks browsing": -10,
    "stores data indefinitely": -15,
    "no mention of user data protection": -10,
    "no opt-out for data collection": -10,
    "uses data for AI training": -15,
    "no transparency on data storage": -5,
}

# Predefined Questions
MAJOR_QUESTIONS = [
    "Does this website share my personal data with third parties?",
    "What types of data does this website collect?",
    "How long does the website store my personal information?",
    "If I delete my account, will my data be removed or stored?"
]

SUGGESTED_QUESTIONS = [
    "Does this website use cookies to track my data?",
    "Can this website sell my data to advertisers?",
    "Does this website track my location?",
    "Is my data stored securely?",
    "Can I request to delete all my personal data?",
    "Does this website share my payment details with others?"
]

ALL_QUESTIONS = MAJOR_QUESTIONS + SUGGESTED_QUESTIONS
predefined_embeddings = sentence_model.encode(ALL_QUESTIONS)

def get_privacy_policy_url(website_url):
    """Finds the privacy policy page URL from a website."""
    try:
        print("🔍 Checking website for a privacy policy link...")
        response = requests.get(website_url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a', href=True):
            if 'privacy' in link.text.lower() or 'privacy' in link['href'].lower():
                policy_url = link['href']
                if policy_url.startswith('/'):
                    return website_url.rstrip('/') + policy_url
                return policy_url
        
        print("❌ Privacy policy page not found.")
        return None

    except Exception as e:
        print("❌ Error:", e)
        return None

def extract_privacy_policy_text(policy_url, website_name):
    """Scrapes the privacy policy page and saves it inside the folder."""
    try:
        print("📄 Extracting privacy policy text...")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(policy_url)
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, 'html.parser')
        paragraphs = [p.text.strip() for p in soup.find_all('p')]
        policy_text = "\n".join(paragraphs)

        # Clean text: remove extra spaces, formatting issues, and legal disclaimers
        policy_text = re.sub(r'\n+', '\n', policy_text).strip()

        # Save the policy inside the folder
        filename = f"saved_policies/{website_name}_privacy_policy.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(policy_text)

        print(f"✅ Privacy policy saved at: {filename}")
        return policy_text, filename
    except Exception as e:
        print("❌ Error extracting privacy policy text:", e)
        return None, None

def calculate_privacy_score(policy_text):
    """Analyzes privacy policy text and assigns a privacy risk score."""
    score = 50  # Start with a neutral score

    for keyword, points in PRIVACY_SCORE_RULES.items():
        if keyword in policy_text.lower():
            score += points

    score = max(0, min(score, 100))
    return score

def find_best_answer(question, policy_text):
    """Finds the best answer by analyzing multiple sections of the privacy policy."""
    policy_sections = policy_text.split("\n\n")  # Splitting into sections

    # Remove empty sections and very short lines
    policy_sections = [section.strip() for section in policy_sections if len(section.strip()) > 10]

    # Encode user question
    user_embedding = sentence_model.encode([question])

    # Encode each section of the policy
    section_embeddings = sentence_model.encode(policy_sections)

    # Find best matching sections (Top 3 Matches)
    similarity_scores = cosine_similarity(user_embedding, section_embeddings)[0]
    best_section_indices = np.argsort(similarity_scores)[-3:]  # Top 3 matches

    # Merge Top 3 Relevant Sections
    best_sections = "\n".join([policy_sections[i] for i in best_section_indices])

    # Use AI to generate answer based on the merged sections
    answer = qa_pipeline(question=question, context=best_sections)

    return answer['answer']

def main():
    website_url = input("🔗 Enter website URL: ").strip()
    website_name = website_url.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]

    policy_url = get_privacy_policy_url(website_url)
    if not policy_url:
        return

    policy_text, filename = extract_privacy_policy_text(policy_url, website_name)
    if not policy_text:
        return

    print("\n🤖 AI is analyzing the privacy policy...\n")
    for i, question in enumerate(MAJOR_QUESTIONS, start=1):
        answer = find_best_answer(question, policy_text)
        print(f"❓ {i}. {question}")
        print(f"✅ AI Answer: {answer}\n")

    # Calculate Privacy Risk Score
    score = calculate_privacy_score(policy_text)
    print(f"\n🔹 **Privacy Risk Score for {website_name}: {score}/100**")

    while True:
        user_question = input("\n❓ Ask any question (or type 'exit' to quit): ")
        if user_question.lower() == "exit":
            break

        print(f"\n🤖 AI Answer: {find_best_answer(user_question, policy_text)}\n")

if __name__ == "__main__":
    main()
