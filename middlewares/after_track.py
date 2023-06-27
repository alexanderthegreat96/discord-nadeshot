import json
class after_track:
    def __init__(self, ctx):
        self.ctx = ctx

    def main(self):
        return {'status': True, 'message': 'This is after middleware'}