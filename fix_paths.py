import os
import re

def fix_html_files():
    templates_dir = 'templates'
    
    # Route mapping
    routes = {
        'index.html': 'home',
        'login.html': 'login',
        'signup.html': 'signup',
        'book.html': 'book',
        'design.html': 'design',
        'how.html': 'how',
        'visit.html': 'visit',
        'show.html': 'show'
    }

    for filename in os.listdir(templates_dir):
        if not filename.endswith('.html'):
            continue
            
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Fix broken tags in index.html (specific fix for previous error)
        # Pattern: src="{{ url_for('static', filename='images/somefile.ext"
        content = re.sub(
            r'src="{{ url_for\(\'static\', filename=\'images/([^"\']+)"', 
            r'src="{{ url_for(\'static\', filename=\'images/\1\') }}"', 
            content
        )

        # 2. Fix Images: src="../source/file.ext" -> src="{{ url_for... }}"
        content = re.sub(
            r'src="\.\./source/([^"]+)"', 
            r'src="{{ url_for(\'static\', filename=\'images/\1\') }}"', 
            content
        )

        # 3. Fix CSS: href="style.css" -> href="{{ url_for... }}"
        # Exclude http/https/urls starting with {{
        def css_replacer(match):
            css_file = match.group(1)
            if css_file.startswith('http') or css_file.startswith('{{'):
                return match.group(0)
            return f'href="{{{{ url_for(\'static\', filename=\'css/{css_file}\') }}}}"'
        
        content = re.sub(r'href="([^"]+\.css)"', css_replacer, content)

        # 4. Fix JS: src="script.js" -> src="{{ url_for... }}"
        def js_replacer(match):
            js_file = match.group(1)
            if js_file.startswith('http') or js_file.startswith('{{'):
                return match.group(0)
            return f'src="{{{{ url_for(\'static\', filename=\'js/{js_file}\') }}}}"'

        content = re.sub(r'src="([^"]+\.js)"', js_replacer, content)

        # 5. Fix Links: href="page.html" -> href="{{ url_for('route') }}"
        def link_replacer(match):
            html_file = match.group(1)
            base_name = html_file.split('?')[0] # Handle query params like show.html?topic=...
            if base_name in routes:
                route = routes[base_name]
                if '?' in html_file:
                    return match.group(0) # Skip query params for now or handle complexity? 
                    # Actually, url_for doesn't easily taking raw query strings without kwargs.
                    # Let's simple-replace the filename part if possible, but keep it simple.
                    # If it has query params, we might break it if we just blindly replace.
                    # Strategy: If exact match, replace. If contains ?, handle separately?
                    # Start with exact matches for navigation.
                return f'href="{{{{ url_for(\'{route}\') }}}}"'
            return match.group(0)

        # Simple exact match replacement for navigation links
        for html_file, route in routes.items():
            # Replace href="index.html"
            content = re.sub(f'href="{html_file}"', f'href="{{{{ url_for(\'{route}\') }}}}"', content)
        
        # 6. Handle show.html?topic=... 
        # href="show.html?topic=living-room" -> href="{{ url_for('show', topic='living-room') }}"
        def query_link_replacer(match):
            page = match.group(1) # show.html
            param = match.group(2) # topic=living-room
            if page == 'show.html':
                 key, value = param.split('=')
                 return f'href="{{{{ url_for(\'show\', {key}=\'{value}\') }}}}"'
            return match.group(0)

        content = re.sub(r'href="(show\.html)\?([^"]+)"', query_link_replacer, content)
        
        # 7. JavaScript btn('show.html?topic=...') fixes
        # onclick="btn('show.html?topic=master-bedroom');"
        content = re.sub(
            r"btn\('show\.html\?topic=([^']+)'\)", 
            r"window.location.href='{{ url_for('show', topic='\1') }}'", 
            content
        )


        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed {filename}")

if __name__ == "__main__":
    fix_html_files()
