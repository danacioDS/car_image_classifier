import hashlib
import os
from posixpath import splitext


def allowed_file(filename:str):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    format = [".png", ".jpg", ".jpeg", ".gif"]
    file_extension = os.path.splitext(filename.lower())[1]
    allowed_file = True if file_extension in format else False

    return allowed_file


def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    
    file_contents = file.read()
    h = hashlib.md5(file_contents)
    h = h.hexdigest()
    extension = splitext(file.filename)[1]
    hashed_name = h + extension
    file.seek(0)
    return hashed_name
