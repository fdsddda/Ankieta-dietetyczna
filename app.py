import streamlit as st
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText

# KONFIGURACJA ODBIORCY
TARGET_EMAIL = "piotrbartynski@gmail.com"

st.set_page_config(page_title="Ankieta Dietetyczna - Piotr", layout="centered")

# LISTA PYTAŃ (Dokładnie wg Twojej listy - 116 pozycji)
questions = [
    "Imię i nazwisko", "Adres e-mail", "Telefon", "Data urodzenia", "Waga", "Wzrost", 
    "Wykonywany zawód", "Godziny pracy poza domem", "Obwód pasa", "Obwód bioder", 
    "Obwód uda", "Obwód ramienia", "Obwód klatki piersiowej", 
    "Czy występowały u Ciebie choroby? (Podaj numer odpowiedzi)", "Inne zdiagnozowane choroby",
    "Kiedy wystąpiły objawy?", "Czy występują alergie?", "Opis alergii", 
    "Czy występują nietolerancje pokarmowe?", "Opis nietolerancji", "Ile razy dziennie się wypróżniasz?",
    "Czy regularnie dochodzi do wypróżnień?", "Choroby przewlekłe w rodzinie",
    "Czy przyjmujesz leki farmaceutyczne?", "Jakie leki?", "Pora przyjmowania leków",
    "Suplementy diety (jakie, ile, kiedy?)", "Zabiegi operacyjne", "Urazy (ostatnie 6 miesięcy)",
    "Zioła i substancje naturalne", "Ostatnie badania krwi", "Ciśnienie krwi",
    "Aktualny tryb życia", "Środki transportu", "Godzina wstawania", "Godzina śniadania",
    "Atmosfera śniadania", "Ile godzin spędzasz w pracy?", "Ostatni posiłek (godzina)",
    "Godzina pójścia spać", "Ile godzin śpisz?", "Czy sen jest jednostajny?", 
    "Czy wysypiasz się?", "Energia w trakcie dnia", "Spadki energii", 
    "Poziom stresu (1-10)", "Odporność na stres (1-10)", "Aktywność fizyczna (jaka i częstość)",
    "Plan treningowy", "Problemy z masą ciała w przeszłości", "Wahania wagi",
    "Zmiana wagi (ostatnie 6 miesięcy)", "Nadwaga w dzieciństwie", "Otyłość w rodzinie",
    "U kogo otyłość?", "Docelowa waga", "Ile posiłków dziennie?", "Częstość warzyw",
    "Częstość owoców", "Obiad z dwóch dań?", "Samodzielne gotowanie?", "Posiłki na mieście",
    "Fastfoody", "Uwaga na kalorie?", "Odstępy między posiłkami", "Podjadanie",
    "Atmosfera posiłków", "Ilość płynów (szklanki)", "Napoje gazowane", "Rodzaj wody",
    "Ilość kawy i herbaty", "Rodzaj kawy", "Mleko do kawy", "Słodzenie kawy", 
    "Rodzaj herbaty", "Ilość herbaty", "Słodzenie herbaty", "Dodatki do herbaty",
    "Pora picia kawy/herbaty", "Częstość alkoholu", "Rodzaj i ilość alkoholu",
    "Papierosy/tytoń", "Częstość tytoniu", "Ilość paczek tygodniowo", "Inne substancje",
    "Ulubione produkty", "Nielubiane produkty", "Czy dieta jest monotonna?", 
    "Pieczywo", "Produkty pełnoziarniste", "Najczęstsze węglowodany", "Produkty wysokotłuszczowe",
    "Tłuszcze do smażenia", "Jajka", "Nabiał", "Mięso", "Ulubione mięso", 
    "Przygotowanie mięsa", "Sosy, majonezy, fixy", "Ulubione sposoby gotowania",
    "Preferowane smaki", "Przyprawy", "Kiedy największy apetyt?", "Poczucie sytości",
    "Oczekiwania po konsultacji", "Cel współpracy", "Dodatkowe informacje o Tobie",
    "Śniadanie (dzienniczek)", "Obiad (dzienniczek)", "Kolacja (dzienniczek)",
    "Przekąski (dzienniczek)", "Napoje (dzienniczek)", "Regularna miesiączka?",
    "Długość cyklu", "Ból podczas menstruacji (1-10)", "Antykoncepcja hormonalna", "Stała kontrola ginekologa"
]

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

st.title("Asystent Głosowy Piotra 🎤")

if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.write(f"### Pytanie {st.session_state.step + 1} z {len(questions)}")
    st.info(f"**{q}**")

    # Komponent JS do automatycznego nagrywania
    # Kliknięcie "Dalej" aktywuje mikrofon dla kolejnego pytania
    js_code = f"""
    <script>
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'pl-PL';
    recognition.interimResults = false;
    
    recognition.onresult = function(event) {{
        var text = event.results[0][0].transcript;
        window.parent.postMessage({{type: 'streamlit:setComponentValue', value: text, key: 'voice'}}, '*');
    }};

    // Automatyczny start przy załadowaniu komponentu
    recognition.start();
    </script>
    """
    
    # Przechwytywanie wyniku z JavaScript
    voice_answer = components.html(js_code, height=0)
    
    user_input = st.text_input("Twoja odpowiedź (mów lub pisz):", key=f"input_{st.session_state.step}")

    if st.button("Następne pytanie ➡️"):
        st.session_state.answers[q] = user_input
        st.session_state.step += 1
        st.rerun()

else:
    st.success("Ankieta zakończona! Wszystkie dane zostały zapisane.")
    if st.button("Wyślij raport do Piotra 📩"):
        report = "\n".join([f"{k}: {v}" for k, v in st.session_state.answers.items()])
        # Tutaj wyślemy maila (wymaga sekretów w Streamlit)
        st.code(report)
        st.balloons()