<template>
  <img :src="logo" alt="BandGap-ml Logo" class="logo" />
</template>

<script>
import logo from "@/logo/band_gap_ml_logo.webp";

export default {
  name: "AppLogo", // Changed from "Logo" to "AppLogo"
  data() {
    return {
      logo: logo,
    };
  },
};
</script>

<style scoped>
.logo {
  max-width: 200px; /* Adjust this value as needed */
  position: absolute;
  top: 10px;
  left: 10px;
}
</style>
