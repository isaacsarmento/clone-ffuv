from argparse import _ArgumentGroup
from core.models import GroupType, PluginType, SessionBaseModel
from core.plugin import Parser

class CustomHeader(Parser):

    _alias_ = 'CustomHeader'
    _group_type_ = GroupType.INPUT
    _plugin_type_ = PluginType.PARSER


    def parser_request(self, sb: SessionBaseModel):
        if self.namespace.headers:
            for header in self.namespace.headers:
                try:
                    for header in self.namespace.headers:
                        key, value = header.split(':')
                        sb.add_headers(key=key, value=value)
                except IndexError:
                    exit(f"[*] Os parametros -H {header} nao esta formatado")
        return True
    
    def initialize(self, main_parser, group):
        super(CustomHeader, self).initialize(main_parser, group)
    
    def add_arguments(self, group: _ArgumentGroup):
        group.add_argument("-H", 
                           dest="headers",
                           nargs="+",
                           action="extend",
                           help='"Nome:valor", separado por colunas. Aceita multiplos -fh'
        )