import Card from '@mui/material/Card';
import api from '../api';


function MovieCard({ movie }) {
  return (
    <a href={`/movie/${movie['id']}`}>
      <img style={{ height: "225px", width: "150px", borderRadius: "20px", maxHeight: "100%", margin: "auto" }} src={api.tmdbImage + '/w342' + movie['poster_path']} />
    </a>
  );
}

export default MovieCard;