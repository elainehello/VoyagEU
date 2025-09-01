# FINAL COURSE PROJECT

## Project: AI Agent “¡Vamos!” – Your Travel Planner for Spain

### The Goal

Create an advanced conversational agent that helps users plan a trip to Spain. The agent doesn’t just give information; it understands complex requests, interacts with different “tools” (APIs and functions), and builds a personalized, coherent itinerary.

---

### Example Scenario

Imagine the user writes a request like this:  
_"Hi! I’d like to organize a 4-day trip to Seville for the May long weekend. We’re two people. We’re interested in history, architecture, and eating good tapas. Our budget for hotel and activities is medium-high. Propose a plan!"_

The agent must break down this request and use its tools to build a complete response.

---

### The Agent’s “Toolbox”

These are the Python functions that students must create and that the agent will learn how to use:

1. **Tool: buscar_transporte(origin, destination, date)**

   - **Purpose:** Find the best travel options for getting to Spain.
   - **Details for Spain:** This function should do two things:
     - **Flights:** Query an API (simulated or real, e.g. Skyscanner) to find flights to major airports like Madrid (MAD), Barcelona (BCN), or Seville (SVQ).
     - **Trains:** Query AVE high-speed train schedules from Renfe. This is crucial for planning internal travel, e.g. from Madrid to Seville.
   - **Example result:**  
     _“I found a direct flight to Seville on April 30th for €120. As an alternative, there’s an AVE train from Madrid that takes 2.5 hours and costs €80.”_

2. **Tool: encontrar_alojamiento(city, budget, area_preferences)**

   - **Purpose:** Suggest hotels or apartments according to budget and style.
   - **Details for Spain:** The function should know the main neighborhoods of major cities.
   - **Example result (for Seville):**  
     _“Given your interest in history, I suggest a hotel in the Santa Cruz neighborhood, the historic heart of the city. For a livelier atmosphere tied to flamenco, you might consider the Triana neighborhood. I found Hotel X for €150 per night.”_

3. **Tool: sugerir_actividades_culturales(city, interests)**

   - **Purpose:** Provide a list of monuments, museums, and experiences based on user interests.
   - **Details for Spain:** This is the core of the project. The function must have specific “knowledge.”
     - If _interests_ include “history” and “architecture” in Seville, suggest:  
       _“The Cathedral with the Giralda (Gothic and Almohad style), the Royal Alcázar (a masterpiece of Mudejar architecture), and a walk through Plaza de España.”_
     - If the interest is “art” in Madrid, suggest the _“Art Triangle”: Prado Museum, Reina Sofía, and Thyssen-Bornemisza._

4. **Tool: crear_itinerario_gastronomico(city, cuisine_type)**

   - **Purpose:** Create a themed food route, suggesting typical dishes and famous areas.
   - **Details for Spain:** Essential for any trip to Spain!
     - If _cuisine_type_ is “tapas” in Seville, suggest:  
       _“I recommend a tapas tour between the city center and Triana. Don’t miss spinach with chickpeas, pork tenderloin with whisky sauce, and a glass of sherry. You could try the bars on Calle Mateos Gago.”_
     - If it’s Valencia, suggest paella near Malvarrosa Beach.

5. **Tool: reservar_espectaculo(city, show_type)**
   - **Purpose:** Find and (simulate) book tickets for cultural events.
   - **Details for Spain:** Perfect for flamenco.
   - **Example result:**  
     _“Seville is the cradle of flamenco. I suggest a show at a traditional tablao in Triana. Can I check availability for you?”_

---

### The Agent’s Reasoning Process

- **Analysis:** The agent reads the request and extracts entities: City = Seville, Dates = May 1–4, Interests = [history, architecture, tapas], Budget = medium-high.
- **Planning:** The agent decides the order of actions: first transport, then accommodation, then activities day by day.
- **Execution and Synthesis:** The agent calls its tools one by one. For example, it calls _sugerir_actividades_culturales_ and _crear_itinerario_gastronomico_ and combines the results to create a daily plan.
- **Final Result:** The agent presents a full itinerary:
  - **Day 1:** Arrival, hotel check-in at Santa Cruz neighborhood, tapas night.
  - **Day 2:** Morning visit to the Alcázar, afternoon at the Cathedral, evening flamenco show.
  - _And so on…_

---

### Extra Features

- **Budget Management:** The agent tracks estimated costs (flight + hotel + tickets) and warns the user if they are exceeding the budget.
- **Interactive Map:** The agent can use the Google Maps API to generate a personalized map with markers for the hotel and all suggested activities.

---

## Project Structure

```text
voyageu/
├── app/                        # Core application code
│   ├── agent/                  # AI reasoning & itinerary logic
│   │   ├── __init__.py
│   │   ├── reasoning.py        # Orchestrates toolbox functions
│   │   ├── itinerary.py        # Builds day-by-day itinerary, manages budget
│   │   └── nlp_parser.py       # Extracts entities from user queries using spaCy
│   │
│   ├── tools/                  # Toolbox functions for each domain
│   │   ├── __init__.py
│   │   ├── transport.py        # buscar_transporte()
│   │   ├── hotels.py           # encontrar_alojamiento()
│   │   ├── activities.py       # sugerir_actividades_culturales()
│   │   ├── food.py             # crear_itinerario_gastronomico()
│   │   └── shows.py            # reservar_espectaculo()
│   │
│   ├── api/                    # FastAPI backend
│   │   ├── __init__.py
│   │   ├── routes.py           # API endpoint definitions (versioned /api/v1)
│   │   ├── schemas.py          # Pydantic models for request/response validation
│   │   └── dependencies.py     # Dependency injection, shared clients, settings
│   │
│   └── utils/                  # Helper & utility functions
│       ├── __init__.py
│       └── helpers.py          # Generic helpers (date parsing, formatting, validation)
│
├── config/                     # Configuration and constants
│   ├── __init__.py
│   ├── settings.py             # API URLs, keys, DATA_PATH, default parameters
│   └── constants.py            # Fixed lists (cities, cuisines, etc.)
│
├── data/                       # Mock or stub data for offline testing
│   ├── flights.json
│   ├── trains.json
│   ├── hotels.json
│   ├── activities.json
│   ├── food.json
│   └── shows.json
│
├── tests/                      # Unit and integration tests
│   ├── __init__.py
│   ├── test_transport.py
│   ├── test_hotels.py
│   ├── test_activities.py
│   ├── test_food.py
│   ├── test_shows.py
│   └── test_agent.py           # Integration tests for the AI agent orchestration
│
├── logs/                       # Optional logging folder
│   └── voyageu.log
│
├── main.py                     # Entry point to run FastAPI app
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Ignore venv, __pycache__, logs, etc.
```
