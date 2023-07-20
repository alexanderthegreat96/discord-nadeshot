import json
from from_root import from_root

class Config:
    @staticmethod
    def config(self):
        try:
            f = open(from_root('config/config.json'), 'r')
            try:
                return json.load(f)
            except Exception as e:
                return False
        except Exception as e:
            return False
    @staticmethod
    def bot_config(self):
        try:
            f = open(from_root('config/bot.json'), 'r')
            try:
                data = json.load(f)
                return data['config']
            except Exception as e:
                return False
        except Exception as e:
            return False

    @staticmethod
    def staff_list(self):
        try:
            f = open(from_root('config/staff.json'), 'r')
            try:
                data = json.load(f)
                return data['users']
            except Exception as e:
                return False
        except Exception as e:
            return False

    @staticmethod
    def staff_groups(self):
        try:
            f = open(from_root('config/staff.json'), 'r')
            try:
                data = json.load(f)
                return data['groups']
            except Exception as e:
                return False
        except Exception as e:
            return False
    @staticmethod
    def command_list(self):
        try:
            f = open(from_root('config/commands.json'), 'r')
            try:
                data = json.load(f)
                return data['commands']
            except Exception as e:
                return False
        except Exception as e:
            return False