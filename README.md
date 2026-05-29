# bookstore-assistant
**Author: Inés Martínez Fernández**

## Context
This virtual assistant is designed for an online bookstore. It helps customers interact with the store's catalogue and reservation system through natural conversation, available 24/7 on the store's website. The assistant uses Rasa CALM with LLM capabilities to understand user requests and guide them through each service.

## Flows

The assistant offers two services:

**1. Book Search (`search_book`):** Allows the customer to search the catalogue by genre (e.g. fantasy, mystery, sci-fi) or by book title. The assistant collects the search criteria and invokes a custom action (`action_search_books`) that queries the catalogue and returns up to 5 matching results, including author name and stock availability.

**2. Book Reservation (`reserve_book`):** Allows the customer to reserve a book for in-store pick-up. The assistant asks for the book title and the customer's name, then checks stock availability via a custom action (`action_check_book_availability`). If the book is in stock, the reservation is confirmed with a 5-day pick-up window. If not, the customer is informed and invited to search for alternatives.

> **Note:** The book catalogue used in this assistant is simulated for demo purposes. In a production environment, both the search and availability check actions would connect to a real inventory database or external API.