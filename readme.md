🚀 AI-Powered Privacy Policy Analyzer

📌 Overview
This AI-powered tool automatically extracts, analyzes, and evaluates privacy policies from any website.
It identifies risks, provides answers to privacy-related questions, and assigns a Privacy Risk Score based on various security factors.

📖 Table of Contents
What is This Project?
Why Was This Project Built?
How Does It Work?
Key Features
Installation
How to Run
How It Works - Code Explanation
Future Improvements
Contributing
License
📌 What is This Project?
This is a Privacy Policy Analyzer that:

Extracts a website’s privacy policy.
Answers privacy-related questions using AI.
Scores the website’s privacy risk (0-100).
Saves extracted policies for future analysis.
It helps users understand what data a website collects, shares, and how it complies with privacy laws like GDPR, CCPA, and more.

❓ Why Was This Project Built?
🔹 Problem
Privacy policies are long, complex, and full of legal jargon.
Users don’t read them and unknowingly accept risky terms.
Websites often change policies without user awareness.
🔹 Solution
This AI tool automates privacy policy analysis by:

Extracting only the relevant sections from policies.
Simplifying privacy risks with a clear risk score.
Answering any privacy-related question from the policy.
Detecting compliance issues with privacy laws.
🛠️ How Does It Work?
Step 1: Extract Privacy Policy
🔹 The user enters a website URL.
🔹 The AI searches for the privacy policy page and extracts the content.
🔹 The policy is saved locally in a folder for future analysis.

Step 2: Answer Key Privacy Questions
🔹 AI automatically answers 4 major privacy questions:

Does this website share my data with third parties?
What types of data does this website collect?
How long is my data stored?
What happens if I delete my account?
Step 3: Calculate Privacy Risk Score
🔹 AI scans the policy for privacy violations and assigns a score (0-100) based on:

Data sharing, storage, encryption, opt-out options, and AI data use.
Higher score = Better privacy, Lower score = Higher risk.
Step 4: User Can Ask Any Question
🔹 Users can type any question, and the AI finds the best-matching section from the policy and answers.

🎯 Key Features
✅ Extracts privacy policies from any website
✅ Automatically answers 4 major privacy-related questions
✅ Suggests 6 additional privacy-related questions
✅ Calculates a Privacy Risk Score (0-100) based on data practices
✅ Saves extracted policies inside a folder for future use
✅ AI selects the most relevant policy sections before answering
✅ Handles errors and missing data properly

🛠️ Installation
🔹 Prerequisites
Ensure you have Python 3.7+ installed.

🔹 Install Required Dependencies
Run the following command:

bash
Copy
Edit
pip install requests beautifulsoup4 selenium webdriver-manager transformers torch sentence-transformers scikit-learn
🚀 How to Run
1️⃣ Run the Script

bash
Copy
Edit
python app.py
2️⃣ Enter a Website URL

mathematica
Copy
Edit
🔗 Enter website URL: https://www.netflix.com
3️⃣ AI Extracts the Privacy Policy

bash
Copy
Edit
✅ Privacy policy saved at: saved_policies/netflix_privacy_policy.txt
4️⃣ AI Answers Major Privacy Questions

kotlin
Copy
Edit
❓ Does this website share my personal data with third parties?
✅ AI Answer: Yes, Netflix may share personal data with advertising partners and third parties.

❓ What types of data does this website collect?
✅ AI Answer: Netflix collects user location, payment data, and watch history.
5️⃣ Privacy Risk Score is Assigned

rust
Copy
Edit
🔹 Privacy Risk Score for netflix.com: 60/100 (Moderate Risk)
6️⃣ Ask Any Privacy Question

kotlin
Copy
Edit
❓ Can this website sell my data to advertisers?
✅ AI Answer: No, the policy states that Netflix does not sell personal data.
📝 How It Works - Code Explanation
🔹 1. Extract Privacy Policy
The script scrapes the privacy policy using BeautifulSoup and Selenium:

python
Copy
Edit
def extract_privacy_policy_text(policy_url, website_name):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(policy_url)
    page_source = driver.page_source
    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    paragraphs = [p.text.strip() for p in soup.find_all('p')]
    policy_text = "\n".join(paragraphs)

    filename = f"saved_policies/{website_name}_privacy_policy.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(policy_text)

    return policy_text, filename
🔹 2. Calculate Privacy Risk Score
The AI assigns points based on privacy violations:

python
Copy
Edit
PRIVACY_SCORE_RULES = {
    "data encryption": 10,
    "GDPR compliance": 10,
    "sells data to third parties": -15,
    "collects location": -10,
    "stores data indefinitely": -15,
}

def calculate_privacy_score(policy_text):
    score = 50  # Neutral score
    for keyword, points in PRIVACY_SCORE_RULES.items():
        if keyword in policy_text.lower():
            score += points
    return max(0, min(score, 100))
🔹 3. Answer Any Privacy Question
The AI selects the most relevant policy sections before answering:

python
Copy
Edit
def find_best_answer(question, policy_text):
    policy_sections = policy_text.split("\n\n") 
    policy_sections = [section.strip() for section in policy_sections if len(section.strip()) > 10]

    user_embedding = sentence_model.encode([question])
    section_embeddings = sentence_model.encode(policy_sections)
    similarity_scores = cosine_similarity(user_embedding, section_embeddings)[0]
    best_section_indices = np.argsort(similarity_scores)[-3:]

    best_sections = "\n".join([policy_sections[i] for i in best_section_indices])
    answer = qa_pipeline(question=question, context=best_sections)

    return answer['answer']
🌍 Future Improvements
🔹 Deploy as a Web App (Flask/Streamlit)
🔹 Make it a Browser Extension
🔹 Track Privacy Policy Changes & Alert Users
🔹 Detect Compliance Issues (GDPR, CCPA violations)
🔹 Expand to Multiple Languages

💡 Contributing
Feel free to submit pull requests for improvements or report any issues.