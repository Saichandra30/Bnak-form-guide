import pyttsx3
import time
import matplotlib.pyplot as plt
import cv2
import easyocr
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        spoken_text = recognizer.recognize_google(audio).lower()
        print(f"You said: {spoken_text}")
        return spoken_text
    except sr.UnknownValueError:
        speak("I did not understand that. Please try again.")
        return recognize_speech()
    except sr.RequestError as e:
        speak(f"Could not request results; {e}")
        return None

def speak_instructions(instructions):
    for instruction in instructions:
        speak(instruction)
        time.sleep(0.5)
        print("Say 'stop' to interrupt instructions.")
        if recognize_speech() == "stop":
            speak("Instructions stopped.")
            break

def plot_gray(image):
    plt.figure(figsize=(16, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='Greys_r')
    plt.title('Grayscale Image')
    plt.axis('off')
    return plt

def process_bank_file(file_path):
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)

    boxes = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB)
    extracted_text = []
    for (bbox, text, prob) in results:
        (top_left, _, bottom_right, _) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))
        boxes = cv2.rectangle(boxes, top_left, bottom_right, (0, 255, 0), 2)
        extracted_text.append(text)

    plot_gray(image).subplot(1, 2, 2)
    plt.imshow(boxes)
    plt.title('Image with Bounding Boxes')
    plt.axis('off')
    plt.show()

    print("Extracted Text:")
    for text in extracted_text:
        print(text)
    return extracted_text

instructions = [
    "Welcome to the Deposit Account Opening Form!",
    "Step 1: Enter date, branch, and customer ID.",
    "Step 2: Choose account type such as Savings or Current Account.",
    "Step 3: Provide personal details and CIF numbers.",
    "Step 4: Fill out business and operational details.",
    "Step 5: Specify additional details like interest payment options.",
    "Step 6: Request additional services like ATM or Debit card."
]

file_paths = {
    '1': "assets/bank_form_1.png",
    '2': "assets/SBI-NEFT-Form.jpg",
    '3': "assets/AC.png",
    '4': "assets/credit_debit_form.png",
    '5': "assets/details_update_form.png"
}

def ai_voice_bot():
    speak("Hello! I'm here to help you with various banking forms.")
    while True:
        speak("Say a number from 1 to 5 to choose a form, or say 'exit' to quit.")
        print("\nBank Form Processing Menu:")
        print("1. Process Internet Banking Form")
        print("2. Process NEFT/RTGS Application Form")
        print("3. Process Account Opening Form")
        print("4. Process Credit/Debit Card Application Form")
        print("5. Process Details Update Application Form")
        print("6. Exit")

        choice = recognize_speech()
        if "one" in choice or "1" in choice:
            process_bank_file(file_paths['1'])
            speak_instructions(instructions)
        elif "two" in choice or "2" in choice:
            process_bank_file(file_paths['2'])
            speak_instructions(instructions)
        elif "three" in choice or "3" in choice:
            process_bank_file(file_paths['3'])
            speak_instructions(instructions)
        elif "four" in choice or "4" in choice:
            process_bank_file(file_paths['4'])
            speak_instructions(instructions)
        elif "five" in choice or "5" in choice:
            process_bank_file(file_paths['5'])
            speak_instructions(instructions)
        elif "exit" in choice or "6" in choice:
            speak("Goodbye!")
            break
        else:
            speak("I didn't understand that. Please choose a number from 1 to 5.")

if __name__ == "__main__":
    ai_voice_bot()
