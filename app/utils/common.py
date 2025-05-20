def format_time(seconds):
    """초를 시간과 분으로 변환"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f"{hours}시간 {minutes}분"

def to_geom_point(coord: list[float]) -> str:
    """좌표 [lat, lng] → GEOMETRY 형식으로 변환"""
    lat, lng = coord
    assert -90 <= lat <= 90 and -180 <= lng <= 180
    return f"POINT({lng} {lat})"
