from typing import List, Tuple
import numpy as np

def transform_coordinates(coords: List[float], 
                        canvas_width: int, 
                        canvas_height: int) -> List[float]:
    min_lon, max_lon = 119.3, 122.0
    min_lat, max_lat = 21.8, 25.3
    
    x = (coords[0] - min_lon) / (max_lon - min_lon) * canvas_width
    y = canvas_height - (coords[1] - min_lat) / (max_lat - min_lat) * canvas_height
    
    return [x, y]

def get_centroid(coordinates: List[List[float]]) -> Tuple[float, float]:
    coords = np.array(coordinates)
    centroid = coords.mean(axis=0)
    return tuple(centroid)