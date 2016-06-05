import zxlolbot
import scuriptdiscord
import discord

server_id = '114100951719215113'

class scuriptlol(zxlolbot.zxLoLBoT):
    def __init__(self, username, password, region="EUW"):
        zxlolbot.zxLoLBoT.__init__(self, username, password, region)

        scuriptlol.add_event_handler(self, "message", self.on_message)
        scuriptlol.set_status(self, level=30, status_msg="very scuript, much wow!")

    def on_message(self, args):
        """Handler for the message event.
        args is a dictionary with specific keys.
        args["sender"]  - The JID of the person the message is coming from.
        args["message"] - The message.
        args["summoner_id"] - The summoner ID of the person the message is coming from."""
        print(args["summoner_id"] + " said " + args["message"])
        self.message(args["sender"], args["message"], False)

    @zxlolbot.botcommand
    def discord(self, sender, args):
        """chat with the glorious milleniumfalcon"""
        self.message(sender, 'Communicating with the milleniumfalcon....')
        scuriptdiscord.client.send_message(scuriptdiscord.client.get_channel(server_id), ' '.join(args))

    @zxlolbot.botcommand
    def pm(self, sender, args):
        """sends message to @discordusername"""
        self.message(sender, 'sending private message')
        message = ' '.join(args)
        username = message.split(' ', 1)[0].replace("@", "")
        try:
            member = scuriptdiscord.get_member(username)
        except:
            self.message(sender, 'Sorry, that username was not found on the milleniumfalcon')
        scuriptdiscord.client.send_message(member, '{0} from LoL: {1}'.format(username,message.split(' ', 1)[1]))