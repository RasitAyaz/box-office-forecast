import MovieCard from "./MovieCard";

function UpcomingMovies() {
  return (
    <div style={{ padding: "30px", display: "flex" }}>
      {[...Array(20).keys()].map(
        movie => <div style={{ padding: "20px" }}>
          <MovieCard />
        </div>
      )}
    </div>
  );
}

export default UpcomingMovies;