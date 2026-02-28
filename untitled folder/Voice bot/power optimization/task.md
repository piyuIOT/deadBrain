Hardware:
ESP32S3R8 based Amoled watch module which used for a small voice assistant bot.
this module has 2 mic, wifi, sd storage, battery support, and display, and speaker, so we are using it to record and stream audio to a ai backend via wifi which then streams back audio answer through it
it also record the conversation for referencing and further training

Task:
Optimize power consumption of the whole module
Read the [wiki](https://www.waveshare.com/wiki/ESP32-S3-Touch-AMOLED-1.75) first, then check relevant the pdfs in this folder (primarily used ics)

Thought process so far:
- Use ULP core for interrupt of touch interface of the display so as to wake the module
- when module is up, user press chat button then start mic and start listening and recording to sd, simultaneously start connection to wifi for starting streaming as soon as it connects.
- only keep the wifi connected for the duration of sending the voice and recieving the response and a small time after that for further conversation without reconnection time.
- disconnect wifi in short time if no conversation was recieved. 
- slowly dim display and then let the system go to ULP core and only check the interrupt again
- during the time display is off, always remember last conversation id to let user continue the convo or start a new one. or maybe not do this and give a option for it, and if user select continue, then connect first to wifi, check the last convo, and continue there?
- keep different modules powerred down or in low energy mode when not in use via help of axp2101 and esp32 itself (whereever posssible)
- all the things that are not used should always stay in low power mode
- thing of all other ways to handle power consumption