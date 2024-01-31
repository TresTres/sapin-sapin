<template>
    <form class="pure-form-1-2">
        <fieldset class="pure-group">
            <input type="text" class="pure-input-1-2" placeholder="Username" />
            <input type="text" class="pure-input-1-2" placeholder="Password" />
            <input type="email" class="pure-input-1-2" placeholder="Email" />
        </fieldset>
        <button type="submit" class="pure-button pure-input-1-2 pure-button-primary">
        Sign in
        </button>
    </form>
</template>

<script setup>
    definePageMeta({
        layout: "landing"
    })

    
</script>