import { padding, width } from "@mui/system";
import { useEffect, useState } from "react";
import api from "../api";
import Banner from "../components/Banner";
import UpcomingMovies from "../components/UpcomingMovies";

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
      <Banner backdrop='/4ke48uabb0K6uDcLlSED2ZvvYEb.jpg' />
      <UpcomingMovies movies={movies} />
    </div>
  );
}

export default Home;