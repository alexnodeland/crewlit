def format_title_key(role):
    title_case = role.title()
    underscores = title_case.lower().replace(' ', '_')
    return title_case, underscores