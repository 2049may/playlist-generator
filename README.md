# Spotify playlist generator

This project is a Spotify playlist generator that helps users expand their musical culture by discovering new artists. Based on a chosen artist, the program generates a playlist made of songs from similar artists.

## How It Works
The user selects an artist as the starting point for the playlist. Then, for each artist, they must choose two similar artists. This process repeats for the newly selected artists, creating an artist tree.

Artist information is retrieved using the Spotify and Last.fm APIs.

## Before Running the Program

### Installing Required Modules

To run this program correctly, you need to install the following Python libraries using `pip install` :
* `requests_cache`
* `spotipy`
* `requests`
* `graphviz`

For graphviz, download and install it from [this website](https://graphviz.org/download/)

After installation, add the `bin` folder of Graphviz to your system's environment variable PATH.

**Example**: C:\Program Files\Graphviz\bin

*(If an error occurs, you may need to add `[path]\Graphviz\bin\dot.exe` to your PATH.)*

### Using the API
Since Spotify limits API usage for small-scale applications, this code cannot be executed by just anyone without setup.

To run the program, you will need:
* A Spotify account
* A **Spotify for Developers** account

### Steps To Follow

1. Go to the Spotify for Developers Dashboard and create an application.
2. Fill in the required fields and set a valid callback address (e.g., `http://127.0.0.1:9000`).
3. Generate your API keys and insert them directly into `main.py` (inside the sp variable) or store them in a `cred.py` file for better security.
4. Do the same for Last.fm.

## How To Use It

### Selecting Artists
At launch, the user enters the name of the artist they want to base their playlist on.
(For better results, choosing a well-known artist here is recommended to avoid limitations.)

This first artist becomes the **root** of the recommendation tree.

From there, the user selects two similar artists, who will become the "children" of the root node. The program suggests a list of 10 similar artists, and the user can request more suggestions (up to 30) by entering `0`.

This process continues for each artist until the desired number of nodes is reached.
Each node in the tree represents one song in the playlist. The number of nodes can be adjusted via the `nb_max` variable in the code.

### Removing An Artist

> *Will be added in future update*

### Tree Visualization

Once all artists are selected, a visual representation of the tree is generated as a PDF file.

### Creating The Playlist

After finalizing the selection, the program asks the user to enter a name for the playlist. (a default name is set if the user enters 0)

The algorithm then traverses the tree and selects a random song from the 10 most popular tracks of each artist to build the playlist.

Finally, a link to the newly created playlist is provided, allowing the user to access it directly on their Spotify profile.

