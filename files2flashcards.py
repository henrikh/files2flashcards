import re

def find_fragments(raw_string, tag):
    """Find HTML fragments by tag.
    
    Returns a list of strings containing the fragments"""
    
    regex = "(?s)" + "<" + tag + ".*?</" + tag + ">"
    return re.findall(regex, raw_string)