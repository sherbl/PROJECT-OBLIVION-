# PROJECT OBLIVION 💀
**Advanced Offensive Reconnaissance & Red-Teaming Framework**

PROJECT OBLIVION is a modular Python-based security tool designed for automated target enumeration, vulnerability mapping, and offensive security auditing. 


<img width="956" height="726" alt="Screenshot_7" src="https://github.com/user-attachments/assets/94e3f38a-94a8-4a17-b0ae-9acd733af28a" />
<img width="628" height="646" alt="Screenshot_8" src="https://github.com/user-attachments/assets/5fd9ff26-979d-4055-9570-2fb722442213" />
<img width="992" height="1160" alt="Screenshot_9" src="https://github.com/user-attachments/assets/65e6510e-50a0-40ca-a8b9-ff175b51254d" />

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
   ```bash
a. Navigate to `config/settings.yaml`.
b. Replace `YOUR_SHODAN_API_KEY` with your actual key:
   shodan_api_key: "PASTE_YOUR_KEY_HERE"
   ```
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
