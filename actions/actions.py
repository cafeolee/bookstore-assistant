from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


# Simulated book catalogue
BOOK_CATALOGUE = [
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss", "genre": "fantasy", "stock": 3},
    {"title": "A Game of Thrones", "author": "George R.R. Martin", "genre": "fantasy", "stock": 2},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "fantasy", "stock": 5},
    {"title": "Gone Girl", "author": "Gillian Flynn", "genre": "mystery", "stock": 4},
    {"title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "genre": "mystery", "stock": 1},
    {"title": "Murder on the Orient Express", "author": "Agatha Christie", "genre": "mystery", "stock": 0},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "romance", "stock": 6},
    {"title": "Outlander", "author": "Diana Gabaldon", "genre": "romance", "stock": 2},
    {"title": "Dune", "author": "Frank Herbert", "genre": "sci-fi", "stock": 4},
    {"title": "The Martian", "author": "Andy Weir", "genre": "sci-fi", "stock": 3},
    {"title": "Neuromancer", "author": "William Gibson", "genre": "sci-fi", "stock": 0},
    {"title": "The Silent Patient", "author": "Alex Michaelides", "genre": "thriller", "stock": 5},
    {"title": "The Da Vinci Code", "author": "Dan Brown", "genre": "thriller", "stock": 3},
]


class ActionSearchBooks(Action):
    """Search the catalogue by genre or by title keyword."""

    def name(self) -> Text:
        return "action_search_books"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        genre = tracker.get_slot("book_genre")
        title_query = tracker.get_slot("book_title")

        matches = []

        if genre:
            genre_lower = genre.lower()
            matches = [
                b for b in BOOK_CATALOGUE
                if genre_lower in b["genre"].lower()
            ]
        elif title_query:
            title_lower = title_query.lower()
            matches = [
                b for b in BOOK_CATALOGUE
                if title_lower in b["title"].lower()
            ]

        if not matches:
            result_text = (
                "I'm sorry, I couldn't find any books matching your search. "
                "Try a different genre or title!"
            )
        else:
            lines = ["Here are the books I found:\n"]
            for book in matches[:5]:  # show at most 5 results
                availability = f"{book['stock']} in stock" if book["stock"] > 0 else "out of stock"
                lines.append(
                    f"  • '{book['title']}' by {book['author']} — {availability}"
                )
            result_text = "\n".join(lines)

        return [SlotSet("search_results", result_text)]


class ActionCheckBookAvailability(Action):
    """Check whether a requested book title is available for reservation."""

    def name(self) -> Text:
        return "action_check_book_availability"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        reserve_title = tracker.get_slot("reserve_title") or ""
        title_lower = reserve_title.lower()

        # Look for the book in the catalogue (partial match)
        found_book = next(
            (b for b in BOOK_CATALOGUE if title_lower in b["title"].lower()),
            None,
        )

        is_available = found_book is not None and found_book["stock"] > 0
        return [SlotSet("is_available", is_available)]
