from argparse import ArgumentParser
from typing import Dict, List

from pluginlib import PluginLoader
import pluginlib
from core.models import GroupType, PluginType, SessionBaseModel

from core.plugin import Parser


class PluginManager:
    _parser: ArgumentParser = None
    _group_plugins: dict = dict()
    _plugins: Dict[str, Parser] = dict()
    _loader: PluginLoader = None
    
    def __init__(self, parser: ArgumentParser):
        self._parser = parser
        
        loader = pluginlib.PluginLoader(paths=['plugins'])
        plugins = loader.plugins
        for group in GroupType:
            self._group_plugins[group.name] = self._parser.add_argument_group(group.value)
        #print(plugins.parser['json']())
        
        for pl_name in plugins.parser:
            inst_pl: Parser = plugins.parser[pl_name]()
            inst_pl.initialize(self._parser, self._group_plugins[inst_pl.get_group_type.name])
            self._plugins[pl_name] = inst_pl
            
    def set_parser_request(self, gt: GroupType, sb: SessionBaseModel):
        for name, inst_pl in self._plugins.items():
            if inst_pl.get_group_type == gt:
                inst_pl.parser_request(sb)
        
    def get_plugins(self, pt: PluginType = None) -> List[Parser]:
        if not pt:
            return [inst_pl for name, inst_pl in self._plugins.items()]
        return [inst_pl for name, inst_pl in self._plugins.items() if inst_pl.get_plugin_type == pt]