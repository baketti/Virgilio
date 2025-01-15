import json
import os
import string


class Virgilio():
    CANTI_QUANTITY = 34
    CHARS_TO_EXCLUDE = string.punctuation + ' ' + '\n' + '«' + '»' + '’'

    def __init__(self, directory):
        self.directory = directory

    class CantoNotFoundError(Exception):
        """
            Exception raised when the canto_number provided is out of range
            (not between 1 and the canti quantity).
        """
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

    def count_hell_verses(self):
        """
            Calculates the total number of verses in the Inferno.
            :return: number of verses in the Inferno
            :rtype: ``int``
        """
        hell_verses = self.get_hell_verses()
        return len(hell_verses)

    def count_tercets(self, canto_number):
        """
            Calculates the number of tercets in a 'canto';
            if the number of verses in the canto is not divisible by 3, 
            the excess verses are not counted (rounding down).
            :param canto_number: number of the canto
            :type canto_number: ``int``
            :return: number of tercets in the canto
            :rtype: ``int``
        """
        canto_verses = self.read_canto_lines(canto_number)
        canto_verses = self.count_verses(canto_number)
        return canto_verses // 3

    def count_verses(self, canto_number):
        """
            Calculates the number of verses in a 'canto'.
            :param canto_number: number of the canto
            :type canto_number: ``int``
            :return: number of verses in the canto
            :rtype: ``int``
        """
        canto_verses = self.read_canto_lines(canto_number)
        return len(canto_verses)

    def count_word(self, canto_number, word):
        """
            Counts how many times the word appears in the 'canto';
            :param canto_number: number of the canto
            :type canto_number: ``int``
            :param word: word to count
            :type word: ``str``
            :return: number of times the word appears in the canto
            :rtype: ``int``
        """
        canto_verses = self.read_canto_lines(canto_number)
        return " ".join(canto_verses).count(word)

    def count_words(self, canto_number, words):
        """
            Counts how many times each word in the list appears in the 'canto' 
            and saves the result to a JSON file;
            :param canto_number: number of the canto
            :type canto_number: ``int``
            :param words: list of words to count
            :type words: ``list``
            :return: dictionary with words as keys and their counts as values
            :rtype: ``dict``
        """
        words_counter = {}
        for word in words:
            words_counter[word] = self.count_word(canto_number, word)
        try:
            with open(f"{self.directory}/words_count.json", "w") as file:
                json.dump(
                    words_counter, 
                    file, 
                    indent=4,
                    sort_keys=True,
                )
        except Exception as e:
            print(f"Errore while serialization: {e}")
        else:
            print("Serialization done successfully")
        return words_counter

    def get_hell_verses(self):
        """
            Retrieves all verses from all canti in the Inferno.
            Iterates for the number of canti to read their lines and append
            each verse to a list;
            :return: a list containing all verses from all canti
            :rtype: ``list``
        """
        hell_verses = []
        for i in range(Virgilio.CANTI_QUANTITY):
            canto_number = i + 1
            canto_verses = self.read_canto_lines(canto_number)
            for verse in canto_verses:
                hell_verses.append(verse)
        return hell_verses
    
    def get_hell_verse_mean_len(self):
        """
            Calculates the mean length of all verses in the Inferno.
            Retrieves all verses, sanitizes them by removing specified 
            characters, and calculates the mean length.
            :return: the mean length of all verses,
                     None if no verses are found
            :rtype: ``float`` or ``None``
        """
        hell_verses = self.get_hell_verses()
        hell_verses_len = 0
        for verse in hell_verses:
            sanitized_verse = verse.strip(Virgilio.CHARS_TO_EXCLUDE)
            hell_verses_len += len(sanitized_verse)
        try:
            hell_verse_mean_len = hell_verses_len / len(hell_verses)
            return round(hell_verse_mean_len, 2)
        except ZeroDivisionError:
            print("No verses found, can't calculate mean length")

    def get_longest_canto(self):
        """
            Finds and returns the longest canto in the Inferno.
            Iterates for the number of canti to read their lines and determines 
            the canto with the most verses. 
            If multiple canti have the same number of verses, 
            the first longest one is returned.
            :return: dictionary with the number of the longest canto and its 
                     length
            :rtype: ``dict``
        """
        longest_canto = {
            'canto_number': 0,
            'canto_len': 0,
        }
        for i in range(Virgilio.CANTI_QUANTITY):
            canto_number = i+1
            canto_verses = self.read_canto_lines(canto_number)
            longest_canto_len = longest_canto["canto_len"]
            if len(canto_verses) <= longest_canto_len: 
                continue
            longest_canto["canto_number"] = canto_number
            longest_canto["canto_len"] = len(canto_verses)
        return longest_canto
    
    def get_longest_verse(self, canto_number):
        """
            Finds and returns the longest verse in the canto.
            Iterates through all verses in the canto and determines the longest;
            if multiple verses have the same number of characters, 
            the first longest one is returned.
            :param canto_number: number of the canto
            :type canto_number: ``int``
            :return: the longest verse in the canto
            :rtype: ``str``
        """
        canto_verses = self.read_canto_lines(canto_number)
        verse_len = 0
        longest_verse = ""
        for verse in canto_verses:
            if len(verse) <= verse_len: 
                continue
            verse_len = len(verse)
            longest_verse = verse
        return longest_verse
        
    def get_verse_with_word(self, canto_number, word):
        """
            Retrieves all verses from the canto containing the word.
            Iterates through all verses in the canto and appends to a list each
            verse which contains the word.
            :param canto_number: number of the canto
            :type canto_number: ``int``
            :param word: word to search for
            :type word: ``str``
            :return: list of verses containing the word
            :rtype: ``list``
        """
        canto_verses = self.read_canto_lines(canto_number)
        verses_with_word = []
        for verse in canto_verses:
            if word not in verse: 
                continue
            verses_with_word.append(verse)
        return verses_with_word
    
    def read_canto_lines(self, canto_number, strip_lines=False, num_lines=None):
        """
            Retrieves the lines from the specified canto file. 
            Optionally strips specified characters from each line and limits
            the number of lines to retrieve.
            :param canto_number: number of the canto to read
            :type canto_number: ``int``
            :param strip_lines: whether to strip specified characters from each 
                                line
            :type strip_lines: ``bool``, optional
            :param num_lines: number of lines to read
            :type num_lines: ``int``, optional
            :return: list of verses from the specified canto
            :rtype: ``list``
        """
        if not isinstance(canto_number, int):
            raise TypeError("canto_number must be an integer")
        if canto_number < 1 or canto_number > Virgilio.CANTI_QUANTITY:
            raise self.CantoNotFoundError(
                f"canto_number must be between 1 and {Virgilio.CANTI_QUANTITY}"
            )
        canto_basename = f"Canto_{canto_number}.txt"
        canto_path = os.path.join(self.directory, canto_basename)
        canto_verses = []
        try:
            with open(canto_path, "r", encoding = "utf-8") as canto:
                for verse in canto:
                    canto_verses.append(
                        verse.strip(Virgilio.CHARS_TO_EXCLUDE) if strip_lines
                        else verse
                    )
                    if len(canto_verses) == num_lines:
                        break
        except FileNotFoundError:
            print(f"File '{canto_path}' not found")
        except Exception:
            print(f"error while opening '{canto_path}'")
        return canto_verses

virgilio = Virgilio('PATH_TO_YOUR_CANTI_DIRECTORY')
