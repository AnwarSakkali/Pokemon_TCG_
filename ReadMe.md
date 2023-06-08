## Intro

This is a project in which was intended to take an yet-to-be-localized japanese Pokémon trading card and translate it to english with the help of a python script. The intentions were as followed:

- The script takes an card with Japanese text on it as input (names, moveset, description are the keypoints)
- The script defines boxes where the keypoints are found (PIL)
- The script finds the text on the card image and reads that text (Tesseract)
- The script gets the pixels from the earlier defined boxes and tries to remove the black pixels that are text (PIL)
- The script translates the earlier found text from Japanese to English (Argostranslate)
- The script writes the translated text to the earlier defined boxes, now that they are textless (PIL)

### Issues
Issues have arisen during the implementation of this project, as removing the text from the image proved to be more difficult than expected, due to the fact that the text blends with the background of the card. This causes darker pixels to appear, but become unrecognizable by the program for them to be removed. This fine line between pixels whether they should be removed or not is an issue that remains to be solved. 
Another issue is that different Pokémon types respond differently to the program, sometimes removing too much or too little text from the image. This inconsistency makes finding a solution more difficult as well.

Aside from the ability to take an image and remove the text from a Pokémon trading card, more functionality has also been implemented within the project:

## Serebii Cardex scraper

Serebii.net is an unofficial Pokémon fanwebsite that contains one of the most expansive databases on the internet regarding anything Pokémon related. The written script is able to receive information from cards released in expansions (which is a parameter). Complications arose when the website doesn't have a standardized format for the different cards and expansions that have been released in the past years. This meant that (almost) every set needs to be verified on supportability. This results in an overabudance of effort and time.

## Pokémon Card Database scraper

The Pokémon Company International contains a massive and clear database for all the cards and expansions that have released since the beginning of the series. This provides a good base to retrieve any information that is required. 

### PokemonDatabaseSearcher
PokemonDatabaseSearcher.py is able to use the search mechanism of the website to return cards of a Pokémon of choice. While the script doesn't support any additional filters yet, the groundwork has been set up in a way to easily add this functionality. The script returns all the results from the query, which are urls to the pages that appeared from the search. Finally, this script also has a function to return the expansions of a Pokémon generation (every generation is about 3 years and defined by the introduction of new pokemon, region and characters). This information is potentially useful for future use. Currently, this script only supports English. 

### ReturnPokemonCard
ReturnPokemonCard.py is able search all the information of a card with an url. As the card database uses a standarized format for every page and url, it was possible to build around the supportability of every card and expansion. Currently, the key card information is printed within the python console. This script also supports multiple languages and more languages can easily be added, as well as more information to be returned from the function if neccesary. Potential future development points are the ability to also obtain information that are originally images on the website, like the weakness and resistance of a Pokémon.

### Combination of both
PokemonDatabaseSearcher.py currently returns a list with urls to the pages that fit the query on which the search was based on. This list can be used to access ReturnPokemonCard.py and so get all the information of every card that fits the query.

## Technology
The following tools have been used while building this project:
- IDE: Visual Studio Code
- Python: Python Version 3.10
- PIL: Image manipulator library
- Requests: retrieving website information
- Beautifulsoup: scraping a website and accessing specific elements from it
- Tesseract: AI-tool that is capable of reading text from images
- Argostranslate: language translation library

## Things I would like to see added or solved
These are potential pointers to what could be done with this project:
- Try to find a way to remove text better (maybe use masked images more)
- Implement the translation functionality with Tesseract and Argostranslate
- Simplify the interface more, as it's currently a bit chaotic with prints and calls everywhere
- Expand the dictionary (Dicts.py) with more than just Sword and Shield expansion sets (a way to do this automatically?)
- Expand the database search query to also support additional filters rather than just the name of the Pokémon
- Display more information from a card that are currently locked behind images on the website, like weaknesses and resistances