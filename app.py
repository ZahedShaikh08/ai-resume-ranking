from flask import Flask, render_template, request, flash, redirect, url_for
import os
import shutil
from utils.extract_text import extract_text
from utils.rank_resumes import rank_resumes
from utils.file_validation import allowed_file, clean_filename
from werkzeug.utils import secure_filename
import uuid
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

# Ensure upload directories exist

os.makedirs(os.path.join(UPLOAD_FOLDER, "resumes"), exist_ok=True)

# ... existing imports ...

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get job description text directly from form
        jd_text = request.form.get('jd_text', '').strip()
        if not jd_text:
            flash('Job description cannot be empty')
            return redirect(request.url)
        
        # Validate resumes
        if 'resumes' not in request.files:
            flash('No resume files uploaded')
            return redirect(request.url)
        
        resumes = request.files.getlist('resumes')
        if not resumes or resumes[0].filename == '':
            flash('No selected resume files')
            return redirect(request.url)

        # Process resumes
        try:
            resume_data = []
            valid_count = 0
            
            for resume in resumes:
                if resume.filename == '' or not allowed_file(resume.filename, ALLOWED_EXTENSIONS):
                    continue
                
                try:
                    # Save resume with unique filename
                    resume_filename = f"resume_{uuid.uuid4().hex}_{secure_filename(resume.filename)}"
                    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], "resumes", resume_filename)
                    resume.save(resume_path)
                    
                    # Extract text
                    resume_text = extract_text(resume_path)
                    if resume_text.strip():
                        resume_data.append({
                            "name": clean_filename(resume.filename),
                            "text": resume_text,
                            "path": resume_path
                        })
                        valid_count += 1
                except Exception as e:
                    app.logger.error(f"Error processing {resume.filename}: {str(e)}")
            
            if valid_count == 0:
                flash('No valid resumes could be processed')
                return redirect(request.url)

            # Rank resumes
            ranked_resumes = rank_resumes(jd_text, resume_data)
            
            return render_template(
                "index.html", 
                results=ranked_resumes,
                jd_text=jd_text[:100] + "..." if len(jd_text) > 100 else jd_text,
                resume_count=valid_count
            )
            
        except Exception as e:
            flash(f'Processing error: {str(e)}')
            app.logger.exception("Processing failed")
            return redirect(request.url)
        finally:
            # Cleanup uploads after processing
            shutil.rmtree(os.path.join(UPLOAD_FOLDER, "resumes"), ignore_errors=True)
            os.makedirs(os.path.join(UPLOAD_FOLDER, "resumes"), exist_ok=True)
    
    return render_template("index.html", results=None)

if __name__ == "__main__":
    app.run(port=5002, debug=False)

@app.route("/preview")
def preview():
    path = request.args.get('path', '')
    
    # Security check
    if not path.startswith(app.config['UPLOAD_FOLDER']):
        return "Unauthorized", 403
        
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except Exception as e:
        return f"Error loading file: {str(e)}", 500