import discord, os, sys
from discord.ext import commands

dict = {}
def alert(who, string):
    print(who + ' ran ' + string)

bot = commands.Bot(command_prefix = 'bot pls ')
bot.remove_command('help')

@bot.event
async def on_ready():
    f = open('solutions/list.txt')
    for line in f.readlines():
        val = line.split()[0]
        dict[line[len(val) + 1 : -1]] = val

    print('bot is ready.')

@bot.event
async def on_message(message):
    if message.content.strip().startswith('bot pls'):
        cmd = message.content[7:].strip()
        alert(message.author.name, cmd)

        if cmd == 'help' or cmd == 'man' or cmd == 'hel' or cmd == 'h':
            delim = '```\n'
            officialhelp = 'bot pls official x - official solution for the x problem\n'
            writehelp = 'bot pls write (or say) - sends a message to the current channel.\n'
            deletehelp = 'bot pls delete x (messages) - deletes the last x (defaults to 0) messages, excluding the one invoking this command.\n'
            restarthelp = 'bot pls restart (or reboot, shut down or stop) - restarts the bot.\n'
            arehelp = 'bot pls are you online? (or any variation) - checks if the bot is there.\n'
            await message.channel.send(delim + 'Currently featuring the following commands:\n' + officialhelp + writehelp + deletehelp + restarthelp + arehelp + delim)

        elif cmd.startswith('official') or cmd.startswith('offic') or cmd.startswith('oficial'):
            arg = cmd[len(cmd.split()[0]):].strip().lower()
            try:
                int(arg)
            except ValueError:
                arg = dict[arg]
        
            f = open('solutions/'+ arg + '.txt', 'r')
            await message.channel.send(file = discord.File('solutions/' + arg + '.txt'))
        
        elif cmd.startswith('say') or cmd.startswith('sa') or cmd.startswith('tell') or cmd.startswith('write') or cmd == 'w':
            arg = cmd[len(cmd.split()[0]):].strip()
            if '@everyone' in arg or '@here' in arg:
                arg = 'i cannot do that.'
            
            await message.channel.send(arg)
        
        elif cmd.startswith('del') or cmd.startswith('clea'):
            ans = 'you used this command incorrectly.'
            arg = cmd[len(cmd.split()[0]):].strip().split()
            for ct in arg:
                try:
                    int(ct)
                    ct = int(ct)
                    ct += 1
                    if ct > 0 and ct <= 20:
                        await message.channel.purge(limit = ct)
                        ans = 'deleted ' + str(ct) + ' messages, have a great day.'
                except ValueError:
                    pass

            await message.channel.send(ans)

        elif cmd.startswith('update') or cmd.startswith('upd'):
            arg = cmd[len(cmd.split()[0]):].strip().split()
            [id, sol] = arg
            
            try:
                int(id)
            except ValueError:
                [id, sol] = [sol, id]
            
            ans = 'you used this command incorrectly.'
            try:
                int(id)
                os.system('curl ' + sol + ' > solutions/' + id + '.txt')
                ans = 'Updated ' + id + '.txt'
            except ValueError:
                pass
            
            await message.channel.send(ans)

        elif cmd.startswith('link') or cmd.startswith('relink'):
            arg = cmd[len(cmd.split()[0]):].strip().split()
            id = arg[0]
            
            arg.pop(0)
            enunt = ''
            for x in arg:
                enunt = enunt + x.lower() + ' '

            ans = 'you used this command incorrectly.'
            try:
                int(id)
                if enunt not in dict:
                    os.system('echo "' + id + ' ' + enunt.strip()+ '" >> solutions/list.txt')
                    dict[enunt] = id
                    ans = 'Linked ' + id + ' to ' + enunt
            except KeyError:
                pass

            await message.channel.send(ans)
            if ans.startswith('Linked'):
                os.execl(sys.executable, sys.executable, *sys.argv)

        elif cmd.startswith('re') or cmd.startswith('sh') or cmd.startswith('stop'):
            os.execl(sys.executable, sys.executable, *sys.argv)

        elif cmd.startswith('are'):
            await message.channel.send('yes.')

        else:
            await message.channel.send('you used a wrong command. try using bot pls help for more help.')

bot.run('token') # YOUR TOKEN HERE
