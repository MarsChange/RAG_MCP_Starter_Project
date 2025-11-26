def logTitle(title: str):
    totalLength = 20
    messageLength = len(title)
    padding = max(0, totalLength - messageLength - 4)
    print("=" * totalLength + "=" * padding + " " + title + " " + "=" * padding + "=" * totalLength)
