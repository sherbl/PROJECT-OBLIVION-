import ftplib

class LowHangingFruit:
    def check_ftp_anonymous(self, ip, port):
        print(f"       [*] Testing FTP Anonymous Login on {ip}:{port}...")
        try:
            # מנסה להתחבר לשרת ה-FTP ללא סיסמה
            ftp = ftplib.FTP()
            ftp.connect(ip, int(port), timeout=5)
            ftp.login('anonymous', 'anonymous@example.com')
            ftp.quit()
            
            print("       [!!!] CRITICAL: FTP Anonymous Login Allowed!")
            return "[CRITICAL] FTP Anonymous Login Allowed"
            
        except Exception as e:
            print("       [-] FTP Anonymous Login failed or disabled.")
            return None
