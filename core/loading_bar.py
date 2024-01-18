def loading_bar(max_value, current_value):
    bar_length = 30
    progress = current_value / max_value
    num_blocks = int(round(bar_length * progress))

    bar = "[" + "█" * num_blocks + "-" * (bar_length - num_blocks) + "]"
    percentage = round(progress * 100, 2)

    print(f"\r{bar} {percentage}% complete", end="", flush=True)
