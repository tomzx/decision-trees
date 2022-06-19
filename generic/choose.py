def choose(question, options=[], default=None):
    textOptions = list(map(str, options))
    text = question
    if options:
        text = text + " (" + ", ".join(textOptions) + ")"

    if default:
        text = text + " (default: " + str(default) + ")"

    while True:
        result = input(text)
        if result == "" and default:
            break
        if result in textOptions:
            break

    return result if result else default
