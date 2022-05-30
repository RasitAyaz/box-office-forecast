import { useEffect, useState } from "react";
import api from "../api";
import Banner from "../components/Banner";
import UpcomingMovies from "../components/UpcomingMovies";

function Home() {

  const [movies, setMovies] = useState([]);

  function dateToStr(date) {
    return date.toISOString().split('T')[0];
  }

  function addDays(date, days) {
    var result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
  }

  useEffect(() => {
    const begin = addDays(new Date(), 1);
    const end = addDays(begin, 60);
    fetch(`${api.tmdb}/discover/movie?api_key=${api.tmdbKey}&primary_release_date.gte=${dateToStr(begin)}&primary_release_date.lte=${dateToStr(end)}&sort_by=popularity.desc&with_release_type=3`)
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