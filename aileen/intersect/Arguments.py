class WithFS:
    commands = []

    @staticmethod
    def add_command(cmd):
        WithFS.commands.append(cmd)

    @staticmethod
    def here(cmd):
        return cmd in WithFS.commands
