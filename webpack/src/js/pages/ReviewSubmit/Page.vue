<template>
    <ReviewForm :thesisId="$route.params.id"></ReviewForm>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import ReviewForm from './ReviewForm';

    export default Vue.extend({
        components: {ReviewForm}
    });
</script>

<style scoped>

</style>