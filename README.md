![](https://github.com/sechlol/whatsapp-chat-analyzer/workflows/Run%20Tests/badge.svg)

# WhatsApp Chat Analyzer

This is a small python application that parses exported WhatsApp chat files and create simple statistics on them. It can visualize the statistics in a plot, or export the data as JSON file. It can also export the plot as a .png file.

## How to use it
### 1. Export chats
From the WhatsApp app you can export your chats in .txt format. Open the chat you want to export, click on the three dots on the top-right corner, tap "More", tap "Export Chat". 
I suggest saving your chats in the same directory, it will be easier when using the analyzer.

### Install and setup the app
You'll need **python 3.7** and **pip** to run this application. First, clone this repo somewhere in your file system.You may want to create a virtualenv to install all the requirements in isolation. (Check here: [https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)). Install the requirements with

    pip install -r requirements.txt
If all is fine, you should be able to run the test without errors:

` pytest path_to_project_folder/`
 
### Using the app
With the command line, **cd** into the project root folder.
You can show the help with 

    cd path_to_project_folder/
    python -m chat_analyzer -h

There is one mandatory parameter and other optional parameters you need to provide to run the app. This is the full parameters list:

    python -m chat_analyzer 
                   input_path  
                   [--chat_stats]
                   [--messages_day]
                   [--initiation interval]
                   [--engagement subject]
                   [--word_rank limit min_size] 
                   [--format out_format]
                   [--out out_path]

 - **input_path** *[mandatory]* the path to the chat file(s) you want to analyze. It supports wildcards to parse multiple files. For example: *./some_folder/\*.txt* This will import all txt .files in the folder.
 - **--chat_stats** *[optional]*:  For each chat file, calculates simple stats in the chat: number of messages per person, total word count and average words per message count.
 - **--messages_day** *[optional]*: For each chat file, creates a time series with the number of message per day per person.
 - **--initiation X** *[optional]* For each chat, creates a time series with the initiation score per person. The initiation score answers the question "Who's the one initiating a conversation the most?". Each time a person writes a message after **X hours** after the last message, it's considered a new initiation and her initiation score increases. See the examples for more details.
 - **--engagement X** *[optional]*: In this command, X is the name of a person participating in a chat (for example, your name). You can use this command if you want to know with who you have chatted with over time, and how many messages were exchanged per day in each chat. **NOTE:** this command requires at least two chats to work properly. 
 - **--word_rank X Y** *[optional]*: For each chat, shows the X most used words, which are at least Y characters long.
 - **--format X** *[optional]*: specifies the output format for the analysis. The possible values are:
	 - **json:** (this is the default) saves the raw data in a json file
	 - **png:** saves the resulting plot in a .png file
	 - **plot** shows the plot in a separate UI window.
 - **--out X** *[optional]*: output path for the results. By default is the same as the input path.
