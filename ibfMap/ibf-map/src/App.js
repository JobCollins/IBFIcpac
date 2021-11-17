import React, { useRef, useEffect } from "react"
import mapboxgl from "mapbox-gl"

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
      zoom: 12,
    })
    //clean up function to remove map on unmount
    return () => map.remove()
  }, [])
  return <div ref={mapContainer} style={{width: "100%", height: "100vh"}}></div>
}

export default App