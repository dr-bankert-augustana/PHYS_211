##================================================================================================##
##                                                                                                ##
## Physics Problem Pipeline:                                                                      ##
##                                                                                                ##
##================================================================================================##

##================================================================================================##
## I) Import Libraries:                                                                           ##
##================================================================================================##

import json
import math
import re
import textwrap
import time

try:

    from google.colab import ai

    _HAS_COLAB_AI = True

except Exception:

    _HAS_COLAB_AI = False

    ai = None

##================================================================================================##
## II) Helper Functions:                                                                          ##
##================================================================================================##

##================================================================================================##
## IIa) JSON Helpers:                                                                             ##
##================================================================================================##

##================================================================================================##
## Function:    find_json_object                                                                  ##
##                                                                                                ##
## Description: Find the first balanced JSON object in a string.                                  ##
##================================================================================================##

def find_json_object(text):
    
    start = text.find("{")
    
    if start == -1: return None

    depth = 0

    in_string = False

    escape = False

    for i in range(start, len(text)):

        ch = text[i]

        if in_string:

            if escape:       escape = False
            
            elif ch == "\\": escape = True

            elif ch == '"':  in_string = False

        else:

            if ch == '"':   in_string = True

            elif ch == "{": depth += 1

            elif ch == "}":
                
                depth -= 1
                
                if depth == 0: return text[start : i + 1]

    return None

##================================================================================================##
## Function:    extract_json                                                                      ##
##                                                                                                ##
## Description: Parse JSON from a model response.                                                 ##
##================================================================================================##

def extract_json(payload):
    
    if isinstance(payload, dict): return payload

    text = str(payload).strip()

    if not text: raise ValueError("Model response was empty.")

    ##--------------------------------------------------------------------------------------------##
    ## Remove common Markdown fences if present.                                                  ##
    ##--------------------------------------------------------------------------------------------##

    if text.startswith("```"):

        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE).strip()

    ##--------------------------------------------------------------------------------------------##
    ## First, try parsing directly.                                                               ##
    ##--------------------------------------------------------------------------------------------##

    try: return json.loads(text)

    except json.JSONDecodeError:

        candidate = find_json_object(text)

        if candidate is None: raise ValueError("Could not locate a JSON object in model response.")

        return json.loads(candidate)

##================================================================================================##
## IIb) Value Validation and Formatting:                                                          ##
##================================================================================================##

##================================================================================================##
## Function:    to_number                                                                         ##
##                                                                                                ##
## Description: Convert a value to float, allowing some forgiveness if the model returns strings  ##
##              like "2.5" or "2.5 seconds".                                                      ##
##================================================================================================##

def to_number(value, name):

    ##--------------------------------------------------------------------------------------------##
    ## Check if the Value is a Boolean:                                                           ##
    ##--------------------------------------------------------------------------------------------##

    if isinstance(value, bool): raise ValueError(f"Variable '{name}' must be numeric, not boolean.")

    ##--------------------------------------------------------------------------------------------##
    ## Save the Value if it is Indeed a Number:                                                   ##
    ##--------------------------------------------------------------------------------------------##

    if isinstance(value, (int, float)): number = float(value)
    
    else:
        
        try:
            
            number = float(value)
        
        except (TypeError, ValueError):
            
            text = str(value).strip().replace(",", "")
            
            match = re.search(
                r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?",
                text,
            )
            if match is None:
                raise ValueError(f"Could not parse numeric value for '{name}': {value!r}")

            number = float(match.group())

    if not math.isfinite(number):

        raise ValueError(f"Variable '{name}' must be finite, got {value!r}")

    return number

##================================================================================================##
## Function:    normalize_values                                                                  ##
##                                                                                                ##
## Description: Ensure all expected variables exist and are numeric.                              ##
##================================================================================================##

def normalize_values(variables, raw_values):
    
    if not isinstance(raw_values, dict):
        
        raise ValueError("'Values' must be a JSON object.")

    missing = [
        variable["name"] for variable in variables if variable["name"] not in raw_values
    ]

    if missing:

        raise ValueError(f"Missing values for variables: {missing}")

    values = {}

    for variable in variables:

        values[variable["name"]] = to_number(raw_values[variable["name"]], variable["name"])

    return values

##================================================================================================##
## Function:    validate_variables                                                                ##
##                                                                                                ##
## Description: Basic validation of the variable definitions.                                     ##
##================================================================================================##

def validate_variables(variables):
    
    if not variables: raise ValueError("variables must contain at least one variable.")

    names = []

    for variable in variables:

        if not isinstance(variable, dict):

            raise ValueError("Each variable must be a dictionary.")

        name = str(variable.get("name", "")).strip()

        if not name: raise ValueError("Each variable must have a non-empty 'name'.")

        if "{" in name or "}" in name:

            raise ValueError("Variable names must not contain curly braces.")

        names.append(name)

    if len(names) != len(set(names)): raise ValueError("Variable names must be unique.")

##================================================================================================##
## Function:    ensure_time_order                                                                 ##
##                                                                                                ##
## Description: Make sure ti and tf form a positive time interval.                                ##
##================================================================================================##

def ensure_time_order(values):
   
    if "ti" not in values or "tf" not in values: return

    delta = values["tf"] - values["ti"]

    ##--------------------------------------------------------------------------------------------##
    ## If the Times are Effectively Equal, then Make tf Magnitude Larger:                         ##
    ##--------------------------------------------------------------------------------------------##

    if abs(delta) < 1e-2:

        values["tf"] = values["ti"] * 1.1

        delta = values["tf"] - values["ti"]

    ##--------------------------------------------------------------------------------------------##
    ## If the Final Time is Before Initial Time, Swap Them:                                       ##
    ##--------------------------------------------------------------------------------------------##

    if values["ti"] > values["tf"]:

        values["ti"], values["tf"] = values["tf"], values["ti"]

        delta = values["tf"] - values["ti"]

##================================================================================================##
## Function:    format_number                                                                     ##
##                                                                                                ##
## Description: Format numeric values cleanly for insertion into the problem text.                ##
##================================================================================================##

def format_number(value):
    
    if abs(value) < 1e16 and float(value).is_integer():
        
        return str(int(value))
    
    return f"{value:.10g}"

##================================================================================================##
## Function:    safe_insert_values                                                                ##
##                                                                                                ##
## Description: Insert values into the problem using simple replacement.                          ##
##================================================================================================##

def safe_insert_values(problem, values):
    
    if not isinstance(problem, str):

        raise ValueError("'Problem' must be a string.")

    for name, value in values.items():

        placeholder = f"{{{name}}}"

        if placeholder not in problem:

            raise ValueError(f"Problem is missing required placeholder {placeholder}.")

        problem = problem.replace(placeholder, format_number(value))

    ##--------------------------------------------------------------------------------------------##
    ## If There are Still Braces Left, Something Went Wrong:                                      ##
    ##--------------------------------------------------------------------------------------------##

    if "{" in problem or "}" in problem:

        raise ValueError("Problem still contains braces after replacement.")

    return problem.strip()

##================================================================================================##
## IIc) Prompt Construction and Problem Generation:                                               ##
##================================================================================================##

##================================================================================================##
## Function:    build_prompt                                                                      ##
##                                                                                                ##
## Description: Build a strict prompt that asks for pure JSON and exact placeholders.             ##
##================================================================================================##

def build_prompt(topic, variables, target):
    
    variable_lines = "\n".join(
        
        f"- {variable['name']}: {variable.get('description', '')}"
        for variable in variables
    )

    target_line = f"- {target['name']}: {target.get('description', '')}"

    placeholder_list = ", ".join(f"{{{variable['name']}}}" for variable in variables)

    example_values = ",\n".join(
        
        f'    "{variable["name"]}": {json.dumps(variable.get("example", 0))}'
        for variable in variables
    )

    example_problem = " ".join(f"{{{variable['name']}}}" for variable in variables)

    example = f"""{{
  "Problem": "Example sentence containing {example_problem}.",
  "Target": "{target_line}",
  "Values": {{
{example_values}
  }}
}}"""

    prompt = f"""You are a physics problem generator.

Return ONLY a valid JSON object. Do not use Markdown, code fences, comments, or extra text.

Required JSON structure:
{{
  "Problem": "one-line word problem string",
  "Values": {{
    "variable_name": 0
  }}
}}

Topic:
{topic}

Target:
{target_line}

Variables:
{variable_lines}

Rules:
- Generate one interesting and physically reasonable word problem for the topic.
- The problem must use every listed variable exactly as a placeholder in braces: {placeholder_list}.
- Do not put numbers, units, or other text inside the braces.
- Do append the appropriate units after the variable name.
- Do not reveal the variable values inside the problem text.
- If present, display the initial time and initial position before the final time and final position.
- Keep the "Problem" value on one line.
- Structure the "Problem" to solve for the "Target".
- Every "Values" entry must be a plain numeric JSON value.

Example shape:
{example}
"""
    return prompt

##================================================================================================##
## Function:    generate_problem                                                                  ##
##                                                                                                ##
## Description: Generate a physics word problem using an LLM.                                     ##
##                                                                                                ##
## Parameters:  topic        (str):  Physics topic.                                               ##
##              variables    (list): List of variable definitions.                                ##
##              max_attempts (int):  # of attempts to make if the model returns invalid output.   ##
##              generator    (func): Function that takes a prompt and returns model output.       ##
##                                   Defaults to google.colab.ai.generate_text when available.    ##
##                                                                                                ##
## Returns:     problem (str):  Final problem text with values inserted.                          ##
##              values  (dict): Dictionary of numeric variable values.                            ##
##================================================================================================##

def generate_problem(topic, variables, target, max_attempts = 3, generator = None):
    
    if max_attempts < 1:

        raise ValueError("max_attempts must be at least 1.")

    validate_variables(variables)

    if generator is None:

        if not _HAS_COLAB_AI:

            raise RuntimeError(
                "google.colab.ai is not available. Run this in Google Colab "
                "or pass a callable generator function."
            )

        def safe_colab_generator(prompt):
            return ai.generate_text(
                prompt, 
                model_name = 'google/gemini-2.5-flash'
            )

        generator = safe_colab_generator

    elif not callable(generator):

        raise TypeError("generator must be callable.")

    last_error = None

    for attempt in range(1, max_attempts + 1):

        prompt = build_prompt(topic, variables, target)

        try:
            raw_response = generator(prompt)
            data = extract_json(raw_response)

            problem_template = str(data["Problem"]).strip()
            values = normalize_values(variables, data["Values"])

            #ensure_time_order(values)
            problem = safe_insert_values(problem_template, values)

            return problem, values

        except Exception as exc:

            last_error = exc

            if attempt < max_attempts:

                print(f"Attempt {attempt} failed: {exc}. Retrying...")

                time.sleep(1)

    raise RuntimeError(
        
        f"Problem generation failed after {max_attempts} attempts. Last error: {last_error}"
    )

##================================================================================================##
## IId) Problem Solving:                                                                          ##
##================================================================================================##

##================================================================================================##
## Function:    solve_problem                                                                     ##
##                                                                                                ##
## Description: Solve a generated physics problem based on topic and values.                      ##
##================================================================================================##

def solve_problem(topic, values):
    
    key = topic.strip().lower()

    if key not in SOLVERS:

        raise ValueError(f"No solution method has been defined for topic: {topic}")

    result = SOLVERS[key](values)

    ##--------------------------------------------------------------------------------------------##
    ## Avoid Printing '-0':                                                                       ##
    ##--------------------------------------------------------------------------------------------##

    if abs(result[0]) < 1e-12: result[0] = 0.0

    ##--------------------------------------------------------------------------------------------##
    ## Return Solution:                                                                           ##
    ##--------------------------------------------------------------------------------------------##

    return result

##================================================================================================##
## IIe) Answer Checking:                                                                          ##
##================================================================================================##

##================================================================================================##
## Outcome Messages:                                                                              ##
##================================================================================================##

OUTCOME_RIGHT          = "Value is Correct!"
OUTCOME_CLOSE          = "Value is close, check for rounding errors!"
OUTCOME_NEG            = "Value is Incorrect, check minus signs!"
OUTCOME_NEG_CLOSE      = "Value is Incorrect, check for rounding errors and minus signs!"
OUTCOME_INV            = "Value is Incorrect, check inverse!"
OUTCOME_INV_CLOSE      = "Value is Incorrect, check for rounding errors and inverse!"
OUTCOME_NEG_INV        = "Value is Incorrect, check for inverse and minus signs!"
OUTCOME_NEG_INV_CLOSE  = "Value is Incorrect, check for rounding errors, inverse, and minus signs!"
OUTCOME_WRONG          = "Value is Incorrect!"
OUTCOME_WRONG_UNITS    = "Units are Incorrect!"
OUTCOME_CORRECT_UNITS  = "Units are Correct!"
OUTCOME_TRY_AGAIN      = "Try Again!"
OUTCOME_VALUE_NOT_NUM  = "Your answer value must be a number only!"
OUTCOME_MISSING_VARS   = "You must generate the problem before checking the answer."
OUTCOME_INCOMPLETE_ANS = "You must fully answer the problem before checking the answer."

##================================================================================================##
## Default Tolerances:                                                                            ##
##================================================================================================##

DEFAULT_RIGHT_TOLERANCE  = 0.1   # 10 %
DEFAULT_CLOSE_TOLERANCE  = 0.2   # 20 %
ZERO_THRESHOLD           = 1e-9  # treat |value| < this as zero

##================================================================================================##
## Unit Normalization:                                                                            ##
##================================================================================================##

_UNIT_ALIASES = {
    "m/s": "m/s",
    "mps": "m/s",
    "meterspersecond": "m/s",
    "meterpersecond": "m/s",
    "meters/second": "m/s",
    "meter/second": "m/s",
    "meter/s": "m/s",
    "meters/sec": "m/s",
    "meter/sec": "m/s",
}

##================================================================================================##
## Function:    normalize_unit                                                                    ##
##                                                                                                ##
## Description: Normalize a unit string for case-insensitive, whitespace-tolerant comparison.     ##
##================================================================================================##

def _normalize_unit(unit):
    
    s = str(unit).strip().lower()

    if not s:

        return ""

    # Convert "per" to "/"
    s = re.sub(r"\s*per\s*", "/", s)

    # Normalize slashes
    s = re.sub(r"\s*/\s*", "/", s)

    # Remove all remaining spaces
    s = s.replace(" ", "")

    return _UNIT_ALIASES.get(s, s)

##================================================================================================##
## Numeric Helpers:                                                                               ##
##================================================================================================##

def _percent_error(solution, candidate):
    """
    Return the absolute percent error between *solution* and *candidate*.

    If *solution* is (near) zero the percent error is undefined, so we fall
    back to the absolute value of *candidate*, which is 0 when the student
    also answered 0.
    """
    if abs(solution) < ZERO_THRESHOLD:
        return abs(candidate)
    return abs((solution - candidate) / solution)


def _coerce_number(value, label="value"):
    """
    Try to coerce *value* into a float.

    Accepts int, float, numeric strings ("42", "3.14", "3,14"),
    and objects that can be converted with float().

    Returns:
        (number, None) on success
        (None, error_message) on failure
    """
    if isinstance(value, bool):
        return None, f"{label} must be a number, not a boolean."

    if isinstance(value, (int, float)):
        number = float(value)
    elif isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        match = re.search(
            r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?",
            cleaned,
        )
        if match is None:
            return None, f"{label} must be a number."
        number = float(match.group())
    else:
        try:
            number = float(value)
        except (TypeError, ValueError):
            return None, f"{label} must be a number, got {type(value).__name__}."

    if not math.isfinite(number):
        return None, f"{label} must be finite."

    return number, None


def _is_close(a, b, tolerance):
    """
    Simple tolerance check that works reasonably well even when b is zero.
    """
    return abs(a - b) <= max(ZERO_THRESHOLD, tolerance * max(1.0, abs(b)))


##================================================================================================##
## Function: check_answer                                                                         ##
##================================================================================================##

def check_answer(
    solution_value,
    solution_units,
    given_value,
    given_units,
    right_tolerance  = DEFAULT_RIGHT_TOLERANCE,
    close_tolerance  = DEFAULT_CLOSE_TOLERANCE,
    custom_checks    = None,
):
    """
    Check a student's numeric answer and units against the known solution.

    Parameters
    ----------
    solution_value : float
        Correct numerical answer.
    solution_units : list[str]
        List of acceptable unit strings.
    given_value : int | float | str
        Student's numerical answer.
    given_units : str
        Student's unit string.
    right_tolerance : float
        Maximum absolute percent error for a "correct" verdict.
    close_tolerance : float
        Maximum absolute percent error for a "close" verdict.
    custom_checks : dict, optional
        Optional dictionary of common pitfall answers:
            {
                "wrong_value_1": "message_1",
                "wrong_value_2": "message_2"
            }

    Returns
    -------
    dict
        {
            "value_outcome" : str,
            "units_outcome" : str,
            "is_correct"    : bool,
            "errors"        : dict,
        }
    """
    # ------------------------------------------------------------------ #
    # Validate solution                                                    #
    # ------------------------------------------------------------------ #
    try:
        solution_value = float(solution_value)
    except (TypeError, ValueError):
        raise ValueError("solution_value must be numeric.")

    if not math.isfinite(solution_value):
        raise ValueError("solution_value must be finite.")

    if solution_units is None:
        solution_units = []

    acceptable_units = {
        _normalize_unit(unit)
        for unit in solution_units
        if unit is not None
    }

    # ------------------------------------------------------------------ #
    # Validate the student's numeric value                                 #
    # ------------------------------------------------------------------ #
    number, err = _coerce_number(given_value, "answer value")
    if err is not None:
        print(OUTCOME_VALUE_NOT_NUM)
        return {
            "value_outcome": OUTCOME_VALUE_NOT_NUM,
            "units_outcome": "",
            "is_correct": False,
            "errors": {},
        }

    # ------------------------------------------------------------------ #
    # Compute percent-error candidates                                     #
    # ------------------------------------------------------------------ #
    err_direct = _percent_error(solution_value, number)
    err_neg    = _percent_error(solution_value, -number)

    if abs(number) >= ZERO_THRESHOLD:
        err_inv     = _percent_error(solution_value, 1.0 / number)
        err_neg_inv = _percent_error(solution_value, -1.0 / number)
    else:
        err_inv     = float("inf")
        err_neg_inv = float("inf")

    # ------------------------------------------------------------------ #
    # Decide the value outcome                                             #
    # ------------------------------------------------------------------ #
    outcome = None

    if err_direct <= right_tolerance:
        outcome = OUTCOME_RIGHT

    elif err_direct <= close_tolerance:
        outcome = OUTCOME_CLOSE

    elif err_neg <= right_tolerance:
        outcome = OUTCOME_NEG

    elif err_neg <= close_tolerance:
        outcome = OUTCOME_NEG_CLOSE

    elif err_inv <= right_tolerance:
        outcome = OUTCOME_INV

    elif err_inv <= close_tolerance:
        outcome = OUTCOME_INV_CLOSE

    elif err_neg_inv <= right_tolerance:
        outcome = OUTCOME_NEG_INV

    elif err_neg_inv <= close_tolerance:
        outcome = OUTCOME_NEG_INV_CLOSE

    else:
        # Optional custom pitfall checks
        if custom_checks:
            for expected_value, message in custom_checks.items():
                expected_num, expected_err = _coerce_number(expected_value, "custom expected value")
                if expected_err is None and _is_close(number, expected_num, right_tolerance):
                    outcome = str(message)
                    break

        if outcome is None:
            outcome = OUTCOME_WRONG

    # ------------------------------------------------------------------ #
    # Check units                                                          #
    # ------------------------------------------------------------------ #
    units_ok = _normalize_unit(given_units) in acceptable_units
    units_msg = OUTCOME_CORRECT_UNITS if units_ok else OUTCOME_WRONG_UNITS

    # ------------------------------------------------------------------ #
    # Display                                                              #
    # ------------------------------------------------------------------ #
    print(outcome)
    print(units_msg)

    is_correct = (outcome == OUTCOME_RIGHT) and units_ok
    if not is_correct:
        print(OUTCOME_TRY_AGAIN)

    # ------------------------------------------------------------------ #
    # Return structured result                                             #
    # ------------------------------------------------------------------ #
    return {
        "value_outcome": outcome,
        "units_outcome": units_msg,
        "is_correct": is_correct,
        "errors": {
            "direct": err_direct,
            "negated": err_neg,
            "inverse": err_inv,
            "neg_inverse": err_neg_inv,
        },
    }


##================================================================================================##
## Input Receiver:                                                                                ##
##================================================================================================##

def get_student_answer():
    """
    Prompt the student for a numeric answer and a unit string.

    Returns:
        (value, units)
    """
    while True:
        value_raw = input("Enter your answer value (number only): ").strip()
        if value_raw:
            break
        print("Please enter a number.")

    while True:
        units = input("Enter the units (e.g. m/s): ").strip()
        if units:
            break
        print("Please enter units.")

    return value_raw, units


##================================================================================================##
## Full Pipeline: Generate → Display → Receive Answer → Check                                     ##
##================================================================================================##

def run_problem_session(
    topic,
    max_generation_attempts = 3,
    max_answer_tries        = 5,
    right_tolerance         = DEFAULT_RIGHT_TOLERANCE,
    close_tolerance         = DEFAULT_CLOSE_TOLERANCE,
    generator               = None,
    provided_answer         = None,
    custom_checks           = None,
    reveal_solution_on_fail = True,
):
    """
    Run the full interactive physics problem pipeline.

    Parameters
    ----------
    topic : str
        Physics topic.
    variables : list[dict]
        Variable definitions for the problem generator.
    max_generation_attempts : int
        Number of LLM generation attempts.
    max_answer_tries : int
        Number of student answer attempts before revealing the solution.
    right_tolerance : float
        Correctness tolerance.
    close_tolerance : float
        "Close" tolerance.
    generator : callable, optional
        Optional LLM generator function.
        If None, uses google.colab.ai.generate_text when available.
    provided_answer : tuple, optional
        Optional pre-provided answer for testing:
            (answer_value, answer_units)
        If provided, the pipeline will not prompt for input.
    custom_checks : dict, optional
        Optional pitfall answers to check.
    reveal_solution_on_fail : bool
        Whether to reveal the solution if the student uses all attempts.

    Returns
    -------
    dict or None
        The final check_answer result if the student answered correctly,
        otherwise None.
    """
    if max_generation_attempts < 1:
        raise ValueError("max_generation_attempts must be at least 1.")

    if max_answer_tries < 1:
        raise ValueError("max_answer_tries must be at least 1.")

    if provided_answer is not None:
        if not isinstance(provided_answer, (tuple, list)) or len(provided_answer) != 2:
            raise ValueError("provided_answer must be a tuple or list: (value, units).")

    print("##" + "=" * 96 + "##")
    print("## Generating Practice Problem. Please Wait, This May Take A Moment." + " " * 30 + "##")
    print("##" + "=" * 96 + "##")
    print()

    # ------------------------------------------------------------------ #
    # Generate and solve                                                   #
    # ------------------------------------------------------------------ #
    problem, values = generate_problem(
        topic,
        VAR_DICT[topic],
        TAR_DICT[topic],
        max_attempts=max_generation_attempts,
        generator=generator,
    )

    solution_value, solution_units = solve_problem(topic, values)

    wrapped_problem = textwrap.fill(problem, width=100)
    print(wrapped_problem)
    print()

    # ------------------------------------------------------------------ #
    # Answer loop                                                          #
    # ------------------------------------------------------------------ #
    attempts = 1 if provided_answer is not None else max_answer_tries

    for attempt in range(1, attempts + 1):

        print()
        print("-" * 100)
        print()
        print(f"Attempt {attempt} of {attempts}:")

        if provided_answer is not None:
            given_value, given_units = provided_answer
        else:
            given_value, given_units = get_student_answer()

        result = check_answer(
            solution_value=solution_value,
            solution_units=solution_units,
            given_value=given_value,
            given_units=given_units,
            right_tolerance=right_tolerance,
            close_tolerance=close_tolerance,
            custom_checks=custom_checks,
        )

        if result["is_correct"]:
            print()
            print(f"Correct answer: {solution_value:.6g} {solution_units[0]}")
            return result

        print()

    # ------------------------------------------------------------------ #
    # Student used all attempts                                            #
    # ------------------------------------------------------------------ #
    if reveal_solution_on_fail:
        print()
        print("No correct answer was entered.")
        print(f"Correct answer: {solution_value:.6g} {solution_units[0]}")

    return None
