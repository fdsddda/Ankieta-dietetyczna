import streamlit as st
from streamlit_mic_recorder import speech_to_text

# KONFIGURACJA
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

questions = [
    "Imię i nazwisko", "Adres e-mail", "Telefon", "Data urodzenia", "Waga", "Wzrost", 
    "Wykonywany zawód", "Godziny pracy", "Obwód pasa", "Obwód bioder"
    # ... (tutaj dopisz resztę swoich 116 pytań)
]

st.title("Twoja Ankieta Dietetyczna 🎤")

if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    st.subheader(f"Pytanie {st.session_state.step + 1}: {q}")
    
    # PROFESJONALNY PRZYCISK GŁOSOWY
    # Kliknięcie tutaj aktywuje mikrofon i automatycznie wpisuje tekst
    text = speech_to_text(
        language='pl',
        start_prompt="KLIKNIJ I MÓW 🎤",
        stop_prompt="ZAKOŃCZ NAGRYWANIE ✅",
        just_once=True,
        key=f'speech_{st.session_state.step}'
    )

    if text:
        st.success(f"Usłyszałem: {text}")
        st.session_state.answers[q] = text

    # Pole ręczne, gdyby klient wolał jednak coś dopisać
    manual_input = st.text_input("Popraw lub wpisz ręcznie:", value=text if text else "", key=f"manual_{st.session_state.step}")

    if st.button("Następne pytanie ➡️"):
        final_answer = manual_input if manual_input else text
        if final_answer:
            st.session_state.answers[q] = final_answer
            st.session_state.step += 1
            st.rerun()
        else:
            st.warning("Proszę odpowiedzieć na pytanie.")

else:
    st.success("Ankieta gotowa!")
    st.write(st.session_state.answers)
