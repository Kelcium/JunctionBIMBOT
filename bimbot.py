import configparser
from whisperAPI import WhisperClient
from openai import OpenAI

config = configparser.ConfigParser()
config.read('guesswhat.ini')

language = config.get('LANGUAGE', 'LANGUAGE')
test = config.getboolean('TEST', 'TEST')
OpenAIKey = config.get('OPENAI', 'OPENAI_KEY')

client = OpenAI(api_key=OpenAIKey)

if test == True:
    VideoClient = WhisperClient(client, language)
    video_input = "sample.mp4"

    video, audio, transcription = VideoClient.process_video(video_input)

    print(video, audio, transcription)
