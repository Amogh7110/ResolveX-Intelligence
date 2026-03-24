import os


def speak_audio(text):

    print("ResolveX speaking:", text)

    os.system(f'say "{text}"')