def custom_pretty_print(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                print(f"{key}: ", end="")
                print(value)
            else:
                print(f"{key}:\n", end="")
                custom_pretty_print(value)
    elif isinstance(data, list):
        print(data)
    else:
        print(data)
