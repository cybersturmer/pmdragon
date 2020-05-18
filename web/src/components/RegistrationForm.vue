<template>
    <form method="post">
        <div class="form-group">
            <label for="prefix_url">Input workplace name</label>
            <input id="prefix_url" type="text" placeholder="URL prefix" class="form-control">
        </div>
        <div class="form-group">
            <label for="email">Input email</label>
            <input id="email" type="email" placeholder="yourmail@mail.com" class="form-control">
        </div>
        <button type="submit" class="btn btn-outline-dark">Register</button>
    </form>
</template>

<script>
export default {
  name: 'RegistrationForm',
};
</script>

<style scoped>

</style>
