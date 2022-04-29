import api from '../api';


function MovieCard({ movie }) {
  return (
    <a href={`/movie/${movie['id']}`}>
      <div style={{ height: "225px", width: "150px", backgroundColor: "var(--backgroundColorLight)", borderRadius: "20px" }}>
        {movie.poster_path && <img style={{ borderRadius: "20px", maxHeight: "100%", margin: "auto" }} src={api.tmdbImage + '/w342' + movie['poster_path']} />}
      </div>
    </a>
  );
}

export default MovieCard;