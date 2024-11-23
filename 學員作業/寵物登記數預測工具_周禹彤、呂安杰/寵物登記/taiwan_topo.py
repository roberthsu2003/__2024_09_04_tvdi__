class TopoJSONParser:
    def __init__(self, topojson_data):
        self.data = topojson_data
        self.transform = self.data.get('transform', {})
        self.scale = self.transform.get('scale', [1, 1])
        self.translate = self.transform.get('translate', [0, 0])
        self.arcs = self.data.get('arcs', [])

    def _convert_point(self, point):
        """轉換座標點"""
        try:
            x = point[0] * self.scale[0] + self.translate[0]
            y = point[1] * self.scale[1] + self.translate[1]
            return [x, y]
        except (IndexError, TypeError):
            return [0, 0]  # 返回默認值

    def _convert_arc(self, arc_index, reverse=False):
        """轉換弧線座標"""
        try:
            points = []
            x, y = 0, 0
            arc = self.arcs[abs(arc_index)]
            if reverse:
                arc = arc[::-1]
            
            for point in arc:
                if len(point) >= 2:
                    x += point[0]
                    y += point[1]
                    points.append(self._convert_point([x, y]))
            return points
        except (IndexError, TypeError):
            return []

    def _process_arc_indices(self, indices):
        """處理弧線索引"""
        points = []
        try:
            for index in indices:
                reverse = index < 0
                if reverse:
                    index = -(index + 1)
                arc_points = self._convert_arc(index, reverse)
                
                if arc_points:
                    if points and points[-1] == arc_points[0]:
                        points.extend(arc_points[1:])
                    else:
                        points.extend(arc_points)
            return points
        except Exception as e:
            print(f"Error processing arc indices: {e}")
            return []

    def _get_polygon_coordinates(self, arcs):
        """獲取多邊形座標"""
        try:
            if not arcs:
                return []
            # 處理第一個環（外環）
            return self._process_arc_indices(arcs[0])
        except Exception as e:
            print(f"Error getting polygon coordinates: {e}")
            return []

    def _get_multipolygon_coordinates(self, arcs):
        """獲取多重多邊形座標"""
        try:
            coordinates = []
            for polygon_arcs in arcs:
                poly_coords = self._get_polygon_coordinates([polygon_arcs])
                if poly_coords:
                    coordinates.append(poly_coords)
            return coordinates[0] if coordinates else []  # 返回第一個有效的多邊形
        except Exception as e:
            print(f"Error getting multipolygon coordinates: {e}")
            return []

    def get_geometries(self):
        """獲取所有幾何資料"""
        geometries = {}
        try:
            for geometry in self.data['objects']['layer1']['geometries']:
                name = geometry['properties']['name']
                geom_type = geometry['type']
                arcs = geometry['arcs']

                if geom_type == 'Polygon':
                    coords = self._get_polygon_coordinates(arcs)
                    if coords:
                        geometries[name] = coords
                elif geom_type == 'MultiPolygon':
                    coords = self._get_multipolygon_coordinates(arcs)
                    if coords:
                        geometries[name] = coords

        except Exception as e:
            print(f"Error processing geometries: {e}")

        return geometries