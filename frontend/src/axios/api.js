import axios from 'axios';

let baseUrl = '';

if( import.meta.env.MODE === 'development' ){
  baseUrl = 'localhost:5000'
} else {
  baseUrl = '107.167.190.202:5000'
}

const api = axios.create({
  baseURL: `http://${baseUrl}/api/`,
  headers: {
    "Content-Type": "application/json; charset=utf-8",
    Accept: "application/json",
  }
});

export default api;