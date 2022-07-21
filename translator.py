import requests
import argparse
from bs4 import BeautifulSoup


class DoesNotSupportException(Exception):
    def __str__(self):
        return "Sorry, the program doesn't support"


class BadConnection(Exception):
    def __str__(self):
        return "Something wrong with your internet connection"


class Translator:

    def __init__(self):
        self.languages = ["arabic", "german", "english", "spanish", "french", "hebrew", "japanese",
                          "dutch", "polish", "portuguese", "romanian", "ukrainian", "turkish"]

    def arguments_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("translate_from", choices=["arabic", "german", "english", "spanish", "french", "hebrew",
                                                       "japanese", "dutch", "polish", "portuguese", "romanian",
                                                       "ukrainian", "turkish"],
                            help="You need choose on of these languages")
        parser.add_argument("translate_to", choices=["arabic", "german", "english", "spanish", "french", "hebrew",
                                                     "japanese", "dutch", "polish", "portuguese", "romanian",
                                                     "ukrainian", "turkish", "all"],
                            help="You need choose on of these languages")
        parser.add_argument("word", help="You need to write any word you want")
        argument = parser.parse_args()
        self.translate_from = argument.translate_from
        self.translate_to = argument.translate_to
        self.word = argument.word

    def connect(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        connect = self.translate_from + "-" + self.translate_to + "/" + self.word
        url = f"https://context.reverso.net/translation/" + connect
        self.request = requests.get(url, headers=headers)

    def translations(self):
        self.translation_words = list()
        soup = BeautifulSoup(self.request.content, "html.parser")
        translation_div = soup.find("div", {"id": "translations-content", "class": "wide-container"})
        try:
            translation_a = translation_div.findAll("a")
        except AttributeError:
            print(f"Sorry, unable to find {self.word}")
            quit()
        for line in translation_a:
            span_word = line.find("span", {"class": "display-term"})
            span_gender = line.find("span", {"class": "gender"})
            if span_gender is None:
                translate = span_word.text
            else:
                translate = span_word.text + " " + span_gender.text
            self.translation_words.append(translate)

        self.translation_words = (w for w in self.translation_words)

    def example(self):
        self.translation_sentences = list()
        soup = BeautifulSoup(self.request.content, "html.parser")
        translation_section = soup.find("section", {"id": "examples-content", "class": "wide-container"})
        try:
            translation = translation_section.findAll("span", {"class": "text"})
        except AttributeError:
            print(f"Sorry, unable to find {self.word}")
            quit()
        for t in translation:
            self.translation_sentences.append(t.text.strip())

        self.translation_sentences = (w for w in self.translation_sentences)

    def default_translation(self):
        with open(f"{self.word}.txt", "w", encoding="utf-8"):
            with open(f"{self.word}.txt", "a", encoding="utf-8") as file:
                self.connect()
                self.checks()
                self.translations()
                self.example()
                print()
                print(f"{self.translate_to.capitalize()} Translations:")
                file.write(f"{self.translate_to.capitalize()} Translations:\n")
                for translation_word in self.translation_words:
                    print(translation_word)
                    file.write(translation_word + "\n")
                print()
                file.write("\n")
                print(f"{self.translate_to.capitalize()} Examples:")
                file.write(f"{self.translate_to.capitalize()} Examples:\n")
                for n in range(5):
                    for i in range(2):
                        translation = next(self.translation_sentences)
                        print(translation)
                        file.write(translation + "\n")
                    print()
                    file.write("\n")

    def all_translation(self):
        with open(f"{self.word}.txt", "w", encoding="utf-8"):
            for value in self.languages:
                if self.translate_from == value:
                    continue
                else:
                    self.translate_to = value
                    self.connect()
                    self.checks()
                    self.translations()
                    self.example()
                    with open(f"{self.word}.txt", "a", encoding="utf-8") as file:
                        print(f"{self.translate_to.capitalize()} Translations:")
                        file.write(f"{self.translate_to.capitalize()} Translations:\n")
                        translation = next(self.translation_words)
                        print(translation)
                        file.write(translation + "\n\n")
                        print()
                        print(f"{self.translate_to.capitalize()} Examples:")
                        file.write(f"{self.translate_to.capitalize()} Examples:\n")
                        for i in range(2):
                            translation = next(self.translation_sentences)
                            print(translation)
                            file.write(translation + "\n")
                        print()
                        print()
                        file.write("\n\n")

    def checks(self):
        try:
            if self.translate_from not in self.languages:
                exception_lang = self.translate_from
                raise DoesNotSupportException
            elif self.translate_to not in self.languages:
                exception_lang = self.translate_to
                raise DoesNotSupportException
            if self.request is False:
                raise BadConnection
        except DoesNotSupportException:
            print(f"Sorry, the program doesn't support {exception_lang}")
            quit()
        except BadConnection as err:
            print(err)
            quit()

    def main(self):
        self.arguments_parser()
        if self.translate_to == "all":
            self.all_translation()
        else:
            self.default_translation()


def main():
    translation = Translator()
    translation.main()


if __name__ == "__main__":
    main()
