import configparser
from whisperAPI import WhisperClient
from cvAPI import VisionClient
from openai import OpenAI

config = configparser.ConfigParser()
config.read('guesswhat.ini')

language = config.get('INITIALISATION', 'LANGUAGE')
test = config.getboolean('TEST', 'TEST')
OpenAIKey = config.get('OPENAI', 'OPENAI_KEY')
classes = config.get('INITIALISATION', 'CLASSES')

client = OpenAI(api_key=OpenAIKey)

if test == True:
    VideoClient = WhisperClient(client, language)
    CVClient = VisionClient(classes)
    video_input = "sample.mp4"

    transcription = VideoClient.process_video(video_input)
    #cvOut = CVClient.video_CV(video_input)

    print(transcription)

personality = 'prompt.txt'
with open(personality, 'r') as file:
    mode = file.read()
    