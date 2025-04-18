from sqlalchemy.types import UserDefinedType
from sqlalchemy.sql import func

class Point(UserDefinedType):
    def get_col_spec(self):
        return "POINT"

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None

            # 1. 이미 Point 객체인 경우 (Shapely)
            if hasattr(value, "x") and hasattr(value, "y"):
                return f"POINT({value.x} {value.y})"
            
            # 2. (x, y) 튜플이나 리스트인 경우
            if isinstance(value, (list, tuple)) and len(value) == 2:
                return f"POINT({value[0]} {value[1]})"
            
            # 3. WKT 문자열
            if isinstance(value, str) and value.startswith("POINT"):
                return value

            raise ValueError(f"Invalid value for Point: {value}")
        return process

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, 4326)

    def column_expression(self, col):
        return func.AsText(col)
