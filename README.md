# 🚀 SmartLead AI Agent

> ค้นหา Leads ธุรกิจจริงจาก Google Maps พร้อมวิเคราะห์และร่างข้อความติดต่อด้วย AI อัตโนมัติ

[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/vyada/smartlead-ai-agent)
[![Python](https://img.shields.io/badge/Python-3.13-green)](https://python.org)
[![Gradio](https://img.shields.io/badge/Gradio-6.x-orange)](https://gradio.app)

---

## ✨ ฟีเจอร์หลัก

- 🔍 **ค้นหาธุรกิจจริง** — ดึงข้อมูลจาก Google Maps (Places API) ได้ทันที ทั้งชื่อ ที่อยู่ เบอร์โทร เว็บไซต์ และคะแนนรีวิว
- 🤖 **วิเคราะห์ Lead ด้วย AI** — ให้คะแนนความน่าสนใจของแต่ละ Lead พร้อมสรุปจุดเด่นธุรกิจ
- ✉️ **ร่าง Cold Email อัตโนมัติ** — AI เขียนข้อความติดต่อเฉพาะสำหรับแต่ละธุรกิจพร้อมส่งได้เลย
- 📊 **แสดงผลเป็นตาราง** — ดูข้อมูลทั้งหมดในรูปแบบ DataFrame ที่อ่านง่าย
- ⬇️ **Export CSV** — ดาวน์โหลดข้อมูลทั้งหมดเป็นไฟล์ Excel ได้ทันที

---

## 🖥️ Demo

🔗 **ทดลองใช้งานได้เลยที่:** [huggingface.co/spaces/vyada/smartlead-ai-agent](https://huggingface.co/spaces/vyada/smartlead-ai-agent)

### ตัวอย่างผลลัพธ์
กรอก "ร้านอาหาร" + "เกาะสมุย" → ได้ผลลัพธ์ทันที:

| Business Name | Address | Phone | Rating | Reviews |
|---|---|---|---|---|
| Talay Beach Restaurant Samui | 90 1, Tambon Bo Put, Ko Samui | 077 300 5x | 4.9 | 1271 |
| Day & Night of Koh Samui | G3J7+P3, Bo Put, Ko Samui | 077 332 9x | 4.6 | 2345 |
| Wok & Pan Koh Samui | 1 97 ตำบล บ่อผุด, Ko Samui | 061 206 0x | 4.9 | 570 |

---

## 🛠️ เทคโนโลยีที่ใช้

| เทคโนโลยี | การใช้งาน |
|---|---|
| Python 3.13 | Backend หลัก |
| Gradio 6.x | UI Framework |
| Google Places API (New) | ค้นหาข้อมูลธุรกิจจริง |
| OpenAI GPT-4o-mini | วิเคราะห์ Lead และร่างข้อความ |
| Pandas | จัดการและ Export ข้อมูล |
| Hugging Face Spaces | Hosting |

---

## ⚙️ วิธีติดตั้งและรันเอง

### 1. Clone repo
```bash
git clone https://github.com/YOUR_USERNAME/smartlead-ai-agent.git
cd smartlead-ai-agent
```

### 2. ติดตั้ง dependencies
```bash
pip install -r requirements.txt
```

### 3. ตั้งค่า API Keys
สร้างไฟล์ `.env` แล้วใส่:
```
GOOGLE_PLACES_API_KEY=your_google_places_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 4. รันแอป
```bash
python app.py
```

เปิดเบราว์เซอร์ที่ `http://localhost:7860`

---

## 📋 Requirements

```
gradio>=6.0.0
requests
openai>=1.0.0
pandas
```

---

## 🔑 API Keys ที่ต้องใช้

- **Google Places API (New)** — สมัครได้ที่ [Google Cloud Console](https://console.cloud.google.com)
- **OpenAI API** — สมัครได้ที่ [platform.openai.com](https://platform.openai.com/api-keys)

---

## 💡 Use Cases

- **Freelancer** — รับจ้างหา Lead ให้ธุรกิจอื่น
- **Sales Team** — หาลูกค้าใหม่อัตโนมัติ
- **Marketing Agency** — บริการ Lead Generation ให้ลูกค้า
- **SME** — หาคู่แข่งหรือพันธมิตรในพื้นที่

---

## 👩‍💻 Developer

Built by **Vyada** — AI-powered tools for business growth 🚀
