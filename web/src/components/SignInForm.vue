<template>
    <form method="post">
        <div class="input-group input-group-sm mb-3">
            <label for="username"></label>
            <input id="username" type="text"
                   placeholder="dragon" class="form-control" required>
        </div>
        <div class="input-group input-group-sm mb-3">
            <label for="password"></label>
            <input id="password" type="password"
                   placeholder="************" class="form-control" required>
        </div>
        <div class="input-group input-group-sm mb-1">
            <button type="submit" class="btn btn-sm btn-dark w-100">Register</button>
        </div>
    </form>
</template>

<script>
export default {
  name: 'SignInForm',
};
</script>

<style scoped>

</style>
