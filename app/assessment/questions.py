QUESTIONS = [

    {
        "id": 1,
        "domain": "mood",
        "text": (
            "During the past two weeks, how often have "
            "you felt down, sad, or emotionally low?"
        ),
        "response_type": "scale"
    },

    {
        "id": 2,
        "domain": "mood",
        "text": (
            "During the past two weeks, how often have "
            "you lost interest in activities you normally enjoy?"
        ),
        "response_type": "scale"
    },

    {
        "id": 3,
        "domain": "mood",
        "text": (
            "How often have you felt emotionally overwhelmed "
            "by your usual responsibilities?"
        ),
        "response_type": "scale"
    },

    {
        "id": 4,
        "domain": "mood",
        "text": (
            "How often have you felt that things will not "
            "get better?"
        ),
        "response_type": "scale"
    },

    {
        "id": 5,
        "domain": "anxiety",
        "text": (
            "How often have you experienced excessive "
            "worry about things in your life?"
        ),
        "response_type": "scale"
    },

    {
        "id": 6,
        "domain": "anxiety",
        "text": (
            "How often have you found it difficult to "
            "control your worrying?"
        ),
        "response_type": "scale"
    },

    {
        "id": 7,
        "domain": "anxiety",
        "text": (
            "How often have you felt restless, tense, "
            "or unable to relax?"
        ),
        "response_type": "scale"
    },

    {
        "id": 8,
        "domain": "anxiety",
        "text": (
            "How often have worries made it difficult "
            "for you to concentrate?"
        ),
        "response_type": "scale"
    },

    {
        "id": 9,
        "domain": "stress",
        "text": (
            "How often have you felt that the demands "
            "in your life were difficult to manage?"
        ),
        "response_type": "scale"
    },

    {
        "id": 10,
        "domain": "stress",
        "text": (
            "How often have you felt under significant "
            "pressure from school, work, family, or other responsibilities?"
        ),
        "response_type": "scale"
    },

    {
        "id": 11,
        "domain": "stress",
        "text": (
            "How often have you felt unable to cope "
            "with the problems you are facing?"
        ),
        "response_type": "scale"
    },

    {
        "id": 12,
        "domain": "sleep",
        "text": (
            "How often have you had difficulty falling "
            "or staying asleep?"
        ),
        "response_type": "scale"
    },

    {
        "id": 13,
        "domain": "sleep",
        "text": (
            "How often have you woken up feeling "
            "unrested?"
        ),
        "response_type": "scale"
    },

    {
        "id": 14,
        "domain": "sleep",
        "text": (
            "How often have low energy or tiredness "
            "made your day more difficult?"
        ),
        "response_type": "scale"
    },

    {
        "id": 15,
        "domain": "functioning",
        "text": (
            "How often have your emotional difficulties "
            "interfered with your school, work, or studies?"
        ),
        "response_type": "scale"
    },

    {
        "id": 16,
        "domain": "functioning",
        "text": (
            "How often have you struggled to concentrate "
            "on tasks that normally require your attention?"
        ),
        "response_type": "scale"
    },

    {
        "id": 17,
        "domain": "functioning",
        "text": (
            "How often have you found it difficult to "
            "complete your normal daily responsibilities?"
        ),
        "response_type": "scale"
    },

    {
        "id": 18,
        "domain": "social",
        "text": (
            "How often have you avoided spending time "
            "with friends, family, or other people?"
        ),
        "response_type": "scale"
    },

    {
        "id": 19,
        "domain": "social",
        "text": (
            "How often have you felt disconnected from "
            "people around you?"
        ),
        "response_type": "scale"
    },

    {
        "id": 20,
        "domain": "social",
        "text": (
            "How often have your difficulties affected "
            "your relationships with others?"
        ),
        "response_type": "scale"
    },

    {
        "id": 21,
        "domain": "coping",
        "text": (
            "How often have you felt that your usual "
            "ways of dealing with problems are no longer helping?"
        ),
        "response_type": "scale"
    },

    {
        "id": 22,
        "domain": "coping",
        "text": (
            "How often have you found it difficult to "
            "ask others for help when you need it?"
        ),
        "response_type": "scale"
    },

    {
    "id": 23,
    "domain": "safety",
    "question": (
        "Have you recently had thoughts of hurting yourself "
        "or ending your life?"
    ),
    "answer_scale": {
        0: "No",
        1: "Rarely",
        2: "Sometimes",
        3: "Often",
        4: "Very often"
    }
},
{
    "id": 24,
    "domain": "safety",
    "question": (
        "Have you recently had thoughts about seriously "
        "hurting another person?"
    ),
    "answer_scale": {
        0: "No",
        1: "Rarely",
        2: "Sometimes",
        3: "Often",
        4: "Very often"
    }
},
{
    "id": 25,
    "domain": "safety",
    "question": (
        "Do you currently feel that you may be unable to "
        "keep yourself safe?"
    ),
    "answer_scale": {
        0: "No",
        1: "Unsure",
        2: "Possibly",
        3: "Probably",
        4: "Yes"
    }
}
]


RESPONSE_OPTIONS = [
    {
        "value": 0,
        "label": "Not at all"
    },
    {
        "value": 1,
        "label": "Rarely"
    },
    {
        "value": 2,
        "label": "Sometimes"
    },
    {
        "value": 3,
        "label": "Often"
    },
    {
        "value": 4,
        "label": "Nearly every day"
    }
]

if __name__ == "__main__":

    print(
        f"Total questions: {len(QUESTIONS)}"
    )

    for question in QUESTIONS:

        print(
            f"{question['id']}. "
            f"[{question['domain']}] "
            f"{question['text']}"
        )