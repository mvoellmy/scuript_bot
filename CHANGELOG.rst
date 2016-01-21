^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for SCURIPTBOT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO
------------------
* clean up the code/create code structure.
* add version number, api keys, etc to an external init.txt file.
* implement permission structure (Admin/Mod)
* !flush to clean up the chat history

  - !flush -bot to clean the bot messages
  - !flush -commands to clean all messages starting with a "!"
  - !flush -1000 Number of messages which should be deleted. Default=100
* make !currgame work for all regions
* add current stats (items/kda/cs) to !currgame
* add option to disable features as admin
* search should only display the first 5 elements or send a private message
* search should print in a single message instead of multiple small ones
* change scuript-bot game to something funny :^)
* add send_typing(destination) to search

KNOWN BUGS
------------------

NICE TO HAVE FEATURES
------------------
* !rekt with sound
* !runtime, time since start of bot
* !soundtest returns voice of the person sending the command
* Admin commands for the bot such as (!runtime, !restart, !pull, !shutdown)
* !currgame for Steam/CSGO
* add sound board
* !stat to display all the statuses of t he bots
* add twitch emotes


0.0.1 (2016-02-01)
------------------
* !join URL joins the specified URL
* !help lists all available commands
* A welcome message with instructions sends instruction how to setup the mic
* !tutorial send the same instructions on the server 

0.0.2 (2016-03-01)
------------------
* !currgame <summoner_name> shows the current game status of the summoner and and some basic ranked stats for the active champion.

0.0.3 (2016-03-01)
------------------
* fixed known bug with !currgame on certain champions, icons for all champions should be displayed now.
* added logging framework
* search now takes whole history in to account
* !callouts <map_name> sends image with callouts for cs go
