# EasyDoctorsnote

![Alt text](./resources/icon_small.png)

An app that simplifies the process of sending a doctor's note to school. It uses SMTP with a username and password.
Note: OAuth has not yet been implemented.

## Description
When your child is sick, it's important to notify the school about their absence, and you may also need to cancel lunch for those days.
This app simplifies the process by allowing you to select a specific date or date range and automatically send the necessary emails.
To use the app, you'll need to configure it with an SMTP server and a password. Below are some screenshots:

![Alt text](./images/main_screen_small.png)
![Alt text](./images/pick_date_small.png)
![Alt text](./images/doctors_note_small.png)

## Features
This project is built on the [Kivy](https://kivy.org/) framework following an MVVM pattern and utilizes [Buildozer](https://github.com/kivy/buildozer) for packaging an APK file. It does 
not access any information on your phone. It assumes the use of [Conda](https://docs.conda.io/en/latest/).

## Download 
If you just want to download the APK file to your Android phone, please follow the instructions (to be added).

## Prerequisites
- An email provider that allows sending emails using a username and password.
- [KivyMD](https://github.com/kivymd/KivyMD) version 2.0.1.dev0.

## Installation
1) Create the conda environment from the environment.yml to make sure you have all the required packages:
   'conda env create -f environment.yml'
2) Activate the newly created environment called easy_doctorsnote:
   'conda activate easy_doctorsnote'
3) If you want to test the program on your computer, you can do:
   'python main.py'
4) To build the app for an Android phone (an APK file), run:
   'buildozer -v android debug'
   This will create a directory called 'bin' and inside the APK file.
7) If you have ADB installed on your phone and the phone is connected to your computer, you can now run:
   'adb install bin/*.apk'
8) For debugging the app, you can use:
   'adb logcat | grep python'

## Usage
Before the first use, you need to fill in the required information in the configuration panel. In addition to the SMTP
information, you can specify your child's name, your own name, the recipients, etc. This information is used to create the corresponding email text.
