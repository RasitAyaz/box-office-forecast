import React from 'react';
import { ScrollMenu } from 'react-horizontal-scrolling-menu';
import api from '../api';


function Crew({ crew }) {

    return (
        <ScrollMenu>
            <div style={{ padding: "0 25px", display: "flex" }}>
                {
                    crew.map((item, i) => (
                        <div key={i} style={{ padding: "15px" }}>
                            <div style={{ height: "180px", width: "120px", backgroundColor: "var(--backgroundColorLight)", borderRadius: "20px" }}>
                                {item.profile_path && <img style={{ borderRadius: "20px", maxHeight: "100%", margin: "auto" }} src={api.tmdbImage + '/w154' + item.profile_path} />}
                            </div>
                            <p style={{ fontWeight: "bold" }}>{item.name}</p>
                            <p style={{ color: "var(--primaryColorLight)" }}>{item.job}</p>
                        </div>
                    ))
                }
            </div>
        </ScrollMenu>
    );
}

export default Crew;
