// src/store/index.js
import { createStore } from "vuex";
import axios from "axios";

// Define the API endpoint of the backend server
const API_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:3000" // Local testing
    : process.env.VUE_APP_PRODUCTION_API_URL; // Production

console.log("Current API URL:", API_URL); // For debugging

export default createStore({
  state: {
    predictions: [],
    apiStatus: "",
    isProcessing: false,
    error: null,
  },
  mutations: {
    setPredictions(state, predictions) {
      state.predictions = predictions;
    },
    setApiStatus(state, status) {
      state.apiStatus = status;
    },
    setProcessing(state, isProcessing) {
      state.isProcessing = isProcessing;
    },
    setError(state, error) {
      state.error = error;
    },
  },
  actions: {
    async checkApiHealth({ commit }) {
      try {
        const response = await axios.get(`${API_URL}/healthcheck`);
        commit("setApiStatus", response.data.status);
      } catch (error) {
        commit("setApiStatus", `Error: ${error.message}`);
        commit("setError", error.message);
      }
    },
    async predictBandGap({ commit }, payload) {
      commit("setProcessing", true);
      commit("setError", null);
      try {
        const response = await axios.post(
          `${API_URL}/predict_bandgap`,
          payload,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );
        commit("setPredictions", response.data);
      } catch (error) {
        console.error("Full error object:", error);
        commit(
          "setError",
          error.response ? JSON.stringify(error.response.data) : error.message
        );
      } finally {
        commit("setProcessing", false);
      }
    },
  },
});
