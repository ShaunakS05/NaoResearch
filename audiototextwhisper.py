import pyaudio
import wave
import whisper

# Initialize the Whisper model
model = whisper.load_model("base")

# Define audio stream parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

try:
    while True:
        frames = []
        for _ in range(0, int(RATE / CHUNK * 5)):  # 5 seconds of audio
            data = stream.read(CHUNK)
            frames.append(data)
        
        # Save the recorded data to a temporary file
        wf = wave.open('temp.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        # Transcribe the audio
        result = model.transcribe("temp.wav")
        print("Transcription:", result["text"])

except KeyboardInterrupt:
    print("Recording stopped")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()
