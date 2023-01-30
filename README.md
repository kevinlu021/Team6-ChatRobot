# Team6-ChatRobot

Brief:
Combining ChatGPT, voice recognition, and a VITS(text-to-speech) model (self-trained or pre-trained). 
Digital approach: make an interface showing the chatbot’s face, implementing emotions and output images with stable diffusion models, other representation methods are also plausible. 
Physical approach: Use servo to blink eyes and control mouth open/close.

Full Description: 

What we want:
A chatbot using ChatGPT as baseline logic that we can interact with.

Programing Language and Tools:
Python
C (Arduino)
3D printing
Modeling skills
Circuit boards and motors etc.
Excel
GitHub

Module Needed:
ChatGPT API			(High priority)
VITS: text-to-speech		(Medium priority, depends on #1)
UI Interface			(Medium priority, depends on #1)
Vosk: voice recognition	(Low priority, depends on #1)

Project Outline (Estimate in hr): 
Write out the API (estimate: 4)
Use ChatGPT’s official API to send and receive messages on the local machine
Convert responded text into voice
Using pre-trained models (estimate: 3)
Train a new model (estimate: 25+)
Searching for clean voice lines, subtitling the voice lines, and organizing them into trainable data requires a significant amount of time. Recommendation: start with using pre-trained models just to test things out
Training takes some time
Build an interface
Software (estimate: 15)
Display chatbot digitally in the screen, build a software user interface for inputting and outputting messages and responses 
Hardware (estimate: 25)
Build a physical model to act as the chatbot and perform certain actions based on the response
*Responses with emotions might be needed
Combined (estimate: 15)
Hologram: An 180-degree hologram with a screen and a reflection sheet.
Display the virtual model on screen to reflect it and make it looks like it's a hologram, details to be discussed.
Voice recognition (estimate: 5)
Use a pre-trained model from GitHub to recognize the user’s voice as input and convert that to text on the local machine

Possible spending: 
	1. ChatGPT’s API. Each account has an 18$, charge once the limit is passed
	2. Hardware interface requires spending
