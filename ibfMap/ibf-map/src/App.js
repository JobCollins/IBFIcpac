import React, { useRef, useEffect } from "react"
import ReactDOM from "react-dom"
import mapboxgl from "mapbox-gl"
import IgadAirports from "./igad_airports_processed.json"
import KenPowerPlants from "./kenyageolocatedpowerplant.json"
import KenSchools from "./schools.json"
import "mapbox-gl/dist/mapbox-gl"

mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_TOKEN

const Popup = ({itemName}) => (
  <div className="popup">
    <h3 className="item-name">{itemName}</h3>
  </div>
)

const App = () => {
  const mapContainer = useRef()
  const popUpRef = useRef(new mapboxgl.Popup({ offset: 15 }));

  // this is where all of our map logic is going to live
  // adding the empty dependency array ensures that the map
  // is only rendered once
  useEffect(() => {
    //create the map and configure it
    //checkout the API reference for options
    //https://docs.mapbox.com/mapbox-gl-js/api/map
    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/dark-v10",
      center:[38, -1],
      zoom: 7,
    })

    map.on("load", ()=>{
      map.addSource("igad-airports", {
        type: "geojson",
        data: IgadAirports
      })
      map.addLayer({
        id: "igad-airports-symbol",
        type: "symbol",
        source: "igad-airports",
        layout:{
          "icon-image": 'airport-15',
          "text-size": 14,
          "text-offset": [0, -1.5],
          'visibility': 'visible'
        }
      })
      map.addSource("ken-pplants", {
        type: "geojson",
        data: KenPowerPlants
      })
      map.addLayer({
        id: "ken-pplants-symbol",
        type: "symbol",
        source: "ken-pplants",
        layout:{
          "icon-image": 'charging-station-15',
          "text-size": 14,
          "text-offset": [0, -1.5],
          'visibility': 'visible'
        }
      })
      map.addSource("ken-schools", {
        type: "geojson",
        data: KenSchools
      })
      map.addLayer({
        id: "ken-schools-symbol",
        type: "symbol",
        source: "ken-schools",
        layout:{
          "icon-image": 'school-11',
          "text-size": 14,
          "text-offset": [0, -1.5],
          'visibility': 'visible'
        }
      })

      // layer visibility toggle handler that could be attached
      // elsewhere in your application
      // something like toggleLayerVisibility('bus-stops-circle')
      function toggleLayerVisibility(layerId) {
        const visibility = map.getLayoutProperty(layerId, "visibility")

        if (visibility === "visible") {
          map.setLayoutProperty(layerId, "visibility", "none")
        } else {
          map.setLayoutProperty(layerId, "visibility", "visible")
        }
      }
      

    })

    map.on('idle', () => {
      // If these two layers were not added to the map, abort
      if (!map.getLayer('ken-schools-symbol') || !map.getLayer('ken-pplants-symbol') || !map.getLayer('igad-airports-symbol')) {
      return;
      }
       
      // Enumerate ids of the layers.
      const toggleableLayerIds = ['ken-schools-symbol', 'ken-pplants-symbol', 'igad-airports-symbol'];
       
      // Set up the corresponding toggle button for each layer.
      for (const id of toggleableLayerIds) {
      // Skip layers that already have a button set up.
      if (document.getElementById(id)) {
      continue;
      }
       
      // Create a link.
      const link = document.createElement('a');
      link.id = id;
      link.href = '#';
      link.textContent = id;
      link.className = 'active';
      link.style.padding = "20px"
       
      // Show or hide layer when the toggle is clicked.
      link.onclick = function (e) {
      const clickedLayer = this.textContent;
      e.preventDefault();
      e.stopPropagation();
       
      const visibility = map.getLayoutProperty(
      clickedLayer,
      'visibility'
      );
       
      // Toggle layer visibility by changing the layout object's visibility property.
      if (visibility === 'visible') {
      map.setLayoutProperty(clickedLayer, 'visibility', 'none');
      this.className = '';
      } else {
      this.className = 'active';
      map.setLayoutProperty(
      clickedLayer,
      'visibility',
      'visible'
      );
      }
      };
       
      const layers = document.getElementById('menu');
      layers.appendChild(link);
      }
    });

    map.on("click", (e) => {
      const features = map.queryRenderedFeatures(e.point, {
        layers: ["ken-schools-symbol", 'igad-airports-symbol', 'ken-pplants-symbol'],
      })
      if (features.length > 0) {
        const feature = features[0]
        const popupNode = document.createElement("div")
        ReactDOM.render(
          <Popup
            itemName={feature?.properties?.name}
          />,
          popupNode
        )
        popUpRef.current
          .setLngLat(e.lngLat)
          .setDOMContent(popupNode)
          .addTo(map)
      }
    })


    

    //clean up function to remove map on unmount
    return () => map.remove()
  }, [])
  return <div>
    <nav style={{borderSpacing: "20px"}} id="menu"></nav>
    <div ref={mapContainer} style={{width: "100%", height: "100vh"}}>
  </div>
    </div>
}

export default App