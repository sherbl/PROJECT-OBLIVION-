from datetime import datetime

class Reporter:
    def generate_html(self, target, data, filename="report.html"):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Vuln Scan Report - {target}</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #121212; color: #e0e0e0; margin: 40px; }}
                h1 {{ color: #00ffcc; border-bottom: 2px solid #333; padding-bottom: 10px; }}
                .summary {{ background-color: #1e1e1e; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 5px solid #00ffcc; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background-color: #1e1e1e; font-size: 14px; }}
                th, td {{ border: 1px solid #333; padding: 12px; text-align: left; vertical-align: top; }}
                th {{ background-color: #2a2a2a; color: #00ffcc; }}
                tr:hover {{ background-color: #2a2a2a; }}
                .cve-found {{ color: #ff4d4d; font-weight: bold; }}
                .safe {{ color: #4dff4d; }}
                .highlight {{ color: #ffbf00; font-weight: bold; }}
                .critical {{ color: #ff3333; font-weight: bold; font-size: 16px; border: 1px solid #ff3333; padding: 5px; display: inline-block; margin-bottom: 5px; }}
            </style>
        </head>
        <body>
            <h1>Advanced Red Team Operations Report</h1>
            <div class="summary">
                <p><strong>Target IP:</strong> {target}</p>
                <p><strong>Scan Date:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                <p><strong>Data Source:</strong> {data.get('source', 'Unknown')}</p>
            </div>
            
            <table>
                <tr>
                    <th>Port</th>
                    <th>Service / Version</th>
                    <th>Vulnerabilities (CVEs)</th>
                    <th>Enum Details & Auto-Checks</th>
                </tr>
        """
        
        for p in data.get('ports', []):
            cves = p.get('cves', [])
            web_data = p.get('web_data', {})
            auto_checks = p.get('auto_checks', [])
            
            cve_str = "<br>".join(cves) if cves else "No known CVEs"
            cve_class = "cve-found" if cves else "safe"
            
            enum_str = ""
            # אם יש התראות פירות נמוכים (כמו FTP)
            if auto_checks:
                for check in auto_checks:
                    enum_str += f"<span class='critical'>{check}</span><br>"
            
            # אם יש מידע על אתר אינטרנט
            if web_data:
                title = web_data.get('title', 'N/A')
                server = web_data.get('server', 'N/A')
                paths = "<br>".join(web_data.get('paths', []))
                
                # מוסיפים רווח יפה אם כבר הדפסנו התראת FTP לפני כן
                if enum_str:
                    enum_str += "<br><br>"
                    
                enum_str += f"<span class='highlight'>Title:</span> {title}<br><span class='highlight'>Server:</span> {server}<br><br><span class='highlight'>Discovered Paths:</span><br>{paths}"
            
            if not enum_str:
                enum_str = "N/A"
            
            html_content += f"""
                <tr>
                    <td><strong>{p['port']}</strong></td>
                    <td>{p['service']}</td>
                    <td class="{cve_class}">{cve_str}</td>
                    <td>{enum_str}</td>
                </tr>
            """
            
        html_content += """
            </table>
        </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html_content)
