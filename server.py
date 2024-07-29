import socket
import openai
import json
import time
import speech_recognition as sr
def server_program():
    # Get the hostname
    host = socket.gethostname()
    port = 8054 # Initiate port number above 1024
    server_socket = socket.socket()  # Get instance
    server_socket.bind((host, port))  # Bind host address and port together
    # Configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # Accept new connection
    print("Connection from: " + str(address))
    client = openai.OpenAI(api_key="")
    conversation_history = []
    body_language_tags = ["body language", "bow", "enthusiastic; happy; rapturous; raring; rousing; warm; zestful", "clear; explain; present", "call; hello; hey; hi; yoo-hoo", "not know; unacquainted; undetermined; undiscovered; unfamiliar; unknown", "I; me; my; myself", "negative; no; oppose; refute; reject", "beg; beseech; entreat; implore; please; supplicate", "affirmative; alright; ok; yeah; yes", "explain", "indicate; show; you; your", "app_1", "macarena_dance"]
    while True:
        # Take input from the keyboard
        # message = input("Enter message for client: ")
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        message = input("Enter to listen or type bye for ending.....")
        if message.lower() == 'bye':
            break
        message = recognize_speech_from_mic(recognizer, microphone)
        if message == None:
            continue
        conversation_history.append({"role": "user", "content": message})
        messages = [
            {"role": "system", "content": "Imagine you are a Nao Robot. Please respond to any given questions in at most two lines. Your tone should be friendly and warm. Additionally, choose a body language tag that would help explain your response. Each of these body language tags triggers an animation that you would play. The output should be in string format and should contain the body language tag in the format ^run('name of body language tag'). Chose app_1 as tag name in response if the robot is asked to play an elephant move. The string response should start with ^mode(disabled). Consider the conversation history provided to understand the context. Here are the available body language tags: " + ";".join(body_language_tags)}
        ] + conversation_history
        # Call the OpenAI API with the conversation history
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages
        )
        response_content = response.choices[0].message.content
        # Parse the JSON response
        #data = json.loads(response_content)
        #assistant_response = data['response']
        conversation_history.append({"role": "assistant", "content": response_content})
        #message = str(assistant_response)
        message = str(response_content)
        print("Response content: " + response_content)
        print("Message: " + message)
        conn.send(message.encode())  # Send message to the client
    conn.close()  # Close the connection
def recognize_speech_from_mic(recognizer, microphone):
    """Capture audio from the microphone and transcribe it to text."""
    with microphone as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        transcription = recognizer.recognize_google(audio)
        print(f"Transcription: {transcription}")
        return str(transcription)
    except sr.RequestError:
        # API was unreachable or unresponsive
        print("API unavailable or unresponsive")
    except sr.UnknownValueError:
        # Speech was unintelligible
        print("Unable to recognize speech")
if __name__ == '__main__':
    server_program()