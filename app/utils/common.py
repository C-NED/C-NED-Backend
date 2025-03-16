def format_time(seconds):
    """초를 시간과 분으로 변환"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}시간 {minutes}분"
