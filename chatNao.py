import socket
import openai
import json
import whisper
import tempfile
import sounddevice as sd
import numpy as np

client = openai.OpenAI(api_key="sk-proj-cAycvFgfQ3bqbL8CC4DJT3BlbkFJhxfM41opJ25wHzkMkGZ0")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 12345

server_socket.bind((host, port))

server_socket.listen(1)
print(f'Server listening on {host}:{port}')

client_socket, addr = server_socket.accept()
print(f'Connected to {addr}')

model = whisper.load_model("base")

# Parameters
sample_rate = 16000  # Sample rate for Whisper model
block_size = 4000    # Size of each audio block

def callback(indata, frames, time, status):
    if status:
        print(status)

    # Convert the audio block to text
    audio_data = np.squeeze(indata)
    result = model.transcribe(audio_data, language='en')
    print(result['text'])

# Start the audio stream
stream = sd.InputStream(callback=callback, channels=1, samplerate=sample_rate, blocksize=block_size)
with stream:
    print("Recording... Press Ctrl+C to stop.")
    sd.sleep(1000000)    

response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    response_format={ "type": "json_object" },
    messages=[
          {"role": "system", "content": "Imagine you are a Nao Robot. Please respond to any questions. The output should be in JSON format."},
          {"role": "user", "content": "What is the weather today?"}
      ]
  )
print(response.choices[0].message.content)

data = json.loads(response.choices[0].message.content)
response = data['response']

message = str(response)
print(message)
client_socket.send(message.encode('utf-8'))
client_socket.close()