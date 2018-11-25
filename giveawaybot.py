import datetime
import secrets
import random
import discord
from discord.ext.commands import Bot
import configparser

config = configparser.ConfigParser()
config.read('giveawaybot_config.ini')

WIN_LOG_NAME = config['MAIN']['WinLogName']
ADMIN_ROLE = config['MAIN']['AdminRole']
ENTRY_LOG_NAME = config['MAIN']['EntryLogName']
SEED_COUNT = config['MAIN']['SeedCount'] 

client = Bot(command_prefix="mv!", pm_help = True)
client.remove_command('help')

entry_dict = {}

try:
    seed_count_int = int(SEED_COUNT)
    if seed_count_int > 0:
        for x in range(1, seed_count_int + 1):
            entry_dict['seedUser' + str(x)] = secrets.token_urlsafe()
except ValueError:
    print("Unable to Seed Entries - Please enter an integer in the config file, restart and try again...")

def log_entries():
        log_full_path = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + WIN_LOG_NAME
        logger = open(log_full_path, "w")
        for key, value in entry_dict.items():
            logger.write("Contestant Name is " + key + " Send to Address is " + value + "\n")
        logger.close()
        return log_full_path

@client.command(name='enterme',
                description="""This command enters an address for the discord membername. \n
                               Example .enterme <address>. \n
                               The command .enterme will create a new entry or replace the existing address""",
                brief="Enter Me in the Giveaway",
                aliases=['entryvu'],
                pass_context=True)
async def new_entry(context, address=None):
    if address != None:
        entry_log_file = open(ENTRY_LOG_NAME, "a")
        entry_log_file.write("Contestant Name - " + 
                             context.message.author.name + 
                             " ** Address - " + 
                             address + 
                             " ** Timestamp - " +
                             datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
                             "\n")
        entry_log_file.close()
        entry_dict[context.message.author.name] = address  
        await client.say("Thankyou " + context.message.author.name + ", your address entry -->" + address + "<-- is successful")
    else:
        await client.say("Come on " + context.message.author.name + ", please enter an address")
        
@client.command(name='showme',
                description="Will show the address that is currently stored for a user. Example .showme <membername>",
                brief="Show the current address for specified member",
                pass_context=True)
async def show_entries(context, username='Not Entered'):
    total_entries = len(entry_dict.keys())
    await client.say("Hello " + context.message.author.name + ", currently there are " + str(total_entries) + " constestants")
    if (username == 'Not Entered') or not(username in entry_dict):
        await client.say("Membername " + username + ", hasn't entered yet, please enter a valid member name")
    else:    
        await client.say("The Address for " + username + " is " + str(entry_dict[username]))

@client.command(name='pickwinner',
                description="""Randomly Selects the Winner. Example .pickwinner. \n 
                               Winner is displayed and all entries are written to a log file. \n
                               Having the Admin Role is required for this command (set in config file)""",
                brief="Pick the Random Winner",
                pass_context=True)
async def pick_winner(context):
    for role in context.message.author.roles:
        if ADMIN_ROLE == str(role):
            break
    else:
        await client.say("Sorry, you do not have the correct role to Pick the Winner")   
        return        
    total_entries = len(entry_dict.keys())
    if total_entries > 0:
        log_full_path = log_entries()
        embed = discord.Embed(title="Drawing Time", description="Let's find out who our lucky winner is!", color=0xFEBA2D)
        embed.add_field(name="Contest", value="Demo Giveaway")
        embed.add_field(name="Entry Count", value=str(total_entries))
        embed.add_field(name="Contestants", value="Please use .showme to see contestants")
        winner, address = random.choice(list(entry_dict.items()))
        embed.add_field(name=":sparkles: The Winner is", value=winner, inline=False)
        embed.add_field(name="Winning Address", value=address)
        embed.add_field(name="Constestants logged to ", value=log_full_path)
        embed.set_footer(text="Thanks For Playing")
        await client.say(embed=embed)
    else:
        await client.say("There are't any contestants, please try again after members enter.")

# check for admin role, same as pick winner log then clear dictionary
@client.command(name='clearentries',
                description="""This command clear the contestent entries. Example .clearentries \n
                               1. Produce a Win Log (same and pickwinner snapshot) \n
                               2. Empty the entry dictionary \n
                               3. Clear the entry log file""",
                brief="Show the current address for user",
                pass_context=True)
async def clear_entries(context):
    for role in context.message.author.roles:
        if ADMIN_ROLE == str(role):
            break
    else:
        await client.say("Sorry, you do not have the correct role to clear entries")   
        return
    log_entries()
    entry_dict.clear()
    entry_log_file = open(ENTRY_LOG_NAME, "w")
    entry_log_file.write("Entry Log Cleared - Timestamp is " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
    entry_log_file.close()
    await client.say("Hello " + context.message.author.name + ", you have cleared the entry dictionary and the entry log file")

@client.event
async def on_ready():
    print("GiveAwayBot Ready")
    print("Logged in as " + client.user.name)
    print("discord.py " + str(discord.version_info))    
    
client.run(os.getenv('Token'))
