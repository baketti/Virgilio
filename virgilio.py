import json
import os
import string

CANTI_DIRNAME = 'PATH_TO_YOUR_CANTI_DIRECTORY'
CANTI_QUANTITY = 34
CHARS_TO_EXCLUDE = string.punctuation + ' ' + '\n' + '«' + '»' + '’'


class Virgilio():
    class CantoNotFoundError(Exception):
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)

    def __init__(self, directory):
        self.directory = directory

    def count_hell_verses(self):
        hell_verses = self.get_hell_verses()
        return len(hell_verses)

    def count_tercets(self, canto_number):
        canto_verses = self.read_canto_lines(canto_number)
        canto_verses = self.count_verses(canto_number)
        return canto_verses // 3

    def count_verses(self, canto_number):
        canto_verses = self.read_canto_lines(canto_number)
        return len(canto_verses)

    def count_word(self, canto_number, word):
        canto_verses = self.read_canto_lines(canto_number)
        return " ".join(canto_verses).count(word)

    def count_words(self, canto_number, words):
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
        hell_verses = []
        for i in range(CANTI_QUANTITY):
            canto_number = i + 1
            canto_verses = self.read_canto_lines(canto_number)
            for verse in canto_verses:
                hell_verses.append(verse)
        return hell_verses
    
    def get_hell_verse_mean_len(self):
        hell_verses = self.get_hell_verses()
        all_hell_verses_len = 0
        all_hell_verses_tot = self.count_hell_verses()
        for verse in hell_verses:
            sanitized_verse = verse.strip(CHARS_TO_EXCLUDE)
            all_hell_verses_len += len(sanitized_verse)
        try:
            hell_verse_mean_len = all_hell_verses_len / all_hell_verses_tot
        except ZeroDivisionError:
            print("No verses found, can't calculate mean length")
        else:
            return round(hell_verse_mean_len, 2)

    def get_longest_canto(self):
        longest_canto = {
            'canto_number': 0,
            'canto_len': 0,
        }
        for i in range(CANTI_QUANTITY):
            canto_number = i+1
            canto_verses = self.read_canto_lines(canto_number)
            longest_canto_len = longest_canto["canto_len"]
            if len(canto_verses) <= longest_canto_len: 
                continue
            longest_canto["canto_number"] = canto_number
            longest_canto["canto_len"] = len(canto_verses)
        return longest_canto
    
    def get_longest_verse(self, canto_number):
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
        canto_verses = self.read_canto_lines(canto_number)
        verses_with_word = []
        for verse in canto_verses:
            if word not in verse: 
                continue
            verses_with_word.append(verse)
        return verses_with_word
    
    def read_canto_lines(self, canto_number, strip_lines=False, num_lines=None):
        if not isinstance(canto_number, int):
            raise TypeError("canto_number must be an integer")
        if canto_number < 1 or canto_number > CANTI_QUANTITY:
            raise self.CantoNotFoundError(
                "canto_number must be between 1 and 34"
            )
        canto_basename = f"Canto_{canto_number}.txt"
        canto_path = os.path.join(self.directory, canto_basename)
        canto_verses = []
        try:
            with open(canto_path, "r", encoding = "utf-8") as canto:
                for verse in canto:
                    canto_verses.append(
                        verse.strip(CHARS_TO_EXCLUDE) if strip_lines else verse
                    )
                    if len(canto_verses) == num_lines:
                        break
        except FileNotFoundError:
            print(f"File '{canto_path}' not found")
        except Exception:
            print(f"error while opening '{canto_path}'")
        return canto_verses

virgilio = Virgilio(CANTI_DIRNAME)
hell_verse_mean_len = virgilio.get_hell_verse_mean_len()
print("hell_verse_mean_len => ", hell_verse_mean_len)
