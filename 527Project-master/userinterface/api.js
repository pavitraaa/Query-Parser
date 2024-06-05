import axios from 'axios';

const BASE_URL = 'http://192.168.0.165:5000/'
export const parseQuery = (database, schema, query) => axios.post(BASE_URL+`query?database=${database}&query=${query}&schema=${schema}`);

