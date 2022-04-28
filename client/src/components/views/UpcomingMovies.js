import { useEffect, useState } from "react";
import api from "../../api";
import MovieCard from "./MovieCard";

function UpcomingMovies() {

  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch(api.tmdb + '/trending/movie/week?api_key=' + api.tmdbKey)
      .then(res => res.json())
      .then(res => {
        setMovies(res['results']);
        console.log(movies);
      });
  }, []);

  return (
    <div style={{ padding: "30px", display: "flex" }}>
      {movies.map(
        movie => <div style={{ padding: "20px" }}>
          <MovieCard movie={movie} />
        </div>
      )}
    </div>
  );
}

export default UpcomingMovies;