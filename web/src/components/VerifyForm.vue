<template>
    <form v-on:submit.prevent>
        <div class="input-group input-group-sm mb-3">
            <label for="email"></label>
            <input id="email" type="email"
                   placeholder="cybersturmer@ya.ru" class="form-control" required>
        </div>
        <div class="input-group input-group-sm mb-3">
            <label></label>
            <input id="password" type="password"
                   placeholder="*********" class="form-control" required>
        </div>
    </form>
</template>

<script>
  export default {
    name: 'VerifyForm'
  };
</script>

<style scoped>

</style>
