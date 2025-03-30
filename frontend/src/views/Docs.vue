<template>
  <div class="docs">
    <AppLogo />
    <h1>BandGap-ml: API Documentation</h1>
    <p>
      API for predicting band gaps of inorganic materials based on their
      chemical formulas
    </p>
    <p>Version: 0.4.1</p>

    <div class="left-aligned-content">
      <h2>Endpoints</h2>

      <h3>1. Predict Band Gap</h3>
      <p><strong>URL:</strong> /predict_bandgap</p>
      <p><strong>Method:</strong> POST</p>
      <p>
        <strong>Description:</strong> Predicts band gaps of materials based on
        their chemical formulas.
      </p>

      <h4>Request Body:</h4>
      <p>Content-Type: multipart/form-data</p>
      <ul>
        <li><code>formula</code> (optional): string | array of strings</li>
        <li><code>model_type</code> (optional): string</li>
        <li><code>file</code> (optional): file upload (CSV or Excel)</li>
      </ul>

      <h4>Responses:</h4>
      <p><strong>200 OK</strong></p>
      <pre><code>
[
  {
    "composition": "string",
    "is_semiconductor": 0,
    "semiconductor_probability": 0,
    "band_gap": 0
  }
]
      </code></pre>

      <p><strong>422 Unprocessable Entity</strong></p>
      <pre><code>
{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
      </code></pre>

      <h3>2. Health Check</h3>
      <p><strong>URL:</strong> /healthcheck</p>
      <p><strong>Method:</strong> GET</p>
      <p><strong>Description:</strong> Checks if the server is running.</p>

      <h4>Responses:</h4>
      <p><strong>200 OK</strong></p>
      <pre><code>"string"</code></pre>

      <h2>Usage Examples</h2>
      <h3>Predicting Band Gap for a Single Chemical Formula</h3>
      <pre><code>
curl -X 'POST' \
  'http://localhost:3000/predict_bandgap' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'formula=SiO2' \
  -F 'model_type=best_model'
      </code></pre>

      <h3>Predicting Band Gap for Multiple Chemical Formulas</h3>
      <pre><code>
curl -X 'POST' \
  'http://localhost:3000/predict_bandgap' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'formula=SiO2' \
  -F 'formula=Fe2O3' \
  -F 'model_type=best_model'
      </code></pre>

      <h3>Predicting Band Gap Using a CSV/Excel File with Chemical Formulas</h3>
      <pre><code>
curl -X 'POST' \
  'http://localhost:3000/predict_bandgap' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@path/to/your/file.csv' \
  -F 'model_type=best_model'
      </code></pre>

      <p>
        Note: Replace "@path/to/your/file.csv" with the actual path to your CSV
        or Excel file.
      </p>
    </div>
  </div>
</template>

<script>
import AppLogo from "@/components/Logo.vue";
import hljs from "highlight.js/lib/core";
import bash from "highlight.js/lib/languages/bash";
import json from "highlight.js/lib/languages/json";
import "highlight.js/styles/github.css"; // You can choose a different style if you prefer

hljs.registerLanguage("bash", bash);
hljs.registerLanguage("json", json);

export default {
  name: "DocsPage",
  components: {
    AppLogo,
  },
  mounted() {
    this.$nextTick(() => {
      document.querySelectorAll("pre code").forEach((block) => {
        hljs.highlightBlock(block);
      });
    });
  },
};
</script>

<style scoped>
.docs {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  padding-bottom: 20px;
  text-align: center;
}

.left-aligned-content {
  text-align: left;
}

h1,
h2,
h3,
h4 {
  margin-top: 20px;
}

pre {
  padding: 15px;
  overflow-x: auto;
  border-radius: 6px;
  background-color: #f8f8f8;
  border: 1px solid #e0e0e0;
  margin: 15px 0;
}

code {
  font-family: "Courier New", Courier, monospace;
  font-size: 14px;
}

ul {
  padding-left: 20px;
}

/* Additional styles for inline code */
p code,
li code {
  background-color: #f0f0f0;
  padding: 2px 4px;
  border-radius: 4px;
}

/* Ensure the code blocks have a minimum height */
pre code {
  display: block;
  min-height: 50px;
}
</style>
