import React, { useState, useEffect } from 'react';

import { useParams } from 'react-router';
import api from '../api';

function CastList({ cast }) {

    return (
        <div className="casts">
            {
                cast.map((item, i) => (
                    <div key={i} className="casts__item">
                        <div className="casts__item__img" style={{ backgroundImage: `url(${api.tmdbImage}/w342${item.profile_path})` }}></div>
                        <p className="casts__item__name">{item.name}</p>
                    </div>
                ))
            }
        </div>
    );
}

export default CastList;
