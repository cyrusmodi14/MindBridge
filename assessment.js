async function submitAssessment(answers) {

    if (!requireAuth()) return;

    try {

        const result =
            await apiFetch(
                "/assessment/score",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        answers: answers
                    })
                }
            );


        /*
         * Safety response
         */

        if (result.safety_override) {

            showSafetyMessage(result);

            return;
        }


        /*
         * Save assessment ID
         */

        localStorage.setItem(
            "latest_assessment_id",
            result.assessment_id
        );


        /*
         * Get AI report
         */

        const report =
            await apiFetch(
                `/assessment/report/${result.assessment_id}`,
                {
                    method: "POST"
                }
            );


        displayAssessmentResult(
            result,
            report
        );


    } catch (error) {

        console.error(
            "Assessment error:",
            error
        );

        alert(
            error.message ||
            "Unable to submit assessment."
        );

    }
}