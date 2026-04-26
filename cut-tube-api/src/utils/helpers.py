from datetime import datetime


def time_to_seconds(str_time: str) -> int:
    time = datetime.strptime(str_time, "%H:%M:%S")

    hours = time.hour
    minutes = time.minute
    seconds = time.second

    return (hours * 3600) + (minutes * 60) + seconds


def get_portion_seconds(video_duration: int, portion_time: str) -> int:
    video_duration_seconds = video_duration
    portion_time_seconds = time_to_seconds(portion_time)
    portion_percentage = portion_time_seconds / video_duration_seconds
    return int(video_duration_seconds * portion_percentage)
