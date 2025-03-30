<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/docs">API Documentation</router-link> |
      <router-link to="/about">About</router-link> |
      <a href="https://github.com/alexey-krasnov/BandGap-ml" target="_blank"
        >GitHub</a
      >
    </nav>
    <router-view></router-view>
    <footer>
      <p>
        &copy; 2024 BandGap-ml. Predicting materials band gaps based on the
        chemical composition.
      </p>
      <p>
        Developed by
        <a href="https://github.com/alexey-krasnov" target="_blank"
          >Dr. Aleksei Krasnov</a
        >. All rights reserved.
      </p>
    </footer>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: #f2f2f2;
  color: black;
  text-align: center;
  padding: 5px;
  font-size: 12px;
}

footer a {
  color: #1f77b4;
  text-decoration: none;
}

footer a:hover {
  text-decoration: underline;
}
</style>
