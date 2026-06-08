def get_decision(score):

    if score >= 80:
        return "Selected"

    elif score >= 60:
        return "Shortlisted"

    else:
        return "Rejected"