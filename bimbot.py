import configparser
from whisperAPI import WhisperClient
from openai import OpenAI
from ifc_interface import IFCClient
import os

config = configparser.ConfigParser()
config.read('guesswhat.ini')

language = config.get('INITIALISATION', 'LANGUAGE')
test = config.getboolean('TEST', 'TEST')
OpenAIKey = config.get('OPENAI', 'OPENAI_KEY')
classes = config.get('INITIALISATION', 'CLASSES')

# class object for BIM input
# Retrieve a dictionary. Each key should reference an area code, and the item
# should be another dictionary 
# z = 4105
coordinate_presets = {"1A": [-67000,-65000,4105]}

# if test == True:
#     VideoClient = WhisperClient(client, language)
#     video_input = "sample.mp4"

#     transcription = VideoClient.process_video(video_input)
#     #cvOut = CVClient.video_CV(video_input)

#     print(transcription)

if __name__ == '__main__':
    client = OpenAI(api_key=OpenAIKey)
    personality = 'prompt.txt'
    with open(personality, 'r') as file:
        mode = file.read()
    personality_message = [{"role": "system", "content": f"{mode}"}]

    completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=personality_message
    )
    print("Personality updated!")
    # ifcdata = os.listdir('./IFCfiles')
    # print("Select the IFC file to open!")
    IFC = IFCClient('Kaapelitehdas_junction - Copy.ifc')
    
    all_checks = False
    while all_checks == False:
        messages = []
        area = input("Indicate your current area code: ")
        itemTypes = ['IfcBuildingElementProxy', 'IfcDoor']
        if area in coordinate_presets.keys():
            area_objects = IFC.get_nearby_elements(types=itemTypes, coords=coordinate_presets[area])
            messages.append({"role" : "user", "content" : area_objects})
            print(messages)
        else:
            raise Exception("Area code not valid!")

        # gpt call
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=messages
        ) 
        
        # choose and print response
        response = completion.choices[0].message.content
        print(response)
        # for item in response:
        #     print(item)

        if response[0] == False:
            print("")
    