^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for SCURIPTBOT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO
------------------
* clean up the code/create code structure.
* add version number, api keys, default_game etc. to an external init.txt file.
* implement permission structure (Admin/Mod)
* !cleanup -num <number_of_messages> Number of messages which should be deleted default=100
* add option to disable features as admin

KNOWN BUGS
------------------
* crashes randomly with the error message in /log/crash.txt

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
* make !currgame work for all regions
* add current stats (items/kda/cs) to !currgame

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
* !set_game <game_name> changes scuript-bot game 
* added send_typing(destination) to search
* added images to !rekt
* !cleanup to clean up the chat history
  - !cleanup -bot to clean the bot messages
  - !cleanup -commands to clean all messages starting with a "!"
  - !cleanup -self cleans history of message_sender
  - !cleanup -all
* !search sends the results via private message
* !search prints in a single message instead of multiple small ones
* !is_admin returns true if author is SirCarfell, ilakarsu or Scuript_Bot
* !rekt now send images of dank memes
* !search now send messages in chunks smaller than the 2000 char limit but stitches the result together
* -here and -any options were added to !search