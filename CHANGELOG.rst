^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for SCURIPTBOT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO
------------------
* make !currgame work for all regions 
* !stat to display all the statuses of t he bots
* add current stats (items/kda/cs) to !currgame
* add option to disable features as admin
* add sound board
* search should only display the first 5 elements or send a private message
* search should print in a single message instead of multiple small ones
* change scuript-bot game
* add send_typing(destination) to search
* add twitch emotes

KNOWN BUGS
------------------

NICE TO HAVE FEATURES
------------------
* !rekt with sound
* !runtime, time since start of bot
* !soundtest returns voice of the person sending the command
* Admin commands for the bot such as (!runtime, !restart, !pull, !shutdown)
* !currgame for Steam/CSGO

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
* !callouts <map_name> send image with callouts for cs go
