import re

def markdown_to_omd(content):
    """
    Convert Markdown content to Optimized Markdown (OMD) format.
    
    Args:
        content (str): Markdown formatted text
        
    Returns:
        str: OMD formatted text
    """
    # Headings - Convert in reverse order to avoid conflicts
    content = re.sub(r'^#{6}\s+', ';', content, flags=re.MULTILINE)
    content = re.sub(r'^#{5}\s+', ':', content, flags=re.MULTILINE)
    content = re.sub(r'^#{4}\s+', '.', content, flags=re.MULTILINE)
    content = re.sub(r'^#{3}\s+', '-', content, flags=re.MULTILINE)
    content = re.sub(r'^#{2}\s+', '>', content, flags=re.MULTILINE)
    content = re.sub(r'^#\s+', '!', content, flags=re.MULTILINE)
    
    # Bold+Italic (process before individual bold/italic to avoid conflicts)
    content = re.sub(r'\*\*\*([^*]+)\*\*\*', r'*/\1/*', content)
    
    # Bold (convert **text** to *text*)
    content = re.sub(r'\*\*([^*]+)\*\*', r'*\1*', content)
    
    # Italic (convert *text* to /text/)
    content = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'/\1/', content)
    
    # Strikethrough (convert ~~text~~ to ~text~)
    content = re.sub(r'~~([^~]+)~~', r'~\1~', content)
    
    # Blockquotes (convert > to ")
    content = re.sub(r'^>\s*', '"', content, flags=re.MULTILINE)
    
    # Task lists
    content = re.sub(r'^(\s*)- \[x\]\s+', r'\1✓ ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)- \[X\]\s+', r'\1✓ ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)- \[ \]\s+', r'\1• ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)\* \[x\]\s+', r'\1✓ ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)\* \[X\]\s+', r'\1✓ ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)\* \[ \]\s+', r'\1• ', content, flags=re.MULTILINE)
    
    # Regular unordered lists (convert - or * to •)
    content = re.sub(r'^(\s*)[-*]\s+', r'\1• ', content, flags=re.MULTILINE)
    
    # Code blocks (fenced) - convert ```lang to `lang
    content = re.sub(r'^```(\w*)\s*$', r'`\1', content, flags=re.MULTILINE)
    content = re.sub(r'^```\s*$', '`', content, flags=re.MULTILINE)
    
    return content

def omd_to_markdown(content):
    """
    Convert Optimized Markdown (OMD) content to standard Markdown format.
    
    Args:
        content (str): OMD formatted text
        
    Returns:
        str: Markdown formatted text
    """
    # Headings - Convert OMD heading markers to Markdown
    content = re.sub(r'^!', '# ', content, flags=re.MULTILINE)
    content = re.sub(r'^>', '## ', content, flags=re.MULTILINE)
    content = re.sub(r'^-', '### ', content, flags=re.MULTILINE)
    content = re.sub(r'^\.', '#### ', content, flags=re.MULTILINE)
    content = re.sub(r'^:', '##### ', content, flags=re.MULTILINE)
    content = re.sub(r'^;', '###### ', content, flags=re.MULTILINE)
    
    # Bold+Italic (process before individual conversions)
    content = re.sub(r'\*/([^/]+)/\*', r'***\1***', content)
    
    # Italic (convert /text/ to *text*)
    content = re.sub(r'/([^/]+)/', r'*\1*', content)
    
    # Bold (convert *text* to **text** - after italic to avoid conflicts)
    content = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'**\1**', content)
    
    # Strikethrough (convert ~text~ to ~~text~~)
    content = re.sub(r'(?<!~)~([^~]+)~(?!~)', r'~~\1~~', content)
    
    # Blockquotes (convert " to >)
    content = re.sub(r'^"', '>', content, flags=re.MULTILINE)
    
    # Task lists
    content = re.sub(r'^(\s*)✓\s+', r'\1- [x] ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)✗\s+', r'\1- [ ] ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*)⟳\s+', r'\1- [ ] ', content, flags=re.MULTILINE)
    
    # Regular unordered lists (convert • to -)
    content = re.sub(r'^(\s*)•\s+', r'\1- ', content, flags=re.MULTILINE)
    
    # Code blocks (fenced) - convert `lang to ```lang
    content = re.sub(r'^`(\w+)\s*$', r'```\1', content, flags=re.MULTILINE)
    content = re.sub(r'^`\s*$', '```', content, flags=re.MULTILINE)
    
    return content