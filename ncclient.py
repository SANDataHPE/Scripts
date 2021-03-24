import lxml.etree as ET
from argparse import ArgumentParser
from ncclient import manager 
from ncclient.operations import RPCError

payload = '''<?xml version="1.0" encoding="utf-8"?> 
 <rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id=""> 
   <cisco-ia:checkpoint xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/> 
 </rpc>'''

if __name__ == '__main__':
  parser = ArgumentParser(description='Usage:')
  # script arguments  
  parser.add_argument('-a', '--host', type=str, required=True,                       
               help="Device IP address or Hostname")
  parser.add_argument('-u', '--username', type=str, required=True,                       
               help="Device Username (netconf agent username)")    
  parser.add_argument('-p', '--password', type=str, required=True,                            
               help="Device Password (netconf agent password)") 
  parser.add_argument('--port', type=int, default=830,                     
               help="Netconf agent port")
  args = parser.parse_args()
  # connect to netconf agent   
  with manager.connect(host=args.host,                        
                port=args.port,                            
                username=args.username,                        
                password=args.password,                        
                timeout=90,                 
                hostkey_verify=False) as m:
    # execute netconf operation 
    try:
      response = m.dispatch(ET.fromstring(payload)).xml
      data = ET.fromstring(response)
    except RPCError as e:
      data = e._raw
      # beautify output
      print(ET.tostring(data, pretty_print=True))
