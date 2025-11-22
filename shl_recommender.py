"""
SHL Assessment Recommendation Engine
Author: Arun Ghatage

Description:
    A rule-based recommendation engine that suggests SHL-style assessments
    based on job role, seniority level, and use case (hiring screening, development,
    talent review). The engine scores and ranks assessments based on matching criteria
    including job role keywords, seniority alignment, use case relevance, and category priority.
"""

import re

# ---------- SHL Product Catalogue ----------
ASSESSMENTS = [
    {
        "id": "verify_g_plus",
        "name": "SHL Verify G+ (General Ability)",
        "category": "cognitive",
        "measures": ["numerical_reasoning", "deductive_reasoning", "inductive_reasoning"],
        "best_for_roles": ["graduates", "analyst", "engineer", "consultant"],
        "level": ["entry", "mid"],
        "use_cases": ["hiring_screening"],
        "duration_min": 36,
        "description": "General ability test measuring problem solving and reasoning across numbers, logic, and patterns."
    },
    {
        "id": "verify_numerical",
        "name": "SHL Verify Numerical Reasoning",
        "category": "cognitive",
        "measures": ["numerical_reasoning"],
        "best_for_roles": ["finance", "analyst", "engineer", "operations"],
        "level": ["entry", "mid"],
        "use_cases": ["hiring_screening"],
        "duration_min": 25,
        "description": "Assesses ability to interpret charts, tables, and perform calculations for job-related decisions."
    },
    {
        "id": "verify_deductive",
        "name": "SHL Verify Deductive Reasoning",
        "category": "cognitive",
        "measures": ["deductive_reasoning"],
        "best_for_roles": ["analyst", "consultant", "manager"],
        "level": ["entry", "mid", "senior"],
        "use_cases": ["hiring_screening"],
        "duration_min": 25,
        "description": "Assesses logical reasoning and ability to draw conclusions from given information."
    },
    {
        "id": "opq32",
        "name": "SHL Occupational Personality Questionnaire (OPQ32)",
        "category": "personality",
        "measures": ["work_style", "interpersonal_style", "thinking_style"],
        "best_for_roles": ["graduates", "manager", "leader", "sales", "engineer"],
        "level": ["entry", "mid", "senior", "leadership"],
        "use_cases": ["hiring_screening", "development", "talent_review"],
        "duration_min": 30,
        "description": "Personality questionnaire providing insight into work preferences and fit to role requirements."
    },
    {
        "id": "motivation_questionnaire",
        "name": "SHL Motivation Questionnaire (MQ)",
        "category": "motivation",
        "measures": ["motivation"],
        "best_for_roles": ["manager", "leader", "sales"],
        "level": ["mid", "senior", "leadership"],
        "use_cases": ["development", "talent_review"],
        "duration_min": 20,
        "description": "Profiles what drives and energizes an individual across multiple motivation dimensions."
    },
    {
        "id": "behavioral_sjt_graduate",
        "name": "Graduate Situational Judgement Test (SJT)",
        "category": "behavioral",
        "measures": ["behavioral_fit"],
        "best_for_roles": ["graduates"],
        "level": ["entry"],
        "use_cases": ["hiring_screening"],
        "duration_min": 25,
        "description": "Scenario-based test to assess behavioral fit for graduate and early-career roles."
    },
    {
        "id": "call_center_sjt",
        "name": "Customer Service / Call Center SJT",
        "category": "behavioral",
        "measures": ["customer_focus", "stress_tolerance"],
        "best_for_roles": ["customer_service", "support", "contact_center"],
        "level": ["entry", "mid"],
        "use_cases": ["hiring_screening"],
        "duration_min": 20,
        "description": "Measures situational judgment in customer-facing service environments."
    },
    {
        "id": "sales_simulation",
        "name": "Sales Skills Simulation",
        "category": "skills_simulation",
        "measures": ["sales_skills", "influence", "closing"],
        "best_for_roles": ["sales", "business_development", "account_manager"],
        "level": ["mid", "senior"],
        "use_cases": ["hiring_screening", "development"],
        "duration_min": 45,
        "description": "Role-play style simulation to assess practical sales and influencing capability."
    },
    {
        "id": "leadership_assessment",
        "name": "Leadership Potential Assessment",
        "category": "cognitive_personality_combo",
        "measures": ["strategic_thinking", "leadership_potential"],
        "best_for_roles": ["manager", "leader"],
        "level": ["senior", "leadership"],
        "use_cases": ["hiring_screening", "talent_review"],
        "duration_min": 60,
        "description": "Integrated assessment combining reasoning and personality indicators for leadership potential."
    },
]

# ---------- Helper Functions ----------
def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def infer_role_keywords(job_title: str):
    tokens = normalize(job_title).split()
    keywords = set()
    if "graduate" in tokens or "fresher" in tokens:
        keywords.add("graduates")
    if "engineer" in tokens or "developer" in tokens or "software" in tokens:
        keywords.add("engineer")
    if "analyst" in tokens:
        keywords.add("analyst")
    if "manager" in tokens:
        keywords.add("manager")
    if "sales" in tokens:
        keywords.add("sales")
    if "leader" in tokens or "director" in tokens or "head" in tokens:
        keywords.add("leader")
    return keywords

# ---------- Recommendation Scoring Engine ----------
def category_bonus(category, use_case):
    if use_case == "hiring_screening" and category in ["cognitive", "behavioral", "skills_simulation"]:
        return 2
    if use_case in ["development", "talent_review"] and category in ["personality", "motivation", "cognitive_personality_combo"]:
        return 2
    return 0

def score_assessment(assessment, job_title, seniority, use_case):
    score = 0
    keywords = infer_role_keywords(job_title)

    if seniority in assessment["level"]:
        score += 2

    if keywords & set(assessment["best_for_roles"]):
        score += 3

    if use_case in assessment["use_cases"]:
        score += 3

    score += category_bonus(assessment["category"], use_case)
    return score

def recommend_assessments(job_title, seniority, use_case, top_n=5):
    scored = [(score_assessment(a, job_title, seniority, use_case), a) for a in ASSESSMENTS]
    scored = [x for x in scored if x[0] > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_n]

# ---------- Output Display Function ----------
def print_results(job_title, seniority, use_case, results):
    print("\n==========================================")
    print("ASSESSMENT RECOMMENDATIONS")
    print("==========================================")
    print(f"Job Title : {job_title}")
    print(f"Seniority : {seniority}")
    print(f"Use Case  : {use_case}")
    print("------------------------------------------\n")

    if not results:
        print("No matching assessments found.\n")
        return

    for rank, (score, a) in enumerate(results, start=1):
        print(f"{rank}. {a['name']} (score: {score})")
        print(f"   Category     : {a['category']}")
        print(f"   Best for     : {', '.join(a['best_for_roles'])}")
        print(f"   Levels       : {', '.join(a['level'])}")
        print(f"   Use cases    : {', '.join(a['use_cases'])}")
        print(f"   Duration     : {a['duration_min']} minutes")
        print(f"   Description  : {a['description']}\n")

# ---------- Command Line Interaction ----------
if __name__ == "__main__":
    print("=== SHL Assessment Recommendation Engine ===")

    job_title = input("Enter job title (e.g., 'Graduate Software Engineer'): ").strip()

    valid_seniority = ["entry", "mid", "senior", "leadership"]
    seniority = input("Seniority [entry/mid/senior/leadership]: ").strip().lower()
    while seniority not in valid_seniority:
        print("❌ Invalid input! Try again.")
        seniority = input("Seniority [entry/mid/senior/leadership]: ").strip().lower()

    valid_use_cases = ["hiring_screening", "development", "talent_review"]
    use_case = input("Use case [hiring_screening/development/talent_review]: ").strip().lower()
    while use_case not in valid_use_cases:
        print("❌ Invalid input! Try again.")
        use_case = input("Use case [hiring_screening/development/talent_review]: ").strip().lower()

    results = recommend_assessments(job_title, seniority, use_case)
    print_results(job_title, seniority, use_case, results)