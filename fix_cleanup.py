import os

def cleanup_html_files():
    templates_dir = 'templates'
    
    for filename in os.listdir(templates_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace \' with '
        content = content.replace("\\'", "'")
        
        # Also check for \" just in case
        content = content.replace('\\"', '"')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned {filename}")

if __name__ == "__main__":
    cleanup_html_files()
