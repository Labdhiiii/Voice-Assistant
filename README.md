# Sakhi – AI Voice Assistant 🌸

## Project Overview
Sakhi is a desktop-based AI voice assistant developed using Python.  
The project focuses on building an interactive system capable of:
- Understanding spoken user input
- Responding through both text and speech
- Providing a graphical user interface for better interaction

## Current Features

* Voice input using microphone
* Intent-based command processing
* Knowledge retrieval using Wikipedia
* Mathematical query handling
* YouTube Music integration
* Polite conversational responses
* Text and voice output
* Tkinter-based graphical interface

The goal of this project is to explore how real-world voice assistants work internally, including speech processing, intent handling, and system coordination.


---

##  Project Structure & Files Used

```

Voice Assistant/
│
├── sakhi.py           # Main application file (core logic + GUI)
├── main.py            # Initial prototype for basic flow
├── sanity_test.py     # Used to test speech recognition functionality
├── test_edge_tts.py   # Used to verify text-to-speech (Edge TTS) working
├── requirements.txt   # Required Python libraries
└──  README.md          # Project documentation

````

### File Descriptions
- **sakhi.py**  
  The main file containing the complete implementation of the voice assistant, including GUI, speech input, intent processing, and audio output.

- **main.py**  
  Used during early development to test basic execution and library integration.

  Testing files:

- **sanity_test.py**  
  A utility file used to verify that the speech recognition library and microphone input were functioning correctly.

- **test_edge_tts.py**  
  A standalone test script to confirm proper text-to-speech generation using Edge TTS.

---

## How to Run the Project

1. Clone the repository:

```bash
git clone https://github.com/Labdhiiii/Voice-Assistant
```

2. Navigate to the project directory:

```bash
cd Voice Assistant
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the main application:

```bash
python sakhi.py
```

5. Click the **🎤 Speak** button in the GUI and interact using voice commands.


---

## Project Status

🛠️ **In Development**
This project is continuously evolving with new features, improvements, and optimizations being explored. New features and improvements are being added iteratively.
---

## Future Enhancements

* NLP-based intent classification
* Context and memory support/Database integration
* Advancement in GUI 
* Improved semantic understanding of user queries

---

