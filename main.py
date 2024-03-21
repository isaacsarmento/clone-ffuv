import argparse
from core.models import GroupType, HTTPMethod, PluginType, SessionBaseModel
import concurrent.futures
from core.plugin_manager import PluginManager
from core.utils import parser_wordlist
import requests

parser = argparse.ArgumentParser(description='Web Fuzzer - iNdk')
parser.add_argument('-u', 
                    dest='url', 
                    help='Definir url para atacar',
                    required=True
)
parser.add_argument('-X', 
                    dest='method', 
                    help='Metodo HTTP que irá ser usado', 
                    default=HTTPMethod.GET.value
)
parser.add_argument('-d', 
                    dest='data', 
                    help='Corpo do metodo HTTP do conteudo post', 
                    default=''
)
parser.add_argument('-t', 
                    dest='timeout', 
                    type=int, 
                    help='TIMEOUT na duracao da request: o tempo padrao é 10 segundos', 
                    default=10
)
parser.add_argument('-w', 
                    dest='wordlist',  
                    help='Caminho (path) do arquivo wordlist', 
                    required=True
)


pm = plugin_manager = PluginManager(parser)

parser_args = parser.parse_args()
wordlists = []
if parser_args.wordlist:
    wordlists = parser_wordlist(parser_args.wordlist)

if not wordlists:
    exit("[*] A wordlist está vazia ou nao foi encontrada")
    
if parser_args.method == HTTPMethod.POST.value:
    if not parser_args.data:
        exit("[*] O corpo da requisicao nao foi encontrado, coloque o parametro -d na linha de comando")

sbms =  [SessionBaseModel(parser_args.url, line) for line in wordlists]

def thread_request_task(sb: SessionBaseModel, pm: PluginManager, parser_args: argparse.Namespace):
    response = None
    
    pm.set_parser_request(GroupType.INPUT, sb)
    
    if parser_args.method == HTTPMethod.GET.value:
        try:
            response = requests.get(url=sb.get_url, 
                                    headers=sb.get_headers, 
                                    timeout=parser_args.timeout)
        except Exception as e:
            print(f'{e}')
    else:
        sb.set_payload(parser_args.data)
        if not 'Content-Type' in sb.get_headers.keys():
            sb.add_headers('Content-Type', 'application/x-www-form-urlencoded')
        try:
            response = requests.post(url=sb.get_url, 
                                     data=sb.get_payload,
                                     headers=sb.get_headers, 
                                     timeout=parser_args.timeout)
        except Exception as e:
            print(f'{e}')
    sb.set_response(response)
      
    plugins_filters = pm.get_plugins(PluginType.FILTER)
    if any([p.check_namespace for p in plugins_filters if p.check_namespace]):
        if all([p.parser_response(sb) for p in plugins_filters if p.check_namespace]):
            return f'{sb.get_url} - [{sb.get_response.status_code}]'
        return None
    return f'{sb.get_url} - [{sb.get_response.status_code}]'
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for sbm in sbms:
        futures.append(executor.submit(thread_request_task, sb=sbm, pm=pm, parser_args=parser_args))
    for future in concurrent.futures.as_completed(futures):
        if future.result():
            print(future.result())
