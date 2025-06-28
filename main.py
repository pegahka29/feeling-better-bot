import os
from dotenv import load_dotenv
load_dotenv()

import logging
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Load token from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Expanded joke list
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "I’m reading a book on anti-gravity. It’s impossible to put down!",
    "Why did the scarecrow win an award? Because he was outstanding in his field.",
    "Did you hear about the restaurant on the moon? Great food, no atmosphere.",
    "Parallel lines have so much in common… it’s a shame they’ll never meet.",
    "Why don't skeletons fight each other? They don't have the guts.",
    "What do you call fake spaghetti? An impasta!",
    "I would tell you a construction pun… but I’m still working on it.",
    "I used to play piano by ear, but now I use my hands.",
    "Why can’t your nose be 12 inches long? Because then it would be a foot.",
    "How does a penguin build its house? Igloos it together.",
    "I asked my dog what's two minus two. He said nothing.",
    "I used to be addicted to soap, but I’m clean now.",
    "What do you call cheese that isn't yours? Nacho cheese.",
    "Why did the bicycle fall over? It was two-tired.",
    "I'm on a seafood diet. I see food and I eat it.",
    "What did one wall say to the other? I'll meet you at the corner.",
    "What do you call a pile of cats? A meowtain.",
    "Why are elevator jokes so good? They work on many levels.",
    "I'm terrified of elevators, so I'm going to start taking steps to avoid them.",
    "What's orange and sounds like a parrot? A carrot.",
    "Why do bees have sticky hair? Because they use honeycombs.",
    "What do you call a fish with no eyes? Fsh.",
    "What’s brown and sticky? A stick.",
    "Did you hear about the kidnapping at school? It’s fine, he woke up.",
    "Why was the math book sad? It had too many problems.",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one.",
    "I told my computer I needed a break, and now it won’t stop sending me KitKats.",
    "What did the zero say to the eight? Nice belt!",
    "I used to be a baker, but I couldn't make enough dough.",
    "Why did the tomato blush? Because it saw the salad dressing.",
    "I couldn't figure out why the baseball kept getting bigger—then it hit me.",
    "Did you hear the rumor about butter? Well, I’m not going to spread it.",
    "What do you get from a pampered cow? Spoiled milk.",
    "Why don’t programmers like nature? Too many bugs.",
    "What do you call an alligator in a vest? An investigator.",
    "Why do seagulls fly over the ocean? Because if they flew over the bay, they’d be bagels.",
    "How does a vampire start a letter? Tomb it may concern...",
    "What's a skeleton's least favorite room in the house? The living room.",
    "Why did the cookie go to the hospital? Because it felt crummy.",
    "What do you get when you cross a snowman and a dog? Frostbite.",
    "I used to be a banker, but I lost interest.",
    "What do you call a belt made of watches? A waist of time.",
    "Why did the chicken join a band? Because it had the drumsticks.",
    "How do cows stay up to date? They read the moos-paper.",
    "Why are ghosts bad at lying? Because they are too transparent.",
    "How do you make holy water? You boil the hell out of it.",
    "I once got into a fight with a broken elevator. I took it to another level."
]

# Expanded motivation list
motivations = [
    "Believe you can and you're halfway there.",
    "Don't watch the clock; do what it does. Keep going.",
    "Dream big. Start small. Act now.",
    "You are stronger than you think.",
    "Push yourself, because no one else will.",
    "Great things never come from comfort zones.",
    "Success is no accident.",
    "Do something today that your future self will thank you for.",
    "Stay positive, work hard, make it happen.",
    "Doubt kills more dreams than failure ever will.",
    "Discipline is the bridge between goals and accomplishment.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Little by little, a little becomes a lot.",
    "Make each day your masterpiece.",
    "You don't have to be perfect to be amazing.",
    "Keep going. Everything you need will come to you.",
    "Success doesn't come to you. You go to it.",
    "You are capable of amazing things.",
    "Action is the foundational key to success.",
    "Your only limit is your mind.",
    "Don’t stop until you’re proud.",
    "Strive for progress, not perfection.",
    "Be so good they can’t ignore you.",
    "Small steps every day.",
    "You were born to do great things.",
    "The secret of getting ahead is getting started.",
    "Fall seven times, stand up eight.",
    "Nothing changes if nothing changes.",
    "Do it with passion or not at all.",
    "Don't wait for opportunity. Create it.",
    "Start where you are. Use what you have. Do what you can.",
    "One day or day one. You decide.",
    "Hard work beats talent when talent doesn’t work hard.",
    "The best way out is always through.",
    "Make it happen. Shock everyone.",
    "Success is a series of small wins.",
    "Focus on the step in front of you, not the whole staircase.",
    "Progress is progress, no matter how small.",
    "Your future is created by what you do today.",
    "It always seems impossible until it’s done.",
    "Act like it’s impossible to fail.",
    "You don’t find willpower, you create it.",
    "Every accomplishment starts with the decision to try.",
    "Be the energy you want to attract.",
    "Success starts with self-discipline.",
    "Motivation gets you going, habit keeps you growing.",
    "You are one decision away from a totally different life.",
    "Big journeys begin with small steps.",
    "The harder you work for something, the greater you’ll feel when you achieve it.",
    "Your dreams don’t work unless you do."
]

# Expanded productivity tips
productivity_tips = [
    "Start your day with a to-do list.",
    "Prioritize your top 3 tasks each day.",
    "Use the Pomodoro technique: 25 minutes work, 5 minutes break.",
    "Eliminate distractions while working.",
    "Turn off notifications during focus time.",
    "Use a timer to stay on task.",
    "Batch similar tasks together.",
    "Schedule tasks on your calendar.",
    "Declutter your workspace.",
    "Set deadlines even for small tasks.",
    "Avoid multitasking—focus on one thing at a time.",
    "Break big tasks into smaller steps.",
    "Review your goals weekly.",
    "Start with the hardest task first (eat the frog).",
    "Use keyboard shortcuts to save time.",
    "Limit your social media time.",
    "Automate repetitive tasks when possible.",
    "Use a task manager app.",
    "Keep a notebook for quick ideas.",
    "Reflect at the end of each day.",
    "Take regular breaks to avoid burnout.",
    "Keep water at your desk and stay hydrated.",
    "Check emails at scheduled times, not constantly.",
    "Use templates for repeated tasks.",
    "Wake up earlier to gain quiet time.",
    "Learn to say no to non-essential tasks.",
    "Organize digital files for easy access.",
    "Use headphones to block out noise.",
    "Plan tomorrow before going to bed.",
    "Don’t aim for perfection—aim for progress.",
    "Delegate tasks when possible.",
    "Unsubscribe from unnecessary emails.",
    "Keep meetings short and to the point.",
    "Group errands and outings together.",
    "Track your time to see where it goes.",
    "Reward yourself after completing tasks.",
    "Create a morning routine.",
    "Keep your phone out of reach while working.",
    "Start tasks before you feel ready.",
    "Avoid checking your phone first thing in the morning.",
    "Use “Do Not Disturb” mode when focusing.",
    "Limit your decisions to reduce mental fatigue.",
    "Use white noise or focus music to concentrate.",
    "Declutter your digital desktop.",
    "Create templates for repeated emails or reports.",
    "Don’t be afraid to delete low-priority tasks.",
    "Review and adjust your goals monthly.",
    "Keep your goals visible.",
    "Use sticky notes for quick reminders.",
    "Rest is productive—sleep well!"
]

# Keyboard options
keyboard = ReplyKeyboardMarkup(
    [["Tell me a joke", "Motivate me", "Give me a productivity tip"]],
    resize_keyboard=True
)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi, Please Select one option:",
        reply_markup=keyboard
    )

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == "Tell me a joke":
        response = random.choice(jokes)
    elif text == "Motivate me":
        response = random.choice(motivations)
    elif text == "Give me a productivity tip":
        response = random.choice(productivity_tips)
    else:
        response = "Hi, Please Select one option:"

    await update.message.reply_text(response)

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot is polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
