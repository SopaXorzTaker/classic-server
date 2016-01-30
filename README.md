# classic-server
A very basic Minecraft Classic server. It only supports 256x64x256 worlds and has only a flat generator.
**Requires Python 3.4 and higher to run!**

Usage
-----
`python main.py` will start the server with the default setttings (see below).

Configuration
-------------
To change the configuration, edit the file `config/config.json` as shown below:

```
{
  "server": {
    "name": "<server name>",
    "motd": "<message of the day>",
    "port": <port, using 25565 is recommended, make sure that no confilicts occur>
  },

  "save": {
    "file": "<to save the map, please specify the path to save the map in>"
  },

  "heartbeat_url": "<Classicube heartbeat by default, change if needed>"
}
```

Legal
-----
Minecraft is a registered trademark of Mojang AB. This project is not in any way affilitated with Mojang AB or Minecraft.
