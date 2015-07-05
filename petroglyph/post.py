import os
from datetime import datetime, time
import hashlib


class Post:
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
        config = yaml.safe_load(self.front_matter)
        if config is None:
            raise ValueError("Empty YAML front-matter in '%s'." % file)
        if 'title' not in config:
            raise ValueError("'%s' does not have title in YAML front-matter." % file)
        self.front_matter_data = config
        self.title = config['title']
        self.text = match.group(2)
        self.overrides = []
        if 'date' in config:
            self.overrides.append('date')
            self.custom_date = datetime.combine(config['date'], time.min)

        self.mtime = datetime.fromtimestamp(os.path.getmtime(file))
        if 'tags' in config:
            self.tags = [tag.strip() for tag in config['tags'].split(',')]
        else:
            self.tags = []
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
            return mistune.markdown(self.text)

    def get_preview(self):
        import re
        match = re.search(r'(.*)<!--\s*more\s*-->', self.get_html(), re.MULTILINE | re.DOTALL)
        if not match:
            return self.get_html()
        return match.group(1)

    def getmtime(self):
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')
        if 'date' in self.overrides:
            mtime = self.custom_date
        else:
            mtime = self.mtime
        return mtime.strftime('{S} %B, %Y').replace(
            '{S}',
            str(mtime.day) + suffix(mtime.day)
        )

    def get_time(self):
        if 'date' in self.overrides:
            return self.custom_date
        return self.mtime

    def get_hash(self):
        return hashlib.md5(self.front_matter + self.text).hexdigest()
