from argparse import _ArgumentGroup, ArgumentParser, Namespace
import pluginlib

from core.models import GroupType, PluginType, SessionBaseModel


@pluginlib.Parent('parser')
class Parser(object):

    _alias_ = "Parser"
    _group_type_ = GroupType.DEFAULT
    main_parser: ArgumentParser = None
    _plugin_type_ = PluginType.PARSER

    def parser_request(self, sb: SessionBaseModel):
        raise NotImplementedError

    def parser_response(self, sb: SessionBaseModel) -> bool:
        raise NotImplementedError

    @pluginlib.abstractmethod
    def initialize(self, main_parser: ArgumentParser, group: _ArgumentGroup):
        self.main_parser = main_parser
        self.add_arguments(group)

    @pluginlib.abstractmethod
    def add_arguments(self, group: _ArgumentGroup):
        raise NotImplementedError

    @property
    def get_group_type(self):
        return self._group_type_

    @property
    def get_plugin_type(self):
        return self._plugin_type_
    
    @property
    def namespace(self) -> Namespace:
        return self.main_parser.parse_args()
    
    @property
    def check_namespace(self):
        raise NotImplementedError
