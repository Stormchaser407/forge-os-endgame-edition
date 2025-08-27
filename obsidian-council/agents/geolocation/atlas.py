#!/usr/bin/env python3
"""
ATLAS - World Mapper
Geolocation Intelligence and Mapping Agent

Specializes in:
- GPS coordinate analysis
- Location intelligence from images
- Movement pattern tracking
- Geographic correlation
- Travel route analysis
"""

import asyncio
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import sqlite3

import requests
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import exifread
from PIL import Image
from PIL.ExifTags import TAGS
import reverse_geocoder as rg
import numpy as np
from sklearn.cluster import DBSCAN

from ..core.agent_base import ObsidianAgent, Priority
from ..core.ai_service_manager import QueryType, QueryContext, AGENT_PROMPTS

@dataclass
class LocationPoint:
    """Geographic location with metadata"""
    latitude: float
    longitude: float
    timestamp: datetime
    accuracy: float
    source: str
    description: str
    metadata: Dict[str, Any]

@dataclass
class MovementPattern:
    """Movement analysis results"""
    locations: List[LocationPoint]
    total_distance: float
    duration: timedelta
    average_speed: float
    stops: List[Dict[str, Any]]
    routes: List[Dict[str, Any]]
    behavioral_patterns: Dict[str, Any]

class ATLASAgent(ObsidianAgent):
    """
    ATLAS - World Mapper Agent
    
    Analyzes geolocation data, tracks movement patterns, and provides
    location intelligence for missing person and trafficking investigations.
    """
    
    def __init__(self):
        super().__init__(
            name="ATLAS - World Mapper",
            codename="ATLAS", 
            specialization="Location Intelligence and Geographic Analysis",
            tools=[
                "folium", "geopy", "reverse-geocoder", "exifread",
                "GPS-analysis", "movement-tracking", "route-optimization",
                "geographic-clustering", "location-correlation",
                "satellite-imagery", "street-view-api"
            ],
            ai_backends=["claude", "chatgpt", "gemini"]
        )
        
        # Geolocation services
        self.geolocator = Nominatim(user_agent="ATLAS-Geolocation/1.0")
        self.google_maps_key = None
        self.mapbox_token = None
        
        # Movement analysis parameters
        self.min_movement_threshold = 50  # meters
        self.stop_duration_threshold = 300  # seconds (5 minutes)
        self.cluster_radius = 0.001  # degrees (~100m)
        
        # Location database
        self.location_cache = {}
        self.known_locations = {}
        
        # Geographic regions of interest
        self.trafficking_corridors = []
        self.border_crossings = []
        self.high_risk_areas = []
        
    async def initialize_services(self, config: Dict[str, str]):
        """Initialize geolocation services"""
        self.logger.info("Initializing geolocation services...")
        
        if config.get("google_maps_api_key"):
            self.google_maps_key = config["google_maps_api_key"]
        
        if config.get("mapbox_token"):
            self.mapbox_token = config["mapbox_token"]
        
        # Load known trafficking corridors and high-risk areas
        await self._load_geographic_intelligence()
        
        self.logger.info("Geolocation services initialized")
    
    async def _load_geographic_intelligence(self):
        """Load known trafficking corridors and high-risk areas"""
        # This would load from intelligence databases
        # Placeholder with some known trafficking routes
        
        self.trafficking_corridors = [
            {
                "name": "US-Mexico Border Corridor",
                "region": "North America",
                "coordinates": [
                    {"lat": 32.5, "lng": -117.0},  # San Diego area
                    {"lat": 25.9, "lng": -97.5}   # Brownsville area  
                ],
                "risk_level": "HIGH",
                "notes": "Major human trafficking route"
            },
            {
                "name": "I-95 Corridor",
                "region": "US East Coast", 
                "coordinates": [
                    {"lat": 25.8, "lng": -80.2},  # Miami
                    {"lat": 40.7, "lng": -74.0}   # New York
                ],
                "risk_level": "MEDIUM",
                "notes": "Interstate trafficking route"
            }
        ]
        
        self.high_risk_areas = [
            {
                "name": "Truck Stops I-10 Corridor",
                "center": {"lat": 29.7, "lng": -95.4},  # Houston area
                "radius_km": 50,
                "risk_factors": ["truck stops", "motels", "isolated areas"],
                "risk_level": "HIGH"
            }
        ]
    
    async def get_capabilities(self) -> Dict[str, Any]:
        """Return ATLAS capabilities"""
        return {
            "supported_tasks": [
                "location_extraction",
                "movement_analysis",
                "route_tracking",
                "geographic_correlation",
                "image_geolocation",
                "travel_pattern_analysis",
                "location_clustering",
                "risk_assessment",
                "mapping_visualization"
            ],
            "data_sources": [
                "GPS_coordinates",
                "EXIF_metadata",
                "cell_tower_data",
                "IP_geolocation",
                "social_media_checkins",
                "photo_metadata",
                "transportation_records"
            ],
            "analysis_types": [
                "movement_patterns",
                "location_clustering",
                "route_optimization",
                "geographic_profiling",
                "travel_behavior",
                "location_correlation"
            ]
        }
    
    async def analyze(self, data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Core analysis method for geolocation intelligence"""
        analysis_type = data.get("type", "location_analysis")
        
        self.logger.info(f"Starting {analysis_type} analysis")
        
        if analysis_type == "location_extraction":
            return await self._analyze_location_extraction(data, context)
        elif analysis_type == "movement_analysis":
            return await self._analyze_movement_patterns(data, context)
        elif analysis_type == "route_tracking":
            return await self._analyze_route_tracking(data, context)
        elif analysis_type == "image_geolocation":
            return await self._analyze_image_geolocation(data, context)
        elif analysis_type == "geographic_correlation":
            return await self._analyze_geographic_correlation(data, context)
        else:
            return await self._general_location_analysis(data, context)
    
    async def _analyze_location_extraction(self, data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and analyze location data from various sources"""
        sources = data.get("sources", [])
        subject_info = data.get("subject_info", {})
        
        results = {
            "subject_info": subject_info,
            "extracted_locations": [],
            "location_clusters": {},
            "geographic_profile": {},
            "risk_assessment": {},
            "confidence_score": 0.0,
            "timestamp": datetime.now().isoformat()
        }
        
        all_locations = []
        
        # Process each source
        for source in sources:
            try:
                source_locations = await self._extract_locations_from_source(source)
                all_locations.extend(source_locations)
                results["extracted_locations"].extend([loc.__dict__ for loc in source_locations])
                
            except Exception as e:
                self.logger.error(f"Error processing source {source.get('type', 'unknown')}: {e}")
        
        if all_locations:
            # Cluster locations to find patterns
            results["location_clusters"] = await self._cluster_locations(all_locations)
            
            # Generate geographic profile
            results["geographic_profile"] = await self._generate_geographic_profile(all_locations)
            
            # Assess risk based on known trafficking areas
            results["risk_assessment"] = await self._assess_location_risks(all_locations)
            
            # AI analysis of geographic patterns
            ai_analysis = await self._ai_analyze_geographic_data(results, context)
            results.update(ai_analysis)
            
            # Generate map visualization
            map_path = await self._create_location_map(all_locations, context.get("case_id", "unknown"))
            results["map_visualization"] = map_path
        
        results["confidence_score"] = self._calculate_location_confidence(results)
        
        return results
    
    async def _extract_locations_from_source(self, source: Dict[str, Any]) -> List[LocationPoint]:
        """Extract location data from a specific source"""
        source_type = source.get("type")
        locations = []
        
        if source_type == "images":
            locations = await self._extract_from_images(source.get("data", []))
        elif source_type == "gps_data":
            locations = await self._extract_from_gps(source.get("data", []))
        elif source_type == "social_media":
            locations = await self._extract_from_social_media(source.get("data", []))
        elif source_type == "cell_tower":
            locations = await self._extract_from_cell_towers(source.get("data", []))
        elif source_type == "ip_addresses":
            locations = await self._extract_from_ip_addresses(source.get("data", []))
        
        return locations
    
    async def _extract_from_images(self, image_data: List[Dict[str, Any]]) -> List[LocationPoint]:
        """Extract GPS coordinates from image EXIF data"""
        locations = []
        
        for image_info in image_data:
            try:
                image_path = image_info.get("path")
                if not image_path:
                    continue
                
                # Extract EXIF data
                coords = await self._extract_gps_from_image(image_path)
                
                if coords:
                    location = LocationPoint(
                        latitude=coords["latitude"],
                        longitude=coords["longitude"],
                        timestamp=datetime.fromisoformat(image_info.get("timestamp", datetime.now().isoformat())),
                        accuracy=coords.get("accuracy", 10.0),  # Default 10m accuracy
                        source="image_exif",
                        description=f"Photo location: {image_info.get('filename', 'unknown')}",
                        metadata={
                            "image_path": image_path,
                            "camera_make": coords.get("camera_make"),
                            "camera_model": coords.get("camera_model"),
                            "altitude": coords.get("altitude")
                        }
                    )
                    locations.append(location)
                    
            except Exception as e:
                self.logger.warning(f"Error extracting location from image: {e}")
        
        return locations
    
    async def _extract_gps_from_image(self, image_path: str) -> Optional[Dict[str, Any]]:
        """Extract GPS coordinates from image EXIF data"""
        try:
            with open(image_path, 'rb') as img_file:
                tags = exifread.process_file(img_file)
            
            # Check for GPS data
            gps_lat_ref = tags.get('GPS GPSLatitudeRef')
            gps_lat = tags.get('GPS GPSLatitude')
            gps_lon_ref = tags.get('GPS GPSLongitudeRef')
            gps_lon = tags.get('GPS GPSLongitude')
            
            if not all([gps_lat_ref, gps_lat, gps_lon_ref, gps_lon]):
                return None
            
            # Convert GPS coordinates to decimal degrees
            lat = self._convert_to_degrees(gps_lat)
            lon = self._convert_to_degrees(gps_lon)
            
            # Apply reference direction
            if str(gps_lat_ref) == 'S':
                lat = -lat
            if str(gps_lon_ref) == 'W':
                lon = -lon
            
            coords = {
                "latitude": lat,
                "longitude": lon,
                "camera_make": str(tags.get('Image Make', '')),
                "camera_model": str(tags.get('Image Model', '')),
            }
            
            # Get altitude if available
            gps_alt = tags.get('GPS GPSAltitude')
            if gps_alt:
                coords["altitude"] = float(gps_alt.values[0])
            
            return coords
            
        except Exception as e:
            self.logger.error(f"GPS extraction error: {e}")
            return None
    
    def _convert_to_degrees(self, value):
        """Convert GPS coordinates to decimal degrees"""
        d, m, s = value.values
        return float(d) + float(m)/60 + float(s)/3600
    
    async def _extract_from_gps(self, gps_data: List[Dict[str, Any]]) -> List[LocationPoint]:
        """Extract locations from GPS tracking data"""
        locations = []
        
        for point in gps_data:
            try:
                location = LocationPoint(
                    latitude=point["latitude"],
                    longitude=point["longitude"],
                    timestamp=datetime.fromisoformat(point["timestamp"]),
                    accuracy=point.get("accuracy", 5.0),
                    source="gps_tracker",
                    description="GPS tracking point",
                    metadata={
                        "speed": point.get("speed"),
                        "heading": point.get("heading"),
                        "altitude": point.get("altitude"),
                        "satellites": point.get("satellites")
                    }
                )
                locations.append(location)
                
            except Exception as e:
                self.logger.warning(f"Error processing GPS point: {e}")
        
        return locations
    
    async def _extract_from_social_media(self, social_data: List[Dict[str, Any]]) -> List[LocationPoint]:
        """Extract locations from social media check-ins and posts"""
        locations = []
        
        for post in social_data:
            try:
                # Check for explicit location data
                if post.get("location"):
                    loc_data = post["location"]
                    
                    if "coordinates" in loc_data:
                        coords = loc_data["coordinates"]
                        location = LocationPoint(
                            latitude=coords["latitude"],
                            longitude=coords["longitude"],
                            timestamp=datetime.fromisoformat(post["timestamp"]),
                            accuracy=100.0,  # Social media location accuracy varies
                            source=f"social_media_{post.get('platform', 'unknown')}",
                            description=f"Check-in: {loc_data.get('name', 'Unknown location')}",
                            metadata={
                                "platform": post.get("platform"),
                                "post_id": post.get("id"),
                                "location_name": loc_data.get("name"),
                                "post_content": post.get("content", "")[:100]
                            }
                        )
                        locations.append(location)
                
                # Try to geocode location mentions in text
                location_mentions = await self._extract_location_mentions(post.get("content", ""))
                for mention in location_mentions:
                    coords = await self._geocode_location(mention)
                    if coords:
                        location = LocationPoint(
                            latitude=coords["lat"],
                            longitude=coords["lng"],
                            timestamp=datetime.fromisoformat(post["timestamp"]),
                            accuracy=1000.0,  # Lower accuracy for text mentions
                            source=f"social_media_mention_{post.get('platform')}",
                            description=f"Location mention: {mention}",
                            metadata={
                                "platform": post.get("platform"),
                                "post_id": post.get("id"),
                                "mention": mention,
                                "post_content": post.get("content", "")[:100]
                            }
                        )
                        locations.append(location)
                        
            except Exception as e:
                self.logger.warning(f"Error extracting location from social media: {e}")
        
        return locations
    
    async def _extract_location_mentions(self, text: str) -> List[str]:
        """Extract location mentions from text using NLP"""
        # This would use NLP libraries like spaCy for named entity recognition
        # Placeholder implementation with basic patterns
        
        import re
        
        # Simple patterns for locations
        location_patterns = [
            r'\b(?:at|in|near|from|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z]{2})\b',  # City, State
            r'\b(\d+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:St|Ave|Rd|Blvd))\b'  # Street addresses
        ]
        
        mentions = []
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            mentions.extend([match if isinstance(match, str) else ' '.join(match) for match in matches])
        
        return list(set(mentions))[:5]  # Limit and deduplicate
    
    async def _geocode_location(self, location_name: str) -> Optional[Dict[str, float]]:
        """Geocode a location name to coordinates"""
        try:
            # Check cache first
            if location_name in self.location_cache:
                return self.location_cache[location_name]
            
            # Use geolocator
            location = self.geolocator.geocode(location_name, timeout=10)
            
            if location:
                coords = {
                    "lat": location.latitude,
                    "lng": location.longitude
                }
                
                # Cache result
                self.location_cache[location_name] = coords
                return coords
            
        except Exception as e:
            self.logger.warning(f"Geocoding error for {location_name}: {e}")
        
        return None
    
    async def _cluster_locations(self, locations: List[LocationPoint]) -> Dict[str, Any]:
        """Cluster locations to identify patterns and frequent areas"""
        if not locations:
            return {}
        
        # Prepare coordinate array
        coords = np.array([[loc.latitude, loc.longitude] for loc in locations])
        
        # Use DBSCAN clustering
        clustering = DBSCAN(eps=self.cluster_radius, min_samples=2)
        labels = clustering.fit_predict(coords)
        
        clusters = {}
        for idx, label in enumerate(labels):
            if label == -1:  # Noise
                continue
            
            cluster_id = f"cluster_{label}"
            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    "locations": [],
                    "center": None,
                    "radius_km": 0,
                    "visit_frequency": 0,
                    "time_spent": timedelta(),
                    "description": ""
                }
            
            clusters[cluster_id]["locations"].append(locations[idx])
        
        # Calculate cluster statistics
        for cluster_id, cluster_data in clusters.items():
            cluster_locations = cluster_data["locations"]
            
            # Calculate center point
            center_lat = sum(loc.latitude for loc in cluster_locations) / len(cluster_locations)
            center_lng = sum(loc.longitude for loc in cluster_locations) / len(cluster_locations)
            cluster_data["center"] = {"lat": center_lat, "lng": center_lng}
            
            # Calculate radius (max distance from center)
            max_distance = 0
            for loc in cluster_locations:
                distance = geodesic((center_lat, center_lng), (loc.latitude, loc.longitude)).kilometers
                max_distance = max(max_distance, distance)
            cluster_data["radius_km"] = max_distance
            
            # Calculate visit frequency and time spent
            cluster_data["visit_frequency"] = len(cluster_locations)
            
            # Try to identify the area
            cluster_data["description"] = await self._identify_area(center_lat, center_lng)
        
        return clusters
    
    async def _identify_area(self, lat: float, lng: float) -> str:
        """Identify what type of area this is (residential, commercial, etc.)"""
        try:
            # Reverse geocode to get address info
            results = rg.search((lat, lng))
            
            if results:
                result = results[0]
                city = result.get('name', '')
                admin1 = result.get('admin1', '')
                country = result.get('cc', '')
                
                return f"{city}, {admin1}, {country}"
            
        except Exception as e:
            self.logger.warning(f"Area identification error: {e}")
        
        return "Unknown area"
    
    async def _generate_geographic_profile(self, locations: List[LocationPoint]) -> Dict[str, Any]:
        """Generate geographic profile from location data"""
        if not locations:
            return {}
        
        profile = {
            "total_locations": len(locations),
            "time_span": {},
            "geographic_spread": {},
            "activity_patterns": {},
            "movement_behavior": {}
        }
        
        # Time analysis
        timestamps = [loc.timestamp for loc in locations]
        if timestamps:
            profile["time_span"] = {
                "earliest": min(timestamps).isoformat(),
                "latest": max(timestamps).isoformat(),
                "duration_days": (max(timestamps) - min(timestamps)).days
            }
        
        # Geographic spread
        latitudes = [loc.latitude for loc in locations]
        longitudes = [loc.longitude for loc in locations]
        
        profile["geographic_spread"] = {
            "center_point": {
                "lat": sum(latitudes) / len(latitudes),
                "lng": sum(longitudes) / len(longitudes)
            },
            "bounding_box": {
                "north": max(latitudes),
                "south": min(latitudes),  
                "east": max(longitudes),
                "west": min(longitudes)
            },
            "max_distance_km": self._calculate_max_distance(locations)
        }
        
        # Activity patterns (by hour, day of week)
        profile["activity_patterns"] = self._analyze_temporal_patterns(locations)
        
        return profile
    
    def _calculate_max_distance(self, locations: List[LocationPoint]) -> float:
        """Calculate maximum distance between any two points"""
        max_dist = 0
        
        for i in range(len(locations)):
            for j in range(i + 1, len(locations)):
                dist = geodesic(
                    (locations[i].latitude, locations[i].longitude),
                    (locations[j].latitude, locations[j].longitude)
                ).kilometers
                max_dist = max(max_dist, dist)
        
        return max_dist
    
    def _analyze_temporal_patterns(self, locations: List[LocationPoint]) -> Dict[str, Any]:
        """Analyze temporal patterns in location data"""
        patterns = {
            "hourly_distribution": [0] * 24,
            "daily_distribution": [0] * 7,
            "most_active_hours": [],
            "most_active_days": []
        }
        
        for loc in locations:
            hour = loc.timestamp.hour
            day = loc.timestamp.weekday()
            
            patterns["hourly_distribution"][hour] += 1
            patterns["daily_distribution"][day] += 1
        
        # Find most active periods
        max_hour_count = max(patterns["hourly_distribution"])
        max_day_count = max(patterns["daily_distribution"])
        
        patterns["most_active_hours"] = [
            i for i, count in enumerate(patterns["hourly_distribution"])
            if count == max_hour_count
        ]
        
        patterns["most_active_days"] = [
            i for i, count in enumerate(patterns["daily_distribution"])
            if count == max_day_count
        ]
        
        return patterns
    
    async def _assess_location_risks(self, locations: List[LocationPoint]) -> Dict[str, Any]:
        """Assess risk levels based on known trafficking areas"""
        risk_assessment = {
            "overall_risk": "LOW",
            "high_risk_locations": [],
            "trafficking_corridor_matches": [],
            "risk_factors": [],
            "recommendations": []
        }
        
        high_risk_count = 0
        
        for loc in locations:
            # Check against trafficking corridors
            for corridor in self.trafficking_corridors:
                if self._point_near_corridor(loc, corridor):
                    risk_assessment["trafficking_corridor_matches"].append({
                        "location": {"lat": loc.latitude, "lng": loc.longitude},
                        "corridor": corridor["name"],
                        "risk_level": corridor["risk_level"],
                        "timestamp": loc.timestamp.isoformat()
                    })
                    
                    if corridor["risk_level"] == "HIGH":
                        high_risk_count += 1
            
            # Check against high-risk areas
            for area in self.high_risk_areas:
                if self._point_in_risk_area(loc, area):
                    risk_assessment["high_risk_locations"].append({
                        "location": {"lat": loc.latitude, "lng": loc.longitude},
                        "area": area["name"],
                        "risk_factors": area["risk_factors"],
                        "timestamp": loc.timestamp.isoformat()
                    })
                    high_risk_count += 1
        
        # Determine overall risk level
        if high_risk_count > len(locations) * 0.3:  # 30% of locations in high-risk areas
            risk_assessment["overall_risk"] = "HIGH"
        elif high_risk_count > 0:
            risk_assessment["overall_risk"] = "MEDIUM"
        
        return risk_assessment
    
    def _point_near_corridor(self, location: LocationPoint, corridor: Dict[str, Any]) -> bool:
        """Check if point is near a trafficking corridor"""
        # Simplified check - in production would use proper line-to-point distance
        coords = corridor.get("coordinates", [])
        if len(coords) < 2:
            return False
        
        for coord in coords:
            dist = geodesic(
                (location.latitude, location.longitude),
                (coord["lat"], coord["lng"])
            ).kilometers
            
            if dist < 50:  # Within 50km of corridor point
                return True
        
        return False
    
    def _point_in_risk_area(self, location: LocationPoint, area: Dict[str, Any]) -> bool:
        """Check if point is within a high-risk area"""
        center = area.get("center", {})
        radius_km = area.get("radius_km", 10)
        
        if not center:
            return False
        
        dist = geodesic(
            (location.latitude, location.longitude),
            (center["lat"], center["lng"])
        ).kilometers
        
        return dist <= radius_km
    
    async def _create_location_map(self, locations: List[LocationPoint], case_id: str) -> str:
        """Create interactive map visualization of locations"""
        if not locations:
            return ""
        
        try:
            # Calculate map center
            center_lat = sum(loc.latitude for loc in locations) / len(locations)
            center_lng = sum(loc.longitude for loc in locations) / len(locations)
            
            # Create folium map
            m = folium.Map(
                location=[center_lat, center_lng],
                zoom_start=10,
                tiles='OpenStreetMap'
            )
            
            # Add location markers
            for i, loc in enumerate(locations):
                # Color code by source
                color = {
                    'gps_tracker': 'red',
                    'image_exif': 'blue', 
                    'social_media': 'green',
                    'cell_tower': 'orange',
                    'ip_address': 'purple'
                }.get(loc.source.split('_')[0], 'gray')
                
                folium.Marker(
                    location=[loc.latitude, loc.longitude],
                    popup=f"""
                    <b>{loc.description}</b><br>
                    Source: {loc.source}<br>
                    Time: {loc.timestamp.strftime('%Y-%m-%d %H:%M:%S')}<br>
                    Accuracy: {loc.accuracy}m
                    """,
                    tooltip=f"Location {i+1}: {loc.timestamp.strftime('%m/%d %H:%M')}",
                    icon=folium.Icon(color=color, icon='info-sign')
                ).add_to(m)
            
            # Add trafficking corridors if any locations are near them
            for corridor in self.trafficking_corridors:
                coords = corridor.get("coordinates", [])
                if len(coords) >= 2:
                    # Check if any location is near this corridor
                    near_corridor = any(self._point_near_corridor(loc, corridor) for loc in locations)
                    
                    if near_corridor:
                        folium.PolyLine(
                            locations=[[c["lat"], c["lng"]] for c in coords],
                            color='red',
                            weight=3,
                            opacity=0.7,
                            popup=f"Trafficking Corridor: {corridor['name']}"
                        ).add_to(m)
            
            # Add high-risk area circles
            for area in self.high_risk_areas:
                center = area.get("center", {})
                if center and any(self._point_in_risk_area(loc, area) for loc in locations):
                    folium.Circle(
                        location=[center["lat"], center["lng"]],
                        radius=area.get("radius_km", 10) * 1000,  # Convert to meters
                        color='red',
                        fill=True,
                        opacity=0.3,
                        popup=f"High Risk Area: {area['name']}"
                    ).add_to(m)
            
            # Save map
            map_path = f"/tmp/atlas_map_{case_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            m.save(map_path)
            
            self.logger.info(f"Location map created: {map_path}")
            return map_path
            
        except Exception as e:
            self.logger.error(f"Map creation error: {e}")
            return ""
    
    async def _ai_analyze_geographic_data(self, results: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to analyze geographic patterns and provide insights"""
        from ..core.ai_service_manager import AIServiceManager
        
        analysis_prompt = f"""
        Analyze these geographic location patterns for a missing person/trafficking investigation:
        
        Total Locations: {len(results.get('extracted_locations', []))}
        Location Clusters: {len(results.get('location_clusters', {}))}
        Geographic Profile: {results.get('geographic_profile', {})}
        Risk Assessment: {results.get('risk_assessment', {})}
        
        Location Details:
        {json.dumps(results.get('extracted_locations', [])[:10], indent=2)}  # First 10 for brevity
        
        Please provide:
        1. Movement pattern analysis
        2. Behavioral insights from location data
        3. Risk assessment and concerning patterns
        4. Potential trafficking indicators
        5. Recommended investigation focus areas
        6. Geographic profiling insights
        """
        
        try:
            ai_manager = AIServiceManager()
            query_context = QueryContext(
                agent_name="ATLAS",
                case_id=context.get("case_id", "unknown"),
                priority=Priority.HIGH.value,
                query_type=QueryType.INVESTIGATION,
                specialization="geographic_analysis"
            )
            
            ai_response = await ai_manager.route_query(
                analysis_prompt,
                query_context,
                AGENT_PROMPTS["ATLAS"]
            )
            
            return {
                "ai_geographic_analysis": ai_response.content,
                "ai_confidence": ai_response.confidence,
                "analysis_provider": ai_response.provider.value,
                "analysis_timestamp": ai_response.timestamp.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"AI geographic analysis error: {e}")
            return {
                "ai_geographic_analysis": f"AI analysis failed: {e}",
                "ai_confidence": 0.0
            }
    
    def _calculate_location_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate confidence score for location analysis"""
        total_score = 0.0
        factors = 0
        
        # Number of locations
        location_count = len(results.get("extracted_locations", []))
        if location_count > 0:
            total_score += min(location_count / 20, 0.3)  # Max 0.3 for quantity
            factors += 1
        
        # Source diversity  
        sources = set(loc.get("source", "") for loc in results.get("extracted_locations", []))
        if sources:
            source_diversity = min(len(sources) / 4, 0.3)  # Max 0.3 for diversity
            total_score += source_diversity
            factors += 1
        
        # Risk indicators
        if results.get("risk_assessment", {}).get("high_risk_locations"):
            total_score += 0.4  # Significant boost for risk indicators
            factors += 1
        
        return total_score / max(factors, 1) if factors > 0 else 0.0

# Agent registration function  
def create_agent() -> ATLASAgent:
    """Create and return ATLAS agent instance"""
    return ATLASAgent()