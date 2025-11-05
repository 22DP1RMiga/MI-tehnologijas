# Ralfs Migals DP4-1

import os
from openai import OpenAI
from dotenv import load_dotenv

# Izdzēš iepriekš izvadīto
os.system('cls')

# ANSI krāsu kodi
RESET = '\033[0m'
CYAN = '\033[96m'

# Ielādē un piešķir konstantam mainīgajam API atslēgu no .env faila
load_dotenv()

# Inicializē OpenAI klientu ar Hugging Face API atslēgu
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HUGGINGFACE_API_KEY"],
)

# Nolasa tekstu no input.txt faila. "r" režīms lasīšanai un UTF-8 kodējums
with open("input.txt", "r", encoding="utf-8") as f:
    user_text = f.read().strip()

# Pārbauda, vai teksts nav tukšs
if not user_text:
    raise ValueError("input.txt is empty")

# Veic pieprasījumu uz modeli ar lietotāja tekstu
completion = client.chat.completions.create(
    model="MiniMaxAI/MiniMax-M2:novita",
    messages=[
        {
            "role": "user",
            "content": user_text
        }
    ],
)


# Print assistant text content with safe fallbacks
# Izvada atbildi no modeļa
msg = completion.choices[0].message
text = None

# Gadījumos, kad atbilde ir pieejama dažādos formātos
if hasattr(msg, "content"):
    text = msg.content
elif isinstance(msg, dict):
    # msg var būt {'role':..., 'content': '...'} or {'role':..., 'content': {'text':'...'}} 
    content = msg.get("content")
    if isinstance(content, dict):
        text = content.get("text") or content.get("content")
    else:
        text = content

# Ja teksts joprojām nav atrasts, izvada pilnu atbildi kā virkni
if not text:
    text = str(completion)

# print(f"{GRAY}{text}{RESET}")
print(text)

# ----- VIKTORĪNAI -------------------------------------------------------------------
print(f"{CYAN}\n----- VIKTORĪNAI -----{RESET}")

# Lietotājs ievada cik atslēgvārdus un jautājumus ģenerēt
num_keywords = int(input("Cik atslēgvārdus izvadīt par tekstu? "))
num_questions = int(input("Cik viktorīnas jautājumus ģenerēt? "))

# Ģenerē atslēgvārdus un viktorīnas jautājumus, izmantojot modeli
keywords_prompt = f"Izveido {num_keywords} atslēgvārdus par šo tekstu:\n\n{user_text}"
questions_prompt = (
    f"Izveido {num_questions} viktorīnas jautājumus par šo tekstu.\n"
    f"Katram jautājumam jābūt ar 4 atbilžu variantiem (A, B, C, D), "
    f"un zem katra jautājuma norādi pareizo atbildi šādā formātā: 'Pareizā atbilde: C'.\n"
    f"Lūdzu savieto atbildes tā, lai atbilžu burti neatkārtotos vairāk kā divas reizes pēc kārtas.\n\n"
    f"Teksts:\n{user_text}"
)

# Veic pieprasījumus uz modeli, lai ģenerētu atslēgvārdus
keywords_completion = client.chat.completions.create(
    model="MiniMaxAI/MiniMax-M2:novita",
    messages=[
        {
            "role": "user",
            "content": keywords_prompt
        }
    ],
)

# Veic pieprasījumus uz modeli, lai ģenerētu viktorīnas jautājumus
questions_completion = client.chat.completions.create(
    model="MiniMaxAI/MiniMax-M2:novita",
    messages=[
        {
            "role": "user",
            "content": questions_prompt
        }
    ],
)

# Izvada ģenerētos atslēgvārdus un jautājumus
print(f"{CYAN}\n--- ĢENERĒTIE ATSLĒGVĀRDI ---\n{RESET}")
print(keywords_completion.choices[0].message.content)
print(f"{CYAN}\n--- ĢENERĒTIE VIKTORĪNAS JAUTĀJUMI ---\n{RESET}")
print(questions_completion.choices[0].message.content)
