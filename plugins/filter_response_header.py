from argparse import _ArgumentGroup
from core.models import GroupType, PluginType, SessionBaseModel
from core.plugin import Parser

class FilterResponseHeader(Parser):

    _alias_ = 'FilterResponseHeader'
    _group_type_ = GroupType.FILTERS
    _plugin_type_ = PluginType.FILTER


    def parser_response(self, sb: SessionBaseModel) -> bool:
        if self.namespace.fh:
            for header in self.namespace.fh:
                try:
                    key, value = header.split(':')
                    if key.strip() not in sb.get_response.headers.keys():
                        return False
                    if value.strip() not in sb.get_response.headers.values():  # correção aqui
                        return False
                except IndexError:
                    exit(f"[*] Os parametros -fh {header} nao esta formatado")
        return True
    
    @property
    def check_namespace(self):
        if self.namespace.fh:
            return True
        return False
    
    def initialize(self, main_parser, group):
        super(FilterResponseHeader, self).initialize(main_parser, group)
    
    def add_arguments(self, group: _ArgumentGroup):
        group.add_argument("-fh", 
                           dest="fh",
                           nargs="+",
                           action="extend",
                           help='"Nome:valor", separado por colunas. Aceita multiplos -fh'
        )