import json
import webbrowser
import os
from datetime import datetime

def evaluate_job_posting(job_posting):
    """
    Analyzes a job posting and provides feedback based on predefined criteria.
    :param job_posting: Dictionary containing job posting details.
    :return: Dictionary with scores and suggestions.
    """
    feedback = {}
    
    # Headline Evaluation
    headline = job_posting.get("headline", "")
    headline_length = len(headline)
    if headline_length > 30:
        feedback["headline_score"] = 10
        feedback["headline_feedback"] = "Excellent headline length and content."
    elif headline_length > 15:
        feedback["headline_score"] = 8
        feedback["headline_feedback"] = "Good headline, but consider making it more engaging."
    elif headline_length > 5:
        feedback["headline_score"] = 6
        feedback["headline_feedback"] = "Headline is a bit short. Add more detail to attract candidates."
    else:
        feedback["headline_score"] = 4
        feedback["headline_feedback"] = "Headline is too short and lacks detail."
    
    # Job Description Evaluation
    description = job_posting.get("description", "")
    description_length = len(description)
    if description_length > 300:
        feedback["description_score"] = 10
        feedback["description_feedback"] = "Comprehensive job description with good detail."
    elif description_length > 150:
        feedback["description_score"] = 8
        feedback["description_feedback"] = "Good description. Consider adding more specific responsibilities."
    elif description_length > 50:
        feedback["description_score"] = 6
        feedback["description_feedback"] = "Description is brief. Add more details about the role."
    else:
        feedback["description_score"] = 4
        feedback["description_feedback"] = "Description is too short. Candidates need more information."
    
    # Job Requirements Evaluation
    requirements = job_posting.get("requirements", "")
    requirements_length = len(requirements)
    if requirements_length > 200:
        feedback["requirements_score"] = 10
        feedback["requirements_feedback"] = "Detailed requirements that clearly define candidate qualifications."
    elif requirements_length > 100:
        feedback["requirements_score"] = 8
        feedback["requirements_feedback"] = "Good requirements. Consider being more specific about necessary skills."
    elif requirements_length > 30:
        feedback["requirements_score"] = 6
        feedback["requirements_feedback"] = "Requirements are basic. Add more specific qualifications."
    else:
        feedback["requirements_score"] = 4
        feedback["requirements_feedback"] = "Requirements are too vague. Be more specific."
    
    # Call to Action Evaluation
    cta = job_posting.get("cta", "")
    cta_lower = cta.lower()
    if len(cta) > 50 and "apply" in cta_lower and ("now" in cta_lower or "today" in cta_lower):
        feedback["cta_score"] = 10
        feedback["cta_feedback"] = "Strong CTA with urgency and clear instructions."
    elif len(cta) > 20 and "apply" in cta_lower:
        feedback["cta_score"] = 8
        feedback["cta_feedback"] = "Good CTA. Consider adding more urgency."
    elif "apply" in cta_lower:
        feedback["cta_score"] = 6
        feedback["cta_feedback"] = "Basic CTA. Add more details on how to apply."
    else:
        feedback["cta_score"] = 4
        feedback["cta_feedback"] = "Weak or missing CTA. Add a clear invitation to apply."
    
    # Calculate overall score
    scores = [feedback["headline_score"], feedback["description_score"], 
              feedback["requirements_score"], feedback["cta_score"]]
    feedback["overall_score"] = round(sum(scores) / len(scores), 1)
    
    return feedback

def create_html_file():
    """
    Creates an interactive HTML file for job posting evaluation.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Job Posting Evaluator</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; color: #333; }
            h1 { color: #2c3e50; text-align: center; }
            .container { max-width: 800px; margin: 0 auto; background: #f9f9f9; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            label { display: block; margin: 15px 0 5px; font-weight: bold; }
            textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; resize: vertical; min-height: 80px; }
            input[type="text"] { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background: #3498db; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; margin-top: 20px; }
            button:hover { background: #2980b9; }
            #results { margin-top: 30px; background: #fff; padding: 15px; border-radius: 4px; border-left: 5px solid #3498db; }
            .score-meter { margin: 10px 0; }
            .meter-bar { height: 20px; background: #eee; border-radius: 10px; overflow: hidden; }
            .meter-fill { height: 100%; background: linear-gradient(90deg, #ff6b6b, #ffb347, #48dbfb, #1dd1a1); transition: width 0.5s ease; }
            .feedback-item { margin: 15px 0; padding: 10px; border-radius: 4px; background: #f1f9fe; }
            .score { font-weight: bold; font-size: 1.2em; }
            .hidden { display: none; }
            #optimized-version { margin-top: 20px; background: #f1f9fe; padding: 15px; border-radius: 4px; white-space: pre-wrap; }
            .save-btn { background: #27ae60; }
            .save-btn:hover { background: #2ecc71; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Job Posting Evaluator</h1>
            <div>
                <label for="headline">Job Headline:</label>
                <input type="text" id="headline" placeholder="e.g., Senior Software Engineer - Python">
                
                <label for="description">Job Description:</label>
                <textarea id="description" placeholder="Describe the role, responsibilities, and what the job entails..."></textarea>
                
                <label for="requirements">Job Requirements:</label>
                <textarea id="requirements" placeholder="List qualifications, skills, experience needed..."></textarea>
                
                <label for="cta">Call to Action:</label>
                <textarea id="cta" placeholder="How should candidates apply? e.g., Apply now via our careers page..."></textarea>
                
                <button id="evaluate-btn">Evaluate Job Posting</button>
                <button id="save-btn" class="save-btn hidden">Save Evaluation Report</button>
            </div>
            
            <div id="results" class="hidden">
                <h2>Evaluation Results</h2>
                <div class="feedback-item">
                    <h3>Overall Score: <span id="overall-score" class="score"></span>/10</h3>
                    <div class="score-meter">
                        <div class="meter-bar">
                            <div id="overall-meter" class="meter-fill"></div>
                        </div>
                    </div>
                </div>
                
                <div class="feedback-item">
                    <h3>Headline</h3>
                    <p>Score: <span id="headline-score" class="score"></span>/10</p>
                    <div class="score-meter">
                        <div class="meter-bar">
                            <div id="headline-meter" class="meter-fill"></div>
                        </div>
                    </div>
                    <p id="headline-feedback"></p>
                </div>
                
                <div class="feedback-item">
                    <h3>Job Description</h3>
                    <p>Score: <span id="description-score" class="score"></span>/10</p>
                    <div class="score-meter">
                        <div class="meter-bar">
                            <div id="description-meter" class="meter-fill"></div>
                        </div>
                    </div>
                    <p id="description-feedback"></p>
                </div>
                
                <div class="feedback-item">
                    <h3>Job Requirements</h3>
                    <p>Score: <span id="requirements-score" class="score"></span>/10</p>
                    <div class="score-meter">
                        <div class="meter-bar">
                            <div id="requirements-meter" class="meter-fill"></div>
                        </div>
                    </div>
                    <p id="requirements-feedback"></p>
                </div>
                
                <div class="feedback-item">
                    <h3>Call to Action</h3>
                    <p>Score: <span id="cta-score" class="score"></span>/10</p>
                    <div class="score-meter">
                        <div class="meter-bar">
                            <div id="cta-meter" class="meter-fill"></div>
                        </div>
                    </div>
                    <p id="cta-feedback"></p>
                </div>
                
                <h3>Optimized Job Posting:</h3>
                <div id="optimized-version"></div>
            </div>
        </div>
        
        <script>
            document.getElementById('evaluate-btn').addEventListener('click', function() {
                const headline = document.getElementById('headline').value;
                const description = document.getElementById('description').value;
                const requirements = document.getElementById('requirements').value;
                const cta = document.getElementById('cta').value;
                
                if (!headline || !description || !requirements || !cta) {
                    alert('Please fill in all fields.');
                    return;
                }
                
                // This would normally be a server request, but we'll simulate it
                const feedback = evaluateJobPosting({
                    headline: headline,
                    description: description,
                    requirements: requirements,
                    cta: cta
                });
                
                // Display results
                document.getElementById('results').classList.remove('hidden');
                document.getElementById('save-btn').classList.remove('hidden');
                
                // Set scores and feedback
                document.getElementById('overall-score').textContent = feedback.overall_score;
                document.getElementById('overall-meter').style.width = (feedback.overall_score * 10) + '%';
                
                document.getElementById('headline-score').textContent = feedback.headline_score;
                document.getElementById('headline-meter').style.width = (feedback.headline_score * 10) + '%';
                document.getElementById('headline-feedback').textContent = feedback.headline_feedback;
                
                document.getElementById('description-score').textContent = feedback.description_score;
                document.getElementById('description-meter').style.width = (feedback.description_score * 10) + '%';
                document.getElementById('description-feedback').textContent = feedback.description_feedback;
                
                document.getElementById('requirements-score').textContent = feedback.requirements_score;
                document.getElementById('requirements-meter').style.width = (feedback.requirements_score * 10) + '%';
                document.getElementById('requirements-feedback').textContent = feedback.requirements_feedback;
                
                document.getElementById('cta-score').textContent = feedback.cta_score;
                document.getElementById('cta-meter').style.width = (feedback.cta_score * 10) + '%';
                document.getElementById('cta-feedback').textContent = feedback.cta_feedback;
                
                // Generate optimized version
                const optimized = generateOptimizedPosting(headline, description, requirements, cta, feedback);
                document.getElementById('optimized-version').textContent = optimized;
            });
            
            document.getElementById('save-btn').addEventListener('click', function() {
                const headline = document.getElementById('headline').value;
                const description = document.getElementById('description').value;
                const requirements = document.getElementById('requirements').value;
                const cta = document.getElementById('cta').value;
                
                const feedback = {
                    headline_score: document.getElementById('headline-score').textContent,
                    headline_feedback: document.getElementById('headline-feedback').textContent,
                    description_score: document.getElementById('description-score').textContent,
                    description_feedback: document.getElementById('description-feedback').textContent,
                    requirements_score: document.getElementById('requirements-score').textContent,
                    requirements_feedback: document.getElementById('requirements-feedback').textContent,
                    cta_score: document.getElementById('cta-score').textContent,
                    cta_feedback: document.getElementById('cta-feedback').textContent,
                    overall_score: document.getElementById('overall-score').textContent
                };
                
                const optimized = document.getElementById('optimized-version').textContent;
                
                // Generate report content
                const report = generateReport(headline, description, requirements, cta, feedback, optimized);
                
                // Create download link
                const blob = new Blob([report], {type: 'text/plain'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.download = 'job_posting_evaluation_report.txt';
                a.href = url;
                a.click();
                URL.revokeObjectURL(url);
            });
            
            // Simulated server-side evaluation function
            function evaluateJobPosting(jobPosting) {
                let feedback = {};
                
                // Headline Evaluation
                const headline = jobPosting.headline;
                const headlineLength = headline.length;
                if (headlineLength > 30) {
                    feedback.headline_score = 10;
                    feedback.headline_feedback = "Excellent headline length and content.";
                } else if (headlineLength > 15) {
                    feedback.headline_score = 8;
                    feedback.headline_feedback = "Good headline, but consider making it more engaging.";
                } else if (headlineLength > 5) {
                    feedback.headline_score = 6;
                    feedback.headline_feedback = "Headline is a bit short. Add more detail to attract candidates.";
                } else {
                    feedback.headline_score = 4;
                    feedback.headline_feedback = "Headline is too short and lacks detail.";
                }
                
                // Job Description Evaluation
                const description = jobPosting.description;
                const descriptionLength = description.length;
                if (descriptionLength > 300) {
                    feedback.description_score = 10;
                    feedback.description_feedback = "Comprehensive job description with good detail.";
                } else if (descriptionLength > 150) {
                    feedback.description_score = 8;
                    feedback.description_feedback = "Good description. Consider adding more specific responsibilities.";
                } else if (descriptionLength > 50) {
                    feedback.description_score = 6;
                    feedback.description_feedback = "Description is brief. Add more details about the role.";
                } else {
                    feedback.description_score = 4;
                    feedback.description_feedback = "Description is too short. Candidates need more information.";
                }
                
                // Job Requirements Evaluation
                const requirements = jobPosting.requirements;
                const requirementsLength = requirements.length;
                if (requirementsLength > 200) {
                    feedback.requirements_score = 10;
                    feedback.requirements_feedback = "Detailed requirements that clearly define candidate qualifications.";
                } else if (requirementsLength > 100) {
                    feedback.requirements_score = 8;
                    feedback.requirements_feedback = "Good requirements. Consider being more specific about necessary skills.";
                } else if (requirementsLength > 30) {
                    feedback.requirements_score = 6;
                    feedback.requirements_feedback = "Requirements are basic. Add more specific qualifications.";
                } else {
                    feedback.requirements_score = 4;
                    feedback.requirements_feedback = "Requirements are too vague. Be more specific.";
                }
                
                // Call to Action Evaluation
                const cta = jobPosting.cta;
                const ctaLower = cta.toLowerCase();
                if (cta.length > 50 && ctaLower.includes("apply") && (ctaLower.includes("now") || ctaLower.includes("today"))) {
                    feedback.cta_score = 10;
                    feedback.cta_feedback = "Strong CTA with urgency and clear instructions.";
                } else if (cta.length > 20 && ctaLower.includes("apply")) {
                    feedback.cta_score = 8;
                    feedback.cta_feedback = "Good CTA. Consider adding more urgency.";
                } else if (ctaLower.includes("apply")) {
                    feedback.cta_score = 6;
                    feedback.cta_feedback = "Basic CTA. Add more details on how to apply.";
                } else {
                    feedback.cta_score = 4;
                    feedback.cta_feedback = "Weak or missing CTA. Add a clear invitation to apply.";
                }
                
                // Calculate overall score
                const scores = [feedback.headline_score, feedback.description_score, 
                              feedback.requirements_score, feedback.cta_score];
                feedback.overall_score = (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1);
                
                return feedback;
            }
            
            function generateOptimizedPosting(headline, description, requirements, cta, feedback) {
                // This is a simplified optimization - in reality you'd want more sophisticated logic
                let optimized = "";
                
                // Optimize headline based on feedback
                if (feedback.headline_score < 8) {
                    // Make headline more compelling
                    optimized += "EXCITING OPPORTUNITY: " + headline + "\n\n";
                } else {
                    optimized += headline + "\n\n";
                }
                
                // Optimize description
                optimized += "ABOUT THE ROLE:\n";
                if (feedback.description_score < 8) {
                    // Add structure to description
                    optimized += "We are seeking a talented professional to join our team. In this role, you will:\n";
                    optimized += "• " + description + "\n";
                    optimized += "• Collaborate with cross-functional teams\n";
                    optimized += "• Contribute to our company's growth and success\n\n";
                } else {
                    optimized += description + "\n\n";
                }
                
                // Optimize requirements
                optimized += "QUALIFICATIONS & REQUIREMENTS:\n";
                if (feedback.requirements_score < 8) {
                    // Structure requirements better
                    const reqs = requirements.split(/[,;.]/);
                    for (let req of reqs) {
                        if (req.trim()) {
                            optimized += "• " + req.trim() + "\n";
                        }
                    }
                    optimized += "\n";
                } else {
                    optimized += requirements + "\n\n";
                }
                
                // Optimize CTA
                if (feedback.cta_score < 8) {
                    // Make CTA stronger
                    optimized += "READY TO JOIN OUR TEAM? Apply now! " + cta + " Don't miss this opportunity to advance your career!";
                } else {
                    optimized += cta;
                }
                
                return optimized;
            }
            
            function generateReport(headline, description, requirements, cta, feedback, optimized) {
                const date = new Date().toLocaleString();
                let report = "JOB POSTING EVALUATION REPORT\n";
                report += "Generated: " + date + "\n\n";
                
                report += "ORIGINAL JOB POSTING:\n";
                report += "--------------------\n";
                report += "Headline: " + headline + "\n";
                report += "Description: " + description + "\n";
                report += "Requirements: " + requirements + "\n";
                report += "Call to Action: " + cta + "\n\n";
                
                report += "EVALUATION RESULTS:\n";
                report += "------------------\n";
                report += "Overall Score: " + feedback.overall_score + "/10\n\n";
                
                report += "Headline Score: " + feedback.headline_score + "/10\n";
                report += "Feedback: " + feedback.headline_feedback + "\n\n";
                
                report += "Description Score: " + feedback.description_score + "/10\n";
                report += "Feedback: " + feedback.description_feedback + "\n\n";
                
                report += "Requirements Score: " + feedback.requirements_score + "/10\n";
                report += "Feedback: " + feedback.requirements_feedback + "\n\n";
                
                report += "Call to Action Score: " + feedback.cta_score + "/10\n";
                report += "Feedback: " + feedback.cta_feedback + "\n\n";
                
                report += "OPTIMIZED JOB POSTING:\n";
                report += "---------------------\n";
                report += optimized;
                
                return report;
            }
        </script>
    </body>
    </html>
    """
    
    # Create the HTML file
    file_path = os.path.join(os.getcwd(), "job_posting_evaluator.html")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    return file_path

def main():
    # Create the HTML file
    file_path = create_html_file()
    print(f"Interactive Job Posting Evaluator created at: {file_path}")
    
    # Open the HTML file in the default browser
    webbrowser.open('file://' + os.path.realpath(file_path))

if __name__ == "__main__":
    main()