import React, { useState, useEffect } from "react";
import "./Banner.css";

function Banner({ backdrop }) {

  function truncate(str, n) {
    return str?.length > n ? str.substr(0, n - 1) + "..." : str;
  }

  return (
    <header
      className="banner"
      style={{
        backgroundSize: "cover",
        backgroundImage: `url(https://image.tmdb.org/t/p/original/${backdrop})`,
        backgroundPosition: "center center",
      }}
    >
      <div className="banner__contents">
        <h1 className="banner__title">
          Box Office Forecast
        </h1>
        <button className="banner__button">Custom Movie</button>
      </div>
    </header>
  );
}

export default Banner;
