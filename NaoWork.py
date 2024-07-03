from naoqi import ALProxy
import argparse
import time
import socket



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#IP = "192.168.1.128"
IP = "192.168.1.30"
host = '127.0.0.1'
port = 12345
tts = ALProxy("ALTextToSpeech", IP, 9559)
#aad = ALProxy("ALAudioDevice", IP, 9559)
asr = ALProxy("ALSpeechRecognition", IP, 9559)
motion = ALProxy("ALMotion", IP, 9559)
memory = ALProxy("ALMemory", IP, 9559)

# prompt = {
#     "Imagine you are a Nao Robot. Please give a response to the following question: {question}"
# }

#   prompt = (
#       "Based on your knowledge, think about the subject that " +  str(person) + " is commonly known for. Does the subject matter in {text} align with the topics that " + str(person) + " usually talks about? The context is: " + str(context) + ". Look for satire and what is plausible in real life. Please provide your answer in json."
#   )

  #content = ("Provide a numerical answer (1 being definitely never aligns, 2 being probably never aligns, 3 being neutral either way, 4 being probably aligns, and 5 being definitely aligns.) Then, give an explanation of why {person} aligns with the {text} in json")

client_socket.connect((host, port))
print('Connected to server {}:{}'.format(host,port))

message = ""
while True:
    message = client_socket.recv(1024).decode('utf-8')
    if message:
        print(str(message))
        break
client_socket.close()

tts.say(str(message))
#memory.removeData("key")
# tts.say("Hi I am now robot")
# tts.say("I will first do an elephant sound")
# memory.insertData("key", "a1")
# time.sleep(20)
# memory.removeData("key")

# tts.say("now I will do a mouse sound")
# memory.insertData("key", "a2")

#walk task
# tts.say("I can walk!")
# motion.move(1,0,0)

# righthandName = 'RHand'
# lefthandName = 'LHand'
# motion.closeHand(righthandName)
# motion.openHand(righthandName)
# motion.closeHand(lefthandName)
# motion.openHand(lefthandName)

#memory.insertData("testData", "Hello")
# asr.setLanguage("English")
# vocabulary = ["yes", "no", "please"]
# asr.pause(True)
# asr.setVocabulary(vocabulary, True)
#tts.say("Hello! I am NAO, a humanoid robot designed to interact with and assist humans. Equipped with advanced sensors and cameras, I can perceive my surroundings and respond intelligently. I am capable of recognizing speech, gestures, and faces, making me a great companion for educational and research purposes. I can walk, talk, and even dance to make learning fun and engaging. Lets explore the world of robotics together!")

#print(aad.getOutputVolume())

# asr.subscribe("Test_ASR")
# while True:
#     print(asr.WordRecognized)

