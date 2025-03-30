<template>
  <div class="about">
    <AppLogo />
    <h1>About BandGap-ml</h1>
    <p>
      BandGap-ml is a tool for predicting band gaps of materials based on their
      chemical composition.
    </p>
  </div>
</template>

<script>
import AppLogo from "@/components/Logo.vue";
export default {
  name: "AboutPage",
  components: {
    AppLogo,
  },
};
</script>
<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  padding-bottom: 100px;
  text-align: center;
}
</style>
