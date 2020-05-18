<template>
    <form method="post">
        <div class="input-group input-group-sm mb-3">
            <label for="prefix_url"></label>
            <input id="prefix_url" type="text"
                   placeholder="yourname" class="form-control" required>
            <div class="input-group-append">
                <div class="input-group-text">pmdragon.org</div>
            </div>
        </div>
        <div class="input-group input-group-sm mb-3">
            <label for="email"></label>
                <input id="email" type="email"
                       placeholder="yourmail@mail.com" class="form-control" required>
        </div>
        <div class="input-group input-group-sm mb-1">
            <button type="submit" class="btn btn-sm btn-dark w-100">Register</button>
        </div>
    </form>
</template>

<script>
export default {
  name: 'RegistrationForm',
};
</script>

<style scoped>

</style>
