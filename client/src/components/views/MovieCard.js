import Card from '@mui/material/Card';
import api from '../../api';


function MovieCard({ movie }) {
  return (
    <img style={{ height: "225px", width: "150px", borderRadius: "20px", maxHeight: "100%", margin: "auto" }} src={api.tmdbImage + '/w342' + movie['poster_path']} />
  );
}

export default MovieCard;