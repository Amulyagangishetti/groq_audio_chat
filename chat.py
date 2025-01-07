from google.colab import files
from groq import Groq
client = Groq()
def process_audio(file_path):
    with open(file_path, "rb") as file:
        translation = client.audio.translations.create(
            file=(file_path, file.read()), 
            model="whisper-large-v3", 
        )
        return translation.text
def process_query(query, transcription):
    client = Groq()
    messages = [
        {"role": "user", "content": [{"type": "text", "text": query}]},
        {"role": "user", "content": [{"type": "text", "text": f"Transcription of the audio: {transcription}"}]}
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.2-90b-vision-preview",
    )
    return chat_completion.choices[0].message.content
uploaded = files.upload()
for audio_file_name in uploaded.keys():
    with open(audio_file_name, 'wb') as f:
        f.write(uploaded[audio_file_name])

    transcription = process_audio(audio_file_name)
    print(f"Transcription for {audio_file_name}:")
    print(transcription)
query = input("Enter your query: ")
response = process_query(query, transcription)
