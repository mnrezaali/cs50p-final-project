## This is the final project for CS50 Introduction to Python
## by Reza Ali
## mnrezaali@github

# Standard Python libraries:
import csv # functionality for reading from and writing to CSV (Comma Separated Values) files
import datetime # classes for working with dates and times (e.g., for timestamps in logs)
import itertools # creating infinite iterators (e.g., cycling through spinner characters)
import getpass # to hide API Key input
import sys #  access to system-specific parameters and functions (e.g., sys.exit(), sys.stdout)
import textwrap # utilities for formatting text (e.g., dedenting multi-line strings)
import threading # concurrent execution (running spinner while waiting for Gemini)
import time #  functions for time-related tasks (e.g., time.sleep() for pauses)

# Third-party libraries (ensure these are installed: pip install simple-term-menu rich stdiomask):
#import stdiomask # to mask the api key
from simple_term_menu import TerminalMenu # create interactive, keyboard-navigable menus in the terminal

# Google AI Library
import google.generativeai as genai # Core Google Generative AI library

# --- 1. UTILITY FUNCTIONS (Defined FIRST, so they can be used by other functions) ---
# --- Main() will be after these functions
# --- Order of the utility functions is critical so that the functions can be called when needed

# typewriter animation function

# --- GLOBAL SETTINGS ---
# Default delay for typewriter_print. This will be updated by get_typing_speed().
_current_typewriter_delay = 0.03

# --- NEW FUNCTION: Get Typing Speed Preference ---
def get_typing_speed():
    """
    Prompts the user to select a typing speed for the typewriter effect
    from predefined options using TerminalMenu, and demonstrates each speed.
    Sets the global _current_typewriter_delay based on user's choice.
    """
    # Declare that we intend to modify the global variable
    global _current_typewriter_delay # CRITICAL: Tells Python we're changing the global variable

    typewriter_print("\n--- Customize Your Typing Speed ---", delay=0.01) # Use a fixed speed for this setup message

    # MODIFIED: Label Medium as (Default)
    speed_options_map = { # Map string choices to their delay values
        "Fast": 0.01,
        "Medium (Default)": 0.03, # Changed name here
        "Slow": 0.06
    }

    menu_display_names = [] # List to hold just the names for the menu
    demo_text = "This demonstration shows how quickly the AI's responses will appear on your screen." # Text for demonstration

    # Build the options for TerminalMenu, including a demo of each speed
    for name, delay_val in speed_options_map.items():
        # Play the demo directly to the console before adding to menu options
        sys.stdout.write(f"  {name} - Demo: ")
        sys.stdout.flush()
        for char in demo_text[:20]: # Show first 20 characters of demo text
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay_val)
        print() # Newline after each demo line

        menu_display_names.append(name) # MODIFIED: Add just the name to the menu options


    while True: # Loop until a valid choice is made or program exits
        typewriter_print("\nSelect your preferred typing speed:")

        terminal_menu = TerminalMenu(menu_display_names) # Create menu using just the names
        options_index = terminal_menu.show() # Show menu and get index

        if options_index is None: # User might have pressed Ctrl+C or Esc
            typewriter_print("No speed selected. Exiting program.")
            sys.exit(0) # Exit cleanly

        # Get the chosen name from the menu list (e.g., "Medium (Default)")
        chosen_speed_name = menu_display_names[options_index]

        # Get the actual delay value from our map using the chosen name
        chosen_delay = speed_options_map[chosen_speed_name]

        _current_typewriter_delay = chosen_delay # SET THE GLOBAL VARIABLE
        typewriter_print(f"Selected speed: {chosen_speed_name} ({chosen_delay:.2f}s/char)")
        return # Exit the function, as a speed has been chosen

# typewriter animation function
def typewriter_print(text, delay=None): # MODIFIED: delay is now None by default
    """
    Prints text character by character with a typewriter effect so that the user can follow and read easily.
    Uses a global delay setting unless a specific delay is provided.

    Args:
        text (str): The string to print.
        delay (float, optional): The delay in seconds between each character.
                                 If None, uses the global _current_typewriter_delay.
    """
    # Use the provided delay, or fallback to the global setting
    actual_delay = delay if delay is not None else _current_typewriter_delay

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()  # Force the character to appear immediately
        time.sleep(actual_delay) # MODIFIED: Use actual_delay
    print()  # Print a final newline after the entire text is done

# Spinner animation function (runs in a separate thread)
def _spinner_animation(stop_event, message="Thinking"):
    """
    Function that runs in a separate thread to display a continuous spinner animation.
    It stops when signaled by the `stop_event`.

    Args:
        stop_event (threading.Event): An event object used to signal the thread to stop.
        message (str): The base message to display before the spinner (e.g., "Gemini is processing").
    """
    spinner_chars = itertools.cycle(['-', '\\', '|', '/']) # Create an infinite cycle of spinner characters

    # Initial print of the spinner to show it immediately
    sys.stdout.write(f"\r{message} {next(spinner_chars)}") # \r moves cursor to start of line, next() gets first char
    sys.stdout.flush() # Force immediate display

    # Loop continuously while the 'stop_event' has NOT been set
    while not stop_event.is_set():
        sys.stdout.write(f"\r{message} {next(spinner_chars)}") # Overwrite the current line with next spinner char
        sys.stdout.flush() # Ensure it's displayed
        time.sleep(0.1) # Pause briefly to create the animation effect (controls spinner speed)

    # Once stop_event is set (meaning Gemini has responded or an error occurred):
    sys.stdout.write('\r' + ' ' * (len(message) + 3) + '\r') # Clear the entire line the spinner was on
    sys.stdout.flush() # Ensure the line is cleared

# Function to start the spinner
def start_spinner(message="Gemini is thinking"):
    """
    Starts the spinner animation in a new, separate thread.
    This allows the spinner to animate continuously while the main thread
    is blocked waiting for a response (e.g., from Gemini API).

    Args:
        message (str): The message to display with the spinner.

    Returns:
        tuple: A tuple containing (stop_event, spinner_thread).
               The 'stop_event' is used to signal the spinner thread to stop.
               The 'spinner_thread' is the Thread object itself.
    """
    stop_event = threading.Event()  # Create an event to signal the thread to stop
    spinner_thread = threading.Thread(target=_spinner_animation, args=(stop_event, message))
    spinner_thread.daemon = True  # Allow main program to exit even if thread is running
    spinner_thread.start()  # Start the thread
    return stop_event, spinner_thread  # Return the event and thread object to control it later

# Function to stop the spinner
def stop_spinner(stop_event, spinner_thread):
    """
    Stops the spinner animation thread.

    Args:
        stop_event (threading.Event): The event object used to signal the spinner thread.
        spinner_thread (threading.Thread): The Thread object of the running spinner.
    """
    stop_event.set()  # Set the event to tell the spinner thread to stop
    spinner_thread.join()  # Wait for the spinner thread to finish
    sys.stdout.write('\r' + ' ' * 50 + '\r')  # Just in case, a final clear (overwrites more widely)
    sys.stdout.flush()

def get_selection_name(systems_prompt):
    """
    Analyzes the system prompt to determine the user-friendly name of the current question/topic.
    This is used for display purposes (e.g., in the conversation header).

    Args:
        systems_prompt (str): The full system prompt string.

    Returns:
        str: A user-friendly name for the topic.
    """
    # These phrases should match unique parts of your actual system prompts
    if "Why do you want to study this course" in systems_prompt:
        return "Question 1: Why study this course?"
    elif "how their academic journey and formal education" in systems_prompt:
        return "Question 2: Academic preparation."
    elif "experiences and activities beyond formal education" in systems_prompt:
        return "Question 3: Extracurriculars and life experience."
    return "Current Topic"  # Fallback if no match is found

# Function to get user's personal details ---
def get_user_details():
    """
    Prompts the user for their first name, intended degree, and university name.
    Ensures non-empty inputs for all fields.

    Returns:
        tuple: (first_name, degree_name, university_name)
    """
    typewriter_print("\n--- Let's get some details for personalization ---")

    while True:
        first_name = input("Please enter your First Name: ").strip()
        if not first_name:
            typewriter_print("First name cannot be empty. Please enter your first name.")
        else:
            break

    while True:
        # TO DELETE degree_name = input(f"Hi {first_name}, what is the full name of the Degree/Course you intend to study (e.g., Bachelor of Laws, Computer Science BSc): ").strip()

        degree_name = input(
            f"Hi {first_name}, what is the full name of the Degree/Course\n "
            f"you intend to study (e.g., Bachelor of Laws, Computer Science BSc): "
        ).strip()
        if not degree_name:
            typewriter_print("Degree/Course name cannot be empty. Please enter it.")
        else:
            break

    while True:
        # TO DELETE university_name = input(f"At which University/College do you intend to study {degree_name} (e.g., University of Malaya, Taylor's University): ").strip()
        university_name = input(
            f"At which University/College do you intend to study {degree_name}\n "
            f"(e.g., University of Malaya, Taylor's University): "
            ).strip()
        if not university_name:
            typewriter_print("University/College name cannot be empty. Please enter it.")
        else:
            break

    typewriter_print(f"\nGreat! We have your details: {first_name}, {degree_name} at {university_name}.")
    return first_name, degree_name, university_name


# --- 2. API Key Management ---

def get_api():
    """
    Prompts the user to enter their Gemini API key.
    Ensures the input is not empty and allows the user to exit the program.

    Returns:
        str: The stripped API key entered by the user.
    """
    while True:
        try:
            api_input = getpass.getpass(prompt="Enter your Gemini API key (input will NOT be echoed, type 'exit' to quit): ").strip()
#            api_input = input("Enter your Gemini API key or enter 'exit' to quit: ").strip()
            #api_input = stdiomask.getpass(prompt="Enter your Gemini API key (input will be masked, type 'exit' to quit): ").strip()
            if api_input.lower() == 'exit':
                typewriter_print("Exiting this program.")
                sys.exit(0)  # Exit cleanly
            elif api_input == "":  # Correctly checks for empty string after stripping
                typewriter_print("Error: No API key was entered. Please try again.")
            else:
                typewriter_print("API key received. Attempting verification...")
                return api_input
        except Exception as e:
            typewriter_print(f"An unexpected error occurred during input: {e}. Please try again.")


def verify_api(user_api_key):
    """
    Verifies the provided API key by attempting a connection to Gemini's API.
    If successful, it configures the 'google.generativeai' library globally with this key.
    It also lists and returns the names of models available for text generation.

    Args:
        user_api_key (str): The API key to verify.

    Returns:
        tuple: (bool, list_of_models) if successful (True and a list of model names),
               (False, None) if verification fails or no suitable models are found.
    """
    if not user_api_key:
        typewriter_print("Internal Error: Attempted to verify an empty/None API key.")
        return False, None # <-- CORRECTED: Returns (False, None)

    available_models_for_generation = [] # Initialize this list before the try block

    try:
        # CONFIGURE GENAI GLOBALLY HERE: This sets the API key for all future genai calls
        genai.configure(api_key=user_api_key)

        typewriter_print(
            "\nAttempting to connect and list models to verify API key and capabilities...")

        # Iterate through all models available via this API key
        for model in genai.list_models():
            # Check if the model supports the 'generateContent' method, which is for chat/text generation
            if "generateContent" in model.supported_generation_methods:
                available_models_for_generation.append(model.name)
                # Use standard print here for immediate, non-typewriter output during system check
                print(f"  - Found available model for generation: {model.name}")

        if not available_models_for_generation:  # If the list remains empty after checking all models
            typewriter_print(
                "Error: No models found that support 'generateContent' with this API key.")
            typewriter_print(
                "Please ensure your project has access to Gemini models (e.g., 'gemini-pro' or 'gemini-1.0-pro').")
            return False, None  # Correct here already

        typewriter_print("API Key successfully verified with Google AI Studio!")
        typewriter_print(
            "Please note the exact model names listed above, especially for 'gemini-pro' or 'gemini-1.0-pro'.")
        # Return True for success and the list of available model names
        return True, available_models_for_generation # Correct here already

    except Exception as e:  # Catch any broad exception during API verification
#  TO DELETE     typewriter_print(f"\nAPI Key Verification Failed: {e}")
#  TO DELETE      typewriter_print(
#   TO DELETE          "Please ensure your API key is correct, active, and has the necessary permissions.")
        error_message = str(e).lower() # Convert exception to string and make lowercase for easy checking

        # --- FRIENDLIER ERROR HANDLING ---
        if "api key expired" in error_message:
            typewriter_print("\nAPI Key Verification Failed: Your API key has expired.")
            typewriter_print("Please generate a new API key from Google AI Studio and try again.")
        elif "api_key_invalid" in error_message or "unauthenticated" in error_message:
             typewriter_print("\nAPI Key Verification Failed: Your API key is invalid or incorrect.")
             typewriter_print("Please double-check your API key for typos or generate a new one from Google AI Studio.")
        elif "quota exceeded" in error_message:
             typewriter_print("\nAPI Key Verification Failed: API quota exceeded.")
             typewriter_print("You might have reached your usage limits. Please try again later or check your Google AI Studio usage.")
        elif "not found" in error_message and "models" in error_message:
            # This covers the 404 for specific models if it wasn't caught by the available_models_for_generation check
            typewriter_print("\nAPI Key Verification Failed: Requested model not found or not available for your key/region.")
            typewriter_print("Please ensure your project has access to Gemini models that support 'generateContent'.")
        else:
            # Generic fallback for unhandled exceptions
            typewriter_print(f"\nAPI Key Verification Failed: An unexpected error occurred: {e}")
            typewriter_print("Please ensure your API key is correct, active, and has the necessary permissions.")

        return False, None

def get_model_choice(available_models):
    """
    Presents a curated menu of highly relevant Gemini models to the user
    and gets their selection, highlighting a recommended model.
    Not part of the original design. This was added to allow user to pick model
    instead of hard-coded. This provide flexibility to user

    How it works:
        - define a recommended model for the user
        - build a list of models to choose from
        - allow user to make a choice
        - return the choice
    """
    typewriter_print("\n--- Model Selection ---")
    typewriter_print("Please choose a model for your conversation:")

    # Define the curated list of top relevant models (these are general recommendations)
    curated_options_base = {
        "models/gemini-1.5-flash": "Balanced for speed & quality",
        "models/gemini-1.5-pro": "Higher quality, deeper reasoning",
        "models/gemini-2.5-pro": "Latest & most powerful (if available)" # This might be a preview
    }

    # Your primary recommendation (must be one of the keys in curated_options_base)
    recommended_model_base = "models/gemini-1.5-flash"

    model_menu_options = []
    actual_available_curated_models = [] # Initialize this list

    # First, build a list of only the curated models that are actually available to the user
    for model_key, description in curated_options_base.items():
        if model_key in available_models: # Check if the curated model is in the list of what's actually available from API
            actual_available_curated_models.append((model_key, description))

    # Fallback if none of the curated models are available (should ideally not happen after verify_api)
    if not actual_available_curated_models:
        typewriter_print(
            "Error: No suitable curated models are available. Please contact support or try a different API key.")
        sys.exit(1)  # Critical error, exit program

    # Now, prioritize the recommended model and add the (Recommended) tag
    # Iterate through the actual available curated models to build the display menu
    for model_name, description in actual_available_curated_models:
        if model_name == recommended_model_base:
            # Insert recommended model at the very beginning of the list
            model_menu_options.insert(0, f"{model_name} (Recommended - {description})")
        else:
            model_menu_options.append(f"{model_name} ({description})")

    # This block ensures the recommended model is definitively at the top
    # (Handles edge cases where it might have been added later then moved)
    if model_menu_options and not model_menu_options[0].startswith(recommended_model_base):
        for i, option in enumerate(model_menu_options):
            if option.startswith(recommended_model_base):
                reco_option = model_menu_options.pop(i) # Remove it from its current position
                model_menu_options.insert(0, reco_option) # Insert it at the beginning
                break

    model_menu_options.append("Exit Program") # Add the option to exit the program

    terminal_menu = TerminalMenu(model_menu_options) # Create the menu object
    options_index = terminal_menu.show()  # Display menu and get user's selection index

    if options_index is None:  # User might have pressed Ctrl+C or Esc
        typewriter_print("No model selected. Exiting program.")
        sys.exit(0) # Exit cleanly

    chosen_model_display = model_menu_options[options_index] # Get the display string of the chosen model

    if chosen_model_display == "Exit Program": # Check if user chose to exit
        typewriter_print("Exiting program as requested.")
        sys.exit(0)

    # Extract the actual model name by stripping any description or recommendation tag
    # Assumes the model name is the first word (or part before the first space)
    chosen_model = chosen_model_display.split(' ')[0]

    typewriter_print(f"You have selected: {chosen_model}")
    return chosen_model

# --- 3. QUESTION SELECTION ---

def get_selection(): # <--- This function takes NO PARAMETERS
    """
    Presents the main menu of questions to the user using simple_term_menu
    and gets their selection. Includes an 'Exit' option.

    Returns:
        str: The chosen question string (e.g., "Question 1", "Exit").
    """
    main_menu_options = ["Question 1", "Question 2", "Question 3", "Exit"]

    typewriter_print("\n--- Main Menu ---")
    typewriter_print(
        "This AI Assistant is designed to guide and coach you through the three personal statement questions required by UCAS for 2026 entry.")
    typewriter_print("Here are the three questions:")
    typewriter_print("  Question 1: Why do you want to study this course or subject?")
    typewriter_print(
        "  Question 2: How have your qualifications and studies helped you to prepare for this course or subject?")
    typewriter_print(
        "  Question 3: What else have you done to prepare outside of education, and why are these experiences useful?")
    typewriter_print(
        "We can discuss any of these questions, one at a time. Please make your selection.")

    # Create and show the menu
    terminal_menu = TerminalMenu(main_menu_options)
    options_index = terminal_menu.show()  # This pauses until user selects

    # Handle the user's choice
    if options_index is None:  # User might have pressed Ctrl+C or Esc
        typewriter_print("No selection made. Exiting program.")
        sys.exit(0)  # Exit cleanly if menu is dismissed

    options_choice = main_menu_options[options_index]

    if options_choice == "Question 1":
        typewriter_print("You have selected Question 1.")
    elif options_choice == "Question 2":  # Removed the colon here to match menu option exactly
        typewriter_print("You have selected Question 2.")
    elif options_choice == "Question 3":  # Removed the colon here
        typewriter_print("You have selected Question 3.")
    elif options_choice == "Exit":
        typewriter_print("You have selected Exit. The program will now exit.")
        # No sys.exit() here; the main loop handles exiting based on this return.

    return options_choice

# --- 4. System Prompt Management ---

# --- 4. System Prompt Management ---

def get_systems_prompt(question_selection, first_name, degree_name, university_name):
    """
    Returns the appropriate system prompt string based on the user's question selection,
    personalized with user details.
    Uses textwrap.dedent to remove unintended leading whitespace from multi-line strings.

    Systems prompt design using Google AI Studio.
    Need constant refinement

    Possible future enhancements:
        - include as part of administrator edits so that enhancements and changes can be edited through program
        and not hard coded
    """
    # Create a personalized introduction for the system prompt
    # This context will be prepended to every specific question's system prompt.
    personal_intro = textwrap.dedent(f"""\
    The user's name is {first_name}.
    They intend to study {degree_name} at {university_name}.
    Your advice should be specifically tailored to this context, addressing them by their name where appropriate.
    """)

    # Using textwrap.dedent and the "\" at the start of the string to ensure
    # no unwanted leading spaces are included in the prompt itself.

    question_1_systems_prompt = textwrap.dedent("""\
    You are an insightful and encouraging student advisor, specializing in helping users articulate their deep, personal motivations for pursuing a specific university or college course. Your core mission for this interaction is to guide the user in uncovering and expressing their genuine passion, existing knowledge, and future ambitions directly related to their chosen subject, as this is precisely what universities are looking for when assessing personal statements.

    Your guidance should specifically focus on helping the user explore and develop content for Question 1: 'Why do you want to study this course or subject?'. Prompt the user to consider and elaborate on:
    Personal Motivations: What specific moments, key role models, intellectual curiosities, or life experiences have ignited their desire to study this particular subject? Encourage them to share their unique story that led them to this course.
    Demonstrated Knowledge & Engagement: What research have they done, or what super-curricular activities have they engaged in, that showcase their existing knowledge and curiosity beyond the classroom? This could include specific books they've read, documentaries watched, subject experts they admire, relevant projects undertaken, or topics they've explored independently. Universities want to see evidence of genuine research and interest.
    Future Aspirations & Course Fit: How does this specific course align with their long-term career aspirations or personal goals? Help them connect the knowledge and skills they anticipate gaining from this particular course to their envisioned future, whether a specific profession or broader personal development.

    When assisting the user, continuously emphasize that:
    This section is profoundly "personal" and must genuinely reflect their own thoughts, feelings, skills, and unique experiences. A "bland AI-generated personal statement is not what universities and colleges are looking for".
    AI is a tool to inspire ideas, clarify thoughts, and assist with articulation, not to replace their voice or generate content for them.
    Copying and pasting all or a large part of their personal statement from an AI tool like ChatGPT is considered cheating by universities and colleges. UCAS employs similarity detection systems, and any similarity greater than 30% will be flagged to universities. The user must declare that their personal statement has not been copied or provided from another source, including AI software.
    The final output is the user's responsibility, requiring them to review it for clarity, relevance, and accuracy.""")

    question_2_systems_prompt = textwrap.dedent("""\
    You are an insightful and encouraging student advisor, focused on helping users effectively articulate how their academic journey and formal education have prepared them for their chosen university or college course. Your primary goal for this interaction is to guide the user in identifying and elaborating on the relevant skills, knowledge, and experiences gained from their studies, demonstrating their suitability and readiness for the subject area.

    Your guidance should specifically prompt the user to explore and develop content that answers Question 2, focusing on:
    Relevance of Studies: Encourage the user to detail how their current or previous formal education (e.g., school, college, training provider, or even a short online university course) directly relates to their chosen course(s) or subject area. The focus should be on what is most recent and relevant.
    Skills Development: Help the user identify and elaborate on the relevant or transferable skills they have gained from their studies that make them a strong candidate for the course. This could include how specific subjects or modules helped them develop core skills or revealed their interests and strengths.
    Educational Achievements (Beyond Grades): Guide the user to discuss any pertinent academic accomplishments that go beyond just their grades, which are listed elsewhere in their application. Examples include winning school or national competitions, serving as a student ambassador or team captain, or taking a lead role in a play.

    When assisting the user, continuously emphasize that:
    The personal statement is precisely that: "personal". It should genuinely reflect their own thoughts, feelings, skills, and unique experiences. Universities are looking for their voice, not a "bland AI-generated personal statement".
    AI is a tool to inspire ideas, clarify thoughts, and assist with articulating their own ideas, but it is not a substitute for their unique thoughts or experiences, nor should it write the statement for them.
    Generating (and then copying, pasting and submitting) all or a large part of their personal statement from an AI tool like ChatGPT is considered cheating by universities and colleges. UCAS employs similarity detection systems, and any similarity greater than 30% will be flagged to universities and colleges. Applicants must declare that their personal statement has not been copied or provided from another source, including AI software.
    The final personal statement is the user's responsibility, requiring thorough review for clarity, relevance, and accuracy before submission, as AI tools "do get things wrong".""")

    question_3_systems_prompt = textwrap.dedent("""\
    You are an insightful and encouraging student advisor, specializing in helping users articulate the value and relevance of their experiences and activities beyond formal education. Your core mission for this interaction is to guide the user in uncovering, reflecting on, and clearly explaining how these non-academic pursuits have prepared them for their chosen university or college course and why these experiences are useful to their application. This section is expected to be "highly personal" and demonstrate a unique fit for the course.

    Your guidance should specifically focus on helping the user explore and develop content for Question 3, prompting them to consider and elaborate on:
    Work Experience, Employment, or Volunteering: Whether paid work, internships, virtual experiences (e.g., through Springpod), or volunteering (e.g., at a dog shelter), encourage the user to reflect on how these experiences relate to their chosen course and what specific skills or insights they gained that are relevant. The key is the reflection on "why you’re including it" and the skills gained.
    Personal Life Experiences or Responsibilities: Help the user identify situations they've overcome, or responsibilities (e.g., caring for a family member), that have helped them develop essential qualities like resilience, empathy, time management, or problem-solving skills relevant to their studies.
    Hobbies and Extracurricular/Outreach Activities: Guide them to think about activities outside of their studies, such as sports, reading, community work, or summer schools. The aim is to showcase how these activities further demonstrate their suitability for the course and reveal interests beyond the classroom.
    Achievements Outside of School or College: Prompt the user to discuss any accomplishments not tied to their formal academic record, such as holding a position of responsibility (e.g., club captain), musical achievements, competitions won, or qualifications attained outside school.
    Post-Education Activities (if applicable): If the user is no longer in full-time education, encourage them to detail what they have been doing since leaving and how these activities have equipped them with relevant skills and qualities for their desired course(s).

    When assisting the user, continuously emphasize that:
    This section, like the entire personal statement, is exactly "personal". It should genuinely reflect their own thoughts, feelings, skills, and unique experiences". Universities are looking for their voice, not a "bland AI-generated personal statement".
    AI is a tool to inspire ideas, clarify thoughts, and assist with articulating their own ideas, rather than replacing their voice or generating content for them.
    Copying and pasting all or a large part of their personal statement from an AI tool like ChatGPT is considered cheating by universities and colleges. UCAS employs similarity detection systems, and any similarity greater than 30% will be flagged to universities. The user must declare that their personal statement has not been copied or provided from another source, including AI software.
    The final output is the user's responsibility, and they must review it for clarity, relevance, and accuracy, as AI tools "do get things wrong".""")

    if question_selection == "Question 1":
        # Ensure 'personal_intro' is prepended here
        systems_prompt = personal_intro + question_1_systems_prompt
    elif question_selection == "Question 2":
        # Ensure 'personal_intro' is prepended here
        systems_prompt = personal_intro + question_2_systems_prompt
    elif question_selection == "Question 3":
        # Ensure 'personal_intro' is prepended here
        systems_prompt = personal_intro + question_3_systems_prompt
    else:
        # Ensure 'personal_intro' is prepended here for default as well
        systems_prompt = personal_intro + "Default system prompt: No specific question selected."

    return systems_prompt

# --- 5. GEMINI INTERACTION ---

def activate_gemini(systems_prompt, question_selection, chosen_model_name, # Existing parameters
                    first_name, degree_name, university_name): # MODIFIED: Added user detail parameters
    """
    Manages a continuous conversation with the Gemini model for a specific system prompt.
    Allows continuous interaction until the user types 'Done'.
    Logs the conversation to a CSV and prints it at the end of the session.

    Args:
        systems_prompt (str): The specific system prompt for the chosen question.
        question_selection (str): The user's chosen question (e.g., "Question 1").
        chosen_model_name (str): The name of the Gemini model selected by the user.
        first_name (str): The user's first name, for personalization.
        degree_name (str): The intended degree/course name, for personalization.
        university_name (str): The intended university/college name, for personalization.
    """
    # Initialize the list to store conversation data for logging for this session
    conversation_data = []

    try:
        # Initialize the model with the system instruction.
        # The API key is implicitly used because genai.configure() was called in verify_api.
        model = genai.GenerativeModel(
            model_name=chosen_model_name,
            system_instruction=systems_prompt # This sets the AI's persona and task for the session
        )

        # Start a new chat session with an empty history for this specific conversation.
        # This is CRITICAL for maintaining context (memory) throughout the continuous chat.
        # Each time activate_gemini is called (e.g., user selects a new question from main menu),
        # a FRESH chat session starts, ensuring previous question's context isn't carried over.
        chat = model.start_chat(history=[])

        # Get a user-friendly name for the current selection for display and logging
        current_selection_display_name = get_selection_name(systems_prompt)

        # Log the system prompt itself as the very first entry in the conversation data
        conversation_data.append([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # Timestamp
            "System Prompt", # Role
            current_selection_display_name, # Topic
            systems_prompt # Content
        ])

        # Initial conversation setup messages for the user
        typewriter_print(f"\n--- Starting conversation for {current_selection_display_name} ---")
#        typewriter_print("The AI is ready. You can now ask questions related to this topic.")

        # Display the specific question context for the user's benefit
#        if question_selection == "Question 1":
#            typewriter_print("We are focused on Question 1: Why do you want to study this course or subject?")
#        elif question_selection == "Question 2":
#            typewriter_print("We are focused on Question 2: How have your qualifications and studies helped you to prepare for this course or subject?")
#        else: # Assuming this 'else' covers "Question 3" based on menu options
#            typewriter_print("We are focused on Question 3: What else have you done to prepare outside of education, and why are these experiences useful?")

        typewriter_print("Type 'Done/End' at any time to return to the main question selection.")

        # --- The continuous conversation loop starts here ---
        while True: # This loop keeps the conversation going until user types 'Done'
            user_input = input("You (type 'End' to return to main menu): ").strip().lower() # Get user's input, remove leading/trailing whitespace

            if user_input.lower() == 'end': # Check if user wants to end the current conversation
                typewriter_print("Ending conversation. Saving the chat and returning to main menu.")
                break  # Exit this inner 'while True' loop, control returns to 'main()'
            elif not user_input: # If user just pressed Enter without typing
                typewriter_print("Please enter a question or 'End' to exit the conversation.")
                continue # Skip the rest of this loop iteration, prompt for input again
            else:
                stop_event = None # Initialize stop_event for spinner control
                spinner_thread = None # Initialize spinner_thread for spinner control
                try:
                    # This tells Gemini the user's name on each turn.
                    augmented_user_message = f"My name is {first_name}. {user_input}"

                    # Log user's original input BEFORE sending to Gemini
                    conversation_data.append([
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # Timestamp
                        "User", # Role
                        current_selection_display_name, # Topic
                        user_input # Log the exact input typed by the user
                    ])

                    # Stage 1: Indicate to the user that query is being sent
                    typewriter_print("We are sending your query to Gemini...")
                    time.sleep(0.5) # A brief pause for readability

                    # Stage 2: Start the continuous processing animation
                    # This will run in a separate thread while the API call is blocking
                    stop_event, spinner_thread = start_spinner("Gemini has received your query and is processing")

                    # Send the AUGMENTED user message to the chat session.
                    # The 'chat' object automatically manages sending the full conversation history
                    # along with this new message for continuous context.
                    response = chat.send_message(augmented_user_message) # MODIFIED: Send the augmented message

                    # Stage 3: Stop the spinner animation as soon as the response is received
                    stop_spinner(stop_event, spinner_thread)

                    if response and response.text: # Check if a valid text response was received
                        typewriter_print("Gemini: " + response.text) # Display Gemini's response
                        # Log Gemini's response
                        conversation_data.append([
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Gemini",
                            current_selection_display_name,
                            response.text # Log the text of Gemini's response
                        ])
                    else:
                        typewriter_print("Gemini: (No readable response received)")
                        # Log that no readable response was received, for debugging
                        conversation_data.append([
                            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Gemini",
                            current_selection_display_name,
                            "(No readable response received)"
                        ])

                except Exception as e: # Catch any errors during the API interaction itself
                    if stop_event and spinner_thread: # Ensure spinner is stopped even on error
                        stop_spinner(stop_event, spinner_thread)
                    typewriter_print(f"An error occurred during Gemini interaction: {e}")
                    typewriter_print("Please try again or type 'Done' to return to the main menu.")
                    # Log the error information
                    conversation_data.append([
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Error",
                        current_selection_display_name,
                        f"API Interaction Error: {e}"
                    ])

        # --- End of inner 'while True' loop. Code here executes when user types 'Done'. ---

        # Generate a unique filename for the CSV conversation log
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Clean the display name for use in filename (replace spaces, colons, hyphens)
        safe_display_name = current_selection_display_name.replace(" ", "_").replace(":", "").replace("-", "_").lower()

        # Make user details safe for filenames (alphanumeric, underscores, hyphens)
        # Using .lower() for consistency
        safe_first_name = "".join(char for char in first_name if char.isalnum()).lower()
        safe_degree_name = "".join(char for char in degree_name if char.isalnum()).lower()
        safe_university_name = "".join(char for char in university_name if char.isalnum()).lower()

        filename = f"{safe_first_name}_{safe_degree_name}_{safe_university_name}_{safe_display_name}_{timestamp_str}.csv"
# ... (inside activate_gemini function, after the CSV saving block) ...

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(conversation_data)
            typewriter_print(f"\nConversation saved to {filename}")
        except IOError as e:
            typewriter_print(f"\nError saving conversation to CSV: {e}")

        # --- REFINED CONSOLE LOG PRINTING ---
        typewriter_print("\n" + "=" * 80) # Top border
        typewriter_print(f"--- CONVERSATION SUMMARY for {current_selection_display_name} ---")
        typewriter_print(f"--- Session with {first_name} for {degree_name} at {university_name} ---")
        typewriter_print("=" * 80) # Bottom border

        # Print header for console table (slightly adjusted to match content better)
        typewriter_print(f"| {'TIMESTAMP':<19} | {'ROLE':<10} | {'TOPIC':<25} | {'CONTENT PREVIEW':<50} |")
        typewriter_print("-" * 115) # Separator line

        # Iterate through conversation_data (skip the first row as it's the CSV header,
        # which we manually print as a table header above)
        for row in conversation_data[1:]:
            timestamp, role, topic, content = row
            display_content = content.replace('\n', ' ').strip() # Replace newlines for single-line console output
            if len(display_content) > 50: # Truncate long content for better table fit
                display_content = display_content[:47] + "..." # Truncate and add ellipsis
            typewriter_print(f"| {timestamp:<19} | {role:<10} | {topic:<25} | {display_content:<50} |")
        typewriter_print("-" * 115) # Separator line
        typewriter_print("--- END OF CONVERSATION SUMMARY ---")
        typewriter_print("=" * 80 + "\n") # Bottom border and newline for separation

        # --- NEW: Clear call to action for the user ---
        typewriter_print("You've completed this conversation session.")
        typewriter_print("The full log has been saved for your records.")
        typewriter_print("You will now be returned to the main menu to select another question or exit the program.")
        # --- END NEW ---

    except Exception as e:
        typewriter_print(f"An error occurred during activate_gemini setup: {e}")
        typewriter_print("This might indicate a problem with the API configuration or model access.")

# --- 6. MAIN PROGRAM EXECUTION FLOW ---

def main():
    typewriter_print("Welcome to your Personal Statement Assistant!")
    typewriter_print("This is a CS50 Introduction To Python Final Project.")
    # Step 1:Get and Validate API Key
    user_api_key = get_api()

    typewriter_print(f"The last 4 digits of you API is {user_api_key[-4:]}. This API key should be kept secure and private.")

    # verify_api will configure genai globally if successful and return True
    # It returns a tuple (boolean success, list of available models)
    is_api_valid, available_models_for_generation = verify_api(user_api_key)

    if not is_api_valid: # If API key verification failed or no models found
        sys.exit(1) # Exit the program

    # Blocking pause to allow user to read verification messages
    input("Your API has been verified. Press enter to continue:")

    # Step 2: Allow user to choose a Gemini model from the available list
    # 'available_models_for_generation' is now correctly defined from verify_api's return
    chosen_model_name = get_model_choice(available_models_for_generation)

    # Step 3: Get User Details (This part will be updated in next major task)
    user_first_name, user_degree, user_university = get_user_details()

    # Step 4: Get Typing Speed
    # Allow the user to customize the typing speed for the typewriter effect.
    # This sets the global _current_typewriter_delay variable.
    get_typing_speed()

    # Step 5: Main Application Loop - Allows user to pick questions repeatedly
    while True: # This outer loop keeps the application running until explicitly exited
        selected_question = get_selection() # Get user's choice from main menu

        if selected_question == "Exit": # Check if user chose to exit the entire program
            typewriter_print("Thank you for using the assistant. Goodbye!")
            sys.exit(0) # Exit cleanly
        else:
            # Get the system prompt specific to the chosen question
            # (This function will be updated in Task 5 to accept user details)
            # TO DELETE systems_prompt_text = get_systems_prompt(selected_question)
            systems_prompt_text = get_systems_prompt(selected_question,
                                                     user_first_name,
                                                     user_degree,
                                                     user_university)

            # Activate Gemini for continuous conversation on this topic
            # This function contains its own inner 'while True' loop for continuous chat.
            # (This function's parameters will be updated in Task 5 to accept user details)
            # TO DELETE activate_gemini(systems_prompt_text, selected_question, chosen_model_name)
            activate_gemini(systems_prompt_text,
                            selected_question,
                            chosen_model_name,
                            user_first_name,    # New parameter
                            user_degree,        # New parameter
                            user_university)    # New parameter

            # When activate_gemini breaks (user types 'Done' in the inner chat loop),
            # control returns here. The outer while loop in main() then continues,
            # bringing the user back to get_selection() to choose a new question.
            typewriter_print("\nReturning to main menu for new selection.")


# --- 7. ENTRY POINT ---
# This standard Python construct ensures that main() is called only when the script
# is executed directly (e.g., 'python project_copy.py'), not when it's imported as a module.
if __name__ == "__main__":
    main()
