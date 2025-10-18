# 🧩 Practical — Complete Assignment (A, B, and C)

---

## 🧩 Part A — Python Log Analysis Script

### 🧠 Overview

This script automates log analysis. It finds the **latest modified text file** inside a specified folder, reads the **last 50 lines**, searches for specific keywords (error, exception, warning), and saves the results. If more than 5 matches are found, it automatically sends an email alert.

### ⚙️ Main Steps

1. **Find the newest file** using `max(files, key=lambda f: f.stat().st_mtime)`
2. **Read the last 50 lines** efficiently with a `deque`
3. **Search for patterns** using the `re` module (case-insensitive)
4. **Write matching lines** into an output file with a timestamp
5. **Send an alert email** if matches exceed threshold

### 🧩 Example Keywords

```python
keywords = ("exception", "error", "warning")
```

### 💌 Email Setup

The script uses Gmail SMTP to send alert emails if needed:

```python
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your_email@example.com"
SMTP_PASS = "app_password_here"
EMAIL_TO  = "destination@example.com"
```

### ✅ Output

* Output file saved in `~/ts-assignment/output/`
* Email alert sent if `matches > 5`

---

## 🧩 Part B — Bash Script: Scheduled Job for Archiving

### 🧠 Objective

Create a scheduled job (cron) to check a specific folder every hour (at minute 10). If any files are older than 12 hours, compress and move them to an archive folder.

### 🧩 Example Bash Script (simplified)

```bash
#!/bin/bash

SOURCE_DIR="/home/pc/ts-assignment/logs"
ARCHIVE_DIR="/home/pc/ts-assignment/archive"

mkdir -p "$ARCHIVE_DIR"

# Find files older than 12 hours and compress them
timefind "$SOURCE_DIR" -type f -mmin +720 -exec gzip {} \; -exec mv {}.gz "$ARCHIVE_DIR" \;
```

### 🕒 Add to Cron Schedule

To open cron editor:

```bash
crontab -e
```

Add this line to run every hour at the 10th minute:

```bash
10 * * * * /home/pc/ts-assignment/archive_script.sh
```

### ⚙️ Explanation

* `find` locates files older than 12 hours (`-mmin +720` → 60min × 12h)
* `-exec gzip {}` compresses each old file
* `mv {}.gz` moves the compressed file to the archive directory
* Cron runs this automatically each hour at minute 10

### 🧾 Note

Use `chmod +x archive_script.sh` to make it executable.

---

## 🧩 Part C — Wireshark Network Capture (analyses below and Data Capture is attached in the Repo)

### 🧠 e Assignment Description

Using Wireshark, capture and analyze network traffic between your **laptop (client)** and a **web server** (Ubuntu VM). Identify the following from the captured packets:

* Source and destination IP addresses
* Source and destination port numbers
* Protocol used

### ⚙️ Setup Steps

1. **Run a web server** inside Ubuntu VM:

   ```bash
   python3 -m http.server 8080
   ```
2. **Find the VM IP:** `ip a`
3. **Access from Windows browser:** `http://<VM-IP>:8080`
4. **Start Wireshark** on Windows → select **Wi-Fi** (since the VM uses Bridged Adapter)
5. **Filter by IP:**

   ```
   ip.addr == 192.168.100.50
   ```

### 📊 Findings from Capture

```
Source IP: 192.168.100.78
Destination IP: 192.168.100.50
Source Port: 56044
Destination Port: 8080
Protocol: TCP (HTTP)
```

This shows:

* **Windows host (192.168.100.78)** acted as the client
* **Ubuntu VM (192.168.100.50)** acted as the server
* Connection used **TCP**, carrying **HTTP** data

### 🔹 Why Source Port Changes

The client (Windows) uses random **ephemeral ports** for each new connection — e.g., 56044, 57720, 64639. The server port (8080) stays fixed, as that’s where the Python server listens.

### 🔹 What is ICMP

ICMP = **Internet Control Message Protocol**, used for network diagnostics. For example:

```bash
ping 192.168.100.50
```

ICMP sends **Echo Request/Reply** messages to test connectivity. These packets also appeared in the capture during network checks.

### 💾 Saved Capture File

```
File → Save As → C_Wireshark_Report.pcapng
```

### 🧾 Summary Table

| Item                   | Description                         |
| ---------------------- | ----------------------------------- |
| **Source IP**          | 192.168.100.78 (Windows Host)       |
| **Destination IP**     | 192.168.100.50 (Ubuntu VM)          |
| **Source Port**        | Dynamic (56044, 57720, 64639, etc.) |
| **Destination Port**   | 8080                                |
| **Protocol**           | TCP (HTTP)                          |
| **Other Traffic Seen** | ICMP (ping)                         |

### ✅ Conclusion

The capture confirms successful HTTP communication between the Windows client and the Ubuntu web server. Wireshark displayed TCP handshakes, HTTP requests/responses, and ICMP messages, proving full two-way network communication.

---

✅ **Final Note:** Practical A is now fully completed — including Part A (Python Script), Part B (Bash Cron Job), and Part C (Wireshark Capture).
