import { useEffect, useState } from "react";
import api from "../api";
import Banner from "../components/Banner";
import UpcomingMovies from "../components/UpcomingMovies";

function Home() {

  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch(`${api.tmdb}/discover/movie?api_key=${api.tmdbKey}&primary_release_date.gte=2022-04-29&primary_release_date.lte=2022-07-29&sort_by=popularity.desc&with_release_type=3`)
      .then(res => res.json())
      .then(res => {
        setMovies(res['results']);
      });
  }, []);


  return (
    <div>
      <Banner backdrop='/uKbX1ha7KWyTecvpPpRCB3iFfj3.jpg' />
      <UpcomingMovies movies={movies} />
    </div>
  );
}

export default Home;