import tempfile
import re
from fpdf import FPDF
from typing import Dict, List, Any

from app.models.candidate import Candidate

def clean_text_for_pdf(text: str) -> str:
    """
    Clean text to remove characters that aren't supported by standard PDF fonts.
    
    Args:
        text: Input text that might contain unsupported Unicode characters
        
    Returns:
        Cleaned text with ASCII-compatible characters
    """
    if not text:
        return ""
    
    # Replace common Unicode characters with ASCII equivalents
    replacements = {
        '•': '- ',  # Bullet point
        '–': '-',   # En dash
        '—': '-',   # Em dash
        ''': "'",   # Left single quotation mark
        ''': "'",   # Right single quotation mark
        '"': '"',   # Left double quotation mark
        '"': '"',   # Right double quotation mark
        '…': '...',  # Horizontal ellipsis
        '®': '(R)',  # Registered trademark
        '©': '(C)',  # Copyright
        '™': '(TM)', # Trademark
        '\u2022': '- ',  # Another bullet point unicode
        '\u00a0': ' ',   # Non-breaking space
    }
    
    # Apply replacements
    for unicode_char, ascii_replacement in replacements.items():
        text = text.replace(unicode_char, ascii_replacement)
    
    # Remove any remaining non-ASCII characters and replace with space
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def create_candidate_report_pdf(candidate: Candidate) -> str:
    """
    Generates a comprehensive PDF report for a single candidate.
    
    Args:
        candidate: The SQLAlchemy Candidate object, with its relationships 
                   (job, submissions, etc.) eagerly loaded.
                   
    Returns:
        The file path to the temporary PDF file.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    # --- Report Header ---
    pdf.cell(0, 10, 'Candidate Evaluation Report', 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f"Candidate Name: {clean_text_for_pdf(candidate.name)}", 0, 1)
    pdf.cell(0, 8, f"Candidate ID: {str(candidate.id)}", 0, 1)
    pdf.cell(0, 8, f"Applied for: {clean_text_for_pdf(candidate.job.title)}", 0, 1)
    pdf.cell(0, 8, f"Status: {clean_text_for_pdf(candidate.status)}", 0, 1)
    pdf.cell(0, 8, f"Application Date: {candidate.created_at.strftime('%Y-%m-%d')}", 0, 1)
    pdf.ln(5)
    
    # --- CV Evaluation Section ---
    if candidate.cv_evaluation:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'CV Evaluation Summary', 0, 1)
        pdf.set_font('Arial', '', 11)
        cv_eval = candidate.cv_evaluation
        
        # Match scores
        pdf.cell(0, 6, f"Overall Match Score: {cv_eval.get('match_score', 'N/A')}/100", 0, 1)
        pdf.cell(0, 6, f"Experience Match: {cv_eval.get('experience_match', 'N/A')}/100", 0, 1)
        pdf.ln(3)
        
        # Skills coverage and gaps
        skills_coverage = cv_eval.get('skills_coverage', [])
        if skills_coverage:
            clean_skills = [clean_text_for_pdf(skill) for skill in skills_coverage]
            pdf.cell(0, 6, f"Skills Covered: {', '.join(clean_skills)}", 0, 1)
        
        skills_gaps = cv_eval.get('skills_gaps', [])
        if skills_gaps:
            clean_gaps = [clean_text_for_pdf(skill) for skill in skills_gaps]
            pdf.cell(0, 6, f"Skills Gaps: {', '.join(clean_gaps)}", 0, 1)
        pdf.ln(3)
        
        # Overall assessment
        pdf.multi_cell(0, 6, f"Assessment: {clean_text_for_pdf(cv_eval.get('overall_assessment', 'N/A'))}")
        pdf.ln(5)

    # --- Project Submissions Section ---
    if candidate.submissions:
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Project Submission Evaluations', 0, 1)
        
        for submission in sorted(candidate.submissions, key=lambda s: s.phase_number):
            if submission.evaluation:
                eval_data = submission.evaluation
                pdf.set_font('Arial', 'B', 12)
                hiring_rec = clean_text_for_pdf(eval_data.get('hiring_recommendation', 'N/A'))
                pdf.cell(0, 8, f"Phase {submission.phase_number}: {hiring_rec} (Score: {eval_data.get('overall_score', 'N/A')}/100)", 0, 1)
                pdf.set_font('Arial', '', 10)
                
                # Technical and other scores
                tech_score = eval_data.get('technical_score', 'N/A')
                comm_score = eval_data.get('communication_score', 'N/A')
                pdf.cell(0, 5, f"Technical: {tech_score}/100, Communication: {comm_score}/100", 0, 1)
                
                # Summary
                summary = clean_text_for_pdf(eval_data.get('hiring_manager_summary', 'N/A'))
                pdf.multi_cell(0, 5, f"Summary: {summary}")
                pdf.ln(3)
    else:
        pdf.set_font('Arial', '', 11)
        pdf.cell(0, 8, "No project submissions found.", 0, 1)
        pdf.ln(5)

    # --- Final Recommendation ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Final Recommendation', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    # Calculate overall recommendation based on CV and submissions
    if candidate.cv_evaluation and candidate.submissions:
        cv_score = candidate.cv_evaluation.get('match_score', 0)
        submission_scores = [s.evaluation.get('overall_score', 0) for s in candidate.submissions if s.evaluation]
        avg_submission_score = sum(submission_scores) / len(submission_scores) if submission_scores else 0
        final_score = (cv_score * 0.3 + avg_submission_score * 0.7) if submission_scores else cv_score
        
        if final_score >= 80:
            recommendation = "STRONG RECOMMEND"
        elif final_score >= 65:
            recommendation = "RECOMMEND"
        elif final_score >= 50:
            recommendation = "CONSIDER"
        else:
            recommendation = "DO NOT RECOMMEND"
            
        pdf.cell(0, 8, f"Final Score: {final_score:.1f}/100", 0, 1)
        pdf.cell(0, 8, f"Recommendation: {recommendation}", 0, 1)

    # --- Save PDF to a temporary file ---
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    return temp_file.name

def create_reference_guide_pdf(job_title: str, project_data: dict, ideal_responses: dict = None) -> str:
    """
    Generates a reference guide PDF for the job's project assessment.
    
    Args:
        job_title: The title of the job position
        project_data: The project dictionary with phases
        ideal_responses: Optional ideal responses for each phase
        
    Returns:
        The file path to the temporary PDF file.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    # --- Header ---
    clean_job_title = clean_text_for_pdf(job_title)
    pdf.cell(0, 10, f'{clean_job_title} - Assessment Reference Guide', 0, 1, 'C')
    pdf.ln(10)
    
    # --- Project Overview ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Project Overview', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    project_title = clean_text_for_pdf(project_data.get('title', 'N/A'))
    project_objective = clean_text_for_pdf(project_data.get('objective', 'N/A'))
    
    pdf.cell(0, 8, f"Project Title: {project_title}", 0, 1)
    pdf.multi_cell(0, 6, f"Objective: {project_objective}")
    pdf.ln(5)
    
    # --- Phase Details ---
    phases = project_data.get('phases', [])
    for phase in phases:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f"Phase {phase.get('phase', 'N/A')}", 0, 1)
        pdf.set_font('Arial', '', 10)
        
        # Task description
        task_text = clean_text_for_pdf(phase.get('task', 'N/A'))
        pdf.multi_cell(0, 5, f"Task: {task_text}")
        pdf.ln(2)
        
        # Submit requirements
        submit_text = clean_text_for_pdf(phase.get('submit', 'N/A'))
        pdf.multi_cell(0, 5, f"Submit: {submit_text}")
        pdf.ln(2)
        
        # AI-resistant tactic
        ai_tactic_text = clean_text_for_pdf(phase.get('ai_resistant_tactic', 'N/A'))
        pdf.multi_cell(0, 5, f"AI-Resistant Strategy: {ai_tactic_text}")
        pdf.ln(5)
        
        # Ideal response if provided
        if ideal_responses and str(phase.get('phase')) in ideal_responses:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, "Ideal Response Guidelines:", 0, 1)
            pdf.set_font('Arial', '', 9)
            ideal_text = clean_text_for_pdf(ideal_responses[str(phase.get('phase'))])
            pdf.multi_cell(0, 4, ideal_text)
            pdf.ln(3)

    # --- Evaluation Criteria ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Evaluation Criteria', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    criteria = [
        "Technical Competency (0-100): Quality of technical implementation and approach",
        "Problem-Solving (0-100): Methodology and reasoning demonstrated", 
        "Communication (0-100): Clarity of documentation and explanations",
        "Cultural Fit (0-100): Collaboration and growth mindset indicators",
        "Overall Score (0-100): Weighted average of all factors"
    ]
    
    for criterion in criteria:
        # Use dash instead of bullet point to avoid Unicode issues
        pdf.cell(0, 6, f"- {criterion}", 0, 1)
    
    # --- Save PDF to a temporary file ---
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    return temp_file.name