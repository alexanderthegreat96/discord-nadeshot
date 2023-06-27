import json
class before_track:
    def __init__(self, ctx):
        self.ctx = ctx

    def main(self):
        return {'status': False, 'error': 'Issue, we hit a wall'}