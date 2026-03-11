import requests
import urllib3
import re
import random
import time
import concurrent.futures

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebFuzzer:
    def __init__(self):
        self.wordlist = ['admin', 'login', 'backup', 'config', '.env', 'api', 'dashboard', 'phpmyadmin', 'robots.txt', '.git']
        
        # מאגר זהויות שונות להתחמקות מ-WAF
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Googlebot/2.1 (+http://www.google.com/bot.html)'
        ]

    def _check_url(self, url):
        # מנגנון Jitter: השהייה אקראית של 0.1 עד 0.5 שניות לפני כל בקשה
        time.sleep(random.uniform(0.1, 0.5))
        
        # בחירת זהות אקראית לכל נתיב שנבדק
        headers = {'User-Agent': random.choice(self.user_agents)}
        
        try:
            res = requests.get(url, headers=headers, timeout=5, verify=False)
            if res.status_code in [200, 301, 302, 401, 403]:
                return f"/{url.split('/')[-1]} (Status: {res.status_code})"
        except requests.exceptions.RequestException:
            pass
        return None

    def analyze_web_app(self, ip, port):
        protocol = 'https' if str(port) in ['443', '8443'] else 'http'
        base_url = f"{protocol}://{ip}:{port}/"
        print(f"\n    [*] Initiating Stealth Web Fuzzing on {base_url}...")
        
        web_data = {'paths': [], 'title': 'Unknown', 'server': 'Unknown'}

        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            res = requests.get(base_url, headers=headers, timeout=5, verify=False)
            web_data['server'] = res.headers.get('Server', 'Unknown')
            
            title_match = re.search(r'<title>(.*?)</title>', res.text, re.IGNORECASE)
            if title_match:
                web_data['title'] = title_match.group(1).strip()
            print(f"       [+] Web Title: {web_data['title']}")
            print(f"       [+] Web Server: {web_data['server']}")
        except:
            print("       [-] Could not connect to the root web page.")

        urls_to_test = [f"{base_url}{word}" for word in self.wordlist]
        
        # משתמשים בעד 5 תהליכונים במקום 10 כדי לשמור על פרופיל נמוך (Stealth)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = executor.map(self._check_url, urls_to_test)
            for result in results:
                if result:
                    print(f"       [+] Found path: {result}")
                    web_data['paths'].append(result)

        if not web_data['paths']:
             print(f"       [-] No hidden paths found.")
             
        return web_data
