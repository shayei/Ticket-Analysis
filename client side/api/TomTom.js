import axios from 'axios';


export default axios.create({
    baseURL:'https://api.tomtom.com/search/2/search',
    headers:{
        Authorization: 'Bearer O39cJUgKuUE0js4ARn11GJ2ZhHQYiyu6',
    }

})