# Smart-Home
Voice-Based Home automation system

Using a phone to control common household electrical appliances like lights, fans, etc. and to detect the presence of and possibly identify a person outside the front door, with the video being streamed to a device of the user’s choice.

## Description

* Voice controlled electrical appliances use the phone microphone to take commands. Speech recognition is done by Google’s text to speech API on the phone. The transcripts are mapped to the relevant commands and data is sent to the Raspberry Pi. This method is used for controlling appliances such as lights and fans.

* Lights can also be turned on/off based on the presence or absence of people in a certain area.

* The functioning of porch lights can also be automated using LDR sensors.

* When the presence of someone is detected at the front door, the video being captured by the camera is streamed to the user, and if this person already exists in the database, a facial detection algorithm is run and the identity of the person is determined, and this too is sent to the user.
