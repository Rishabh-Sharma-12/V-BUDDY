import os
import uuid
import logging
import whisper
import string
import speech_recognition as sr
import time 
import pyttsx3
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_groq import ChatGroq
from app.QRCODE.QRCODE import create_qr_code_with_custom
from app.WEATHER.weather import run_weather_func
import random
# -------------------------------
# Setup: Logging and Environment and Directory
# -------------------------------
logging.basicConfig(level=logging.INFO)
load_dotenv()
TEMP_DIR="app/AUDIO"
QR_DIR="app/QRCODE"
WEATHER_DIR="app/WEATHER"
# Conversation cache
MAX_CACHE_SIZE = 10
convo_cache = []

# -------------------------------
# Global Whisper Model Load
# -------------------------------
logging.info("Loading Whisper model...")
whisper_model = whisper.load_model("small")
logging.info("Whisper model loaded.")


# -------------------------------
# loading cache
# -------------------------------

def add_to_cache(role, text):
    """Add conversation to cache and clear after MAX_CACHE_SIZE exchanges."""
    global convo_cache
    convo_cache.append({"role": role, "text": text})

    # Only clear if total exchanges exceed MAX_CACHE_SIZE * 2 (user + bot)
    if len(convo_cache) >= MAX_CACHE_SIZE * 2:
        logging.info("🧹 Clearing conversation cache...")
        convo_cache.clear()
        speak("Alright, starting fresh!")

# -------------------------------
# chat history
# -------------------------------
        
def get_chat_history():
    """Format chat history into a single string for LLM context."""
    history = []
    for turn in convo_cache:
        if turn["role"] == "user":
            history.append(f"User: {turn['text']}")
        else:
            history.append(f"Assistant: {turn['text']}")
    return "\n".join(history)

# -------------------------------
# LLM Setup (Groq + LangChain)
# -------------------------------
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="Llama3-8b-8192"
)

# -------------------------------
# LLM PROMPT SETUP-
# -------------------------------

def invoke_chat_response(user_text: str) -> str:
    prompt = PromptTemplate(
        template = """
            You are a helpful and friendly chatbot that chats like a buddy. Respond to the person politely, briefly, and in a conversational tone. Keep your replies to 1 sentences for casual or short messages.

            However, if the user is asking for detailed help, explanations, or complex information, feel free to use more sentences — but still keep the tone warm, clear, and supportive.

            YOU ARE HAVING A CHAT, and the text provided below is part of the conversation you must respond to:

            {text}
    """,

        input_variables=["text"]
    )
    parser = StrOutputParser()
    chain = prompt | llm | parser
    
    return chain.invoke({"text": user_text})

# -------------------------------
# LLM PROMPT SETUP-
# -------------------------------

def extract_city_for_weather(user_text: str) -> dict:
    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template="""
You are a smart assistant. Extract the city name if the user is asking for weather. 
If not related to weather, return: {{ "city": null }}

{text}
{format_essential}
""",
        input_variables=["text"],
        partial_variables={
            "format_essential": parser.get_format_instructions()
        }
    )

    chain = prompt | llm | parser
    return chain.invoke({"text": user_text})

# -------------------------------
# TTS Engine Setup
# -------------------------------
tts_engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()

def speak_naturally(text):
    fillers = ["Hmm...", "Okay...", "Alright!", "Gotcha!", "Let me think...", "One sec..."]
    speak(random.choice(fillers))
    speak(text)
    time.sleep(0.3)
# -------------------------------
# Audio Functions
# -------------------------------
def record_audio():
    """Record audio from mic and return full file path."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Fine-tuned parameters
        recognizer.energy_threshold = 300         # Mic sensitivity: lower = detects softer speech
        recognizer.pause_threshold = 1.0          # Pause duration before auto-stop
        recognizer.phrase_threshold = 0.2         # Minimum speaking time to consider as a phrase
        recognizer.non_speaking_duration = 0.5  
        print("🎤 Speak now (say 'exit' to quit)...")
        try:
            audio_data = recognizer.listen(source)
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected. Please try again.")
            return None

    temp_name = f"temp_{uuid.uuid4().hex}.wav"
    temp_path = os.path.join(TEMP_DIR, temp_name)
    try:
        with open(temp_path, "wb") as f:
            f.write(audio_data.get_wav_data())
        return temp_path
    except Exception as e:
        print(f"❌ Failed to save audio: {e}")
        return None

def transcribe_audio(audio_path):
    """Transcribe using Whisper."""
    if not audio_path or not os.path.exists(audio_path):
        return ""
    
    print("🧠 Transcribing...")
    result = whisper_model.transcribe(audio_path)
    
    # Clean up
    try:
        os.remove(audio_path)
    except Exception as e:
        print(f"⚠️ Could not delete temp file: {e}")
    
    return result["text"]

def greet_user():
    greetings = [
        "Hey there! I'm here to chat, help, or just listen. What’s on your mind?",
        "Hi! I’m your voice buddy. You can ask me anything — or just talk!",
        "Hello! Ready when you are. Let’s get started, yeah?"
    ]
    speak(random.choice(greetings))

# -------------------------------
# Main Loop
# -------------------------------
def main():
    greet_user()
    while True:
        try:
            audio_path = record_audio()
            text_content = transcribe_audio(audio_path)

            if not text_content.strip():
                fillers_n = [
                    "Oops, I missed that. Wanna say it again?",
                    "Hmm, didn't quite catch that. Can you repeat?",
                    "My ears blinked! Try once more?",
                    "Sorry, could you say that again a little louder?"
                ]
                speak(random.choice(fillers_n))
                continue
            print(f"🗣️ You said: {text_content}")
            
            if "my name is" in text_content.lower():
                name = text_content.split("my name is")[-1].strip().split()[0].title()
                speak(f"Nice to meet you, {name}! I’ll remember that.")
                user_name = name


            if "create qr code" in text_content.lower() or "make qr code" in text_content.lower() or "qrcode" in text_content.lower()or "qr code"in text_content.lower():
                speak_naturally("PLEASE PROVIDE ME LINK OR INFO TO CREATE QR:")
                info=input("Can you please enter information-")
                speak("Generating url")
                create_qr_code_with_custom(info,QR_DIR)
                speak_naturally("the QR code is generated and saved in QRCODE REPO ID")
                continue
            
            if "weather"  in text_content.lower() or "feels in" in text_content.lower():
                weather_llm_result = extract_city_for_weather(text_content)
                city = weather_llm_result.get("city")

                if city:
                    try:
                        # Remove unwanted punctuation, normalize
                        city = city.translate(str.maketrans('', '', string.punctuation)).strip().title()

                        speak_naturally(f"Fetching weather for {city}")
                        weather_info = run_weather_func(city)

                        if weather_info:
                            weather_summary = (
                                f"The weather in {weather_info['city']} is {weather_info['description']} "
                                f"with a temperature of {weather_info['temp']} degrees Celsius, "
                                f"feels like {weather_info['feels_like']}, humidity is {weather_info['humidity']} percent, "
                                f"and wind speed is {weather_info['wind_speed']} meters per second."
                            )
                            speak(weather_summary)
                        else:
                            speak("Sorry, I couldn't get the weather information right now.")
                    except Exception as werr:
                        logging.error(f"🌦️ Weather Error: {werr}")
                        speak("Sorry, I had trouble getting the weather.")
                    continue
                

            if "exit" in text_content.lower()or "Good Bye" in text_content.lower() or "go away" in text_content.lower():
                print("👋 Exiting. Goodbye!")
                speak("Goodbye!")
                break
            
            
            # Add user message to cache
            add_to_cache("user", text_content)

            # Prepare full context for LLM
            full_context = get_chat_history()

            # Get AI response with history
            response = invoke_chat_response(full_context)
            print("📝 Response:", response)
            speak_naturally(response)

            # Add assistant reply to cache
            add_to_cache("assistant", response)

        except Exception as e:
            logging.error(f"⚠️ Error: {e}")
            speak("Something went wrong. Please try again.")

if __name__ == "__main__":
    main()
