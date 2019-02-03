


# Brain Extension - Vocabulary

A vocabulary training app and platform that is reduced to the essence. It uses data analytics features, artificial intelligence and machine learning to maximise learning speed.

## Motivation

I love learning languages. And I learned a few of them. To prevent forgetting and to increase my vocabulary, constant training is needed. Doing that via flipcards is usually my way, but it becomes problematic over time for a range of reasons and so I am building an app. 

## Key features

The initial version of the application will be available by end of 2017 and will have these features:

- Subscribe as a user
- Chose languages you are studying
- Add words by adding them one by one and obtain a automatic translation
- Add a sentence and get translation
- Add a piece of text and statistically get the words you don't know and add them ot the list of words to learn
- Add an URL from a blog post or newspaper and obtain all words you don't know and add them to the vocabulary list sorted by importance. And importance it the frequency of occurrence in texts. 
- Learn vocabulary from a mobile phone
- Learn vocabulary from a browser on notebook/PC
- Add words by sending them from a Google Spreadsheet to the application.

## technology stack

**Frontend:**

- No frameworks are being used
- Plain vanilla HTML, CSS, JavaScript

**Backend:**
- Python
- Postgresql


## Architecture

The application is a single-page application that does not use specific JavaScript frameworks. The architecture is as follows: 

When the application is access the server sends a minimal HTML code that loads a few JavaScript classes:

- A class to add and remove HTML components on the GUI
- A class that controls the user interaction and data flow
- A class that handles communication with the backend. This is done via JSON objects that are sent and received via AJAX calls.

## icons

https://www.flaticon.com/search?word=more