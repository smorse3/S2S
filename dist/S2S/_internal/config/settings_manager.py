import yaml


class SettingsManager:

    def save(self, path, settings):

        with open(path, "w") as f:

            yaml.dump(settings, f)

    def load(self, path):

        with open(path, "r") as f:

            return yaml.safe_load(f)