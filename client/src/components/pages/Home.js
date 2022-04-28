import { padding, width } from "@mui/system";
import { useEffect, useState } from "react";
import api from "../../api";
import UpcomingMovies from "../views/UpcomingMovies";


function Home() {

  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch(api.tmdb + '/movie/upcoming?region=US&api_key=' + api.tmdbKey)
      .then(res => res.json())
      .then(res => {
        setMovies(res['results']);
      });
  }, []);


  return (
    <div>
      <div style={{ height: 'calc(100vh - 345px)', overflow: "hidden" }}>
        <img src={api.tmdbImage + "/original/4ke48uabb0K6uDcLlSED2ZvvYEb.jpg"} style={{ width: "100%" }} />
      </div>
      <div style={{ backgroundColor: "var(--primaryColor)", padding: "25px", color: "white" }}>
        <a style={{ fontWeight: "bold", fontSize: "18px", display: "inline" }} href='/'>Box Office Forecast</a>
        <div style={{ display: "inline", float: "right" }}>Custom Movie</div>
      </div>
      <UpcomingMovies movies={movies} />
    </div>
  );
}

export default Home;