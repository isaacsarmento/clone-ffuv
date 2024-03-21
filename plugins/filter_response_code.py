from argparse import _ArgumentGroup
from core.models import GroupType, PluginType, SessionBaseModel
from core.plugin import Parser

class FilterResponseCode(Parser):

    _alias_ = 'FilterResponseCode'
    _group_type_ = GroupType.FILTERS
    _plugin_type_ = PluginType.FILTER


    def parser_response(self, sb: SessionBaseModel) -> bool:
        if self.namespace.fc:
            if str(sb.get_response.status_code) in self.namespace.fc.split(','):
                return True
        return False
    
    @property
    def check_namespace(self):
        if self.namespace.fc:
            return True
        return False
    
    def initialize(self, main_parser, group):
        super(FilterResponseCode, self).initialize(main_parser, group)
    
    def add_arguments(self, group: _ArgumentGroup):
        group.add_argument("-fc", 
                           dest="fc", 
                           help="Filtre o status do HTTP Request: 200, 404"
        )