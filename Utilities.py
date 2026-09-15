def printlist(data):
    index = 1
    for i in range(len(data)):
        category = data[i]["category"]

        if category != "REMOVED":
            print(
                f"{index}: {data[i]['amount']} / {data[i]['category']} / {data[i]['description']}"
            )
            index += 1
