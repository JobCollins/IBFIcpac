import React, { useRef, useEffect } from "react"
import mapboxgl from "mapbox-gl"
import IgadAirports from "./igad_airports_processed.json"
import KenPowerPlants from "./kenyageolocatedpowerplant.json"
import KenSchools from "./schools.json"
import "mapbox-gl/dist/mapbox-gl"

mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_TOKEN

const App = () => {
  const mapContainer = useRef()

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
        }
      })
      

    })

    

    //clean up function to remove map on unmount
    return () => map.remove()
  }, [])
  return <div ref={mapContainer} style={{width: "100%", height: "100vh"}}></div>
}

export default App