import shodan

class ShodanRecon:
    def __init__(self, api_key):
        self.api_key = api_key

    def scan(self, ip):
        if not self.api_key:
            return {'error': 'No Shodan API key provided in config/settings.yaml'}
        
        try:
            api = shodan.Shodan(self.api_key)
            host = api.host(ip)
            results = {'source': 'Shodan', 'ports': []}
            
            for item in host['data']:
                results['ports'].append({
                    'port': item['port'],
                    'service': item.get('product', 'Unknown')
                })
            return results
        except shodan.APIError as e:
            return {'error': f"Shodan API Error: {e}"}
        except Exception as e:
            return {'error': str(e)}
