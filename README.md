# traveloke

## Requirements
- Python >= 3.10
- Gemini API key from https://aistudio.google.com/app/apikey

## Installation
0. Clone repo
```bash
git clone https://github.com/khoileuser/traveloke
```

1. Create `.env` file with this content
```bash
GEMINI_API="yoursupersecretapikey"
```

2. Virtual environment
- Windows
```bash
python -m venv venv && venv\Scripts\activate
```
- Linux/Mac
```bash
python -m venv venv ; source venv/bin/activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Run development server
```bash
fastapi dev main.py
```

5. Run production server
```bash
fastapi run main.py
```