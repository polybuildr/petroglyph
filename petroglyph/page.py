import os
import hashlib
from datetime import datetime


class Page:
    def __init__(self, file):
        if file[-4:] == '.rst':
            self.text_type = 'rst'
        else:
            self.text_type = 'md'
        f = open(file, 'r')
        text = f.read()
        import yaml
        import re
        match = re.search(r'^\s*---(.*?)---\s*(.*)$', text, re.DOTALL | re.MULTILINE)
        if match is None:
            raise ValueError("YAML front-matter missing from '%s'." % file)
        self.front_matter = match.group(1)
        self.config = yaml.safe_load(self.front_matter)
        if self.config is None:
            raise ValueError("Empty YAML front-matter in '%s'." % file)
        if 'title' not in self.config:
            raise ValueError("'%s' does not have title in YAML front-matter." % file)
        self.front_matter_data = self.config
        self.title = self.config['title']
        self.text = match.group(2)
        self.overrides = []
        self.mtime = datetime.fromtimestamp(os.path.getmtime(file))
        file = os.path.basename(file)
        if file[-3:] == '.md':
            self.slug = file[:-3]
        else:
            self.slug = file
        if self.slug in ('js', 'css', 'search', 'pages', 'special'):
            raise ValueError("Title '%s' is a reserved title ('%s')." % (self.slug, file))

    def __str__(self):
        return self.slug

    def __repr__(self):
        return str(self)

    def get_html(self):
        if self.text_type == 'rst':
            from docutils.core import publish_parts
            return publish_parts(self.text, writer_name='html')['html_body']
        else:
            import mistune
            return mistune.markdown(self.text, escape=False)

    def get_hash(self):
        return hashlib.md5(self.front_matter + self.text).hexdigest()
