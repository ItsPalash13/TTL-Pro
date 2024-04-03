const apiConfig = {
    baseUrl: 'https://api.themoviedb.org/3/',
    apiKey: '82c1916249ce382939bd56d536e073c4',
    originalImage: (imgPath) => `https://image.tmdb.org/t/p/original/${imgPath}`,
    w500Image: (imgPath) => `https://image.tmdb.org/t/p/w500/${imgPath}`
}

export default apiConfig;