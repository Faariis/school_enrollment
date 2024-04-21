
# Helper for calculating acknowledgment points;
def calculate_ack_points(ack_position, ack_level):
    if ack_position == 1:
        points = 3
    elif ack_position == 2:
        points = 2
    elif ack_position == 3:
        points = 1
    else:
        points = 0

    if ack_level == "Federalno":
        points += 2
    elif ack_level == "Kantonalno":
        points += 1

    return points


