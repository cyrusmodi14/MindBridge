def check_safety(answers: dict[int, int]):
    """
    Check whether assessment responses contain
    an indication of an immediate safety concern.

    This is a safety screening mechanism, not a diagnosis.
    """

    safety_flags = []

    # These question IDs will correspond to the
    # dedicated safety questions in questions.py.

    SAFETY_QUESTIONS = {
        23: "self_harm",
        24: "harm_to_others",
        25: "immediate_safety"
    }

    for question_id, flag_type in SAFETY_QUESTIONS.items():

        if question_id not in answers:
            continue

        answer = answers[question_id]

        # For these safety questions:
        # 0 = No / Not at all
        # 1-4 = some level of concern
        if answer >= 1:
            safety_flags.append(flag_type)

    if safety_flags:

        return {
            "safety_concern": True,
            "flags": safety_flags,
            "message": (
                "Your responses indicate that you may need "
                "immediate support. Solace cannot assess "
                "or manage an emergency. Please contact a "
                "qualified mental-health professional or your "
                "local emergency/crisis service, and consider "
                "staying with someone you trust rather than "
                "being alone."
            )
        }

    return {
        "safety_concern": False,
        "flags": [],
        "message": None
    }