
from pathlib import Path   # to deal with folders easily instead of os.path
from collections import deque  # keeps last lines only, مش لازم اقرا الملف كله
import re    # to search for error or warning using patterns
import smtplib  # for sending email
from email.message import EmailMessage  # عشان ابني الرسالة نفسها

# define folders
LOG_DIR = Path.home() / "ts-assignment" / "logs"     #مثلا مكان اللوق فايلات انا عاملو 
OUTPUT_DIR = Path.home() / "ts-assignment" / "output" # فولدر النتائج
OUTPUT_FILE = OUTPUT_DIR / "log_results.txt"  # اسم الملف الناتج

# words i need to search for
KEYWORDS = ("exception", "error", "warning")
THRESHOLD = 5  # لو اكثر من 5 لازم ابعت ايميل

# email setup
SMTP_HOST = "smtp.gmail.com"  # سيرفر الجيميل
SMTP_PORT = 587               # tls port
SMTP_USER = "alaa24taher@gmail.com"   # الايميل اللي رح يرسل
SMTP_PASS = "cyoq mduh vswj qlvq"   # from fake email for security
EMAIL_TO = "alaabin10@gmail.com"  # الايميل اللي رح توصله الرسالة


# اول اشي اتأكد انو فولدر الاوتبوت موجود
# i used pathlib cuz its newer, more flixble easier to use
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# اجيب اخر ملف معدل باللوق فولدر
txt_files = list(LOG_DIR.glob("*.txt"))  # كل الفايلات .txt
if not txt_files:
    print("no files ya zalameh")  # لو فاضي ما يكمل
    quit()

latest_file = max(txt_files, key=lambda f: f.stat().st_mtime)  # احدث ملف
print("latest file:", latest_file)

# اقرا اخر 50 سطر بس مش الكل
with open(latest_file, "r", encoding="utf-8", errors="replace") as f:    # ERRORS replacve عشان ما يقرا كود بصيغه تخليه يفكره امر بدال كتابه و بصير يبدلل الاوامر ب اموجي كئنه
    last_lines = deque(f, maxlen=50)  # الديك بيخلي بس اخر 50 سطر

# ابني الباترن اللي بدور عليه
pattern = re.compile("|".join(KEYWORDS), re.IGNORECASE) 
matches = [line for line in last_lines if pattern.search(line)]  # الخطوط اللي فيها ايرور

# اكتب الناتج بملف جديد
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    if matches:
        out.writelines(matches)  # كل لاين فيه newline جاهز
    else:
        out.write("(no matches found)\n")

print(f"wrote {len(matches)} lines to output file")

# لو عدد الايرورات اكثر من الليميت 5 ابعت ايميل
if len(matches) > THRESHOLD:
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"log alert: {len(matches)} issues in {latest_file.name}"
    msg.set_content(
        f"{len(matches)} issues found in {latest_file.name}\n"
        f"check {OUTPUT_FILE.name} for details"
    )

    # حط الملف الناتج  بالايميل  attach
    with open(OUTPUT_FILE, "rb") as fp:
        msg.add_attachment(
            fp.read(),
            maintype="text",
            subtype="plain",
            filename=OUTPUT_FILE.name
        )

    # ابعت الايميل
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()  # connection secure
        s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
        print("email sent ya bro")

else:
    print("less than 5 matches, no email this time")


# الحمدلله اشتغل و  بنفس اليوم haha


#TLS (Transport Layer Security) for seccurity 
#This was really fun i enjoyed learning and applying what i know with what i learned escpically when it acctualy sent the email and was working finally alhamdullah
