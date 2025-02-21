import pytest

from llm_web_kit.model.resource_utils.singleton_resource_manager import \
    SingletonResourceManager


class TestSingletonResourceManager:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.manager = SingletonResourceManager()

    def test_has_name(self):
        # "test" should not exist before setting
        assert not self.manager.has_name('test')

        self.manager.set_resource('test', 'resource')
        # "test" should exist after setting
        assert self.manager.has_name('test')
        # "test1" should not exist
        assert not self.manager.has_name('test1')

    def test_set_resource(self):
        self.manager.set_resource('test', 'resource')
        # "test" should exist after setting and the resource should be "resource"
        assert self.manager.has_name('test')
        assert self.manager.get_resource('test') == 'resource'

        # "test" should not be set again
        with pytest.raises(AssertionError):
            self.manager.set_resource('test', 'resource')

        # name should be a string
        with pytest.raises(TypeError):
            self.manager.set_resource(1, 'resource')

        # resource should not be None
        with pytest.raises(TypeError):
            self.manager.set_resource(None, 'resource')

    def test_get_resource(self):
        self.manager.set_resource('test', 'resource')
        # "test" should exist after setting and the resource should be "resource"
        assert self.manager.get_resource('test') == 'resource'
        # Exception should be raised if the resource does not exist
        with pytest.raises(Exception):
            self.manager.get_resource('test1')

    def test_release_resource(self):
        self.manager.set_resource('test', 'resource')
        self.manager.release_resource('test')
        # "test" should not exist after releasing
        assert not self.manager.has_name('test')
        # Exception should be raised if the resource does not exist
        with pytest.raises(Exception):
            self.manager.get_resource('test')
        # Should not raise exception if the resource does not exist
        self.manager.release_resource('test')
