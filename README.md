# UCAS Personal Statement AI Advisor
#### Video Demo: <https://youtu.be/jquWwAJhTNQ>
#### Description:

This project is a Command-Line Interface (CLI) AI assistant, developed in Python, designed to guide and coach students in crafting their UCAS Personal Statements for the 2026 entry cycle. Leveraging Google's Gemini large language models, it offers **personalized, interactive advice**, empowering students to effectively articulate their motivations, academic preparation, and extracurricular experiences.

**Purpose & Value:**
The primary goal of this AI advisor, as part of a larger 4-phase development effort, is to demonstrate the skills acquired during the CS50 Introduction to Python course. More importantly, it aims to **solve a significant real-world problem for UK university applicants.**

The process of writing a personal statement can be daunting and often unfair in its assessment. Many students find it hard to write well, articulate their suitability, and struggle to stand out. Recognizing these challenges, **UCAS is actively moving away from the traditional personal statement for some applications, introducing a series of three short, structured questions instead, starting with the 2026 entry year** (as explained by UCAS: [The new personal statement for 2026](https://www.ucas.com/applying/applying-to-university/writing-your-personal-statement/the-new-personal-statement-for-2026)).

This AI assistant is specifically developed to help students **think through** and brainstorm content for these new 3 questions, providing a structured and guided approach. It serves as an "AI-powered assistant" to boost productivity and creativity in this crucial context. This problem is highly impactful, as approximately **700,000 people apply to UCAS every year, all of whom are required to submit a personal statement.**

---

#### **Ethical AI Usage & Integrity Guidelines:**

This project is designed with the explicit understanding of UCAS's guidelines regarding the use of AI tools in personal statements. As UCAS explicitly states:

> *"Generating (and then copying, pasting and submitting) all or a large part of your personal statement from an AI tool such as ChatGPT, and presenting it as your own words, could be considered cheating by universities and colleges and could affect your chances of an offer."*
> *"When you complete your application, you now have to declare that your personal statement hasn't been copied or provided from another source, including artificial intelligence software."*
> *"As part of our responsibility to applicants and universities and colleges, the UCAS Verification Team run checks to detect fraudulent applications and patterns of similarity in personal statements."*

This AI assistant directly addresses these concerns by:
* **Emphasizing Guidance, Not Generation:** The system prompts consistently instruct the AI to act as an advisor to help students *think through* and *articulate their own ideas*, explicitly stating that it will *not write for them*.
* **Reinforcing Personal Voice:** The AI is repeatedly prompted to emphasize that the final output must genuinely reflect the student's unique thoughts, feelings, and experiences.
* **Educating Users on Integrity:** The system implicitly and explicitly warns users about UCAS's similarity detection systems and the declaration required from applicants, reinforcing the consequences of plagiarism.

The goal is to use AI as a tool for inspiration and clarification, empowering students to find their authentic voice, rather than replacing it.

---

#### **Development Roadmap: A 4-Phase Vision**

This AI Agent is envisioned as a multi-stage development, with this CS50P project forming its foundational Phase 1.

**Phase 1: CS50P - Core Backend Logic and Proof of Concept (CLI) (Current Project)**
* **Focus:** This initial phase, serving as the final project for CS50 Introduction to Python, establishes the fundamental program logic and a proof of concept as a Command Line Interface (CLI) program.
* **Strategic Choice of CLI:** The **CLI was chosen primarily to act as a rapid proof of concept and to ensure the core AI logic and interaction flow were robust and correct.** CLIs offer several advantages for this initial stage: they are lightweight, resource-efficient, simplify debugging, and allow developers to quickly iterate on backend logic without the overhead of building a graphical user interface or web framework. This enabled a direct focus on the AI's conversational capabilities and the project's core problem-solving aspects.
* **Contribution:** It implements the essential "backend logic where the AI processing happens." This phase handles core functionalities like processing user input (e.g., chosen course, motivations, experiences), and interacting with a Large Language Model (LLM) API to generate or refine ideas for personal statement sections.
* **Data Persistence with CSV (for CLI):**
    * For this CLI-based MVP, CSV (Comma-Separated Values) files are utilized for simple data persistence of conversation logs. This choice aligns with the project's current scope, focusing on demonstrating core Python and LLM interaction skills without the overhead of a full database.
    * CSV files provide a simple, human-readable, and widely compatible format that can be easily processed by other software (like spreadsheet applications) for review or analysis. They are efficient for sequential writing of records and are a practical choice for simpler, non-relational data in a CLI context.
    * The project demonstrates how conversation turns (user inputs, AI responses) can be systematically stored in a structured, tabular format for future reference.
* **Outcome:** This phase represents the Minimal Viable Product (MVP) of the AI Agent.

**Phase 2: CS50X - Web Front-End Component (Flask) and Database Integration**
* **Focus:** (Planned for CS50 Introduction to Computer Science final project). This phase will introduce a web front-end element using Flask, transforming the CLI proof-of-concept into a more accessible and user-friendly "AI-powered assistant."
* **Database Integration:** Phase 2 introduces a web front-end using Flask, JavaScript, Python, and SQL, necessitating a formal relational database schema to store user and personal statement data. This transition allows for persistent storage, user accounts, and a more accessible user experience, handling complexities that CSV files are not suited for (e.g., concurrent access, complex queries, managing relationships between different data entities).
* **Contribution:** This phase will involve building a web-based application using JavaScript, Python, and SQL. It will include a user interface with pages for login/registration, a dashboard showing completion progress, and dedicated brainstorming sections for each of the three new UCAS personal statement questions. It will also design and implement a database schema to store user-related data and potentially their personal statement drafts or progress.
    * *(Note: All problem sets for CS50X have been completed; the final project for CS50X will be submitted after this CS50P project.)*
* **Relational Database Schema Design (Proposed for Phase 2):**
    * *(You can add proposed table names and simple columns here if you wish, e.g., `Users (id, username, password_hash)`, `PersonalStatements (id, user_id, question_id, draft_text, status)` etc., or state this will be detailed in CS50X project.)*

**Phase 3: CS50 Web Development - Enhanced Front-End Experience**
* **Focus:** (Future course). This phase will build upon the web foundation from CS50X, aiming to create a richer and more dynamic front-end user experience, potentially exploring more advanced web technologies.

**Phase 4: CS50 AI - Enhanced AI Capabilities**
* **Focus:** (Future course). While there isn't a dedicated final project for CS50 AI, the knowledge and skills acquired from this course will be crucial for significantly enhancing the AI capabilities of the Agent, potentially incorporating more advanced AI techniques and models.

---

#### **Development Stack:**

* **Python:** Chosen as the primary development language due to its widespread use in AI development and its foundational role within the CS50x curriculum, providing a familiar and robust environment.
* **LLM using Gemini:** Gemini, a family of multimodal large language models developed by Google DeepMind, was selected for the core AI functionality. This choice was paramount for several reasons:
    * **Extensive Documentation and API Support:** Google provides comprehensive documentation and robust API support, simplifying integration.
    * **Google AI Studio Integration:** Direct access to Google AI Studio was critical, allowing for easy prototyping, testing, and **effective generation and refinement of the system prompts.**
    * **Unlimited Development Calls:** The availability of free API calls during the development phase was crucial, enabling extensive testing and iteration without financial constraints.
    * Gemini's capabilities in "understanding and generating human-like text," "question answering," and assisting with "creative writing" make it an ideal tool for brainstorming and refining personal statement content.
* **User Experience (UX) Enhancements (CLI-focused):** A significant effort was made to enhance the user experience within the Command Line Interface (CLI) environment. This includes:
    * **Typewriter Effect:** For engaging display of AI responses.
    * **Processing Indicator (Spinning Wheel):** A visual cue to reassure the user that the system is actively processing their request, mitigating perceived delays.
    * **Clear Multi-Stage Feedback:** Distinct messages indicating "sending query" and "processing query."
    * **Masked API Key Input:** For improved security and privacy.
    * **Friendly Error Handling:** Converting technical API errors into understandable and actionable messages.
    * **Curated Model Selection:** Simplifying model choice for the user while providing advanced options.
* **CSV (for Phase 1 Data Persistence):** CSV files are used for structured logging of conversation sessions, providing a simple persistence solution tailored for this CLI phase.
* **Future Development Components (Phase 2+):**
    * **Flask:** A lightweight Python web framework, slated for backend development in Phase 2 to build the web application's server-side logic and routes.
    * **SQL:** Chosen for the database in Phase 2, leveraging its foundational role in managing structured data and its inclusion in web development curricula, aligning with the need for persistent storage and user management in the web application.

---

#### **Design Principles & Philosophy:**

This project is built upon several strong programming philosophies, aligning with principles emphasized in the50 curriculum:

* **Minimizing Hardcoding ("Magic Numbers/Variables"):** We actively avoid embedding literal values or configurations directly into the code where they might change or obscure meaning. Prime examples include:
    * **API Key Input:** The API key is acquired securely from the user at runtime, rather than being hardcoded in the script.
    * **Dynamic Model Selection:** Instead of a single hardcoded Gemini model, the application dynamically lists available models and allows the user to select their preference, providing flexibility and robustness against API changes.
* **Don't Repeat Yourself (DRY) & Modularity:** Repeated tasks are abstracted into reusable functions to promote clean, maintainable, and efficient code.
    * The `typewriter_print()` function is a prime example, centralizing the logic for animated text display across the entire application.
    * Utility functions like `get_selection_name()`, `start_spinner()`, and `stop_spinner()` further encapsulate specific functionalities.
* **User Experience (UX) First (even in CLI):** Despite being a Command Line Interface, significant effort was dedicated to enhancing the user experience, making the interaction intuitive and responsive. This is evident through features such as:
    * The **spinning wheel** and multi-stage processing indicators that provide real-time feedback during API calls.
    * Friendly error messages that guide the user on how to resolve issues.
    * Curated and interactive menus for easier navigation.
* **Design for Scalability & Future Phases:** Decisions in this CLI version were made with an eye toward future expansion into a more complex web application (Version 2.0).
    * **Omission of User Management in Phase 1:** For this CLI-focused MVP, a user management system (including registration and user profiles) was intentionally omitted. There was no direct requirement to maintain user profiles or long-term chat history in this stateless, single-session CLI context.
    * **CSV for Current Data Persistence:** Consequently, a full relational database was bypassed in favor of simpler CSV files for conversation logging. This keeps the current project lightweight and focused on core AI interaction.
    * **Future Integration:** Both a robust **user management system** (leveraging user sessions in Flask) and a full **relational database** (SQL) are explicitly planned for Phase 2 (CS50X) to support persistent user profiles, historical data, and a more sophisticated web application.

---

#### **Functions Overview: Building Blocks of the AI Advisor**

This project is structured around a set of modular functions, each performing a specific task to manage the user interaction, API communication, and data handling. They are grouped below by their primary responsibilities.

**I. Core Application Flow & Interaction Management:**
* `main()`: The program's entry point. Orchestrates the overall application flow, managing initial setup, session transitions, and the main application loop.
* `get_selection()`: Manages the main menu, displaying UCAS personal statement questions and handling the user's topic selection.
* `activate_gemini(systems_prompt, question_selection, chosen_model_name, first_name, degree_name, university_name)`: The core conversation engine. Manages the continuous, interactive chat session with the Gemini model, including sending queries, receiving responses, handling display, and logging data for a specific topic.

**II. User Input & Configuration:**
* `get_user_details()`: Prompts the user to collect their first name, intended degree, and target university, ensuring valid input for personalization.
* `get_api()`: Handles secure acquisition of the Google Gemini API key from the user, including masked input for privacy and basic validation.
* `get_model_choice(available_models)`: Presents a curated menu of available Gemini models to the user, highlights a recommended model, and returns the user's selection for the session.
* `get_typing_speed()`: Prompts the user to select their preferred typing speed for the typewriter effect from predefined options, demonstrates each speed, and sets a global speed preference for the application.

**III. User Experience (UX) & Display Utilities:**
* `typewriter_print(text, delay)`: A versatile utility function that prints text character by character, creating an engaging typewriter animation for all major text outputs.
* `_spinner_animation(stop_event, message)`: The background worker function for the spinner, running in a separate thread to display a continuous animating indicator.
* `start_spinner(message)`: Initializes and starts the `_spinner_animation` in a new thread, providing the necessary controls to manage it.
* `stop_spinner(stop_event, spinner_thread)`: Signals the running spinner thread to terminate gracefully and ensures its visual cleanup.
* `get_selection_name(systems_prompt)`: A helper function that extracts a concise, user-friendly topic name from the often-detailed system prompt string, primarily used for display purposes in conversation headers and logs.

**IV. External API & AI Prompt Management:**
* `verify_api(user_api_key)`: Verifies the provided API key by attempting to connect to Gemini, configures the `genai` library globally, and lists compatible models. It includes robust, user-friendly error handling for API-related issues.
* `get_systems_prompt(question_selection, first_name, degree_name, university_name)`: Generates the specific base system prompt for the AI based on the chosen UCAS question and dynamically personalizes it with the user's name, degree, and university context, guiding the AI's behavior.

---

#### **Challenges Encountered:**

Developing this AI assistant presented several interesting challenges, which served as valuable learning opportunities:

* **Persistent Environment `NameError` for `genai`:** One of the most perplexing issues involved a recurring `NameError: name 'genai' is not defined` despite correct import statements and `pip` installations. This required extensive debugging, including:
    * Thorough environment resets (`pip uninstall/install`).
    * Manual virtual environment creation and activation.
    * Deep dives into VS Code interpreter selection.
    * This problem ultimately highlighted the complexities of Python's module loading and environment management in containerized development spaces like CS50 Codespaces. The solution often involved ensuring precise interpreter paths and robust `pip` operations within the active environment.

* **Dynamic API Interaction & Error Handling:** Integrating with the Gemini API involved more than just sending text. Challenges included:
    * **`TypeError` due to inconsistent API return values:** Ensuring all code paths in `verify_api` returned a consistent two-element tuple (`(bool, list_or_None)`) to prevent `TypeError: cannot unpack non-iterable bool object`.
    * **`AttributeError` from misplaced method calls:** A subtle bug where a method object (`.lower` without `()`) was assigned instead of its result, leading to `AttributeError: 'builtin_function_or_method' object has no attribute 'lower'` when later used. This emphasized meticulous attention to syntax.
    * **`404 Model Not Found`:** Despite a valid API key, the default `gemini-pro` alias was not universally available. This necessitated implementing dynamic model listing and user selection to ensure compatibility.

* **User Experience (UX) in CLI:** Making a text-based interface feel responsive and intuitive posed its own challenges:
    * **Blocking API Calls & Animations:** The synchronous nature of API calls meant that basic `time.sleep()` loops couldn't create continuous "processing" animations. This led to the implementation of **threading** to run a spinner concurrently with the API request, providing fluid user feedback.
    * **Clear Multi-Stage Feedback:** Crafting multi-line `input()` prompts for better readability and ensuring clear instructions (like "Type 'End' to return to main menu") required careful formatting.
    * **Secure Input:** Masking the API key input was a priority for security. This involved integrating a specialized library (`stdiomask`) which, despite its functionality, presented unique challenges during environment setup and testing.

---

#### **Google Gemini's Role in Development & Troubleshooting:**

This project, while entirely coded and conceived by me, significantly benefited from leveraging Google Gemini (the model itself, accessed via Google AI Studio) as an **intelligent coding and debugging assistant**.

* **Conceptual Guidance:** Gemini helped clarify Python concepts, explain library usage patterns (e.g., proper `threading.Event` usage, `textwrap.dedent` applications, `pytest` fixtures like `monkeypatch`), and suggest architectural approaches (like the main application loop).
* **Code Generation & Refinement:** For specific functionalities or challenging blocks, Gemini provided initial code snippets or alternative implementations, which I then critically analyzed, adapted, and integrated into the project. This accelerated development and exposed me to diverse coding patterns.
* **Troubleshooting & Debugging Partner:** Crucially, Gemini served as an invaluable debugging assistant. By providing tracebacks and describing symptoms, Gemini helped in:
    * Identifying the root cause of complex errors (`TypeError`s, `AttributeError`s, `NameError`s).
    * Suggesting targeted fixes for specific error messages.
    * Explaining *why* an error occurred, deepening my understanding of Python's behavior.
    * This iterative process of providing error, receiving analysis, applying fixes, and verifying allowed for efficient problem-solving that might have taken significantly longer otherwise.

The final project represents my own comprehensive understanding, logical design, and implementation, with Gemini acting as a powerful tool to enhance learning and accelerate the development cycle.

---

#### **How to Run the Project:**

1.  **Prerequisites:**
    * Python 3.x installed.
    * A Google Gemini API key (obtainable from [Google AI Studio](https://aistudio.google.com/app/apikey)).
    * Access to a terminal (like VS Code's integrated terminal or a CS50 Codespace).

2.  **Installation (in your project directory/Codespace terminal):**
    ```bash
    pip install --upgrade google-generativeai simple-term-menu stdiomask pytest
    ```
    * *(Note: If you encounter `ModuleNotFoundError` for any package despite installation, and you are in a CS50 Codespace, ensure your virtual environment is active or try creating a new Codespace if issues persist. Specifically for `stdiomask`, if previous installation attempts in your environment caused persistent `ModuleNotFoundError` during `pytest` collection, you may consider an alternative. This project was initially developed with `stdiomask` for visual masking, but if environmental issues with `stdiomask` persist during testing, a fallback to `getpass` (standard library, no visual masking) can be implemented in `project.py` to ensure testability, though this compromises visual masking in the running app.)*

3.  **Execution:**
    ```bash
    python project.py
    ```

4.  **Follow the Prompts:**
    * The program will first ask for your **First Name, Intended Degree, and University**.
    * Then, it will prompt you for your **Google Gemini API Key** (input will be masked).
    * It will verify the API key and list available Gemini models.
    * You will be asked to **select a Gemini model** for the session.
    * Finally, you can **choose a UCAS Personal Statement question** to discuss.
    * Type **`End`** when prompted for your input in the chat to conclude a conversation session and return to the main menu.

---

#### **Testing:**

This project includes automated tests using `pytest` to ensure core functionalities work as expected.

To run the tests:

1.  Navigate to your project directory in the terminal.
2.  Activate your virtual environment if you are using one (`source .venv/bin/activate`).
3.  Run `pytest`:
    ```bash
    pytest
    ```

Tests are implemented for:
* `get_selection_name()`: Verifies that the correct user-friendly topic name is derived from system prompts.
* `get_systems_prompt()`: Checks if the system prompts are correctly generated and personalized with user details.
* `get_user_details()`: Ensures correct handling of user detail input (first name, degree, university), including valid returns and handling of empty inputs.
* `get_api()`: Ensures correct handling of API key input, including valid returns, empty input, and the 'exit' command.
