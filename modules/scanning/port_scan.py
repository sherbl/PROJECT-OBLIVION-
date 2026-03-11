import subprocess

class ActiveScanner:
    def scan(self, ip, target_ports=None):
        if target_ports:
            # אם קיבלנו פורטים משודאן, נסרוק רק אותם לעומק
            port_str = ",".join(str(p) for p in target_ports)
            cmd = ['nmap', '-sV', '-Pn', '-p', port_str, ip]
            print(f"[*] Running targeted Smart Nmap on specific ports: {' '.join(cmd)}")
        else:
            # אם שודאן נכשל לחלוטין, נריץ סריקה מהירה כללית
            cmd = ['nmap', '-sV', '-Pn', '-F', ip]
            print(f"[*] Running general fast Nmap scan: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            
            ports = []
            for line in result.stdout.split('\n'):
                if '/tcp' in line and 'open' in line:
                    parts = line.split()
                    port = parts[0].split('/')[0]
                    service = parts[2] if len(parts) > 2 else 'Unknown'
                    version = " ".join(parts[3:]) if len(parts) > 3 else ''
                    ports.append({'port': port, 'service': f"{service} {version}".strip()})
            
            return {'source': 'Smart Nmap', 'ports': ports} if ports else {'error': 'No open ports found.'}
        except Exception as e:
            return {'error': str(e)}
