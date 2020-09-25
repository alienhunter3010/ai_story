class Answer:
    def __init__(self, rows=[], raw_rows=[], style="HTML"):
        self.rows = rows
        self.raw_rows = raw_rows
        self.style = style
        self.setup = {}
        self.binary = None

    def get_dict(self):
        return {'rows': self.rows,
                'raw_rows': self.raw_rows,
                'style': self.style,
                'setup': self.setup
                }

    def has_totalk(self):
        if len(self.rows):
            return True
        if len(self.raw_rows):
            return True
        return False

    def prepend_rows(self, rows=[], raw_rows=[]):
        self.rows = rows + self.rows
        self.raw_rows = raw_rows + self.raw_rows
        return self

    def append_rows(self, rows=[], raw_rows=[]):
        self.rows = self.rows + rows
        self.raw_rows = self.raw_rows + raw_rows
        return self
