import fitdecode

with fitdecode.FitReader("ScubaDiving_2024-03-08T09_29_45.fit") as fit_file:
    for frame in fit_file:
        if isinstance(frame, fitdecode.records.FitDataMessage):
            if frame.name == "record":
                print(
                    # frame.name,
                    # [x.name for x in frame.fields],
                    frame.get_value("timestamp"),
                    frame.get_value("depth"),
                )
