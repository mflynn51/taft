import axios from "axios";

class GeoDataService{
    getAll(token) {
        axios.defaults.headers.common["Authorization"] = "Token " + token;
        return axios.get("http://localhost:8000/api/points/");
    }

    createGeoPoint(data, token) {
        axios.defaults.headers.common["Authorization"] = "Token " + token;
        return axios.post("http://localhost:8000/api/points/", data);
    }

    updateGeoPoint(id, data, token) {
        axios.defaults.headers.common["Authorization"] = "Token " + token;
        return axios.post(`http://localhost:8000/api/points/${id}`, data);
    }

    deleteGeoPoint(id, token) {
        axios.defaults.headers.common["Authorization"] = "Token " + token;
        return axios.post(`http://localhost:8000/api/points/${id}`);
    }

    /*
    completeGeoPoint(id, token) {
        axios.defaults.headers.common["Authorization"] = "Token " + token;
        return axios.post(`http://localhost:8000/api/points/${id}/complete`);
    }
    */

    login(data) {
        return axios.post("http://localhost:8000/api/login/", data);
    }

    signup(data) {
        return axios.post("http://localhost:8000/api/signup/", data);
    }

}

export default new GeoDataService();
