
# Regstrike

*RegStrike is a .reg payload generator.*

![](/assets/ui.PNG)

It's simple, intuitive, lightweight, and dependency free.

The main purpose of the .reg payloads is to add persistence using various techniques (including combination with UAC bypass techniques).
It also capable of messing with some other registry settings. 

Although .reg files are basically textual files, turns out that adding binary data to it won't break it, and the .reg file will still be parsed correctly. This fact lets you obfuscate the .reg file with tons of jibberish data and fool users to believe that this file is unreadable binary. Therefore supply RegStrike with the amount of obfuscation to add and it's got you covered.

One of the main reasons one would want to use .reg as a payload is because of the very low detection rate by AV products, and apparently obfuscation even lowering it more. 

For Example here is a .reg payload example that uses the [Silent Process Exit](https://pentestlab.blog/2020/01/13/persistence-image-file-execution-options-injection/) technique for persistence:

![](/assets/not_obf.PNG)

And its very low detection on VT:

![](/assets/not_obf_vt.PNG)

Adding 3 MB of binary obfuscation:

![](/assets/obf.PNG)

Will make it zero :smiling_imp:

![](/assets/obf_vt.PNG)

RegStrike is easily extendable for more persistence methods / registry values that attacker would want to add.
Feel free to open PRs and issues and contact me at ([Gmail](itaymigdal9@gmail.com) | [Linkedin](https://www.linkedin.com/in/itay-migdal-b91821116/) | [Twitter](https://twitter.com/0xTheBruter)).
