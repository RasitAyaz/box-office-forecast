import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";
import Cast from "../components/Cast";
import Crew from "../components/Crew";

function MoviePage() {
  const { id } = useParams();

  const [movie, setMovie] = useState(null);
  const [linearRegressionResult, setLinearRegressionResult] = useState(null);

  useEffect(() => {
    fetch(`${api.tmdb}/movie/${id}?api_key=${api.tmdbKey}&append_to_response=credits,release_dates,keywords`)
      .then(res => res.json())
      .then(res => {
        setMovie(res);
      });
  }, [id]);

  useEffect(() => {
    fetch(`${api.backend}/forecast?movie_id=${id}`)
      .then(res => res.json())
      .then(res => {
        setLinearRegressionResult(res.linear_regression);
      });
  }, [id]);

  function formatNumber(number) {
    var nf = new Intl.NumberFormat();
    return nf.format(number);
  }

  if (movie == null) {
    return (<center>
      Loading...
    </center>);
  } else {
    return (<>
      {
        movie && (
          <>
            {movie.backdrop_path && <div className="banner" style={{ backgroundImage: `url(${api.tmdbImage}/original${movie['backdrop_path']})`, backgroundSize: "cover", backgroundPosition: "center" }} />}
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
              <div style={{ padding: "0 40px", paddingBottom: "20px" }}>
                <h2>Details</h2>
                <p>Release date: <span style={{ fontWeight: "bold", color: "var(--primaryColorLight)" }}>{movie.release_date}</span></p>
              </div>
              <div style={{ padding: "0 40px", paddingBottom: "20px" }}>
                <h2>Prediction Results</h2>
                <p>Linear regression: <span style={{ fontWeight: "bold", color: "var(--primaryColorLight)" }}>{formatNumber(linearRegressionResult)} $</span></p>
                <p>Support vector machine: <span style={{ fontWeight: "bold", color: "var(--primaryColorLight)" }}>not calculated</span></p>
                <p>Artificial neural network: <span style={{ fontWeight: "bold", color: "var(--primaryColorLight)" }}>not calculated</span></p>
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