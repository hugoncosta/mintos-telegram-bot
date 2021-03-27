import os
from dotenv import load_dotenv
import pandas as pd
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from getLoans import getLoans

check = emojize(":white_check_mark:", use_aliases=True)
cross = emojize(":x:", use_aliases=True)

# Load dbs
LO_db = pd.read_csv("LO_db.csv")
user_db = pd.read_csv("user_db.csv")

def start(update, context):
    main_menu_keyboard = [[InlineKeyboardButton('Check Current Rates', callback_data='getLoansbtn')]
                        , [InlineKeyboardButton('Choose LOs', callback_data='chooseLOsbtn')]
                        , [InlineKeyboardButton('Help', callback_data='help')]]
    
    start_rmarkup = InlineKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)
    
    update.message.reply_text(text = 'Welcome to the Mintos Bot. Please select from the options below.'
                             , reply_markup=start_rmarkup) 


def start_over(update, context):
    query = update.callback_query
    query.answer()
    
    main_menu_keyboard = [[InlineKeyboardButton('Check Current Rates', callback_data='getLoansbtn')]
                        , [InlineKeyboardButton('Choose LOs', callback_data='chooseLOsbtn')]
                        , [InlineKeyboardButton('Help', callback_data='help')]]
    
    start_rmarkup = InlineKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)
    
    query.edit_message_text(text = 'Welcome back to the beginning. Please select from the options below.'
                            , reply_markup=start_rmarkup) 


def help(update, context):
    query = update.callback_query
    query.answer()
    
    help_keyboard = [[InlineKeyboardButton('GitHub Link', url='https://github.com/hugoncosta/mintos-telegram-bot')]
                     , [InlineKeyboardButton('Go Back', callback_data='startover')]]
    
    help_rmarkup = InlineKeyboardMarkup(help_keyboard, resize_keyboard = True)
    
    query.edit_message_text(text = "Simple bot to keep track of your fav LOs. Get PM/SM data on demand."
                            , reply_markup=help_rmarkup)


def getLoansbtn(update, context):
    query = update.callback_query
    query.answer()
    
    chat_id = query['message']['chat']['id']
    user_db = pd.read_csv("user_db.csv")    
    
    getloans_keyboard = [[InlineKeyboardButton('Check Again', callback_data='getLoansbtn')]
                        , [InlineKeyboardButton('Change your LOs', callback_data='chooseLOsbtn')]
                        , [InlineKeyboardButton('Go Back', callback_data='startover')]]
    
    getloans_rmarkup = InlineKeyboardMarkup(getloans_keyboard
                                         , resize_keyboard=True)
    
    query.edit_message_text(text = getLoans(user_db[user_db["chat_id"] == chat_id]["LO"].to_list())
                            , reply_markup=getloans_rmarkup)
    
    
def chooseLOsbtn(update, context):
    query = update.callback_query
    query.answer()
    
    user_db = pd.read_csv("user_db.csv")
    chat_id = query['message']['chat']['id'] 
    
    LOs_keyboard = []
    for LO in LO_db["LO"].to_list():
        if LO in user_db[(user_db.chat_id == chat_id)]["LO"].to_list():
            LOs_keyboard.append([InlineKeyboardButton(LO + ' - ' + cross, callback_data=LO.replace(' ', '_') + '-remove-changeLOs')])
        else:
            LOs_keyboard.append([InlineKeyboardButton(LO + ' - ' + check, callback_data=LO.replace(' ', '_') + '-add-changeLOs')])
    LOs_keyboard.append([InlineKeyboardButton('Go Back', callback_data='startover')])
    
    LOs_rmarkup = InlineKeyboardMarkup(LOs_keyboard, resize_keyboard=False)
    
    query.edit_message_text(text='Which LOs do you want to keep track of?', reply_markup=LOs_rmarkup) 


def changeLOs(update, context):
    query = update.callback_query
    query.answer()
    
    user_db = pd.read_csv("user_db.csv")
    chat_id = query['message']['chat']['id']
    chosen_LO = query.data.split('-')[0].replace('_', ' ')
    action = query.data.split('-')[1]
    
    if action == 'add':
        user_db = user_db.append({'chat_id': chat_id, 'LO': chosen_LO}, ignore_index=True)
    else:
        user_db = user_db[user_db["chat_id"] == chat_id][user_db["LO"] != chosen_LO]
    
    user_db.to_csv('user_db.csv', index=False)
    
    LOs_keyboard = []
    for LO in LO_db["LO"].to_list():
        if LO in user_db[(user_db.chat_id == chat_id)]["LO"].to_list():
            LOs_keyboard.append([InlineKeyboardButton(LO + ' - ' + cross, callback_data=LO.replace(' ', '_') + '-remove-changeLOs')])
        else:
            LOs_keyboard.append([InlineKeyboardButton(LO + ' - ' + check, callback_data=LO.replace(' ', '_') + '-add-changeLOs')])
    LOs_keyboard.append([InlineKeyboardButton('Go Back', callback_data='startover')])
    
    LOs_rmarkup = InlineKeyboardMarkup(LOs_keyboard, resize_keyboard=False)
    
    if action == 'add':
        query.edit_message_text(text=chosen_LO + ' has been added. Any other change?', reply_markup=LOs_rmarkup) 
    else:
        query.edit_message_text(text=chosen_LO + ' has been removed. Any other change?', reply_markup=LOs_rmarkup)
    
def main():
    load_dotenv('.env')
    updater = Updater(token=os.getenv('bot_api'), use_context=True)
    
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(chooseLOsbtn, pattern='^' + 'chooseLOsbtn' + '$'))
    dispatcher.add_handler(CallbackQueryHandler(changeLOs, pattern=r'^[a-zA-Z]+_[a-zA-Z]+-[a-zA-Z]+-changeLOs$'))
    dispatcher.add_handler(CallbackQueryHandler(changeLOs, pattern=r'^[a-zA-Z]+_[a-zA-Z]+_[a-zA-Z]+-[a-zA-Z]+-changeLOs$'))
    dispatcher.add_handler(CallbackQueryHandler(changeLOs, pattern=r'^[a-zA-Z]+-[a-zA-Z]+-changeLOs$'))
    dispatcher.add_handler(CallbackQueryHandler(getLoansbtn, pattern='^' + 'getLoansbtn' + '$'))
    dispatcher.add_handler(CallbackQueryHandler(start_over, pattern='^' + 'startover' + '$'))
    dispatcher.add_handler(CallbackQueryHandler(help, pattern='^' + 'help' + '$'))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()