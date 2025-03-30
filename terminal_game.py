import time
import random
import os
import threading

# Local variables
name = "?"

# List of rooms with short stories
rooms = [
    "You step into a vast library where books float in the air. A whispering voice asks for your name...",
    "A dark forest surrounds you. The trees seem to move when you're not looking.",
    "A golden desert stretches endlessly. In the distance, you see a figure waving at you.",
    "A massive hall filled with mirrors. But your reflection is missing.",
    "A city in the clouds. Bridges made of light connect the floating islands.",
    "An ancient ruin with glowing symbols on the walls. They pulse as you step closer.",
    "A frozen lake under a violet sky. Something stirs beneath the ice.",
    "A marketplace full of creatures you've never seen before. They seem surprised to see you.",
    "A cavern filled with giant mushrooms. Their glow changes colors as you walk.",
    "A vast ocean. You stand on the surface as if it were solid ground.",
    "A never-ending staircase spiraling up and down. Footsteps echo, but you're alone.",
    "A garden where time moves strangely. Flowers bloom and wither in seconds.",
    "A ruined temple where a statue holds a key. The moment you touch it, the ground trembles.",
    "A grand ballroom where invisible musicians play a haunting melody.",
    "A prison of glass walls. You see shadows moving on the other side."
]

# Global variable for the timer
time_up = False
timer_thread = None
lock = threading.Lock()

# Countdown function
def countdown_timer(seconds_left):
    global time_up
    for seconds_left in range(seconds_left, 0, -1):
        if time_up:
            return  # Stop the timer if the game ends
        print("\r⏳ Time left in this world: {:02d} seconds...".format(seconds_left), end="", flush=True)
        time.sleep(1)
    
    # Time's up
    print("\n\n⚠️ You feel yourself being pulled back into the realm of doors, " + name + "! ⚠️\n")
    time.sleep(2)
    time_up = True  # Stop the game after time is up

# Function to safely reset the timer
def reset_timer():
    global time_up, timer_thread
    with lock:  # Ensures that only one thread modifies the timer state at a time
        time_up = True
        if timer_thread and timer_thread.is_alive():
            timer_thread.join()  # Wait for the timer thread to finish
        time_up = False  # Reset the time up flag
        timer_thread = threading.Thread(target=countdown_timer, args=(60,))
        timer_thread.start()

def main():
    global time_up, timer_thread
    room_count = 0

    while room_count < 10:
        time_up = False  # Reset time up flag at the start of each room
        clear()
        print("\n" + "="*56)
        print(random.choice(rooms))  # Selects a random room description
        print("="*56 + "\n")
        
        print(f"\nAlright, {name}, you're about to face a new challenge...\n")
        time.sleep(2)  # Give time to read the room description

        # Start countdown timer in a separate thread
        reset_timer()  # Reset the timer for the new room

        # Randomly determine the deadly door
        deadly_door = random.choice(["1", "2", "3"])

        # Player chooses a door (allowing input during countdown)
        while not time_up:
            choice = input(f"{name}, which door will you choose? (1, 2, 3)\n")
            
            if choice == deadly_door:
                print("\n💀 You stepped into the abyss... Your journey ends here, " + name + ". 💀\n")
                break
            
            print("\n✨ You pass through the door and find yourself in another world... ✨\n")
            room_count += 1
            time.sleep(2)

            # Reset the timer after passing through a door
            reset_timer()  # Reset the timer for the next room
            break  # Exit the loop to proceed to the next room
        
        # If time is up, the player dissolves
        if time_up:
            print(f"You feel as if bubbles arise and just see cloudy... {name}, you will fall asleep....\n")
            time.sleep(8)
            exit()

    if room_count == 10:
        print("✨ Congratulations, you made it through! You may now leave this world! ✨")
        time.sleep(2)
        print(f"Have a safe journey back, {name}!\n")
        time.sleep(2)

def get_name():
    global name
    name = input("\nOkey! BTW. What's your name?\n")

def clear():
    os.system("cls" if os.name == "nt" else "clear")  # Cross-platform screen clearing

def intro():
    clear()
    print("\n" + "="*56)
    print("      🌌 WELCOME TO THE WORLD OF ENDLESS DOORS 🌌      ")
    print("="*56)
    print("\nIn this realm, nothing exists but doors... endless doors.\n")
    print("🚪 Every room you enter has 3 doors.")
    print("❌ One leads to the abyss, where existence ends.")
    print("🔄 The other two lead to a new world, full of wonders and horrors.")
    print("\n⚠️  But beware! You may only stay in each world for one minute.")
    print("⏳ After 60 seconds, your body will begin to dissolve,")
    print("forcing you back into the labyrinth of doors.")
    print("\nSome say that one of these worlds holds the key to an *exit*...")
    print("...but no one has ever found it.")
    print("="*56 + "\n")
    
    ready = input("\nAre you ready to play the game of doors? 🚪 (Yes)\n").lower()
    
    if ready == "yes":
        get_name()
        main()
    else:
        print("Take your time and reread it.")
        time.sleep(5)
        ready = input("\nAre you ready to play the game of doors now? 🚪 (Yes)\n").lower()
    
        if ready == "yes":
            get_name()
            main()
        else:
            print("You have had enough time!")
            get_name()
            main()

def __init__():
    intro()

__init__()