import re

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def clean_filename(filename):
    """Remove potentially harmful characters from filenames"""
    clean = re.sub(r'[^\w\-_. ]', '', filename)
    return clean[:50]  # Truncate long filenames