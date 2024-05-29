# user_management.py

import time

users = {}
referrals = {}

def get_balance(user_id):
    """Get the balance for a user."""
    if user_id not in users:
        users[user_id] = {'balance': 0, 'last_claim': 0}
    return users[user_id]['balance']

def claim_balance(user_id):
    """Allow the user to claim money every 24 hours."""
    current_time = time.time()
    if user_id not in users:
        users[user_id] = {'balance': 0, 'last_claim': 0}

    last_claim = users[user_id]['last_claim']
    if current_time - last_claim >= 24 * 3600:
        users[user_id]['balance'] += 100  # Adding $1 as the claimed amount
        users[user_id]['last_claim'] = current_time
        return "You have successfully claimed $1!"
    else:
        remaining_time = 24 * 3600 - (current_time - last_claim)
        hours = int(remaining_time // 3600)
        minutes = int((remaining_time % 3600) // 60)
        return f"You can claim again in {hours} hours and {minutes} minutes."

def add_referral(user_id, referral_code):
    """Add a referral for the user."""
    referrals[user_id] = referral_code

def get_referral_link(referral_code):
    """Get the referral link for a given referral code."""
    return f"https://t.me/timecoinswapper_bot?start={referral_code}" 
 # Replace YourBotUsername with your bot's username
