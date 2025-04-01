<template>
  <div class="home">
    <AppLogo />
    <h1>BandGap-ml: Band Gap Prediction</h1>
    <p>
      This web app allows you to predict the band gap of inorganic materials
      either by uploading a CSV file or by entering chemical formulas.
    </p>

    <div class="model-selection">
      <h2>Select Model for Prediction</h2>
      <select v-model="selectedModel">
        <option value="best_model">Best Model (Random Forest-based)</option>
        <option value="RandomForest">Random Forest</option>
        <option value="GradientBoosting">Gradient Boosting</option>
        <option value="XGBoost">XGBoost</option>
      </select>
    </div>

    <div class="model-info">
      <h3>Model Information</h3>
      <p v-if="selectedModel === 'best_model'">
        The best model is a RandomForest-based model that has been optimized for
        band gap prediction.
      </p>
      <p v-else-if="selectedModel === 'RandomForest'">
        Random Forest is an ensemble learning method that operates by
        constructing multiple decision trees during training.
      </p>
      <p v-else-if="selectedModel === 'GradientBoosting'">
        Gradient Boosting is a machine learning technique that builds an
        ensemble of decision trees in a stage-wise fashion.
      </p>
      <p v-else-if="selectedModel === 'XGBoost'">
        XGBoost is an optimized distributed gradient boosting library designed
        to be highly efficient, flexible and portable.
      </p>
    </div>

    <button @click="checkApiHealth">Check API Health</button>
    <p v-if="apiStatus">API Status: {{ apiStatus }}</p>

    <div class="file-upload">
      <h2>Upload CSV File</h2>
      <input type="file" @change="handleFileUpload" accept=".csv" />
      <button @click="predictBandGapFromFile" :disabled="!file || isProcessing">
        Predict Band Gaps from File
      </button>
    </div>

    <div class="manual-input">
      <h2>
        Enter Chemical Formulas
        <span class="small-text">(comma separated)</span>
      </h2>
      <textarea
        v-model="formulasInput"
        placeholder="Enter one or more chemical formulas (separate by commas)"
      ></textarea>
      <button @click="predictBandGapFromFormulas" :disabled="isProcessing">
        Predict Band Gaps from Formulas
      </button>
    </div>

    <div v-if="isProcessing" class="processing">Processing... Please wait.</div>

    <div v-if="error" class="error">Error: {{ error }}</div>

    <div
      v-if="predictions.length > 0"
      class="predictions"
      ref="predictionsTable"
    >
      <h2>Predictions</h2>
      <table>
        <thead>
          <tr>
            <th>Composition</th>
            <th>Band Gap</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pred in predictions" :key="pred.composition">
            <td>{{ pred.composition }}</td>
            <td>{{ pred.band_gap.toFixed(4) }}</td>
          </tr>
        </tbody>
      </table>
      <button @click="downloadPredictions">Download Predictions as CSV</button>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import AppLogo from "@/components/Logo.vue";

export default {
  name: "HomePage",
  components: {
    AppLogo,
  },
  data() {
    return {
      selectedModel: "best_model",
      file: null,
      formulasInput: "BaLa2In2O7, TiO2, Bi4Ti3O12",
    };
  },
  computed: {
    ...mapState(["predictions", "apiStatus", "isProcessing", "error"]),
  },
  methods: {
    ...mapActions(["checkApiHealth", "predictBandGap"]),
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    async predictBandGapFromFile() {
      if (!this.file) return;
      const formData = new FormData();
      formData.append("file", this.file);
      formData.append("model_type", this.selectedModel);
      await this.predictBandGap(formData);
      this.scrollToPredictions();
    },
    async predictBandGapFromFormulas() {
      const formulas = this.formulasInput.split(",").map((f) => f.trim());
      const formData = new FormData();
      formulas.forEach((formula) => {
        formData.append("formula", formula);
      });
      formData.append("model_type", this.selectedModel);
      await this.predictBandGap(formData);
      this.scrollToPredictions();
    },

    scrollToPredictions() {
      this.$nextTick(() => {
        if (this.$refs.predictionsTable) {
          this.$refs.predictionsTable.scrollIntoView({ behavior: "smooth" });
        }
      });
    },

    downloadPredictions() {
      const headers = ["Composition", "Band Gap"];
      const csv = [
        headers.join(","),
        ...this.predictions.map((pred) =>
          [pred.composition, pred.band_gap.toFixed(4)].join(",")
        ),
      ].join("\n");
      const blob = new Blob([csv], { type: "text/csv" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `predicted_band_gaps_${new Date().toISOString()}.csv`;
      link.click();
    },
  },
};
</script>
<style scoped>
.home {
  max-width: 1000px;
  margin: 0 auto;
  padding: 10px;
  padding-bottom: 60px;
  text-align: center;
}

.model-selection,
.model-info,
.file-upload,
.manual-input,
.predictions {
  margin-bottom: 30px;
}

textarea {
  width: 100%;
  height: 100px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.processing,
.error {
  margin-top: 20px;
  padding: 10px;
  border-radius: 5px;
}

.processing {
  background-color: #e6f7ff;
  color: #1890ff;
}

.error {
  background-color: #fff1f0;
  color: #f5222d;
}

.predictions button {
  display: block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.predictions button:hover {
  background-color: #45a049;
}

.small-text {
  font-size: 0.8em;
  font-weight: normal;
}
</style>
