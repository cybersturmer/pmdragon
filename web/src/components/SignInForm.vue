<template>
    <form>
        <div class="input-group input-group-sm mb-3">
            <label for="email"></label>
            <input id="email" type="email"
                   placeholder="cybersturmer@ya.ru" class="form-control" required>
        </div>
        <div class="input-group input-group-sm mb-3">
            <label for="password"></label>
            <input id="password" type="password"
                   placeholder="************" class="form-control" required>
        </div>
        <div class="input-group input-group-sm mb-1">
            <button type="submit" class="btn btn-sm btn-dark w-100">
                Sign In
            </button>
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
