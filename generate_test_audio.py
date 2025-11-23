from gtts import gTTS

text = "Take me to the nearest hospital please."
tts = gTTS(text=text, lang='en')
tts.save("test_audio.mp3")
print("Generated test_audio.mp3")
