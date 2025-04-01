<template>
  <img :src="logo" alt="BandGap-ml Logo" class="logo" />
</template>

<script>
import logo from "@/logo/band_gap_ml_logo.webp";

export default {
  name: "AppLogo",
  data() {
    return {
      logo: logo,
    };
  },
};
</script>

<style scoped>
.logo {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 15vw; /* 15% of the viewport width */
  max-width: 200px; /* Maximum size for larger screens */
  min-width: 100px; /* Minimum size to ensure visibility */
}

/* For tablets */
@media screen and (max-width: 1024px) {
  .logo {
    width: 20vw;
    max-width: 150px;
    min-width: 80px;
  }
}

/* For mobile phones */
@media screen and (max-width: 768px) {
  .logo {
    position: static; /* Remove absolute positioning */
    display: block; /* Make it a block element */
    margin: 10px auto; /* Center the logo */
    width: 25vw;
    max-width: 100px;
    min-width: 60px;
  }
}

/* For very small screens */
@media screen and (max-width: 480px) {
  .logo {
    width: 30vw;
    max-width: 80px;
    min-width: 50px;
  }
}
</style>
