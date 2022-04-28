import Card from '@mui/material/Card';
import api from '../../api';

function MovieCard({ movie }) {
  return (
    <Card style={{ height: "225px", width: "150px" }}>
      <img style={{ maxHeight: "100%", margin: "auto"}} src={api.tmdbImage + movie['poster_path']} />
    </Card>
  );
}

export default MovieCard;