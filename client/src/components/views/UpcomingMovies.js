import { ScrollMenu } from 'react-horizontal-scrolling-menu';
import MovieCard from "./MovieCard";

function UpcomingMovies({ movies }) {

  return (
    <ScrollMenu>
      <div style={{ padding: "30px", display: "flex" }}>
        {movies.map(
          movie => <div style={{ padding: "20px" }}>
            <MovieCard movie={movie} />
          </div>
        )}
      </div>
    </ScrollMenu>
  );
}

export default UpcomingMovies;