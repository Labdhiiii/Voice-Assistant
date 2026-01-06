import asyncio
import edge_tts
import os

async def main():
    text = "Hello. This is Edge text to speech. If you hear this, it is working."
    voice = "en-IN-NeerjaNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("test.mp3")

    # Play using Windows default player
    os.system("start test.mp3")

asyncio.run(main())
