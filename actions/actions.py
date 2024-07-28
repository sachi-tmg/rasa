from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
import pandas as pd
import logging
from typing import Any, Text, Dict, List , Optional

logger = logging.getLogger(__name__)

class ActionAnswerAuthor(Action):
    def name(self) -> str:
        return "action_answer_author"

    def __init__(self):
        try:
            # Load your dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        try:
            # Extract the title from the latest user message
            user_message = tracker.latest_message['text']
            title = self.extract_title(user_message)
            logger.info(f"Extracted title: {title}")
            
            # Find the author in the dataset
            author = self.get_author(title)
            logger.info(f"Found author: {author}")

            # Send the author back to the user
            dispatcher.utter_message(text=author)
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching the author.")
        
        return []

    def extract_title(self, message: str) -> str:
        try:
            # List of phrases to look for
            phrases = ["author of", "who wrote", "author"]
            
            for phrase in phrases:
                start = message.lower().find(phrase)
                if start != -1:
                    start += len(phrase)
                    end = message.find('}', start)
                    if end == -1:
                        end = len(message)
                    title = message[start:end].strip(' {}')
                    return title
        
            return ""
        except Exception as e:
            logger.error(f"Failed to extract title: {e}")
            return ""

    def get_author(self, title: str) -> str:
        if not title:
            return "Sorry, I couldn't find any book title in your message."

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                return f"The author of '{title}' is {matched_row['Author'].values[0]}."
            else:
                return f"Sorry, I don't know the author of '{title}'."
        except Exception as e:
            logger.error(f"Failed to get author: {e}")
            return "Sorry, I don't know the author of that book."

        
class ActionAnswerDescription(Action):
    def name(self) -> str:
        return "action_answer_description"

    def __init__(self):
        try:
            # Load your dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
            logger.info(f"Columns in CSV: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        try:
            # Extract the title from the latest user message
            user_message = tracker.latest_message['text']
            title = self.extract_title(user_message)
            logger.info(f"Extracted title: {title}")
            
            # Find the description in the dataset
            description = self.get_description(title)
            logger.info(f"Found description: {description}")

            # Send the description back to the user
            dispatcher.utter_message(text=description)
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching the description.")
        
        return []

    def extract_title(self, message: str) -> str:
        try:
            # List of phrases to look for
            phrases = ["description of", "tell me about", "what is", "describe", "about", "summary of", "description for"]
            
            for phrase in phrases:
                start = message.lower().find(phrase)
                if start != -1:
                    start += len(phrase)
                    end = message.find('}', start)
                    if end == -1:
                        end = len(message)
                    title = message[start:end].strip(' {}')
                    return title
        
            return ""
        except Exception as e:
            logger.error(f"Failed to extract title: {e}")
            return ""

    def get_description(self, title: str) -> str:
        if not title:
            return "Sorry, I couldn't find any book title in your message."

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                return f"{matched_row['Description'].values[0]}."
            else:
                return f"Sorry, I don't know the description of '{title}'."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get description: {e}")
            return "Sorry, I don't know the description of that book."

        

class ActionAnswerCategory(Action):
    def name(self) -> str:
        return "action_answer_category"

    def __init__(self) -> None:
        self.data = None
        self.load_data()

    def load_data(self) -> None:
        try:
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("Excel file loaded successfully.")
            logger.info(f"Columns in the file: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load Excel file: {e}")

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, any]) -> List[Dict[str, any]]:
        try:
            user_message = tracker.latest_message['text']
            title = self.extract_title(user_message)
            logger.info(f"Extracted title: {title}")
            
            category = self.get_category(title)
            logger.info(f"Found category: {category}")

            dispatcher.utter_message(text=category)
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching the category.")
        
        return []

    def extract_title(self, message: str) -> str:
        phrases = ["category of", "genre of", "type of book is", "type of", "category for", "genre is"]
        
        for phrase in phrases:
            start = message.lower().find(phrase)
            if start != -1:
                start += len(phrase)
                end = message.find('}', start) if '}' in message[start:] else len(message)
                title = message[start:end].strip(' {}')
                return title
        
        return ""

    def get_category(self, title: str) -> str:
        if not title:
            return "Sorry, I couldn't find any book title in your message."

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                return f"The category of '{title}' is {matched_row['Category'].values[0]}."
            return f"Sorry, I don't know the category of '{title}'."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get category: {e}")
            return "Sorry, I don't know the category of that book."

class ActionAnswerBookInfo(Action):
    def name(self) -> str:
        return "action_answer_info"

    def __init__(self):
        try:
            # Load your dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
            logger.info(f"Columns in CSV: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        try:
            # Extract the title from the latest user message
            user_message = tracker.latest_message['text']
            title = self.extract_title(user_message)
            logger.info(f"Extracted title: {title}")
            
            # Find the author, description, and category in the dataset
            author = self.get_author(title)
            description = self.get_description(title)
            category = self.get_category(title)
            logger.info(f"Found author: {author}, description: {description}, category: {category}")

            # Send all information back to the user
            dispatcher.utter_message(text=f"{author}\n{description}\n{category}")
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching the book information.")
        
        return []

    def extract_title(self, message: str) -> str:
        try:
            # List of phrases to look for
            phrases = ["information about", "details of", "info on", "book info for", "tell me about", "information on", "details about", "like to know about", "information for"]
            
            for phrase in phrases:
                start = message.lower().find(phrase)
                if start != -1:
                    start += len(phrase)
                    end = message.find('}', start)
                    if end == -1:
                        end = len(message)
                    title = message[start:end].strip(' {}')
                    return title
        
            return ""
        except Exception as e:
            logger.error(f"Failed to extract title: {e}")
            return ""

    def get_author(self, title: str) -> str:
        if not title:
            return "Sorry, I couldn't find any book title in your message."

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                return f"The author of '{title}' is {matched_row['Author'].values[0]}."
            else:
                return f"Sorry, I don't know the author of '{title}'."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get author: {e}")
            return "Sorry, I don't know the author of that book."

    def get_description(self, title: str) -> str:
        if not title:
            return "Sorry, I couldn't find any book title in your message."

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                return f"The description of '{title}' is {matched_row['Description'].values[0]}."
            else:
                return f"Sorry, I don't know the description of '{title}'."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get description: {e}")
            return "Sorry, I don't know the description of that book."

    def get_category(self, title: str) -> str:
        if not title:
            return "Sorry, I couldn't find any book title in your message."

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                return f"The category of '{title}' is {matched_row['Category'].values[0]}."
            else:
                return f"Sorry, I don't know the category of '{title}'."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get category: {e}")
            return "Sorry, I don't know the category of that book."

        
class ActionAnswerSimilarBooks(Action):
    def name(self) -> str:
        return "action_answer_similar_books"

    def __init__(self):
        try:
            # Load your dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
            logger.info(f"Columns in CSV: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        try:
            # Extract the title from the latest user message
            user_message = tracker.latest_message['text']
            title = self.extract_title(user_message)
            logger.info(f"Extracted title: {title}")
            
            # Find similar books in the dataset
            similar_books = self.get_similar_books(title)
            logger.info(f"Found similar books: {similar_books}")

            # Send the similar books back to the user
            dispatcher.utter_message(text=similar_books)
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching similar books.")
        
        return []

    def extract_title(self, message: str) -> str:
        try:
            # List of phrases to look for
            phrases = ["similar to", "like", "related to"]
            
            for phrase in phrases:
                start = message.lower().find(phrase)
                if start != -1:
                    start += len(phrase)
                    title = message[start:].strip()
                    return title
            
            return ""
        except Exception as e:
            logger.error(f"Failed to extract title: {e}")
            return ""


    def get_similar_books(self, title: str) -> str:
        if not title:
            return "Sorry, I couldn't find any book title in your message."

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                category = matched_row['Category'].values[0]
                similar_books = self.data[self.data['Category'] == category]
                similar_books_titles = similar_books['Title'].sample(n=10).tolist()  # Randomly select 10 books
                return f"Books similar to '{title}' are: {', '.join(similar_books_titles)}."
            else:
                return f"Sorry, I don't know any books similar to '{title}'."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get similar books: {e}")
            return "Sorry, I don't know any books similar to that one."



class ActionAnswerBooksByCategory(Action):
    def name(self) -> str:
        return "action_answer_books_by_category"

    def __init__(self) -> None:
        self.data = self.load_data()

    def load_data(self) -> Optional[pd.DataFrame]:
        try:
            data = pd.read_excel('actions/Books.xlsx')
            logger.info("Excel file loaded successfully.")
            logger.info(f"Columns in the file: {data.columns.tolist()}")
            return data
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except pd.errors.EmptyDataError as e:
            logger.error(f"File is empty: {e}")
        except pd.errors.ParserError as e:
            logger.error(f"File parsing error: {e}")
        except Exception as e:
            logger.error(f"Failed to load file: {e}")
        return None

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, any]) -> List[Dict[str, any]]:
        if self.data is None:
            dispatcher.utter_message(text="Sorry, the data could not be loaded.")
            return []

        try:
            user_message = tracker.latest_message['text']
            category = self.extract_category(user_message)
            logger.info(f"Extracted category: {category}")
            
            books_in_category = self.get_books_in_category(category)
            logger.info(f"Books in category: {books_in_category}")

            dispatcher.utter_message(text=books_in_category)
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching books in that category.")
        
        return []

    def extract_category(self, message: str) -> str:
        phrases = [
            "books in the", "books about", "books of the", 
            "list some", "recommend me some", "have any", 
            "what books have", "suggest me some books in", "suggest me","i need some",
            "i need", "i want to read a", "i want to read"
        ]
        
        stop_phrases = ["category", "genre", "book", "books"]
        message_lower = message.lower()
        
        # Find the position of the first stopping phrase
        start_idx = min((message_lower.find(stop_phrase) for stop_phrase in stop_phrases if message_lower.find(stop_phrase) != -1), default=len(message_lower))

        for phrase in phrases:
            start = message_lower.find(phrase)
            if start != -1 and start < start_idx:
                start += len(phrase)
                category = message[start:start_idx].strip()
                return category.strip('{}').strip()

        return ""

    def get_books_in_category(self, category: str) -> str:
        if not category:
            return "Sorry, I couldn't find any category in your message."

        try:
            books = self.data[self.data['Category'].str.contains(category, case=False, na=False)]
            if not books.empty:
                if len(books) > 10:
                    books = books.sample(n=10)
                books_titles = books['Title'].tolist()
                return f"Books in the '{category}' category are: {', '.join(books_titles)}."
            return f"Sorry, we do not currently have books in the '{category}' category in our library."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get books in category: {e}")
            return "Sorry, I don't know any books in that category."

        
class ActionAnswerBooksByAuthor(Action):
    def name(self) -> str:
        return "action_answer_books_by_author"

    def __init__(self):
        try:
            # Load your dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
            logger.info(f"Columns in CSV: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        try:
            # Extract the author from the latest user message
            user_message = tracker.latest_message['text']
            author = self.extract_author(user_message)
            logger.info(f"Extracted author: {author}")
            
            # Find books by the given author
            books_by_author = self.get_books_by_author(author)
            logger.info(f"Found books by author: {books_by_author}")

            # Send the books back to the user
            dispatcher.utter_message(text=books_by_author)
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching books by that author.")
        
        return []

    def extract_author(self, message: str) -> str:
        try:
            # List of phrases to look for
            phrases = ["books by", "books from", "books written by"]
            
            for phrase in phrases:
                start = message.lower().find(phrase)
                if start != -1:
                    start += len(phrase)
                    author = message[start:].strip()
                    if author.startswith('{') and author.endswith('}'):
                        return author[1:-1].strip()
                    return author
            
            return ""
        except Exception as e:
            logger.error(f"Failed to extract author: {e}")
            return ""

    def get_books_by_author(self, author: str) -> str:
        if not author:
            return "Sorry, I couldn't find any author in your message."

        try:
            books = self.data[self.data['Author'].str.contains(author, case=False, na=False)]
            if not books.empty:
                if len(books) > 10:
                    books = books.sample(n=10)  # Randomly select 10 books
                books_titles = books['Title'].tolist()
                return f"Books by '{author}' are: {', '.join(books_titles)}."
            else:
                return f"Sorry, I don't know any books by '{author}'."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get books by author: {e}")
            return "Sorry, I don't know any books by that author."
        




class ActionFindBookLocation(Action):
    def name(self) -> str:
        return "action_find_book_location"

    def __init__(self):
        try:
            # Load your dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
            logger.info(f"Columns in CSV: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        try:
            # Extract the title from the latest user message
            user_message = tracker.latest_message['text']
            title = self.extract_title(user_message)
            logger.info(f"Extracted title: {title}")
            
            # Find the location in the dataset
            location = self.get_location(title)
            logger.info(f"Found location: {location}")

            # Send the location back to the user
            dispatcher.utter_message(text=location)
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching the book location.")
        
        return []

    def extract_title(self, message: str) -> str:
        try:
            # List of phrases to look for
            phrases = ["location of", "where is", "find", "locate", "where can i get"]
            
            for phrase in phrases:
                start = message.lower().find(phrase)
                if start != -1:
                    start += len(phrase)
                    end = message.find('}', start)
                    if end == -1:
                        end = len(message)
                    title = message[start:end].strip(' {}')
                    return title
        
            return ""
        except Exception as e:
            logger.error(f"Failed to extract title: {e}")
            return ""

    def get_location(self, title: str) -> str:
        if not title:
            return "Sorry, I couldn't find any book title in your message."

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                return f"The location of '{title}' is {matched_row['Location'].values[0]}."
            else:
                return f"Sorry, I don't know the location of '{title}'."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get location: {e}")
            return "Sorry, I don't know the location of that book."
        



class ActionCheckBookAvailability(Action):
    def name(self) -> str:
        return "action_check_book_availability"

    def __init__(self):
        try:
            # Load your dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
            logger.info(f"Columns in CSV: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        try:
            # Extract the title from the latest user message
            user_message = tracker.latest_message['text']
            title = self.extract_title(user_message)
            logger.info(f"Extracted title: {title}")
            
            # Find the availability in the dataset
            availability = self.get_availability(title)
            logger.info(f"Found availability: {availability}")

            # Send the availability back to the user
            dispatcher.utter_message(text=availability)
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while checking the book's availability.")
        
        return []

    def extract_title(self, message: str) -> str:
        try:
            # List of start and end phrases to look for
            start_phrases = ["availability of", "is", "check", "have", "do you have", "tell me if"]
            end_phrases = ["available", "in stock", "right now", "in the library", "in stock"]
            
            start_index = -1
            for phrase in start_phrases:
                start_index = message.lower().find(phrase)
                if start_index != -1:
                    start_index += len(phrase)
                    break

            if start_index == -1:
                return ""

            end_index = len(message)
            for phrase in end_phrases:
                end_index_temp = message.lower().find(phrase, start_index)
                if end_index_temp != -1:
                    end_index = min(end_index, end_index_temp)

            title = message[start_index:end_index].strip(' {}')
            return title
        
        except Exception as e:
            logger.error(f"Failed to extract title: {e}")
            return ""

    def get_availability(self, title: str) -> str:
        if not title:
            return "Sorry, I couldn't find any book title in your message."

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                return f"The availability of '{title}' is {matched_row['Availability'].values[0]}."
            else:
                return f"Sorry, I don't know the availability of '{title}'."
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return "Sorry, the information could not be retrieved due to a data issue."
        except Exception as e:
            logger.error(f"Failed to get availability: {e}")
            return "Sorry, I don't know the availability of that book."


class ActionFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        dispatcher.utter_message(text="Sorry, I didn't understand that. Can you please rephrase or provide more details?")
        return []
    
class ActionCheckBookAvailability(Action):
    def name(self) -> str:
        return "action_check_book_borrow"

    def __init__(self):
        try:
            # Load your dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
            logger.info(f"Columns in CSV: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        try:
            # Extract the title from the latest user message
            user_message = tracker.latest_message['text']
            title = self.extract_title(user_message)
            logger.info(f"Extracted title: {title}")
            
            # Find the availability and location in the dataset
            availability, location = self.get_availability_and_location(title)
            logger.info(f"Found availability: {availability}, location: {location}")

            # Send the availability and location back to the user
            dispatcher.utter_message(text=f"The book '{title}' is {availability} and can be found at {location}.")
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while checking the book's availability.")
        
        return []

    def extract_title(self, message: str) -> str:
        try:
            # List of start phrases to look for
            start_phrases = [ "i want to borrow", "how can i get"]
            
            start_index = -1
            for phrase in start_phrases:
                start_index = message.lower().find(phrase)
                if start_index != -1:
                    start_index += len(phrase)
                    break

            if start_index == -1:
                return ""

            title = message[start_index:].strip()
            return title
        
        except Exception as e:
            logger.error(f"Failed to extract title: {e}")
            return ""

    def get_availability_and_location(self, title: str) -> tuple:
        if not title:
            return ("Sorry, I couldn't find any book title in your message.", "an unknown location")

        try:
            matched_row = self.data[self.data['Title'].str.contains(title, case=False, na=False)]
            if not matched_row.empty:
                availability = matched_row['Availability'].values[0]
                location = matched_row['Location'].values[0]
                return (availability, location)
            else:
                return ("not available", "an unknown location")
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return ("Sorry, the information could not be retrieved due to a data issue.", "an unknown location")
        except Exception as e:
            logger.error(f"Failed to get availability and location: {e}")
            return ("Sorry, I don't know the availability of that book.", "an unknown location")



class ActionFindNewArrivals(Action):
    def name(self) -> str:
        return "action_find_new_arrivals"

    def __init__(self):
        try:
            # Load the dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
            logger.info(f"Columns in CSV: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        try:
            # Extract the phrase from the latest user message
            user_message = tracker.latest_message['text']
            if self.is_request_for_new_arrivals(user_message):
                new_arrivals = self.get_new_arrivals()
                logger.info(f"New arrivals: {new_arrivals}")

                # Send the new arrivals back to the user
                if new_arrivals:
                    dispatcher.utter_message(text=f"Here are the latest arrivals:\n{new_arrivals}")
                else:
                    dispatcher.utter_message(text="Sorry, there are no new arrivals at the moment.")
            else:
                dispatcher.utter_message(text="Sorry, I didn't understand your request.")
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching the new arrivals.")
        
        return []

    def is_request_for_new_arrivals(self, message: str) -> bool:
        try:
            # List of phrases to look for
            phrases = ["new arrivals", "latest books", "newest books", "recent additions"]

            for phrase in phrases:
                if phrase in message.lower():
                    return True
        
            return False
        except Exception as e:
            logger.error(f"Failed to determine if message is a request for new arrivals: {e}")
            return False

    def get_new_arrivals(self) -> str:
        try:
            # Ensure to get only the last 10 entries
            last_10_books = self.data.tail(10)
            new_arrivals_list = "\n".join(last_10_books['Title'])
            return new_arrivals_list
        except KeyError as e:
            logger.error(f"Column not found: {e}")
            return ""
        except Exception as e:
            logger.error(f"Failed to get new arrivals: {e}")
            return ""
        
class ActionListRandomBooks(Action):
    def name(self) -> str:
        return "action_list_random_books"

    def __init__(self):
        try:
            # Load your dataset
            self.data = pd.read_excel('actions/Books.xlsx')
            logger.info("CSV file loaded successfully.")
            logger.info(f"Columns in CSV: {self.data.columns.tolist()}")
        except Exception as e:
            logger.error(f"Failed to load CSV file: {e}")

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            
            random_titles = self.data['Title'].sample(n=10).tolist()
            titles_text = "\n".join(random_titles)
            logger.info(f"Random book titles: {titles_text}")

            # Send the book titles back to the user
            dispatcher.utter_message(text=f"Here are 10 book titles:\n{titles_text}")
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            dispatcher.utter_message(text="Sorry, something went wrong while fetching the book titles.")
        
        return []