import axios from 'axios';

let baseUrl = '';

// baseUrl = 'http://34.152.28.2:5000'

// if( import.meta.env.MODE === 'development' ){
//   baseUrl = 'http://localhost:5000/'
// } else {
  baseUrl = 'https://backend.locostall.shop'
// }

const api = axios.create({
  baseURL: `${baseUrl}/api/`,
  headers: {
    "Content-Type": "application/json; charset=utf-8",
    Accept: "application/json",
    withCredentials: true
  }
});

export default api;