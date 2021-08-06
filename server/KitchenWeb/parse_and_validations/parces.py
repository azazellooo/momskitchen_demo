

def deep_link_parce(message_text):
    return message_text.split(' ')[-1]

def review_text_parse(message_text):
    return ' '.join(message_text.split()[1:])