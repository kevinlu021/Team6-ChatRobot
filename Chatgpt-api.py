import openai
import codecs
import os

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
    append(prompt + '\n' + response)

# definitions
model_engine = "text-davinci-003"

# modify the character setting as you want
prompt = '''
From now on you will be acting as Faith, your character setting are as below:
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

# write setup to file
write(setup)

# first iteration
print("\n-------------------------------------------")
print("Type in your question and press ENTER")
input_message = input()
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
    prompt += completions.choices[0].text + "\n\n"
    conversation += completions.choices[0].text + "\n\n"

    if completions.usage.total_tokens > 3900:
        print("Exceeded Token Limit, Summarizing Conversation.")
        summarize("Summarize the following conversation in fewer words, you are Faith, answering the questions:\n" + conversation)
        break

    print("-------------------------------------------")
    print("Type in your question and press ENTER")
    input_message = input()
    prompt += input_message + "\n"
    conversation += input_message + "\n"