<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/login">Sign In</router-link> |
      <router-link to="/news">What's new</router-link>
    </div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  watch: {
    $route(to) {
      document.title = to.meta.title || '~PMDragon~';
    },
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #929292;
}
</style>
