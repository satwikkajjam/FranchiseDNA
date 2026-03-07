import React, { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMapEvents, useMap } from 'react-leaflet';
import L from 'leaflet';

// Fix Leaflet default icon issue with bundlers
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const competitorIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const populationIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
  iconSize: [20, 33],
  iconAnchor: [10, 33],
  popupAnchor: [1, -28],
  shadowSize: [33, 33],
});

function MapClickHandler({ onMapClick }) {
  useMapEvents({
    click(e) {
      onMapClick(e.latlng);
    },
  });
  return null;
}

function FlyToLocation({ location }) {
  const map = useMap();
  useEffect(() => {
    if (location) {
      map.flyTo([location.lat, location.lng], 10, { duration: 1 });
    }
  }, [location, map]);
  return null;
}

function MapView({ selectedLocation, radius, populationAreas, competitors, onMapClick }) {
  const center = selectedLocation
    ? [selectedLocation.lat, selectedLocation.lng]
    : [20.5937, 78.9629]; // India center

  return (
    <MapContainer
      center={center}
      zoom={5}
      style={{ height: '100%', width: '100%' }}
      zoomControl={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MapClickHandler onMapClick={onMapClick} />
      {selectedLocation && <FlyToLocation location={selectedLocation} />}

      {/* Selected Location Marker */}
      {selectedLocation && (
        <>
          <Marker position={[selectedLocation.lat, selectedLocation.lng]}>
            <Popup>
              <strong>Selected Location</strong><br />
              Lat: {selectedLocation.lat.toFixed(4)}<br />
              Lng: {selectedLocation.lng.toFixed(4)}
            </Popup>
          </Marker>
          <Circle
            center={[selectedLocation.lat, selectedLocation.lng]}
            radius={radius * 1000}
            pathOptions={{
              color: '#1a73e8',
              fillColor: '#1a73e8',
              fillOpacity: 0.1,
              weight: 2,
            }}
          />
        </>
      )}

      {/* Population Area Markers */}
      {populationAreas.map((area) =>
        area.latitude && area.longitude ? (
          <Marker
            key={area.id}
            position={[area.latitude, area.longitude]}
            icon={populationIcon}
          >
            <Popup>
              <strong>{area.area}</strong><br />
              Population: {area.population?.toLocaleString()}<br />
              Households: {area.households?.toLocaleString()}<br />
              Literacy: {area.literacy_rate}%
            </Popup>
          </Marker>
        ) : null
      )}

      {/* Competitor Markers */}
      {competitors.map((comp, idx) =>
        comp.latitude && comp.longitude ? (
          <Marker
            key={`comp-${idx}`}
            position={[comp.latitude, comp.longitude]}
            icon={competitorIcon}
          >
            <Popup>
              <strong>{comp.name}</strong><br />
              Type: {comp.type}<br />
              {comp.brand && <>Brand: {comp.brand}<br /></>}
            </Popup>
          </Marker>
        ) : null
      )}
    </MapContainer>
  );
}

export default MapView;
