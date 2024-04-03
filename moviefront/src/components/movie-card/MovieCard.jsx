import React, { useState, useEffect } from 'react';

import './movie-card.scss';

import { Link } from 'react-router-dom';

import Button from '../button/Button';

import { category } from '../../api/tmdbApi';
import apiConfig from '../../api/apiConfig';
import axios from 'axios';

const MovieCard = props => {
    
    const [posterUrl, setPosterUrl] = useState(null);
    const item = props.item;
    const link = '/' + category[props.category] + '/' + item.id;

   
    useEffect(() => {
        const fetchPosterUrl = async () => {
            try {
                // Fetch the movie details using the ID
                const response = await axios.get(`https://api.themoviedb.org/3/movie/${item.id}?api_key=82c1916249ce382939bd56d536e073c4`);
                // Construct the poster URL from the response data
                const posterPath = response.data.poster_path;
                const posterUrl = apiConfig.w500Image(posterPath);
                // Set the poster URL to the state
                setPosterUrl(posterUrl);
            } catch (error) {
                console.error('Error fetching poster:', error);
            }
        };

        fetchPosterUrl();
    }, [item.id]);

    return (
        <Link to={link}>
            <div className="movie-card" style={{backgroundImage: `url(${posterUrl})`}}>
                <Button>
                    <i className="bx bx-play"></i>
                </Button>
            </div>
            <h3>{item.title || item.name}</h3>
        </Link>
    );
}

export default MovieCard;
