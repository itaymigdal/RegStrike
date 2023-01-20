
# Regstrike

*RegStrike is a .reg payload generator.*

![](/assets/ui.png)

It's simple, intuitive, lightweight, and dependency free.

The main purpose of the .reg payloads is to add persistence using various techniques (including combination with UAC bypass techniques).
It also capable of messing with some other registry settings. 

Although .reg files are basically textual files, turns out that adding binary data to it won't break it, and the .reg file will still be parsed correctly. This fact lets you obfuscate the .reg file with tons of jibberish data and fool users to believe that this file is unreadable binary. Therefore supply RegStrike with the amount of obfuscation to add and it's got you covered.
