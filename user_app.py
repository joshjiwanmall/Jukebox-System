#
# Program Name: user_app.py
#
# Author(s): Joshua Jiwanmalla
#
# Date: 03/12/2026
#
# Description: This program displays all the available jukebox songs and allows the user to select the ones to queue. 
# 




import csv




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
# Function Name: load_songs
#
# Author: Joshua Jiwanmall
#
# Parameters: None
#
# Return Value: List
#
# Description: Opens the ArtistDatabase. csv file to create a list of dictionaries of each song’s info.
#

def load_songs():
    songs = []                     
    with open('ArtistDatabase .csv', newline ='', encoding='utf-8') as file:  # Prevents blank line issues and character errors
        reader = csv.DictReader(file)  # Reads each row of the CSV file and turns each song's info into a dictionary
        for row in reader:  # Adds each dictionary of song info to the songs list
            songs.append(row) 
    return songs 






#
# Function Name: display_songs
#
# Author: Mujtaba Raza
#
# Parameters: List of dictionaries produced by load_songs 
#
# Return Value: None
#
# Description: Assigns each song dictionary with a number to print a clean list of each song to the user. 
#

def display_songs(songs): 
    print("Available Songs:")
    for i, song in enumerate(songs, start=1): # Gives a number to each song dictionary
        print(f"{i}. {song['Artist']} - {song['Title']} ({song['Duration']})")






#
# Function Name: select_songs
#
# Author: Mujtaba Raza
#
# Parameters: List of dictionaries produced by load_songs 
#
# Return Value: Queue
#
# Description: Prompts the user to select 3 songs to queue based on their assigned numbers. 
#

def select_songs(songs):
    q = Queue()
    
    while True:
        try:
            choices = input("Select up to 3 songs (comma-separated numbers): ")
            numbers = [int(x.strip()) for x in choices.split(",")][:3] # Adds the 3 numbers representing songs that the user gave to a list
            for n in reversed(numbers): # Adds the selected songs to the queue  
                if 1 <= n <= len(songs):
                    q.enqueue(songs[n-1])
                else:
                    print(f"{n} is not a valid song number.")
            return q
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas (example: 1,3,5).")




#
# Function Name: add_to_play_queue
#
# Author: Joshua Jiwanmall
#
# Parameters: Queue produced by select_songs
#
# Return Value: None
#
# Description: Writes the selected queued songs into the PlayQueue . csv file 
#

def add_to_play_queue(q):
    with open("PlayQueue .csv", "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for song in q._items:
            writer.writerow([
                song["Artist"],
                song["Title"],
                song["Duration"],
                song["Link"]
            ])




# Main

songs = load_songs()
display_songs(songs)

q = select_songs(songs)
print("\nYou selected:")
for song in q._items:
    print(f"{song['Artist']} - {song['Title']}")

add_to_play_queue(q)
print("Added to play queue.")

            


    


