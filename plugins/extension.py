from argparse import _ArgumentGroup
from core.models import GroupType, PluginType, SessionBaseModel
from core.plugin import Parser

class Extension(Parser):

    _alias_ = 'extension'
    _group_type_ = GroupType.INPUT
    _plugin_type_ = PluginType.PARSER


    def parser_request(self, sb: SessionBaseModel):
        if self.namespace.ext:
            sb.set_url(sb.get_url + self.namespace.ext)
    
    def initialize(self, main_parser, group):
        super(Extension, self).initialize(main_parser, group)
    
    def add_arguments(self, group: _ArgumentGroup):
        group.add_argument("-e", 
                           dest="ext", 
                           help="Lista de extensoes separadas por virgulas. Palavra chave FUZZ"
        )