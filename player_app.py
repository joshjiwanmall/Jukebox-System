#
# Program Name: player_app.py
#
# Author(s): Joshua Jiwanmalla
#
# Date: 03/12/2026
#
# Description: This program plays or waits for queued songs and displays recently played songs.  
# 




import csv
import time
import webbrowser





#
# Class Name: Queue
#
# Author: Taken from https://runestone.academy/ns/books/published/pythonds3/BasicDS/ImplementingaQueueinPython.html?mode=browsing 
#
# Description: This is a queue class. This class is used to ensure that the first song chosen is the first played.
# 

class Queue: 
    """Queue implementation as a list"""

    def __init__(self):
        """Create new queue"""
        self._items = []

    def is_empty(self):
        """Check if the queue is empty"""
        return not bool(self._items)

    def enqueue(self, item):
        """Add an item to the queue"""
        self._items.insert(0, item)

    def dequeue(self):
        """Remove an item from the queue"""
        return self._items.pop()

    def size(self):
        """Get the number of items in the queue"""
        return len(self._items)





#
# Class Name: Stack
#
# Author: Taken from https://runestone.academy/ns/books/published/pythonds3/BasicDS/ImplementingaStackinPython.html?mode=browsing  
#
# Description: This is a stack class. This class is used to track recently played songs.
# 

class Stack: 
    """Stack implementation as a list"""

    def __init__(self):
        """Create new stack"""
        self._items = []

    def is_empty(self):
        """Check if the stack is empty"""
        return not bool(self._items)

    def push(self, item):
        """Add an item to the stack"""
        self._items.append(item)

    def pop(self):
        """Remove an item from the stack"""
        return self._items.pop()

    def peek(self):
        """Get the value of the top item in the stack"""
        return self._items[-1]

    def size(self):
        """Get the number of items in the stack"""
        return len(self._items)
    





PLAY_QUEUE_FILE = "PlayQueue .csv"




#
# Function Name: load_queue
#
# Author: Mujtaba Raza
#
# Parameters: None
#
# Return Value: Queue
#
# Description: Opens the PlayQueue . csv file to create a queue containing dictionaries of each queued song’s info. 
#

def load_queue():
    q = Queue()
    with open(PLAY_QUEUE_FILE, newline ='', encoding='utf-8') as file:
        reader = csv.DictReader(file, fieldnames = ["Artist", "Title", "Duration", "Link"]) # fieldnames adds the header/keys to the file and each song's info is turned into a dictionary
        for row in reader:
            q.enqueue(row)    
    return q






#
# Function Name: play_songs
#
# Author: Joshua Jiwanmall
#
# Parameters: None
#
# Return Value: None
#
# Description: Gives user time to queue songs, plays songs, and displays the 3 most recently played songs. 
#

def play_songs():
    recent_stack = Stack() # Stack for recently played songs 
    while True:
        q = load_queue()
        if q.is_empty():
            print("Queue empty, checking again in 15 seconds...")
            time.sleep(15) # Program pauses for 15 seconds to give the user time to queue songs
            continue # Goes back to the start of the loop

        while not q.is_empty(): 
            song = q.dequeue() # Selects the song to play
            
            recent_stack.push(song) # Adds to recently played stack             

            print(f"Now playing: {song['Artist']} - {song['Title']}") 
            webbrowser.open(song['Link']) # Plays the song

            
            with open(PLAY_QUEUE_FILE, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file, fieldnames=["Artist", "Title", "Duration", "Link"])
                all_songs = [row for row in reader if row != song]  # Keeps all songs except the one just played

            with open(PLAY_QUEUE_FILE, "w", newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["Artist", "Title", "Duration", "Link"])
                writer.writerows(all_songs) # Rewrites PlayQueue file to get rid of song that was just played
            

            mins, secs = map(int, song['Duration'].split(":")) # Assigns the amount of mins and secs to seperate integer variables
            time.sleep(mins * 60 + secs) # Program pauses for total length (secs) of song


        print("\nRecently Played:")
        for i, s in enumerate(recent_stack._items[-3:][::-1], start=1): # Numbers the 3 most recently played songs
            print(f"{i}. {s['Artist']} - {s['Title']}") # i represents song number, s represents dict of song info
        print("----------------------")





# Main

play_songs()



