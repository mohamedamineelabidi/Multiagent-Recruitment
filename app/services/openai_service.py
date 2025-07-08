import re
import json
import uuid
from openai import AzureOpenAI

from app.core.config import settings

class OpenAIService:
    """
    A service class to handle all interactions with the Azure OpenAI API.
    """
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_API_BASE,
        )
        self.deployment_name = settings.AZURE_OPENAI_DEPLOYMENT_NAME

    def extract_job_details(self, job_description: str) -> dict:
        """Extracts structured details from a raw job description string."""
        prompt = f"""
        Extract the following details from the job description:

        1. **Job Title**: Extract the **exact job title** from the job description.
        2. **Technical Skills**: Include programming languages, cloud platforms, big data tools, frameworks, and database technologies.
        3. **Soft Skills**: Extract soft skills required. If none are mentioned, infer typical ones based on the job role.
        4. **Industry**: Extract the **most specific industry** that best fits the job description.

        Job Description:
        {job_description}

        Provide the response in the following format:

        **Job Title**: [job title]
        **Technical Skills**: [comma-separated list]
        **Soft Skills**: [comma-separated list]
        **Industry**: [industry]
        """
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400
        )
        response_text = response.choices[0].message.content.strip()

        try:
            job_title = re.search(r"\*\*Job Title\*\*:\s*(.+)", response_text).group(1).strip()
            tech_skills = re.search(r"\*\*Technical Skills\*\*:\s*(.+)", response_text).group(1).strip()
            soft_skills = re.search(r"\*\*Soft Skills\*\*:\s*(.+)", response_text).group(1).strip()
            industry = re.search(r"\*\*Industry\*\*:\s*(.+)", response_text).group(1).strip()
            
            return {
                "title": job_title,
                "tech_skills": [s.strip() for s in tech_skills.split(",")],
                "soft_skills": [s.strip() for s in soft_skills.split(",")],
                "industry": industry
            }
        except AttributeError:
            return {}

    def generate_project_dict(self, job_title: str, tech_skills: list, soft_skills: list, industry: str, applicant_id: str = None) -> dict:
        """Generates a project-based assessment for a job role."""
        if applicant_id is None:
            applicant_id = str(uuid.uuid4())[:8]
        
        prompt = f"""
        **GOAL**: Design a 3-phase async project for a role in the {industry} industry that evaluates {', '.join(tech_skills)} (technical skills) and {', '.join(soft_skills)} (soft skills). The project must be resistant to AI/LLM shortcuts while allowing async submissions.

        **STRUCTURE**:
        **Role**: {job_title}
        **Project Title**: [Creative Name Tied to Industry]
        **Objective**: [1-sentence concise goal]

        **Phase 1**:
        - **Task**: [Action] + [randomized parameter, e.g., "incorporating {applicant_id} into a unique real-world challenge"].
        - **Submit**: [Deliverable] + [process artifact, e.g., "a changelog of key decisions"].
        - **AI-Resistant Tactic**: [How this phase blocks LLM shortcuts].

        **Phase 2**:
        - **Task**: Iterate on Phase 1 + [new constraint, e.g., "add compliance for regulations"].
        - **Submit**: Updated work + [self-critique, e.g., "300-word limitation analysis"].
        - **AI-Resistant Tactic**: [How this phase ensures continuity].

        **Phase 3**:
        - **Task**: [Reflective/creative task, e.g., "Write a postmortem for stakeholders"].
        - **Submit**: Final deliverable (such as a report or document) + [humanizing artifact, e.g., "audio note explaining trade-offs"].
        - **AI-Resistant Tactic**: [How this phase tests originality].

        For Phase 3, ensure Submit has two clear deliverables: a written document/report and an audio presentation.
        """
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You are an expert in designing AI-resistant project-based tasks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        response_text = response.choices[0].message.content.strip()
        
        try:
            # Extract project title and objective
            project_title_match = re.search(r"\*\*Project Title\*\*:\s*(.+)", response_text)
            objective_match = re.search(r"\*\*Objective\*\*:\s*(.+)", response_text)
            
            project_title = project_title_match.group(1).strip() if project_title_match else f"{job_title} Assessment Project"
            objective = objective_match.group(1).strip() if objective_match else f"Evaluate candidate skills for {job_title} role"
            
            # Extract phases
            phases = []
            for phase_num in range(1, 4):
                phase_pattern = rf"\*\*Phase {phase_num}\*\*:(.*?)(?=\*\*Phase {phase_num + 1}\*\*|\Z)"
                phase_match = re.search(phase_pattern, response_text, re.DOTALL)
                
                if phase_match:
                    phase_content = phase_match.group(1).strip()
                    
                    # Extract task, submit, and AI-resistant tactic
                    task_match = re.search(r"- \*\*Task\*\*:\s*(.+?)(?=\n- \*\*Submit\*\*|\n- \*\*AI-Resistant)", phase_content, re.DOTALL)
                    submit_match = re.search(r"- \*\*Submit\*\*:\s*(.+?)(?=\n- \*\*AI-Resistant|\Z)", phase_content, re.DOTALL)
                    ai_resistant_match = re.search(r"- \*\*AI-Resistant Tactic\*\*:\s*(.+)", phase_content, re.DOTALL)
                    
                    task = task_match.group(1).strip() if task_match else f"Phase {phase_num} task"
                    submit = submit_match.group(1).strip() if submit_match else f"Phase {phase_num} deliverable"
                    ai_resistant = ai_resistant_match.group(1).strip() if ai_resistant_match else "AI resistance strategy"
                    
                    phases.append({
                        "phase": phase_num,
                        "task": task,
                        "submit": submit,
                        "ai_resistant_tactic": ai_resistant
                    })
                else:
                    # Fallback phase if parsing fails
                    phases.append({
                        "phase": phase_num,
                        "task": f"Complete phase {phase_num} requirements for {job_title} role",
                        "submit": f"Submit deliverable for phase {phase_num}",
                        "ai_resistant_tactic": f"Phase {phase_num} includes verification mechanisms"
                    })
            
            return {
                "title": project_title,
                "objective": objective,
                "phases": phases
            }
            
        except Exception as e:
            # Fallback project structure if parsing completely fails
            return {
                "title": f"{job_title} Assessment Project",
                "objective": f"Comprehensive evaluation of candidate skills for {job_title} position",
                "phases": [
                    {
                        "phase": 1,
                        "task": f"Design and implement a solution demonstrating {tech_skills[0] if tech_skills else 'core technical'} skills",
                        "submit": "Technical implementation and documentation",
                        "ai_resistant_tactic": "Requires personalized implementation details"
                    },
                    {
                        "phase": 2,
                        "task": "Enhance the Phase 1 solution with additional requirements and constraints",
                        "submit": "Updated implementation with detailed change analysis",
                        "ai_resistant_tactic": "Builds on previous work requiring continuity"
                    },
                    {
                        "phase": 3,
                        "task": "Present the complete solution and provide strategic recommendations",
                        "submit": "Final report and presentation recording",
                        "ai_resistant_tactic": "Requires personal reflection and verbal presentation"
                    }
                ]
            }

    def evaluate_cv(self, cv_text: str, job_title: str, tech_skills: list, soft_skills: list, industry: str) -> dict:
        """Evaluates a candidate's CV against job requirements."""
        prompt = f"""
        You are an expert HR recruiter. Evaluate this candidate's CV/resume for a {job_title} position in the {industry} industry.

        **Job Requirements:**
        - Position: {job_title}
        - Industry: {industry}
        - Required Technical Skills: {', '.join(tech_skills)}
        - Required Soft Skills: {', '.join(soft_skills)}

        **CV/Resume:**
        {cv_text}

        **Evaluation Criteria:**
        Provide a comprehensive evaluation covering:

        1. **Overall Match Score** (0-100): How well does this candidate fit the role?
        2. **Experience Match** (0-100): Relevance of their work experience
        3. **Skills Coverage**: List the technical skills they possess from our requirements
        4. **Skills Gaps**: List the required technical skills they're missing
        5. **Strengths**: Top 3-5 strengths based on their background
        6. **Development Areas**: Top 3-5 areas for improvement
        7. **Overall Assessment**: 2-3 sentence summary of their candidacy
        8. **Interview Recommendations**: Specific areas to probe during interviews

        Format your response as a JSON object with the following structure:
        {{
            "match_score": number,
            "experience_match": number,
            "skills_coverage": [list of strings],
            "skills_gaps": [list of strings],
            "strengths": [list of strings],
            "development_areas": [list of strings],
            "overall_assessment": "string",
            "interview_recommendations": [list of strings]
        }}
        """
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
        
    def evaluate_submission(self, submission: str, phase_details: dict, ideal_response: str = None) -> dict:
        """Evaluates a candidate's submission for a project phase."""
        prompt = f"""
        You are an experienced technical recruiter evaluating a job candidate's submission for a project phase.

        **Phase Details:**
        - Phase Number: {phase_details.get('phase', 'N/A')}
        - Task: {phase_details.get('task', 'N/A')}
        - Expected Deliverable: {phase_details.get('submit', 'N/A')}

        **Candidate's Submission:**
        {submission}

        **Evaluation Instructions:**
        Evaluate this submission from a RECRUITMENT perspective, focusing on:

        1. **Technical Competency**: How well does this demonstrate the required technical skills?
        2. **Problem-Solving Approach**: Is their methodology sound and well-reasoned?
        3. **Communication Skills**: How clearly do they explain their work and decisions?
        4. **Attention to Detail**: Did they follow instructions and cover all requirements?
        5. **Cultural Fit Indicators**: Do they show collaboration, growth mindset, etc.?

        **Scoring Guidelines:**
        - Technical Score (0-100): Technical execution and accuracy
        - Problem-Solving Score (0-100): Approach and methodology
        - Communication Score (0-100): Clarity and documentation quality
        - Cultural Fit Score (0-100): Team compatibility indicators
        - Overall Score (0-100): Weighted average of all factors

        **Output Requirements:**
        Provide specific, actionable feedback that could be shared with the candidate and hiring manager.

        Format your response as a JSON object with the following structure:
        {{
            "hiring_recommendation": "Recommend/Consider/Do Not Recommend",
            "overall_score": number,
            "technical_score": number,
            "problem_solving_score": number,
            "communication_score": number,
            "cultural_fit_score": number,
            "technical_strengths": [list of specific strengths],
            "technical_weaknesses": [list of specific weaknesses],
            "behavioral_strengths": [list of soft skill strengths],
            "behavioral_weaknesses": [list of soft skill weaknesses],
            "red_flags": [list of concerning patterns],
            "interview_questions": [list of follow-up questions for interviews],
            "hiring_manager_summary": "2-3 sentence executive summary for hiring manager"
        }}
        """
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

# Create a single instance of the service to be used by other services
openai_service = OpenAIService()