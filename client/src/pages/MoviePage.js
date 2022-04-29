import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import Cast from "../components/Cast";
import Crew from "../components/Crew";

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
            {movie.backdrop_path && <div className="banner" style={{ backgroundImage: `url(${api.tmdbImage}/original${movie['backdrop_path']})`, backgroundSize: "cover", backgroundPositionX: "center" }} />}
            <div>
              <div style={{ padding: "40px" }}>
                <img className="movie_page_poster" style={{ float: "left", marginRight: "20px", marginBottom: "20px" }} src={api.tmdbImage + '/w342' + movie['poster_path']} />
                <h1>
                  {movie.title || movie.name}
                </h1>
                <div>
                  {
                    movie.genres && movie.genres.slice(0, 5).map((genre, i) => (
                      <span className="banner__button" style={{ display: "inline-block", marginBottom: "15px" }} key={i} >{genre.name}</span>
                    ))
                  }
                </div>
                <p>{movie.overview}</p>
              </div>
              <div style={{ padding: "0 40px" }}>
                <h2>Prediction Results</h2>
                <p>Linear regression: <span style={{fontWeight: "bold", color: "var(--primaryColorLight)"}}>3,000,000 $</span></p>
                <p>Support vector machine: <span style={{fontWeight: "bold", color: "var(--primaryColorLight)"}}>not calculated</span></p>
                <p>Artificial neural network: <span style={{fontWeight: "bold", color: "var(--primaryColorLight)"}}>not calculated</span></p>
              </div>
              <div style={{ clear: "both" }}>
                <div style={{ padding: "0 40px" }}>
                  <h2>Cast</h2>
                </div>
                <Cast cast={movie.credits.cast} />
                <div style={{ padding: "0 40px" }}>
                  <h2>Crew</h2>
                </div>
                <Crew crew={movie.credits.crew} />
              </div>
            </div>
          </>
        )
      }
    </>);
  }
}

export default MoviePage;