import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import CastList from "../components/CastList";
import "./MoviePage.scss";

function MoviePage() {
  const { id } = useParams();

  const [movie, setMovie] = useState(null);

  useEffect(() => {
    fetch(`${api.tmdb}/movie/${id}?api_key=${api.tmdbKey}&append_to_response=credits`)
      .then(res => res.json())
      .then(res => {
        setMovie(res);
      });
  }, [id]);

  if (movie == null) {
    return (<div>
      Loading...
    </div>);
  } else {
    return (<>
      {
        movie && (
          <>
            <div className="banner" style={{ backgroundImage: `url(${api.tmdbImage}/original${movie['backdrop_path']})` }}></div>
            <div className="mb-3 movie-content container">
              <div className="movie-content__poster">
                <div className="movie-content__poster__img" style={{ backgroundImage: `url(${api.tmdbImage}/original${movie['poster_path']})` }}></div>
              </div>
              <div className="movie-content__info">
                <h1 className="title">
                  {movie.title || movie.name}
                </h1>
                <div className="genres">
                  {
                    movie.genres && movie.genres.slice(0, 5).map((genre, i) => (
                      <span key={i} className="genres__item">{genre.name}</span>
                    ))
                  }
                </div>
                <p className="overview">{movie.overview}</p>
                <div className="cast">
                  <div className="section__header">
                    <h2>Cast</h2>
                  </div>
                  <CastList cast={movie.credits.cast} />
                </div>
              </div>
            </div>
          </>
        )
      }
    </>);
  }
}

export default MoviePage;