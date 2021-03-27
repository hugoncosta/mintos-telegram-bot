# Mintos Telegram Bot

The Mintos Telegram Bot is a simple Telegram Bot to keep track of your favourite Loan Originators on demand. Code is Python, user data as well as LO data is stored in csv.

## Features

- Choose your favourite Loan Originators 
- Check both their highest interest/YTM loans on the Primary/Secondary Market at the time
- Gets the data on demand using the Mintos API

## Installation

Clone the repo, create a .env file with bot_api = 'your_bot_token' and run the Mintos Telegram Bot file. 

## Future Ideas for Development

- Create a proper db system that isn't based out of csv files (keep in mind that the bot runs continously, functions need to open/insert/save in the same step)
- Make the API calls every x minutes for all LOs instead of on demand (Mintos will likely ban the IP if too many people do the check)
- Bot keeps a track of changes and sends out a message to people subscribing to the changed LO as soon as the change is visible
- Integrate the checks with the actual account to buy/sell according to the user's preferences

## License

MIT

## Thanks

Special thanks to Samuel for helping me find the proper API and explaining the Telegram Bot API.