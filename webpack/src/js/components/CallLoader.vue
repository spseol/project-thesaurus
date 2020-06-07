<template>
    <v-progress-linear
        indeterminate v-if="$calls.isPending(identifier)"
        class="my-3"
    ></v-progress-linear>
</template>
<script>
    export default {
        name: 'CallLoader',
        props: {
            identifier: {
                type: String,
                required: true,
            },
        },
    };
</script>