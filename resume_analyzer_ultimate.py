import customtkinter as ctk
from tkinter import filedialog
from PyPDF2 import PdfReader
from PIL import Image
import threading
import time

# ---------------- THEME ----------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# ---------------- MAIN WINDOW ----------------
app = ctk.CTk()
app.title("🔥 Resume Analyzer for Royal Mechs")
app.geometry("900x700")

# ---------------- LOGO ----------------
try:
    logo_img = ctk.CTkImage(
        light_image=Image.open("logo.png"),
        size=(120, 120)
    )
    ctk.CTkLabel(app, image=logo_img, text="").pack(pady=5)
except:
    print("Logo not found")

# ---------------- TITLE ----------------
ctk.CTkLabel(
    app,
    text="🔥 Resume Analyzer for Royal Mechs",
    font=("Arial", 24, "bold")
).pack(pady=5)

# ---------------- TABS ----------------
tabs = ctk.CTkTabview(app)
tabs.pack(expand=True, fill="both", padx=20, pady=10)

tab1 = tabs.add("📌 Skills")
tab2 = tabs.add("📂 Projects")
tab3 = tabs.add("📊 Analysis")

# ---------------- INPUTS ----------------
skills_entry = ctk.CTkEntry(tab1, width=500, placeholder_text="Enter skills (Python, CAD, ANSYS...)")
skills_entry.pack(pady=20)

projects_entry = ctk.CTkEntry(tab2, width=500, placeholder_text="Describe your projects")
projects_entry.pack(pady=20)

# ---------------- PDF UPLOAD ----------------
resume_text = ""

def upload_pdf():
    global resume_text
    file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file:
        reader = PdfReader(file)
        resume_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text.lower()
        upload_label.configure(text="✅ PDF Loaded Successfully")

ctk.CTkButton(tab2, text="📄 Upload Resume (PDF)", command=upload_pdf).pack(pady=10)
upload_label = ctk.CTkLabel(tab2, text="")
upload_label.pack()

# ---------------- PROGRESS BAR ----------------
progress = ctk.CTkProgressBar(tab3, width=400)
progress.pack(pady=20)
progress.set(0)

# ---------------- RESULT ----------------
result_label = ctk.CTkLabel(tab3, text="", font=("Arial", 14))
result_label.pack()

# ---------------- SUGGESTIONS ----------------
suggestions_box = ctk.CTkTextbox(tab3, width=500, height=150)
suggestions_box.pack(pady=10)

# ---------------- ANIMATION ----------------
def animate_bar(target):
    for i in range(target + 1):
        progress.set(i / 100)
        time.sleep(0.02)

# ---------------- ANALYSIS FUNCTION ----------------
def analyze():
    text = (skills_entry.get() + " " + projects_entry.get() + " " + resume_text).lower()
    score = 0
    feedback = []

    if "python" in text:
        score += 15
        feedback.append("🔥 Python detected")
    else:
        feedback.append("⚠️ Add Python")

    if "solidworks" in text or "cad" in text:
        score += 15
        feedback.append("👍 CAD skill strong")
    else:
        feedback.append("⚠️ Add CAD tools")

    if "ansys" in text:
        score += 15
        feedback.append("🔥 Simulation skill present")
    else:
        feedback.append("⚠️ Add ANSYS")

    if "cfd" in text:
        score += 15
        feedback.append("🔥 CFD knowledge detected")
    else:
        feedback.append("⚠️ Add CFD")

    if len(projects_entry.get()) > 20:
        score += 20
        feedback.append("👍 Good project description")
    else:
        feedback.append("⚠️ Improve project description")

    if score >= 70:
        status = "🔥 Excellent"
        color = "green"
    elif score >= 40:
        status = "👍 Good"
        color = "orange"
    else:
        status = "⚠️ Needs Improvement"
        color = "red"

    threading.Thread(target=animate_bar, args=(score,)).start()

    result_label.configure(
        text=f"Score: {score}/100\n{status}",
        text_color=color
    )

    suggestions_box.delete("1.0", "end")
    suggestions_box.insert("end", "\n".join(feedback))

# ---------------- BUTTON ----------------
ctk.CTkButton(app, text="🚀 Analyze Resume", command=analyze).pack(pady=10)

# ---------------- FOOTER ----------------
ctk.CTkLabel(
    app,
    text="Developed using AI-based logic by Vetrivel VP (23BMV1057)",
    font=("Arial", 10)
).pack(pady=5)

# ---------------- RUN ----------------
app.mainloop()