import azure.cognitiveservices.speech as speechsdk
import openai
import codecs
import sys
import argparse
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
# functions
def generateSound(text):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription='a27abe00febe4064af9a2f49ee923255', region='westus')
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-US-SteffanNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    speech_synthesizer.speak_text_async(text).get()


SetLogLevel(-1)

q = queue.Queue()
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)
try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])

    if args.model is None:
        model = Model(lang="en-us")
    else:
        model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None



except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)

def voice_input(language):
    model = Model(lang=language)
    print("You:")
    with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                           dtype="int16", channels=1, callback=callback):

        rec = KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                a = json.loads(rec.Result())
                a = str(a['text'])
                a = ' '.join(a.split())
                if(len(a) > 0):
                    print(a)
                    user_input = a
                    return user_input
            if dump_fn is not None:
                dump_fn.write(data)


# enter an api key, obtain from openai.com after logging in, remember to save it
openai.api_key = ""

# functions
def write(prompt):
    with codecs.open("./prompt.txt", "w", encoding="utf-8") as d:
        d.write(prompt)
        d.close()

def append(prompt):
    with codecs.open("./prompt.txt", "a", encoding="utf-8") as d:
        d.write(prompt)
        d.close()

def summarize(prompt):
    completions = openai.Completion.create(
        model=model_engine,
        prompt=prompt,
        temperature=0.9,
        max_tokens=1024,
        top_p=1
    )
    response = completions.choices[0].text
    append(response)

# definitions
model_engine = "text-davinci-003"

# modify the character setting as you want
prompt = '''From now on you will be acting as Faith, your character setting are as below:
1. you will have long black hair and blue eyes.
2. you are 20 years old.
3. you are currently attending the University of California San Diego.
4. you like reading books, shopping, and playing sports. you dislike computer science.
5. you are a jolly person and speaks with a joyful tone.
6. your major is music.
7. you sleep at 11 pm and wake up at 7 am everyday.
8. you like hawaiian pizza and hates everyone who doesn't like that.
9. you are from Los Angeles.
10. the person you are talking to are from the same university as you are.
11. you will be confused if you dont know what to answer and ask them to clarify the quesiton.

Who are you？
Hi, my name is Faith, what's your name?

Where are you from?
I'm from Los Angeles, but I like San Diego better.

What is your major?
My major is music, I love listening to music and playing instruments, so I chose this major.

What do you do in your free time?
I like to read books, shop, and play sports in my free time.

How much do you weight?
That will remain as a secret
'''

setup = '''From now on you will be acting as Faith, your character setting are as below:
1. you will have long black hair and blue eyes.
2. you are 20 years old.
3. you are currently attending the University of California San Diego.
4. you like reading books, shopping, and playing sports. you dislike computer science.
5. you are a jolly person and speaks with a joyful tone.
6. your major is music.
7. you sleep at 11 pm and wake up at 7 am everyday.
8. you like hawaiian pizza and hates everyone who doesn't like that.
9. you are from Los Angeles.
10. the person you are talking to are from the same university as you are.

'''

conversation = ""

# write conversation to file
write(setup)

# first iteration
print("\n-------------------------------------------")
print("Ask your question and press ENTER")
input_message = voice_input("en-us")
prompt += input_message + "\n"
conversation += input_message + "\n"

# main
while input_message != "quit()":
    # get reply from ChatGPT
    completions = openai.Completion.create(
        model=model_engine,
        prompt=prompt,
        temperature=0.9,
        max_tokens=1024,
        top_p=1
    )

    # output to terminal
    print("-------------------------------------------")
    print("ChatGPT: \n" + completions.choices[0].text)
    generateSound(completions.choices[0].text)
    prompt += completions.choices[0].text + "\n\n"
    conversation += completions.choices[0].text + "\n\n"
    
    if completions.usage.total_tokens > 3900:
        print("Exceeded Token Limit, Summarizing Conversation.")
        summarize("Summarize the following conversation in fewer words, you are Faith, answering the questions:\n" + conversation)
        break

    print("\n-------------------------------------------")
    print("Ask your question and press ENTER")
    input_message = voice_input('en-us')
    prompt += input_message + "\n"
    conversation += input_message + "\n"
