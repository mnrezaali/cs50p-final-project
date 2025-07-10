import pytest
import sys


# Import the functions you want to test from your project.py file
# Removed get_api (as it uses stdiomask)
# Added get_user_details as a third test function
from project import get_selection_name, get_systems_prompt, get_api, get_user_details


# --- Test 1: Testing get_selection_name() ---
# This function takes a system prompt string and returns a display name string.
def test_get_selection_name():
    # Test for Question 1 specific prompt
    # We use a unique part of the actual system prompt as a proxy
    q1_prompt_part = "Why do you want to study this course"
    assert get_selection_name(q1_prompt_part) == "Question 1: Why study this course?"

    # Test for Question 2 specific prompt
    q2_prompt_part = "how their academic journey and formal education"
    assert get_selection_name(q2_prompt_part) == "Question 2: Academic preparation."

    # Test for Question 3 specific prompt
    q3_prompt_part = "experiences and activities beyond formal education"
    assert get_selection_name(q3_prompt_part) == "Question 3: Extracurriculars and life experience."

    # Test for an unknown/default prompt (should return "Current Topic")
    unknown_prompt = "This is a random sentence not matching any question."
    assert get_selection_name(unknown_prompt) == "Current Topic"


# --- Test 2: Testing get_systems_prompt() ---
# This function takes question_selection and user details, and returns a personalized system prompt string.
def test_get_systems_prompt():
    # Define some dummy user details for testing
    test_first_name = "TestUser"
    test_degree = "Computer Science BSc"
    test_university = "Fake University"

    # Test Question 1 prompt generation
    q1_prompt_output = get_systems_prompt("Question 1", test_first_name, test_degree, test_university)
    # Check if the personalized intro is present
    assert f"The user's name is {test_first_name}." in q1_prompt_output
    assert f"They intend to study {test_degree} at {test_university}." in q1_prompt_output
    # Check if a key phrase from the actual Q1 prompt is present (dedented due to textwrap.dedent)
    assert "Your guidance should specifically focus on helping the user explore and develop content for Question 1" in q1_prompt_output

    # Test Question 2 prompt generation
    q2_prompt_output = get_systems_prompt("Question 2", test_first_name, test_degree, test_university)
    assert f"The user's name is {test_first_name}." in q2_prompt_output
    assert f"They intend to study {test_degree} at {test_university}." in q2_prompt_output
    assert "Your guidance should specifically prompt the user to explore and develop content that answers Question 2" in q2_prompt_output

    # Test Question 3 prompt generation
    q3_prompt_output = get_systems_prompt("Question 3", test_first_name, test_degree, test_university)
    assert f"The user's name is {test_first_name}." in q3_prompt_output
    assert f"They intend to study {test_degree} at {test_university}." in q3_prompt_output
    assert "Your guidance should specifically focus on helping the user explore and develop content for Question 3" in q3_prompt_output

    # Test default/unrecognized question prompt generation
    default_prompt_output = get_systems_prompt("Invalid Question", test_first_name, test_degree, test_university)
    assert f"The user's name is {test_first_name}." in default_prompt_output
    assert f"They intend to study {test_degree} at {test_university}." in default_prompt_output
    assert "Default system prompt: No specific question selected." in default_prompt_output

# --- Test 3: Testing get_api() ---
# This function involves input() and sys.exit(), so we need to use pytest's mocking features.
# We are mocking getpass.getpass as that is what get_api now uses.
def test_get_api_valid_input(monkeypatch, capsys):
    test_api_key = "test_valid_api_key"
    # MODIFIED: Mock getpass.getpass
    monkeypatch.setattr('getpass.getpass', lambda prompt: test_api_key)

    returned_key = get_api()
    assert returned_key == test_api_key
    captured = capsys.readouterr()
    assert "API key received. Attempting verification..." in captured.out


def test_get_api_empty_input_loop(monkeypatch, capsys):
    inputs = ["", "another_valid_key"]
    def mock_getpass_sequence(prompt): # Modified mock function name
        return inputs.pop(0)
    # MODIFIED: Mock getpass.getpass
    monkeypatch.setattr('getpass.getpass', mock_getpass_sequence)

    returned_key = get_api()
    assert returned_key == "another_valid_key"
    captured = capsys.readouterr()
    assert "Error: No API key was entered. Please try again." in captured.out


def test_get_api_exit_command(monkeypatch, capsys):
    # MODIFIED: Mock getpass.getpass
    monkeypatch.setattr('getpass.getpass', lambda prompt: "exit")

    with pytest.raises(SystemExit) as excinfo:
        get_api()

    assert excinfo.type == SystemExit
    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "Exiting this program." in captured.out

# --- Test 4: Testing get_user_details() ---
# This function involves input(), so we need to use monkeypatch.
def test_get_user_details_valid_input(monkeypatch, capsys):
    # Mock user inputs for first name, degree, and university
    inputs = ["John", "Bachelor of Science", "Harvard University"]

    # Create a mock_input function that returns one input from the list each time it's called
    def mock_input(prompt):
        # We need to print the prompt, as capsys will capture actual stdout
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return inputs.pop(0)

    monkeypatch.setattr('builtins.input', mock_input)

    # Call the function
    first_name, degree_name, university_name = get_user_details()

    # Assert that the function returned the correct values
    assert first_name == "John"
    assert degree_name == "Bachelor of Science"
    assert university_name == "Harvard University"

    # Assert on some of the printed output
    captured = capsys.readouterr()
    assert "Let's get some details for personalization" in captured.out
    assert "Great! We have your details: John, Bachelor of Science at Harvard University." in captured.out


def test_get_user_details_empty_input_loop(monkeypatch, capsys):
    # Mock inputs: empty name, then valid name; empty degree, then valid; empty uni, then valid.
    inputs = [
        "", "Jane",             # First name
        "", "Master of Arts",   # Degree name
        "", "MIT"               # University name
    ]

    def mock_input_sequence(prompt):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return inputs.pop(0)

    monkeypatch.setattr('builtins.input', mock_input_sequence)

    # Call the function
    first_name, degree_name, university_name = get_user_details()

    # Assert that the valid inputs were ultimately returned
    assert first_name == "Jane"
    assert degree_name == "Master of Arts"
    assert university_name == "MIT"

    # Assert that error messages for empty inputs were printed
    captured = capsys.readouterr()
    assert "First name cannot be empty." in captured.out
    assert "Degree/Course name cannot be empty." in captured.out
    assert "University/College name cannot be empty." in captured.out
