import time
from modules.recon.shodan_api import ShodanRecon
from modules.scanning.port_scan import ActiveScanner
from modules.scanning.web_spider import WebFuzzer
from modules.vulnerability.cve_lookup import CVELookup
from modules.scanning.auto_checker import LowHangingFruit
from core.reporter import Reporter

class ScannerEngine:
    def __init__(self, config):
        self.shodan_key = config.get('api_keys', {}).get('shodan', '')

    def run(self, target):
        start_time = time.time() # מתחילים למדוד זמן
        
        print("\n" + "="*50)
        print(f"[*] Starting Advanced Red Team Scan for {target}")
        print("="*50)

        # שלב 1: איסוף פסיבי
        print("\n[*] Phase 1: Passive Reconnaissance (Shodan)")
        shodan = ShodanRecon(self.shodan_key)
        results = shodan.scan(target)
        scanner = ActiveScanner()

        # שלב 2: סריקה אקטיבית וחכמה
        if 'error' in results or not results.get('ports'):
            print(f"[-] Passive recon failed. Executing general Active Scan...")
            results = scanner.scan(target)
        else:
            print(f"[+] Passive recon found {len(results['ports'])} ports.")
            print("\n[*] Phase 2: Smart Active Scanning")
            known_ports = [p['port'] for p in results['ports']]
            smart_scan_results = scanner.scan(target, target_ports=known_ports)
            
            if 'error' not in smart_scan_results:
                results = smart_scan_results
            else:
                 print("[-] Smart scan failed. Falling back to Shodan data.")

        if 'error' in results:
            print(f"\n[-] Scan failed: {results['error']}")
            return

        # שלב 3: בדיקות עומק
        print("\n[*] Phase 3: Deep Enumeration & Auto-Checks")
        vuln_checker = CVELookup()
        web_fuzzer = WebFuzzer()
        auto_checker = LowHangingFruit()
        
        for p in results['ports']:
            port_num = str(p['port'])
            service_name = p['service']
            print(f"\n    -> Analyzing Port {port_num} ({service_name})...")
            
            # א. חיפוש חולשות
            p['cves'] = []
            if service_name != 'Unknown':
                cves = vuln_checker.check_vulnerabilities(service_name)
                if cves:
                    p['cves'] = cves
                    print(f"       [!] Potential Vulnerabilities: {', '.join(cves)}")
                else:
                    print(f"       [-] No known CVEs found.")

            # ב. ציד "פירות נמוכים" (FTP אנונימי כרגע)
            p['auto_checks'] = []
            if port_num == '21' or 'ftp' in service_name.lower():
                ftp_result = auto_checker.check_ftp_anonymous(target, port_num)
                if ftp_result:
                    p['auto_checks'].append(ftp_result)

            # ג. סריקת נתיבי Web
            p['web_data'] = {}
            if port_num in ['80', '443', '8080', '8443'] or 'http' in service_name.lower():
                web_results = web_fuzzer.analyze_web_app(target, port_num)
                p['web_data'] = web_results

        # שלב 4: יצירת דוח
        print("\n[*] Phase 4: Generating Report")
        reporter = Reporter()
        report_name = f"scan_report_{target.replace('.', '_')}.html"
        reporter.generate_html(target, results, report_name)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        print(f"\n[*] All operations completed successfully in {duration} seconds!")
        print(f"[*] Report saved to: {report_name}")
