from llm_web_kit.exception.exception import ModelResourceException


class SingletonResourceManager:

    def __init__(self):
        self.resources = {}

    def has_name(self, name):
        return name in self.resources

    def set_resource(self, name: str, resource):
        if not isinstance(name, str):
            raise ModelResourceException(
                f'Name should be a string, but got {type(name)}'
            )
        if name in self.resources:
            raise ModelResourceException(f'Resource {name} already exists')

        self.resources[name] = resource

    def get_resource(self, name):
        if name in self.resources:
            return self.resources[name]
        else:
            raise ModelResourceException(f'Resource {name} does not exist')

    def release_resource(self, name):
        if name in self.resources:
            del self.resources[name]


singleton_resource_manager = SingletonResourceManager()
