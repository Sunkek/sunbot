# Sunbot

My discord bot. Rewritten. Again.

## Goals

- Collecting and displaying discord server and user statistics. 
- Automation of some boring stuff.
- Adding fun features to my discord community.
- Learning something new.

## Stack

- Python, obviously. The discord.py library is just awesome.
- For database I use PostgreSQL. 
- To address the database I use asyncpg for its outstanding speed.
- The bot and the database are used as Docker containers for easier deployment.

## Features & TODO

1. Settings - admins should be able to turn som,e options on and off and tune them
    - Set trackers
    - ✔️ Set activity
    - Set emoji emotions
    - ✔️ Set birthday feed
    - Set welcome and leave message
    - Set verification
    - ✔️ Set ranks
    - Set special roles
    - Set warnings
    - Set ping roulette
2. Trackers - saving data to the database
    - ✔️ Message tracking
    - ✔️ Reaction tracking
    - ✔️ Voice tracking
    - ✔️ Games tracing
    - Emoji tracking
    - N-word tracking
3. Topcharts - displaying saved data
    - Top postcounts
    - Top attachmetns
    - Top reactors
    - Top reaction receivers
    - Top voice chatters
    - Top players
    - Top channels, postcount
    - Top channels, attachments
    - Top channels, voice
    - Top emoji
    - Top games
    - Top countries
    - Top oldest
    - Top youngest
    - Top active members
    - Top ping roulette winners
4. ✔️ Binder - collect some info about the members
    - ✔️ Bind birthday
    - ✔️ Bind steam
    - ✔️ Bind country
    - More binds
5. ✔️ Oracle - ask your questions
    - ✔️ Just use the previously created one
    - Add more replies
6. ✔️ Ad reminder - reminds you to bump your server
    - ✔️ Just use the previously created one
    - ✔️ Remind after 2h since last !d bump
7. Verification system - new members must prove that they're human
    - Send verified message
    - Purge unverified members daily, send message about it
8. Ranks - there's hierarchy everywhere
    - Automatically promote and demote members according to their activity and join date
    - Start votes for selected positions, send  message with candidate list
    - Send bulletins to those who can vote
    - Count the votes
    - Automaticlly promote and demote members according to the vote outcome
9. Special roles - personal titles
    - Let them create and change special roles if they meet the requirements
10. ✔️ Mod functions - easier than Discord interface
    - Mute
    - ✔️ Unmute
    - ✔️ Kick
    - ✔️ Ban
    - ✔️ Unban
11. ✔️ Embedder - create and edit embed messages
    - ✔️ New embed
    - ✔️ Edit embed
    - Copy & paste embed
12. Russian roulette - feeling risky? 
    - Mute roulette
    - Kick roulette
    - Ban roulette
13. Warnings - easier automated moderation
    - Give warning
    - Automatically remove expired warnings
    - Take action according to the amount of active warnings
14. ✔️ Ping roulette - pings 3 random members. Those members can ping 3 more random members! Or opt-out of the ping-roulette, forever.
    - ✔️ Ping roulette
    - ✔️ Opt-out
    - ✔️ Members with roulette charges
    - Auto-roll every N days
15. Activity system - those who speak should be rewarded
    - ✔️ Give activity points for messages...
    - ✔️ Voice...
    - Ignore voice AFK channel
    - ✔️ And reactions
    - Give activity points for mod actions?
    - Reward top active members with convertable SB tokens
777. Minor features
        - Pagination in topcharts and wherever applicable
        - Filters in topcharts and wherever applicable
        - ✔️ Short command descriptions in help
        - Help by command alias
        - ✔️ Filter for show settings command
        
    
To be continued.
