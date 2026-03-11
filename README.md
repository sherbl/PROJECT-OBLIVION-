# PROJECT OBLIVION 💀
**Advanced Offensive Reconnaissance & Red-Teaming Framework**

PROJECT OBLIVION is a modular Python-based security tool designed for automated target enumeration, vulnerability mapping, and offensive security auditing. 



## 🚀 Key Features
* **Passive Reconnaissance:** Integration with Shodan API for silent intelligence gathering.
* **Smart Scanning:** Targeted Nmap integration based on passive discovery.
* **Vulnerability Mapping:** Automated CVE lookup for identified services.
* **Web Fuzzing:** Stealthy directory and file discovery on multiple ports.
* **Automatic Breach Detection:** Built-in handlers for common misconfigurations (e.g., FTP Anonymous Login).
* **Professional Reporting:** Generates clean HTML reports and tactical log files.

## 🛠 Installation & Usage
1. Clone the repository:
   ```bash
   git clone [https://github.com/sherbl/Project-Oblivion.git]
   
   cd Project-Oblivion
   ```
   ## ⚙️ Configuration
Before running the tool, you need to provide your **Shodan API Key**.
a. Navigate to `config/settings.yaml`.
b. Replace `YOUR_SHODAN_API_KEY` with your actual key:
   shodan_api_key: "PASTE_YOUR_KEY_HERE"
   
2.Install dependencies:
```bash
   pip3 install -r requirements.txt
   ```
3.Run a scan:
```bash
python3 main.py -t <domain_or_ip>
```

📜 Disclaimer
This tool is for educational purposes and authorized penetration testing only. Use it responsibly.

Lead Developer: Sherbl.ab
