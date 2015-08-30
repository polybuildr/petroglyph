from datetime import datetime, time
from petroglyph.page import Page


class Post(Page):
    def __init__(self, file):
        Page.__init__(self, file)
        if 'date' in self.config:
            self.overrides.append('date')
            self.custom_date = datetime.combine(self.config['date'], time.min)

        if 'tags' in self.config:
            self.tags = [tag.strip() for tag in self.config['tags'].split(',')]
        else:
            self.tags = []

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
