"""
    Functions related to file verifications
"""

def check_file_extension(filename: str):
    allowed_extensions = {'txt', 'pdf'}
    # Check if there is a period in the filename and splits the extension at the last period. 
    # Then convert it to lowercase and checks if it is allowed
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions