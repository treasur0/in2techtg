import logging
import uuid
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Updater, CallbackQueryHandler
from user_management import get_balance, claim_balance, add_referral, get_referral_link

logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    user_name = update.message.from_user.first_name
    message = (
        f"Hi {user_name}, welcome to CoinSwapper. You can now choose from our below buttons if you want to trade with us.\n"
        "You can also refer your friends to use the bot and earn $2.\n"
        "Don't forget to use the /claim command to claim your daily bonus and use the /balance command to check your balance"
    )

    keyboard = [
        [InlineKeyboardButton("Buy", callback_data='buy'),
         InlineKeyboardButton("Sell", callback_data='sell')],
        [InlineKeyboardButton("Swap", callback_data='swap'),
         InlineKeyboardButton("Receive", callback_data='receive')],
        [InlineKeyboardButton("Claim", callback_data='claim'),  
         InlineKeyboardButton("Referral", callback_data='referral')],
        [InlineKeyboardButton("Join Channel", url='https://t.me/allcoinswaps/')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup)


async def join_channel(update: Update, context: CallbackContext) -> None:
    """Handle the "Join Channel" button press."""
    user_id = update.effective_user.id
    channel_username = '@allcoinswaps'  # Replace with your channel's username
    if await context.bot.get_chat_member(channel_username, user_id):
        # User has joined the channel
        add_balance(user_id, 100)  # Give $1 to the user
        await update.message.reply_text("You have successfully joined the channel and received $1!")
        chat_member = await context.bot.get_chat_member(chat_id, user_id)

    else:
        # User has not joined the channel
        await update.message.reply_text("Please join our channel to receive $1.")

async def referral(update: Update, context: CallbackContext) -> None:
    """Generate a referral link for the user and reply with it."""
    user_id = update.effective_user.id
    referral_code = str(uuid.uuid4())  # Generate a unique referral code
    add_referral(user_id, referral_code)
    referral_link = get_referral_link(referral_code)

    if update.message:
        await update.message.reply_text(f'Your referral link is: {referral_link}')
    else:
        await context.bot.send_message(chat_id=update.callback_query.from_user.id, text=f'Your referral link is: {referral_link}')

async def button(update: Update, context: CallbackContext) -> None:
    """Handle button press."""
    query = update.callback_query
    query_data = query.data
    if query_data == 'buy':
        keyboard = [
            [InlineKeyboardButton("Bitcoin", callback_data='buy_bitcoin')],
            [InlineKeyboardButton("Tether", callback_data='buy_tether')],
            [InlineKeyboardButton("USDT", callback_data='buy_usdt')],
            [InlineKeyboardButton("Others", callback_data='buy_others')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Would you want to buy:", reply_markup=reply_markup)

    elif query_data == 'sell':
        keyboard = [
            [InlineKeyboardButton("Bitcoin", callback_data='sell_bitcoin')],
            [InlineKeyboardButton("Tether", callback_data='sell_tether')],
            [InlineKeyboardButton("USDT", callback_data='sell_usdt')],
            [InlineKeyboardButton("Others", callback_data='sell_others')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Would you want to sell:", reply_markup=reply_markup)

    else:
        await query.answer()
        await query.edit_message_text(text=f"Selected option: {query_data}")
    if query_data == 'claim':
        await claim_money(update, context)    
    elif query_data == 'referral':
        await referral(update, context)
    
    else:
        await query.answer()
        await query.edit_message_text(text=f"Selected option: {query_data}")



async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Here is how you can use this bot: Type the /start menu to start trading with the bot')

async def custom_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the custom command /custom is issued."""
    await update.message.reply_text('This is a custom command. You can customize it as needed.')

async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def balance(update: Update, context: CallbackContext) -> None:
    """Send the user's balance."""
    user_id = update.message.from_user.id
    user_balance = get_balance(user_id)
    await update.message.reply_text(f'Your balance is: {user_balance} units.')

async def claim_money(update: Update, context: CallbackContext) -> None:
    """Allow the user to claim money every 24 hours."""
    user_id = update.effective_user.id
    result = claim_balance(user_id)
    await update.message.reply_text(result)


if __name__ == '__main__':
    main()
